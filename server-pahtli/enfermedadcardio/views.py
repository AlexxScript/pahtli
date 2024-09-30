from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#LIBRERIA PARA CARGAR EL MODELO Y ESCALADOR
import joblib
import pandas as pd
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score, roc_auc_score,confusion_matrix
from sklearn.preprocessing import LabelEncoder

#LLAMADA DEL MODELO PACIENTE Y ESCALADOR
from .models import Paciente
from .serializers import PacienteSerializer,CardioSerializer

#CARGANDO EL MODELO DE ML
modelo = joblib.load("./enfermedadcardio/modeloMl/modelo (1).joblib")

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
        lines = lines[:-1]
        lines = lines[1:]
        escalador = joblib.load("./enfermedadcardio/modeloMl/escalador.joblib")
        predicciones = []
        rows = []
        for line in lines:
            fields = line.split(",")
            
            edad = int(fields[0])
            genero = fields[1]
            dolor_pec = fields[2]
            presion_art = float(fields[3])
            colesterol = float(fields[4])
            azucar = float(fields[5])
            electrocar = fields[6]
            frecuencia_car = int(fields[7])
            ang_ejercicio = fields[8]
            viejo_pico_ST = float(fields[9])
            st_slope = fields[10]
            tags = fields[11]
            rows.append([edad, genero, dolor_pec, presion_art, colesterol, azucar, electrocar, frecuencia_car, ang_ejercicio, viejo_pico_ST, st_slope,tags])

        df = pd.DataFrame(data = rows, columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
       'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope',
       'HeartDisease'])
        # for column in df.select_dtypes(include=['object']).columns:
        df['FastingBS'] = df['FastingBS'].astype('int64') 
        le = LabelEncoder()
        df['Sex'] = le.fit_transform(df['Sex'])
        df['ChestPainType'] = le.fit_transform(df['ChestPainType'])
        df['RestingECG'] = le.fit_transform(df['RestingECG'])
        df['ExerciseAngina'] = le.fit_transform(df['ExerciseAngina'])
        df['ST_Slope'] = le.fit_transform(df['ST_Slope'])
        df['HeartDisease'] = le.fit_transform(df['HeartDisease'])

        x = df.drop('HeartDisease', axis=1)
        y = df["HeartDisease"]
        x = escalador.transform(x)
        prediccion = modelo.predict(x)
        print(df.head())
        matriz = confusion_matrix(y,prediccion)
        metrica = f1_score(y,prediccion)
        print(matriz)
        predicciones.append({"a": prediccion, "prediccion": prediccion[0],"evaluacion":metrica})
        print(df.dtypes)
        return Response({"predicciones":predicciones},status=status.HTTP_200_OK)

