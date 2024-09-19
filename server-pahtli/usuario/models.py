from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

#https://docs.djangoproject.com/en/5.1/topics/auth/customizing/ Recursos utilizados

#ESTAMOS PERSONALIZANDO EL REGISTRO DE USUARIO A TRAVES DE LO CAMPOS QUE ACABAMOS DE AÑADIR
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombres, apellido_pa, apellido_ma, numero_celular, password=None,**extra_fields):
        if not email:
            raise ValueError('El email es requerido') 
        user = self.model(
            email=self.normalize_email(email),
            nombres=nombres,
            apellido_pa=apellido_pa,
            apellido_ma=apellido_ma,
            numero_celular=numero_celular,
            #EL DOBLE ASTERISTO NOS PERMITE EXTRAER LOS DATOS QUE SE INGRESARON EN ESE CAMPO
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombres, apellido_pa, apellido_ma, numero_celular, password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        return self.create_user(email, nombres, apellido_pa, apellido_ma, numero_celular, password,**extra_fields)

#AÑADIMOS LOS CAMPOS QUE QUEREMOS QUE CONTENGA EL MODELO DE USUARIO
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombres = models.CharField(max_length=100)
    apellido_pa = models.CharField(max_length=100)
    apellido_ma = models.CharField(max_length=100)
    numero_celular = models.CharField(max_length=10,unique=True)

    #DATOS OBLIGATORIOS PARA DJANGO
    # date_joined = models.DateTimeField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #USO DE LOS MÉTODOS PARA GUARDAR AL USUARIO
    objects = CustomUserManager()

    #CAMPO QUE SE VA A UTILIZAR PARA LA AUTENTICACIÓN DEL USUARIO
    USERNAME_FIELD = 'email'

    #CAMPOS OBLIGATORIOS QUE DEBEN ESTAR LLENOS O NO PUEDEN SER NULOS
    REQUIRED_FIELDS = ['nombres', 'apellido_pa', 'apellido_ma', 'numero_celular']

    def __str__(self):
        return self.email