from django.urls import path
from test_training import views

urlpatterns = [
    path('training/', views.select_ttype, name="testpage"),
    path('select_ttype/', views.select_ttype2, name="selectttype"),
    path("add_ttype/",views.add_ttype, name="addtype")
    ]
