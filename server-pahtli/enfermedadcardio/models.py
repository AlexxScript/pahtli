from django.db import models
from usuario.models import CustomUser

# Create your models here.
class Paciente(models.Model):
    #0,1 se guardaran en la base de datos en el formulario
    SELECCION_GENERO = [
        (1,"MASCULINO"),
        (0,"FEMENINO")
    ]
    nombre_paciente = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.IntegerField(choices=SELECCION_GENERO) 

class Cardio(models.Model):

    SELECCION_DOLOR_PECHO = [
        (0,'ASINTOMATICO'),
        (2,'SIN DOLOR ANGINAL'),
        (1,'ANGINA ATIPICA'),
        (3,'ANGINA TIPICA')
    ]

    RESULTADOS_ELECTRO_REPOSO = [
        (1, 'NORMAL'),
        (0, 'ANOMALIA DEL SEGMENTO ST'),
        (2, 'HIPERTROFIA VENTRICULAR IZQUIERDA (LVH)'),
    ]

    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    tipo_dolor_pecho = models.IntegerField(choices=SELECCION_DOLOR_PECHO)
    presion_arterial_reposo = models.DecimalField(max_digits=10,decimal_places=2) #mm Hg
    colesterol = models.DecimalField(max_digits=10,decimal_places=2) #mm/dl
    azucar_sangre_ayuno = models.DecimalField(max_digits=10,decimal_places=2) #mg/dl si es mayor a 120 entonces es 1
    electrogardiograma_reposo = models.IntegerField(choices=RESULTADOS_ELECTRO_REPOSO)
    frecuencia_cardiaca_maxima = models.IntegerField()
    angina_por_ejercicio = models.IntegerField(choices=[(1,'SI'),(0,'NO')]) #N:0,S:1
    viejo_pico_ST = models.DecimalField(max_digits=10,decimal_places=2)
    st_slope = models.IntegerField(choices=[(2, 'ASCENDENTE'),(1, 'PLANO'),(0, 'DESCENDENTE')])
    medico = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

