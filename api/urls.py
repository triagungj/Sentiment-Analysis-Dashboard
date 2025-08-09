from django.urls import path
from .views import PredictSentimentView, NewsSourceListView

urlpatterns = [
    path('predict/', PredictSentimentView.as_view(), name='predict-sentiment'),
    path('news-sources/', NewsSourceListView.as_view(), name='news-source-list'),
]
