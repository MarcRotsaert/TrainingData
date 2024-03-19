from django.db import models

# from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    portfolio = models.URLField(blank=True)
    inlogname = models.TextField(default="")
    databasename = models.TextField(default="polartest")
    password = models.TextField(default="")
    host = models.TextField(default="localhost")
    port = models.IntegerField(default=27017)

    def __str__(self):
        return self.user.get_username()

    @classmethod
    def get_entry(cls, idnr):
        print(cls.objects)
        # print(cls.objects.get(pk=idnr))
        # cls.objects.
        # print(cls.objects.filter(user_id=idnr))
        print(cls.objects.filter(user_id=idnr))
        return cls.objects.filter(user_id=idnr)
