import re, html
import feedparser
from email.utils import parsedate_to_datetime
from django.utils.timezone import make_aware
from django.db import transaction
from api.models.news_model import News
from api.services.sentiment import predict_sentiment

FEED_URL = "https://www.cnbcindonesia.com/market/rss/"

def _first_image(entry):
    media = entry.get("media_content") or []
    if media:
        u = media[0].get("url")
        if u: return u
    enc = entry.get("enclosures") or []
    if enc:
        u = enc[0].get("href") or enc[0].get("url")
        if u: return u
    summary = html.unescape(entry.get("summary", "") or "")
    m = re.search(r'<img[^>]+src="([^"]+)"', summary)
    return m.group(1) if m else ""

def _pubdate(entry):
    raw = entry.get("published") or entry.get("updated")
    if not raw: return None
    try:
        dt = parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            dt = make_aware(dt)
        return dt
    except Exception:
        return None


def fetch_cnbc_market_and_predict_sync(limit=50, backfill_existing=False):
    """
    Insert ONLY NEW items from CNBC Market RSS.
    Dedup key: link.
    Predict sentiment ONLY for new items.
    If backfill_existing=True, also fill sentiment for existing rows with missing sentiment/score.
    Returns: {"inserted": N, "updated": M, "skipped": K}
    """
    feed = feedparser.parse(FEED_URL)
    entries = feed.entries[:limit]

    # 1) Pre-parse minimal fields (no prediction yet)
    parsed = []
    for e in entries:
        link = e.get("link") or ""
        if not link:
            continue
        parsed.append({
            "link": link,
            "title": (e.get("title") or "").strip(),
            "date": _pubdate(e),              # <- rename to published_at if your model uses that
            "image_link": _first_image(e),    # <- keep your field name
        })

    if not parsed:
        return {"inserted": 0, "updated": 0, "skipped": 0}

    # 2) Check what already exists
    wanted_links = [p["link"] for p in parsed]
    existing_qs = (News.objects
        .filter(link__in=wanted_links)
        .only("id", "link", "title", "date", "image_link", "sentiment", "sentiment_score"))
    existing_by_link = {n.link: n for n in existing_qs}

    to_create = []
    to_update = []

    # 3) Build create/update sets, predicting ONLY when needed
    for p in parsed:
        n = existing_by_link.get(p["link"])
        if n:
            if backfill_existing:
                needs_sentiment = (not n.sentiment) or (n.sentiment_score is None)
                changed_meta = (
                    (n.title != p["title"]) or
                    (n.date != p["date"]) or
                    (getattr(n, "image_link", None) != p["image_link"])
                )
                if needs_sentiment:
                    pred = predict_sentiment(p["title"])
                    n.sentiment = pred.get("label")
                    n.sentiment_score = pred.get("confidence")
                if needs_sentiment or changed_meta:
                    n.title = p["title"]
                    n.date = p["date"]
                    n.image_link = p["image_link"]
                    to_update.append(n)
            # else: skip silently
            continue

        # New row: now we predict
        pred = predict_sentiment(p["title"])
        p["sentiment"] = pred.get("label")
        p["sentiment_score"] = pred.get("confidence")
        to_create.append(News(**p))

    # 4) Commit
    with transaction.atomic():
        if to_create:
            News.objects.bulk_create(to_create)
        if to_update:
            News.objects.bulk_update(
                to_update,
                ["title", "date", "image_link", "sentiment", "sentiment_score"]
            )

    inserted = len(to_create)
    updated = len(to_update)
    skipped = len(parsed) - inserted - updated
    return {"inserted": inserted, "updated": updated, "skipped": skipped}
