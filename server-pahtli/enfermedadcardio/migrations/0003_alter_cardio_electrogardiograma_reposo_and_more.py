# Generated by Django 5.0.6 on 2024-09-27 22:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enfermedadcardio", "0002_alter_cardio_angina_por_ejercicio_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cardio",
            name="electrogardiograma_reposo",
            field=models.IntegerField(
                choices=[
                    (1, "NORMAL"),
                    (0, "ANOMALIA DEL SEGMENTO ST"),
                    (2, "HIPERTROFIA VENTRICULAR IZQUIERDA (LVH)"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="cardio",
            name="st_slope",
            field=models.IntegerField(
                choices=[(2, "ASCENDENTE"), (1, "PLANO"), (0, "DESCENDENTE")]
            ),
        ),
    ]
