from django.core.management.base import BaseCommand
from api.models.news_model import News
from api.services.sentiment import predict_sentiment
import logging
class Command(BaseCommand):
    help = 'Predict sentiment for news items without sentiment.'

    def handle(self, *args, **options):
        unsentimented_news = News.objects.filter(sentiment__isnull=True)
        count = 0

        for news in unsentimented_news:
            print(f"Predicting sentiment for news item: {news.title}")
            result = predict_sentiment(news.title)
            print(f"Predicted label: {result.get('label')}, Confidence: {result.get('confidence'):.4f}")
            news.sentiment = result.get('label')
            news.sentiment_score = result.get('confidence')
            news.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully updated sentiment for {count} news items.'))
