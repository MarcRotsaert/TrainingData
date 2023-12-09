from django.urls import path, re_path
from test_training2 import views

app_name = "test_training2"

urlpatterns = [
    path("training/", views.select_ttype, name="testpage"),
    # path("select_ttype/", views.select_ttype2, name="selectttype"),
    # re_path(r"^add_ttype/$", views.add_ttype, name="addttype")
    path("add_ttype/", views.add_ttype, name="addttype"),
    # path("polar/", views.show_polar, name="showpolar"),
]
