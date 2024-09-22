from django.db import models
from usuario.models import CustomUser

# Create your models here.
class Paciente(models.Model):
    SELECCION_GENERO = [
        ('M',"MASCULINO"),
        ('F',"FEMENINO")
    ]
    nombre_paciente = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.CharField(max_length=10,choices=SELECCION_GENERO) 

class Cardio(models.Model):

    SELECCION_DOLOR_PECHO = [
        ('ASY','ASINTOMATICO'),
        ('NAP','SIN DOLOR ANGINAL'),
        ('ATA','ANGINA ATIPICA'),
        ('TA','ANGINA TIPICA')
    ]

    RESULTADOS_ELECTRO_REPOSO = [
        ('NORMAL', 'NORMAL'),
        ('ST', 'ANOMALIA DEL SEGMENTO ST'),
        ('LVH', 'HIPERTROFIA VENTRICULAR IZQUIERDA (LVH)'),
    ]

    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    tipo_dolor_pecho = models.CharField(max_length=20,choices=SELECCION_DOLOR_PECHO)
    presion_arterial_reposo = models.DecimalField(max_digits=10,decimal_places=2) #mm Hg
    colesterol = models.DecimalField(max_digits=10,decimal_places=2) #mm/dl
    azucar_sangre_ayuno = models.DecimalField(max_digits=10,decimal_places=2) #mg/dl si es mayor a 120 entonces es 1
    electrogardiograma_reposo = models.CharField(max_length=20,choices=RESULTADOS_ELECTRO_REPOSO)
    frecuencia_cardiaca_maxima = models.IntegerField()
    angina_por_ejercicio = models.CharField(max_length=5,choices=[('S','SI'),('N','NO')]) #N:0,S:1
    viejo_pico_ST = models.DecimalField(max_digits=10,decimal_places=2)
    st_slope = models.CharField(max_length=15,choices=[('up', 'ASCENDENTE'),('flat', 'PLANO'),('down', 'DESCENDENTE')])
    medico = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

