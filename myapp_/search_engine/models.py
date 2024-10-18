from django.db import models

# Create your models here.
class Uploadxml(models.Model):
    file = models.FileField(upload_to='./search_engine/data')
    uploaded_at = models.DateTimeField(auto_now_add=True)