from django.db import models

# from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    portfolio = models.URLField(blank=True)
    inlogname = models.TextField(default="")
    databasename = models.TextField(default="")
    password = models.TextField(default="")
    host = models.TextField(default="localhost")
    port = models.IntegerField(default=27017)

    def __str__(self):
        return self.user.get_username()

    @classmethod
    def get_entry(cls, idnr):
        try:
            return cls.objects.get(user_id=idnr)
        except cls.DoesNotExist:
            return None
