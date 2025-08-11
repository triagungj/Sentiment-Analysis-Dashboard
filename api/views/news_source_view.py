from rest_framework import viewsets, permissions, filters
from api.models.news_source_model import NewsSource, NewsSourceSerializer
from drf_yasg.utils import swagger_auto_schema

class NewsSourceViewSet(viewsets.ModelViewSet):
    queryset = NewsSource.objects.all().order_by("id")
    serializer_class = NewsSourceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "homepage"]
    ordering_fields = ["id", "name"]

    @swagger_auto_schema(operation_summary="List news sources", tags=["NewsSource"])
    def list(self, *args, **kwargs): return super().list(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a news source", tags=["NewsSource"])
    def retrieve(self, *args, **kwargs): return super().retrieve(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a news source",
        tags=["NewsSource"],
        request_body=NewsSourceSerializer,
        responses={201: NewsSourceSerializer},
    )
    def create(self, *args, **kwargs): return super().create(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a news source", tags=["NewsSource"])
    def update(self, *args, **kwargs): return super().update(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Partially update a news source", tags=["NewsSource"])
    def partial_update(self, *args, **kwargs): return super().partial_update(*args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a news source", tags=["NewsSource"])
    def destroy(self, *args, **kwargs): return super().destroy(*args, **kwargs)
