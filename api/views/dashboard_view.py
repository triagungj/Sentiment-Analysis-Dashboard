from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.news_model import News
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DashboardSentimentStatsView(APIView):
    @swagger_auto_schema(
        operation_summary="Get sentiment statistics per day",
        tags=["Dashboard"],
        responses={200: openapi.Response(
            description="List of sentiment stats per day",
            examples={
                "application/json": [
                    {"date": "2025-08-14", "positive": 5, "neutral": 3, "negative": 2, "total": 10},
                    {"date": "2025-08-13", "positive": 2, "neutral": 4, "negative": 1, "total": 7}
                ]
            }
        )}
    )
    def get(self, request):
        # Aggregate sentiment counts per day
        qs = News.objects.values('date').annotate(
            positive=Count('id', filter=Q(sentiment='positive')),
            neutral=Count('id', filter=Q(sentiment='neutral')),
            negative=Count('id', filter=Q(sentiment='negative')),
        ).order_by('-date')
        # Add total field to each result
        result = []
        for item in qs:
            total = item['positive'] + item['neutral'] + item['negative']
            result.append({
                'date': item['date'],
                'positive': item['positive'],
                'neutral': item['neutral'],
                'negative': item['negative'],
                'total': total
            })
        return Response(result)