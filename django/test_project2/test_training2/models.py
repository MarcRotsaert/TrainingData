from django.db import models
from djongo import models as mongomod


from django.contrib.auth.models import User
# Create your models here.


class PolarModel(mongomod.Model):
    sport = mongomod.CharField(max_length=256, default="RUNNING")
    latitude = mongomod.DecimalField(decimal_places=6, max_digits=8)
    longitude = mongomod.DecimalField(decimal_places=6, max_digits=8)

    class Meta:
        db_table = "garminfit"
        app_label = "test_polar"
        managed = False


# @classmethod
# def using_mongo(cls):
#     return cls.objects.using("default")


class Trainingtype(models.Model):
    type_name = models.CharField(max_length=50, unique=True, primary_key=True)
    datapath = models.FilePathField(max_length=256, path="C:/TEMP")

    @classmethod
    def using_sqlite(cls):
        return cls.objects.using("sqlite")


# class Trainingtype2(models.Model):
#     type_name = models.CharField(max_length=50, unique=True, primary_key=True)
#     image = models.FileField(max_length=256)
#     datapath = models.FilePathField(max_length=256, path="C:TEMP")


class Testpage(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.CharField(max_length=20)
    date = models.DateField()


class UserProfile(models.model):
    user = models.OneToOneField(User)
    portfolio = models.UrlField(blank=True)


    def __str__(self):
        return self.user.username
    