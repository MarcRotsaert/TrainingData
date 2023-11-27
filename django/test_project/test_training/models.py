from django.db import models
# Create your models here.


class Trainingtype(models.Model):
    type_name = models.CharField(max_length=50, unique=True, primary_key=True)
    image = models.FileField(max_length=256)
    datapath = models.FilePathField(max_length=256, path="C:/TEMP")


# class Trainingtype2(models.Model):
#     type_name = models.CharField(max_length=50, unique=True, primary_key=True)
#     image = models.FileField(max_length=256)
#     datapath = models.FilePathField(max_length=256, path="C:TEMP")


class Testpage(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.CharField(max_length=20)
    date = models.DateField()


