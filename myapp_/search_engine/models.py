from django.db import models

# Create your models here.
class Uploadxml(models.Model):
    file = models.FileField(upload_to='./search_engine/data')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Word(models.Model):
    

class article(models.Model):
    file = models.CharField(max_length=200)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, , related_name='terms')