from django.db import models

# Create your models here.
class Cardio(models.Model):
    SELECCION_GENERO = [
        ('M',"MASCULINO"),
        ('F',"FEMENINO")
    ]

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
    edad = models.BigIntegerField()
    genero = models.CharField(choices=SELECCION_GENERO)
    tipo_dolor_pecho = models.CharField(choices=SELECCION_DOLOR_PECHO)
    presion_arterial_reposo = models.DecimalField(decimal_places=2) #mm Hg
    colesterol = models.DecimalField(decimal_places=2) #mm/dl
    azucar_sangre_ayuno = models.DecimalField(decimal_places=2) #mg/dl si es mayor a 120 entonces es 1
    electrogardiograma_reposo = models.CharField(choices=RESULTADOS_ELECTRO_REPOSO)
    frecuencia_cardiaca_maxima = models.IntegerField()
    angina_por_ejercicio = models.CharField(choices=[('S','SI'),('N','NO')]) #N:0,S:1
    viejo_pico_ST = models.DecimalField(decimal_places=2)
    ST_Slope = models.CharField(choices=[('up', 'ASCENDENTE'),('flat', 'PLANO'),('down', 'DESCENDENTE')])
