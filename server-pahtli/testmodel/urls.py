from django.urls import path
from . import views

app_name = "models"

urlpatterns = [
    path("",views.index)
]