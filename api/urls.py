from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.news_source_view import NewsSourceViewSet
from api.views.news_view import NewsViewSet
from api.views.predict_view import PredictSentimentView
from api.views.import_csv_view import ImportNewsCSVView
from api.views.dashboard_view import DashboardSentimentStatsView

router = DefaultRouter()
router.register(r"news-sources", NewsSourceViewSet, basename="news-source")
router.register(r"news", NewsViewSet, basename="news")

urlpatterns = [
    path("predict/", PredictSentimentView.as_view(), name="predict-sentiment"),
    path("import-csv/", ImportNewsCSVView.as_view(), name="import-news-csv"),
    path("dashboard/sentiment-stats/", DashboardSentimentStatsView.as_view(), name="dashboard-sentiment-stats"),
    path("", include(router.urls)),  # gives /api/news-sources/ and /api/news-sources/{id}/
]