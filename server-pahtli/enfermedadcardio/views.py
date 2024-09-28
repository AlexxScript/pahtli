from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#LIBRERIA PARA CARGAR EL MODELO Y ESCALADOR
import joblib

#LLAMADA DEL MODELO PACIENTE Y ESCALADOR
from .models import Paciente
from .serializers import PacienteSerializer,CardioSerializer

#CARGANDO EL MODELO DE ML
modelo = joblib.load("./enfermedadcardio/modeloMl/modelo.joblib")

#CREANDO VISTA DE PACIENTE PARA REALIZAR CONSULTAS PERSONALIZADAS (APIVIEW)
class PacienteView(APIView):
    #SE REQUIERE AUTENTICACION Y TOKEN PARA TENER ACCESO A ESTA VISTA O ENDPOINT
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #EN LA OPERACION POST VAMOS A CREAR UN USUARIO
    def post(self,request):
        #MANDAMOS LOS DATOS AL SERIALIZADOR
        serializer = PacienteSerializer(data=request.data)
        #VALIDAMOS QUE TENGAN LOS FORMATOS CORRECTOR
        if serializer.is_valid():
            #SE GUARDA EN LA BASE DE DATOS Y SE UTILIZA EL MÉTODO CREATE DEL SERIALIZADOR Y MODELO
            serializer.save()
            return Response({"idPaciente":serializer.data["id"]},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CREANDO LA VISTA PARA LA PREDICCION MAS NO ALMACENAMIENTO DE ENTRENAMIENTO
class PrediccionCardioView(APIView):
    #SE REQUIERE AUTENTICACION Y TOKEN PARA TENER ACCESO A ESTA VISTA O ENDPOINT
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #CARAGAMOS EL ESCALADOR
        escalador = joblib.load("./enfermedadcardio/modeloMl/escalador.joblib")
        #MANDAMOS LOS DATOS AL SERIALIZADOR PARA SU VALIDACIÓN
        serializer = CardioSerializer(data=request.data)
        if serializer.is_valid():
            #EXTRAEMOS LO DATOS DE LA PETICIÓN PARA SU TRATAMIENTO 
            fasting_bs = 0
            paciente = request.data['paciente']
            dolor_pec = request.data['tipo_dolor_pecho']
            presion_art = request.data['presion_arterial_reposo']
            colesterol = request.data['colesterol']
            azucar = request.data['azucar_sangre_ayuno']
            electrocar = request.data['electrogardiograma_reposo']
            frecuencia_car = request.data['frecuencia_cardiaca_maxima']
            ang_ejercicio = request.data['angina_por_ejercicio']
            viejo_pico_ST = request.data['viejo_pico_ST']
            st_slope = request.data['st_slope']
            medico = request.data['medico']
            patient = Paciente.objects.get(id=paciente)

            if azucar > 120:
                fasting_bs = 1
            #ESCALAMOS Y PREDECIMOS
            escalador.transform([[patient.edad,patient.genero,dolor_pec,presion_art,colesterol,fasting_bs,electrocar,frecuencia_car,ang_ejercicio,viejo_pico_ST,st_slope]])
            prediccion = modelo.predict_proba([[patient.edad,patient.genero,dolor_pec,presion_art,colesterol,fasting_bs,electrocar,frecuencia_car,ang_ejercicio,viejo_pico_ST,st_slope]])
            return Response({"prediccion":prediccion[0]},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

