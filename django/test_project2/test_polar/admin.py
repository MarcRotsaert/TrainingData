from django.contrib import admin
from test_polar.models import PolarModel, UnittestModel
from test_training2.models import Trainingtype

admin.register(PolarModel)
admin.register(UnittestModel)
admin.register(Trainingtype)
# Register your models here.
