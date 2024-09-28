from django.urls import path
from .views import PacienteView,PrediccionCardioView

app_name = "cardio"

urlpatterns = [
    path("paciente/",PacienteView.as_view(),name="paciente"),
    path("predecir/",PrediccionCardioView.as_view(),name="cardio")
]