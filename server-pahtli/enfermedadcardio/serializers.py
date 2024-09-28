from rest_framework import serializers
from .models import Cardio, Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id','nombre_paciente','edad','genero']

class CardioSerializer(serializers.Serializer):
    paciente = serializers.PrimaryKeyRelatedField(queryset = Paciente.objects.all())

    class Meta:
        model = Cardio
        fields = '__all__'