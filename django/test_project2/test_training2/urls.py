from django.urls import path, re_path
from test_training2 import views

app_name = "test_training2"

urlpatterns = [
    # re_path(r"^add_ttype/$", views.add_ttype, name="addttype")
    # path("", views.add_ttype, name="addttype"),
    path("", views.select_ttype, name="testpage"),
]
