# Generated by Django 5.0.6 on 2024-09-28 00:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("enfermedadcardio", "0003_alter_cardio_electrogardiograma_reposo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paciente",
            name="nombre_paciente",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
