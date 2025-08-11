from django.core.management.base import BaseCommand
from api.seeders.seed_news_sources import run as seed_news_sources_run

class Command(BaseCommand):
    help = "Seed the NewsSource table with initial data (idempotent)."

    def handle(self, *args, **options):
        seed_news_sources_run()