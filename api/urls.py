from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.news_source_view import NewsSourceViewSet
from api.views.news_view import NewsViewSet
from api.views.predict_view import PredictSentimentView

router = DefaultRouter()
router.register(r"news-sources", NewsSourceViewSet, basename="news-source")
router.register(r"news", NewsViewSet, basename="news")

urlpatterns = [
    path("predict/", PredictSentimentView.as_view(), name="predict-sentiment"),
    path("", include(router.urls)),  # gives /api/news-sources/ and /api/news-sources/{id}/
]