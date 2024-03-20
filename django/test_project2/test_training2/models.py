from django.db import models
from djongo import models as mongomod


from django.contrib.auth.models import User

# Create your models here.


# class PolarModel(mongomod.Model):
#     sport = mongomod.CharField(max_length=256, default="RUNNING")
#     latitude = mongomod.DecimalField(decimal_places=6, max_digits=8)
#     longitude = mongomod.DecimalField(decimal_places=6, max_digits=8)

#     class Meta:
#         # db_table = "polar2022"
#         app_label = "test_polar"
#         managed = False


# @classmethod
# def using_mongo(cls):
#     return cls.objects.using("default")


class Trainingtype(models.Model):
    type_name = models.CharField(max_length=50, unique=True, primary_key=True)
    # datapath = models.FilePathField(max_length=256, path="C:/TEMP")
    datapath = models.FilePathField(max_length=256, path=".")

    @classmethod
    def using_sqlite(cls):
        return cls.objects.using("sqlite")


class Testpage(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.CharField(max_length=20)
    date = models.DateField()
