from django.core.management.base import BaseCommand
from api.services.rss_ingest import fetch_cnbc_market_and_predict_sync

class Command(BaseCommand):
    help = "Sync CNBC Market RSS once and exit."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=50)

    def handle(self, *args, **opts):
        res = fetch_cnbc_market_and_predict_sync(limit=opts["limit"])
        self.stdout.write(self.style.SUCCESS(
            f"Inserted {res.get('inserted',0)}, Skipped {res.get('skipped',0)}"
        ))
