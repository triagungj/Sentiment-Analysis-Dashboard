from django.core.management.base import BaseCommand
from api.models.news_model import News
from api.services.sentiment import predict_sentiment

class Command(BaseCommand):
    help = 'Predict sentiment for news items without sentiment.'

    def handle(self, *args, **options):
        unsentimented_news = News.objects.filter(sentiment__isnull=True)
        count = 0
        for news in unsentimented_news:
            result = predict_sentiment(news.title)
            news.sentiment = result.get('label')
            news.sentiment_score = result.get('confidence')
            news.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully updated sentiment for {count} news items.'))
