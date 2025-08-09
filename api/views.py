from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
import pickle
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import NewsSource

# ==== Load model dan tokenizer ====
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# Load label mapping
with open(os.path.join(MODEL_PATH, "label_mappings.pkl"), "rb") as f:
    w2i, i2w = pickle.load(f)

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
            inputs = tokenizer(
                text,
                return_tensors="pt",
                max_length=128,
                truncation=True,
                padding=True
            )
            with torch.no_grad():
                outputs = model(**inputs)
                probs = softmax(outputs.logits, dim=1)
                predicted_label = torch.argmax(probs, dim=1).item()
                confidence = torch.max(probs).item()
            return Response({
                "text": text,
                "label": i2w[predicted_label],
                "confidence": round(confidence, 4)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = ['id', 'name', 'homepage', 'logo_img']

class NewsSourceListView(APIView):
    @swagger_auto_schema(
        operation_description="Get list of news sources",
        responses={
            200: openapi.Response(
                description="List of news sources",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'homepage': openapi.Schema(type=openapi.TYPE_STRING),
                            'logo_img': openapi.Schema(type=openapi.TYPE_STRING, format='uri', nullable=True),
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        sources = NewsSource.objects.all()
        serializer = NewsSourceSerializer(sources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
