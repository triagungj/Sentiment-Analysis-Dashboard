# filepath: /Users/tj/Projects/Analisis-sentimen/dashboard/sentiment_dashboard/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from sentiment_dashboard.views import sentiment_chart_page

schema_view = get_schema_view(
    openapi.Info(
        title="IndoBERT Stock News Sentiment API",
        default_version="v1",
        description="API untuk klasifikasi sentimen berita saham menggunakan IndoBERT",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path('chart/', sentiment_chart_page, name='sentiment-chart-page'),
]