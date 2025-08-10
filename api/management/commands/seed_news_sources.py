from django.core.management.base import BaseCommand
from api.models import NewsSource

class Command(BaseCommand):
    help = "Seed the NewsSource table with initial data (idempotent)."

    def handle(self, *args, **options):
        sources = [
            {"name": "Kompas", "homepage": "https://www.kompas.com", "logo_img": None},
            {"name": "Detik", "homepage": "https://www.detik.com", "logo_img": None},
            {"name": "CNBC Indonesia", "homepage": "https://www.cnbcindonesia.com", "logo_img": None},
            {"name": "Bisnis.com", "homepage": "https://www.bisnis.com", "logo_img": None},
        ]

        created_count = 0
        for src in sources:
            obj, created = NewsSource.objects.get_or_create(**src)
            created_count += int(created)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded NewsSource data. Created: {created_count}, total now: {NewsSource.objects.count()}"
        ))
