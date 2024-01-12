from django.urls import path, re_path
from test_polar import views

app_name = "test_polar"

urlpatterns = [
    # re_path(r"^add_ttype/$", views.add_ttype, name="addttype")
    path("summary/return_lapdata/", views.show_lapdata, name="showlapdata"),
    path("summary/", views.show_polar, name="showpolar"),
    path("adapt/", views.show_adapt, name="showadapt"),
    path("adapt/change", views.show_form, name="showform"),
]
