from .models import CustomUser
from rest_framework import serializers

#SERIALIZANDO PARA CONVERTIR LOS TIPOS DE DATOS DE PYTHON AL FORMATO JSON
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','email','nombres','apellido_pa','apellido_ma','password','numero_celular']

#MÉTODO QUE SE EJECUTA DESPUES DE LLAMAR EL MÉTODO SAVE
    def create(self, validated_data):
        #CREACIÓN O REGISTRO DEL USUARIO EN LA BASE DE DATOS
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            nombres=validated_data['nombres'],
            apellido_pa=validated_data['apellido_pa'],
            apellido_ma=validated_data['apellido_ma'],
            numero_celular=validated_data['numero_celular'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email","password"]