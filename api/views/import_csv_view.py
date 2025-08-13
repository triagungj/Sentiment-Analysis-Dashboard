from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import csv
from io import TextIOWrapper
from api.models.news_model import News
from api.models.news_source_model import NewsSource
from api.services.sentiment import predict_sentiment
from rest_framework.decorators import action
from rest_framework.response import Response

class ImportNewsCSVView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="Import news from CSV",
        tags=["News"],
        manual_parameters=[
            openapi.Parameter(
                'file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description='CSV file to import'
            )
        ],
        request_body=None,
        responses={200: openapi.Response('Import summary', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'imported': openapi.Schema(type=openapi.TYPE_INTEGER),
                'errors': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
            }
        ))},
    )
    def post(self, request):
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
                domain = url.split("/")[2] if url else None
                news_source = NewsSource.objects.filter(homepage__contains=domain).first()
                if not news_source:
                    news_source = NewsSource.objects.first()
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
