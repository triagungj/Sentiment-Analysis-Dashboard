# Seeder script for NewsSource model
from api.models import NewsSource

def run():
    sources = [
        {"name": "Kompas", "homepage": "https://www.kompas.com", "logo_img": None},
        {"name": "Detik", "homepage": "https://www.detik.com", "logo_img": None},
        {"name": "CNBC Indonesia", "homepage": "https://www.cnbcindonesia.com", "logo_img": None},
        {"name": "Bisnis.com", "homepage": "https://www.bisnis.com", "logo_img": None},
    ]
    for src in sources:
        NewsSource.objects.get_or_create(**src)
    print("Seeded NewsSource data.")

if __name__ == "__main__":
    run()
