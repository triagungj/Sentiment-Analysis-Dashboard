from rest_framework import viewsets, permissions, filters
from api.models.news_model import News, NewsReadSerializer, NewsWriteSerializer
from drf_yasg.utils import swagger_auto_schema
from api.services.sentiment import predict_sentiment 
from rest_framework.pagination import PageNumberPagination

class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by("id")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["id", "title"]
    pagination_class = NewsPagination

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return NewsReadSerializer
        return NewsWriteSerializer

    def perform_create(self, serializer):
        # Save the object first
        instance = serializer.save()

        # Run prediction on the title (or full text if available)
        result = predict_sentiment(instance.title)

        # Save the predicted label to sentiment field
        instance.sentiment = result["label"]  # must match your model's choices
        instance.sentiment_score = result["confidence"]
        instance.save()

        # Optionally: log or attach confidence somewhere
        print(f"Predicted sentiment: {result['label']} (confidence: {result['confidence']})")

    @swagger_auto_schema(operation_summary="List news", tags=["News"])
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
