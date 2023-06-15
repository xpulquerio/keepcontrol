from django.db import models

# Create your models here.
   
class Serie(models.Model):
    title = models.CharField(max_length=255)
    title_en = models.CharField(null=True, max_length=255, blank=True)
    autor = models.CharField(null=True, max_length=255, blank=True)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.title
    
    