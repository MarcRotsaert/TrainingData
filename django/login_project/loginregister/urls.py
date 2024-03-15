from django.urls import path, re_path
from loginregister import views

app_name = "loginregister"

urlpatterns = [
    # re_path(r"^add_ttype/$", views.add_ttype, name="addttype")
    # path("", views.add_ttype, name="addttype"),
    path("login/", views.login_page, name="login"),
    path("register/", views.registration, name="register"),
]
