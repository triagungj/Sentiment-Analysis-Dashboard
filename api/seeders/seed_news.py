import datetime
from api.models.news_model import News
from api.models.news_source_model import NewsSource

def run():
    news_source = NewsSource.objects.get(name="CNBC Indonesia")
    News.objects.get_or_create(
        news_source=news_source,
        title="Meningkatkan penjualan mobil dengan perusahaan",
        date=datetime.date(2025, 8, 9),
        sentiment="positive",
    )
    News.objects.get_or_create(
        news_source=news_source,
        title="Meningkatkan penjualan mobil dengan perusahaan Uhuy",
        date=datetime.date(2025, 8, 9),
        sentiment=None,
    )

if __name__ == "__main__":
    run()
    print("Seeded News data.")