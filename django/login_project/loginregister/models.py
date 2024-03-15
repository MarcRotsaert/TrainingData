from django.db import models

# from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return self.user.get_username()
