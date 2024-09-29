from django.urls import path
from .views import PacienteView,PrediccionIndividualCardioView,PrediccionCSView

app_name = "cardio"

urlpatterns = [
    path("paciente/",PacienteView.as_view(),name="paciente"),
    path("predecir/",PrediccionIndividualCardioView.as_view(),name="cardio"),
    path("subir/",PrediccionCSView.as_view(),name="cardiocsv"),
]