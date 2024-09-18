from django.urls import path
from .views import UsuarioRegisterView, UsuarioLoginView

app_name = "usuario"

urlpatterns = [
    path('registrar/', UsuarioRegisterView.as_view(), name='registrar'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
]
