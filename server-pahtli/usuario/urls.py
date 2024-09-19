from django.urls import path
from .views import UsuarioRegisterView, UsuarioLoginView, TestView

app_name = "usuario"

urlpatterns = [
    path('registrar/', UsuarioRegisterView.as_view(), name='registrar'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('test/', TestView.as_view(), name='test'),
]
