from django.db import models
# Create your models here.


class Trainingtype(models.Model):
    type_name = models.CharField(max_length=50, unique=True, primary_key=True)
    image = models.FileField(max_length=256)
    



