from django.urls import path, re_path
from test_polar import views

app_name = "test_polar"

urlpatterns = [
    # re_path(r"^add_ttype/$", views.add_ttype, name="addttype")
    path("summary/", views.show_polar, name="showpolar"),
    path(
        "summary/return_lapdata/<str:fname>",
        views.show_lapdata,
        name="showlapdata",
    ),
    path("adapt/", views.action_adapt, name="actionadapt"),
    path("adapt/form/<str:fname>", views.show_form, name="showform"),
]
