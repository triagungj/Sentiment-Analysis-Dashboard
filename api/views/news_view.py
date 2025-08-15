from datetime import datetime
from calendar import monthrange

from rest_framework import viewsets, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.utils.timezone import make_aware

from api.models.news_model import News, NewsReadSerializer, NewsWriteSerializer
from api.services.sentiment import predict_sentiment

from api.services.rss_ingest import fetch_cnbc_market_and_predict_sync



class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by(f"-date", "-id")  # newest first
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["id", "title", "date"]
    pagination_class = NewsPagination

    def get_queryset(self):
        qs = super().get_queryset()

        params = self.request.query_params
        start = params.get("start")
        end = params.get("end")
        month = params.get("month")
        sentiment = params.get("sentiment")

        if month and not (start or end):
            try:
                year, m = map(int, month.split("-"))
                start_dt = datetime(year, m, 1, 0, 0, 0)
                last_day = monthrange(year, m)[1]
                end_dt = datetime(year, m, last_day, 23, 59, 59)
                try:
                    start_dt = make_aware(start_dt)
                    end_dt = make_aware(end_dt)
                except Exception:
                    pass
                qs = qs.filter(**{f"date__gte": start_dt, f"date__lte": end_dt})
            except Exception:
                return qs.none()

        if start:
            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
                try:
                    start_dt = make_aware(start_dt)
                except Exception:
                    pass
                qs = qs.filter(**{f"date__gte": start_dt})
            except ValueError:
                return qs.none()

        if end:
            try:
                end_dt = datetime.strptime(end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                try:
                    end_dt = make_aware(end_dt)
                except Exception:
                    pass
                qs = qs.filter(**{f"date__lte": end_dt})
            except ValueError:
                return qs.none()

        if sentiment:
            qs = qs.filter(sentiment__iexact=sentiment)

        return qs

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return NewsReadSerializer
        return NewsWriteSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        result = predict_sentiment(instance.title)
        instance.sentiment = result["label"]
        instance.sentiment_score = result["confidence"]
        instance.save()
        print(f"Predicted sentiment: {result['label']} (confidence: {result['confidence']})")
    
    @action(detail=False, methods=["post"], url_path="refresh-rss")
    def refresh_rss(self, request):
        try:
            limit = int(request.data.get("limit", 50))
        except Exception:
            limit = 50
        created, updated = fetch_cnbc_market_and_predict_sync(limit=limit)
        return Response({"created": created, "updated": updated}, status=status.HTTP_200_OK)

    # ---- Swagger docs (adds params to the existing list endpoint) ----
    @swagger_auto_schema(
        operation_summary="List news",
        tags=["News"],
        manual_parameters=[
            openapi.Parameter("start", openapi.IN_QUERY, description="Start date YYYY-MM-DD", type=openapi.TYPE_STRING),
            openapi.Parameter("end", openapi.IN_QUERY, description="End date YYYY-MM-DD", type=openapi.TYPE_STRING),
            openapi.Parameter("month", openapi.IN_QUERY, description="Month shortcut YYYY-MM (e.g., 2025-08)", type=openapi.TYPE_STRING),
            openapi.Parameter("sentiment", openapi.IN_QUERY, description="Filter sentiment (positive|neutral|negative)", type=openapi.TYPE_STRING),
            openapi.Parameter("search", openapi.IN_QUERY, description="Search in title (DRF SearchFilter)", type=openapi.TYPE_STRING),
            openapi.Parameter("ordering", openapi.IN_QUERY, description=f"Order by: id|title|date (prefix with - for desc)", type=openapi.TYPE_STRING),
            openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Page number"),
            openapi.Parameter("page_size", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Items per page"),
        ],
        responses={200: NewsReadSerializer(many=True)}
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a news", tags=["News"])
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a news",
        tags=["News"],
        request_body=NewsWriteSerializer,
        responses={201: NewsReadSerializer},
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a news", tags=["News"])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Partially update a news", tags=["News"])
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a news", tags=["News"])
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)
