from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.services.sentiment import predict_sentiment

class SentimentRequestSerializer(serializers.Serializer):
    text = serializers.CharField()

class PredictSentimentView(APIView):
    @swagger_auto_schema(
        request_body=SentimentRequestSerializer,
        responses={
            200: openapi.Response(
                description="Sentiment prediction result",
                examples={
                    "application/json": {
                        "text": "Contoh kalimat",
                        "label": "positive",
                        "confidence": 0.9876
                    }
                }
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = SentimentRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            result = predict_sentiment(text)
            return Response({"text": text, **result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
