from rest_framework import viewsets, permissions, filters
from api.models.news_model import News, NewsReadSerializer, NewsWriteSerializer
from drf_yasg.utils import swagger_auto_schema
from api.services.sentiment import predict_sentiment 
from rest_framework.decorators import action
from rest_framework.response import Response
import csv
from io import TextIOWrapper
from api.models.news_source_model import NewsSource

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by("id")
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["id", "title"]

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

    @swagger_auto_schema(
        operation_summary="Import news from CSV",
        tags=["News"],
        request_body={
            'type': 'object',
            'properties': {
                'file': {'type': 'string', 'format': 'binary'}
            },
            'required': ['file']
        },
        responses={200: 'Import summary'},
    )
    @action(detail=False, methods=["post"], url_path="import-csv")
    def import_csv(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded."}, status=400)
        reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))
        imported = 0
        errors = []
        for row in reader:
            try:
                title = row["title"]
                date = row["date"]
                url = row["url"]
                img_url = row.get("img_url")
                # Find news source by URL domain (simple heuristic)
                domain = url.split("/")[2] if url else None
                news_source = NewsSource.objects.filter(homepage__contains=domain).first()
                if not news_source:
                    news_source = NewsSource.objects.first()  # fallback
                instance = News.objects.create(
                    news_source=news_source,
                    title=title,
                    date=date,
                    link=url,
                    image_link=img_url,
                )
                # result = predict_sentiment(title)
                # instance.sentiment = result["label"]
                # instance.sentiment_score = result["confidence"]
                instance.save()
                imported += 1
            except Exception as e:
                errors.append(str(e))
        return Response({"imported": imported, "errors": errors})
