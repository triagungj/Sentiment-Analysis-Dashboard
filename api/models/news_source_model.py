from django.db import models
from rest_framework import serializers

class NewsSource(models.Model):
    name = models.CharField(max_length=255)
    homepage = models.URLField(max_length=500)

    def __str__(self):
        return self.name

class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = ["id", "name", "homepage"]
        read_only_fields = ["id"]

