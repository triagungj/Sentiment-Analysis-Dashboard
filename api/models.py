from django.db import models

class NewsSource(models.Model):
    name = models.CharField(max_length=255)
    homepage = models.URLField(max_length=500)
    logo_img = models.ImageField(upload_to='news_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
