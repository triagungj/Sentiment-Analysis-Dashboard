from django.db import models
from rest_framework import serializers

from api.models.news_source_model import NewsSource, NewsSourceSerializer

class News(models.Model):
    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("neutral",  "Neutral"),
        ("negative", "Negative"),
    ]

    news_source = models.ForeignKey(
        "api.NewsSource", on_delete=models.CASCADE, related_name="news_items", 
        null=True, blank=True
    )
    title = models.CharField(max_length=255)
    date = models.DateField()
    sentiment = sentiment = models.CharField(
        max_length=8,                 # "negative" is 8 chars
        choices=SENTIMENT_CHOICES,
        blank=True,
        null=True,
        db_index=True,
    )
    sentiment_score = models.FloatField(blank=True, null=True)
    image_link = models.URLField(max_length=500, blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

class NewsReadSerializer(serializers.ModelSerializer):
    news_source = NewsSourceSerializer(read_only=True)
    news_source_id = serializers.PrimaryKeyRelatedField(
        queryset=NewsSource.objects.all(),
        source="news_source",
        write_only=True
    )

    class Meta:
        model = News
        fields = [
            "id", "news_source", "news_source_id", "title", "date", "image_link", "link",
            "sentiment", "sentiment_score"
        ]

class NewsWriteSerializer(serializers.ModelSerializer):
    news_source_id = serializers.PrimaryKeyRelatedField(
        queryset=NewsSource.objects.all(),
        source="news_source"
    )

    class Meta:
        model = News
        fields = ["news_source_id", "title", "date", "image_link", "link", "sentiment", "sentiment_score"]
        read_only_fields = ["id", "sentiment", "sentiment_score"]
