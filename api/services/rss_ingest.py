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

def fetch_cnbc_market_and_predict_sync(limit=50):
    """
    Parse CNBC Market RSS and INSERT ONLY NEW items into News.
    Dedup key: link (stable in CNBC RSS).
    Returns dict: {"inserted": N, "skipped": M}
    """
    feed = feedparser.parse(FEED_URL)
    entries = feed.entries[:limit]

    # Build rows we WANT to insert
    rows = []
    for e in entries:
        title = (e.get("title") or "").strip()
        link  = e.get("link") or ""
        if not link:
            continue  # skip if no link (rare)
        published_at = _pubdate(e)
        image_url = _first_image(e)
        sentiment = predict_sentiment(title)
        

        rows.append(dict(
            title=title,
            link=link,
            image_link=image_url,
            date=published_at,
            sentiment=sentiment.get("label", ""),
            sentiment_score=sentiment.get("confidence", 0.0),
        ))

    # Dedup against DB by link
    wanted_links = [r["link"] for r in rows]
    existing = set(
        News.objects.filter(link__in=wanted_links).values_list("link", flat=True)
    )

    to_create = [News(**r) for r in rows if r["link"] not in existing]

    with transaction.atomic():
        if to_create:
            News.objects.bulk_create(to_create)

    return {"inserted": len(to_create), "skipped": len(rows) - len(to_create)}