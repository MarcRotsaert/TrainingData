from django.db import models
from djongo import models as mongomod

# Create your models here.

# class PolarModel(mongomod.Model):
#     # garminfit = mongomod.JSONField()
#     sport = mongomod.CharField(max_length=256, default="RUNNING")
#     class Meta:
#         db_table = "testdatabase"
#         app_label= "test_training"
        # managed = False
        # using = "mongodb"


class Trainingtype(models.Model):
    type_name = models.CharField(max_length=50, unique=True, primary_key=True)
    # image = models.FileField(max_length=256)
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


