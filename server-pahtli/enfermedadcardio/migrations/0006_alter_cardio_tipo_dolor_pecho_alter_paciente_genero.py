# Generated by Django 5.0.6 on 2024-09-28 00:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "enfermedadcardio",
            "0005_alter_cardio_tipo_dolor_pecho_alter_paciente_genero",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="cardio",
            name="tipo_dolor_pecho",
            field=models.IntegerField(
                choices=[
                    (0, "ASINTOMATICO"),
                    (2, "SIN DOLOR ANGINAL"),
                    (1, "ANGINA ATIPICA"),
                    (3, "ANGINA TIPICA"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="paciente",
            name="genero",
            field=models.IntegerField(choices=[(1, "MASCULINO"), (0, "FEMENINO")]),
        ),
    ]
