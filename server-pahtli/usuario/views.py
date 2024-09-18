from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserCreateSerializer, UserLoginSerializer
from django.contrib.auth import password_validation, authenticate
# Create your views here.

#CREACIÓN DE LAS APIS O ENDPOINTS

#VISTAS PARA LA LÓGICA DEL REGISTRO DE USUARIO CON EL CONTROL COMPLETO DE LOS DATOS (APIView)
class UsuarioRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
   
    #LA CLASE VA A EJECUTAR ESTE MÉTODO CUANDO EL TIPO DE PETICIÓN SEA POST
    def post(self,request):
        #VA A VALIDAR LOS DATOS CON BASE EN LAS CARACTERÍSTICAS QUE ESPECIFICAMOS
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            #SE VA A GUARDAR EL USUARIO CON BASE EN EL MÉTODO CREATE CREADO EN EL SERIALIZADOR
            serializer.save()
            user = CustomUser.objects.get(email=serializer.data["email"])
            token = Token.objects.create(user=user)
            return Response({"token":token.key,"user":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#VISTAS PARA LA LÓGICA DE LA AUTENTICACIÓN DEL USUARIO CON EL CONTROL COMPLETO DE LOS DATOS (APIView)
class UsuarioLoginView(APIView):
    def post(self,request):
        user = get_object_or_404(CustomUser,email=request.data["email"])
        if not user.check_password(request.data["password"]):
            return Response({"error":"contrasenia invalida"},status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserLoginSerializer(instance=user)
        return Response({"token":token.key,"user": serializer.data}, status=status.HTTP_200_OK)