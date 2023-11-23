from django.urls import path
from test_training import views

urlpatterns = [
    path('training/', views.test, name="testpage")
    ]
