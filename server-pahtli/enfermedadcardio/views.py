from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#LIBRERIA PARA CARGAR EL MODELO Y ESCALADOR
import joblib
import pandas as pd
from sklearn.metrics import f1_score,accuracy_score,precision_score,recall_score, roc_auc_score,confusion_matrix
from sklearn.preprocessing import LabelEncoder, RobustScaler

#LLAMADA DEL MODELO PACIENTE Y ESCALADOR
from .models import Paciente
from .serializers import PacienteSerializer,CardioSerializer, CardioGuardarSerializer

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
        escalador = joblib.load("./enfermedadcardio/modeloMl/escalador_o.joblib")
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

#CREANDO LA VISTA PARA LA PREDICCION A PARTIR DE CSV Y SIN ALMACENAR EN LA BD
class PrediccionCSView(APIView):
    #TIPO DE AUTENTICACION QUE SE ESTA UTILIZANDO
    authentication_classes = [TokenAuthentication]
    #QUIENES TENDRAN ACCESO A ESTE ENDPOINT
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #OBTENESMOS EL ARCHIVO QUE VIENE EN EL JSON CON LA KEY archivo 
        csv_file = request.FILES['archivo']
        #LEEMOS EL ARCHIVO QUE OBTUVIMOS DEL FORM

        file_data = csv_file.read().decode("utf-8")
        #CADA VEZ QUE VEA UN SALTO DE LINEA CREA UN NUEVO ELEMENTO EN LA LISTA, ES DECIR LA
        #LISTA VA A CONTENER CADA ELEMENTO DE LA FILA DEL CSV
        lines = file_data.split("\n")
        #ELIMINA LA ULTIMA LINEA DE LA LISTA
        lines = lines[:-1]
        #ELIMINA LA PRIMERA LINEA DE LA LISTA
        lines = lines[1:]
        #CARGAMOS EL ESCALADOR
        escalador = joblib.load("./enfermedadcardio/modeloMl/escalador_o.joblib")
        predicciones = []
        #LISTA PARA ALMACENAR CADA UNO DE LOS ELEMENTOS DE LA LISTA ANTERIOR DE TAL FORMA QUE SE SEPAREN POR LISTAS Y NO POR COMAS 
        rows = []
        for line in lines:
            #SE TOMA EL STRING LINE Y POR CADA COMA QUE ENCUENTRE EN EL STRING SE CONVIERTE EN UN ELEMENTO DE LA LISTA QUE SE CREA
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
            #AÑADE LA LISTA DENTRO DE LA LISTA ROWS
            rows.append([edad, genero, dolor_pec, presion_art, colesterol, azucar, electrocar, frecuencia_car, ang_ejercicio, viejo_pico_ST, st_slope,tags])
        #SE CREA EL DF O TABLA 
        df = pd.DataFrame(data = rows, columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
       'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope',
       'HeartDisease'])
        

        #SE ETIQUETAN LOS VALORES CATEGÓRICOS EN VALORES ENTEROS PARA SU PROCESAMIENTO EN EL MODELO
        le = LabelEncoder()
        df['Sex'] = le.fit_transform(df['Sex'])
        df['ChestPainType'] = le.fit_transform(df['ChestPainType'])
        df['RestingECG'] = le.fit_transform(df['RestingECG'])
        df['ExerciseAngina'] = le.fit_transform(df['ExerciseAngina'])
        df['ST_Slope'] = le.fit_transform(df['ST_Slope'])
        df['HeartDisease'] = le.fit_transform(df['HeartDisease'])

        #SE SEPARAN LOS DATOS PREDICTORES Y LOS OBJETIVOS, EN ESTE SOLO SON NECESARIOS LOS PREDICTORES
        x = df.drop('HeartDisease', axis=1)
        #NO ES NECESARIO Y YA QUE SON PREDICCIONES, EN ESTE MOMENTO ESTA AQUÍ POR CUESTIONES DE PRUEBAS
        y = df["HeartDisease"]
        #SE ESCALAN LOS DATOS PREDICTORES
        x = escalador.transform(x)
        #SE REALIZA LA PREDICCION
        prediccion = modelo.predict(x)
        probabilidades = modelo.predict_proba(x)
        print(df.head())
        #SE MUESTRA LA MATRIZ DE CONFUSION SOLO PARA PRUEBA
        matriz = confusion_matrix(y,prediccion)
        metrica = f1_score(y,prediccion)
        print(matriz)
        predicciones.append({"a": prediccion, "prediccion": prediccion[0],"evaluacion":metrica,"probabilidades":probabilidades})
        return Response({"predicciones":predicciones},status=status.HTTP_200_OK)
 
#CREANDO VISTA O ENDPOINT PARA ALMACENAR DATOS DE ENTRENAMIENTO (TAG O RESULTADO) EN LA BASE DE DATOS
class EntrenarCardio(APIView):
    #TIPO DE AUTENTICACION QUE SE ESTA UTILIZANDO
    authentication_classes = [TokenAuthentication]
    #QUIENES PODRAN ACCEDER A ESTE ENDPOINT
    permission_classes = [IsAuthenticated]
    def post(self, request):
        csv_file = request.FILES['archivo']
        
        file_data = csv_file.read().decode("utf-8")
        #CADA VEZ QUE VEA UN SALTO DE LINEA CREA UN NUEVO ELEMENTO EN LA LISTA, ES DECIR LA
        #LISTA VA A CONTENER CADA ELEMENTO DE LA FILA DEL CSV
        lines = file_data.split("\n")
        #ELIMINA LA ULTIMA LINEA DE LA LISTA
        lines = lines[:-1]
        #ELIMINA LA PRIMERA LINEA DE LA LISTA
        lines = lines[1:]
        for line in lines:
            fields = line.split(",")

            nombre = fields[0]
            edad = int(fields[1])
            genero = fields[2]
            paciente_data = {
                'nombre': nombre,
                'edad': edad,
                'genero': genero
            }

            serializador_paciente = PacienteSerializer(data = paciente_data)
            #SE TOMA EL STRING LINE Y POR CADA COMA QUE ENCUENTRE EN EL STRING SE CONVIERTE EN UN ELEMENTO DE LA LISTA QUE SE CREA

            if not serializador_paciente.is_valid():
            #SE GUARDA EN LA BASE DE DATOS Y SE UTILIZA EL MÉTODO CREATE DEL SERIALIZADOR Y MODELO
                return Response(serializador_paciente.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                paciente = serializador_paciente.save()
                dolor_pec = fields[3]
                presion_art = float(fields[4])
                colesterol = float(fields[5])
                azucar = float(fields[6])
                electrocar = fields[7]
                frecuencia_car = int(fields[8])
                ang_ejercicio = fields[9]
                viejo_pico_ST = float(fields[10])
                st_slope = fields[11]
                tags = fields[12]
                cardio_data = {
                    'paciente': paciente.id,  # Aquí asociamos el paciente creado
                    'dolor_pec': dolor_pec,
                    'presion_art': presion_art,
                    'colesterol': colesterol,
                    'azucar': azucar,
                    'electrocar': electrocar,
                    'frecuencia_car': frecuencia_car,
                    'ang_ejercicio': ang_ejercicio,
                    'viejo_pico_ST': viejo_pico_ST,
                    'st_slope': st_slope,
                    'tags': tags
                }
                serializador_cardio = CardioGuardarSerializer(data = cardio_data)
                if serializador_cardio.is_valid():
                    serializador_cardio.save()
                    return Response({"mensaje": "Datos guardados correctamente."}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializador_cardio.errors, status=status.HTTP_400_BAD_REQUEST)