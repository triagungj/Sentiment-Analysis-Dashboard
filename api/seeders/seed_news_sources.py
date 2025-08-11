# Seeder script for NewsSource model
from api.models.news_source_model import NewsSource

def run():
    sources = [
        {"name": "Kompas", "homepage": "https://www.kompas.com"},
        {"name": "Detik", "homepage": "https://www.detik.com"},
        {"name": "CNBC Indonesia", "homepage": "https://www.cnbcindonesia.com"},
        {"name": "Bisnis.com", "homepage": "https://www.bisnis.com"},
    ]
    for src in sources:
        NewsSource.objects.get_or_create(**src)
    print("Seeded NewsSource data.")

if __name__ == "__main__":
    run()
