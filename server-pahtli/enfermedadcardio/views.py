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
class PrediccionIndividualCardioView(APIView):
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

class PrediccionCSView(APIView):
    def post(self, request):
        csv_file = request.FILES['archivo']
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        escalador = joblib.load("./enfermedadcardio/modeloMl/escalador.joblib")
        predicciones = []
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict['paciente'] = fields[0]
            dolor_pec = fields[1]
            presion_art = float(fields[2])
            colesterol = float(fields[3])
            azucar = float(fields[4])
            electrocar = fields[5]
            frecuencia_car = float(fields[6])
            ang_ejercicio = fields[7]
            viejo_pico_ST = float(fields[8])
            st_slope = fields[9]

            datos_paciente = [[presion_art, colesterol, azucar, electrocar, frecuencia_car, ang_ejercicio, viejo_pico_ST, st_slope]]
            datos_paciente_escalados = escalador.transform(datos_paciente)
            prediccion = modelo.predict(datos_paciente_escalados)
            predicciones.append({"paciente": fields[0], "prediccion": prediccion[0]})

            # fasting_bs = 0
            # data_dict['paciente'] = fields[0]
            # data_dict['dolor_pec'] = fields[1]
            # data_dict['presion_art'] = fields[2]
            # data_dict['colesterol'] = fields[3]
            # data_dict['azucar'] = fields[4]
            # data_dict['electrocar'] = fields[5]
            # data_dict['frecuencia_car'] = fields[6]
            # data_dict['ang_ejercicio'] = fields[7]
            # data_dict['viejo_pico_ST'] = fields[8]
            # data_dict['st_slope'] = fields[9]
            # medico = request.data['medico']

        print(csv_file)
        return Response({"predicciones":predicciones},status=status.HTTP_200_OK)

