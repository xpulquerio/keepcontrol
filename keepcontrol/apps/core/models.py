from django.db import models
from apps.series.models import Serie

# Create your models here.
class Season(models.Model):
    title = models.CharField(max_length=255)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.title

class Episode(models.Model):
    title = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=False)
    

    def __str__ (self):
        return self.title


    