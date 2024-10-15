from django.urls import path
from .views import PacienteView,PrediccionIndividualCardioView,PrediccionCSView, EntrenarCardio,PacienteUpdateView,EntrenarCardioActualizarView

app_name = "cardio"

urlpatterns = [
    path("paciente/",PacienteView.as_view(),name="paciente"),
    path("paciente/<int:id_paciente>",PacienteUpdateView.as_view(),name="pacienteupdate"),
    path("predecir/",PrediccionIndividualCardioView.as_view(),name="cardio"),
    path("subir/",PrediccionCSView.as_view(),name="cardiocsv"),
    path("entrenar/",EntrenarCardio.as_view(),name="cardioentrenar"),
    path("entrenar/<int:id_paciente>",EntrenarCardioActualizarView.as_view(),name="cardioentrenaractualizar"),
]