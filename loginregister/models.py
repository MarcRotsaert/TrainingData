from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return self.user.get_username()

    @classmethod
    def using_sqlite(cls):
        return cls.objects.using("sqlite")
