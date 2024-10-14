from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#LIBRERIA PARA CARGAR EL MODELO Y ESCALADOR
import joblib

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
            angina = 0
            electro = 0
            st = 0
            paciente = request.data['paciente']
            ang_ejercicio = 1 if request.data['angina_por_ejercicio'] == "SI" else 0
            patient = Paciente.objects.get(id=paciente)

            if request.data['azucar_sangre_ayuno'] > 120:
                fasting_bs = 1

            if request.data['tipo_dolor_pecho'] == "ASINTOMATICO":
                angina = 0
            elif request.data['tipo_dolor_pecho'] == "ANGINA ATIPICA":
                angina = 1
            elif request.data['tipo_dolor_pecho'] == "SIN DOLOR ANGINAL":
                angina = 2
            else:
                angina = 3

            if request.data['electrogardiograma_reposo'].upper() == "ANOMALIA DEL SEGMENTO ST":
                electro = 0
            elif request.data['electrogardiograma_reposo'].upper() == "NORMAL":
                electro = 1      
            else:
                electro = 2

            if request.data['st_slope'].upper() == "DESCENDENTE":
                st = 0
            elif request.data['st_slope'].upper() == "PLANO":
                st = 1      
            else:
                st = 2
            #ESCALAMOS Y PREDECIMOS
            x = escalador.transform([[patient.edad,patient.genero,angina, request.data['presion_arterial_reposo'],request.data['colesterol'],fasting_bs,electro,request.data['frecuencia_cardiaca_maxima'],ang_ejercicio,request.data['viejo_pico_ST'],st]])
            # prediccion = modelo.predict([[patient.edad,patient.genero,angina,request.data['presion_arterial_reposo'],request.data['colesterol'],fasting_bs,electro,request.data['frecuencia_cardiaca_maxima'],ang_ejercicio,request.data['viejo_pico_ST'],st]])
            prediccion = modelo.predict(x)
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
        # lines = lines[:-1]
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
            #ELIMINA LOS ESPACIOS EN BLANCO DEL INICIO Y FINAL DEL STRING
            fields[-1] = fields[-1].strip()
            angina = 0
            angina_eje = 0
            azucar = 0
            st = 0
            electro = 0

            if fields[2] == "ASINTOMATICO":
                angina = 0
            elif fields[2] == "ANGINA ATIPICA":
                angina = 1
            elif fields[2] == "SIN DOLOR ANGINAL":
                angina = 2
            else:
                angina = 3

            if float(fields[5]) > 120:
                azucar = 1
            else:
                azucar = 0

            if fields[8].upper() == "SI":
                angina_eje = 1
            else:
                angina_eje = 0         

            if fields[10].upper() == "DESCENDENTE":
                st = 0
            elif fields[10].upper() == "PLANO":
                st = 1      
            else:
                st = 2
            
            if fields[6].upper() == "ANOMALIA DEL SEGMENTO ST":
                electro = 0
            elif fields[6].upper() == "NORMAL":
                electro = 1      
            else:
                electro = 2

            if fields[1].upper() == "M":
                genero = 1
            else:
                genero = 0
            x = escalador.transform([[int(fields[0]), genero, angina, float(fields[3]), float(fields[4]), float(azucar), electro, int(fields[7]), angina_eje, float(fields[9]), st]])
            prediccion = modelo.predict(x)
            predicciones.append({"a": prediccion, "prediccion": prediccion[0]})
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

            if fields[3] == 'M':
                fields[3] = 1
            else:
                fields[3] = 0

            serializador_paciente = PacienteSerializer(data = {'nombre_paciente': fields[1],'edad': int(fields[2]),'genero': fields[3]})
            #SE TOMA EL STRING LINE Y POR CADA COMA QUE ENCUENTRE EN EL STRING SE CONVIERTE EN UN ELEMENTO DE LA LISTA QUE SE CREA

            if not serializador_paciente.is_valid():
            #SE GUARDA EN LA BASE DE DATOS Y SE UTILIZA EL MÉTODO CREATE DEL SERIALIZADOR Y MODELO
                return Response(serializador_paciente.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                paciente = serializador_paciente.save()
                angina = 0
                angina_eje = 0
                azucar = 0
                st = 0
                electro = 0
                tag_int = 0

                if fields[4] == "ASINTOMATICO":
                    angina = 0
                elif fields[4] == "ANGINA ATIPICA":
                    angina = 1
                elif fields[4] == "SIN DOLOR ANGINAL":
                    angina = 2
                else:
                    angina = 3

                if float(fields[7]) > 120:
                    azucar = 1
                else:
                    azucar = 0
                
 
                if fields[10].upper() == "SI":
                    angina_eje = 1
                else:
                    angina_eje = 0         

                if fields[12].upper() == "DESCENDENTE":
                    st = 0
                elif fields[12].upper() == "PLANO":
                    st = 1      
                else:
                    st = 2
                
                if fields[8].upper() == "ANOMALIA DEL SEGMENTO ST":
                    electro = 0
                elif fields[8].upper() == "NORMAL":
                    electro = 1      
                else:
                    electro = 2
                
                if fields[13].upper() == 'NORMAL':
                    tag_int = 0
                else:
                    tag_int = 1

                serializador_cardio = CardioGuardarSerializer(data = {
                    'paciente': paciente.id,
                    'tipo_dolor_pecho': angina,  # Aquí asociamos el paciente creado
                    'presion_arterial_reposo': fields[5],
                    'colesterol': fields[6],
                    'azucar_sangre_ayuno': azucar,
                    'electrogardiograma_reposo': electro,
                    'frecuencia_cardiaca_maxima': fields[9],
                    'angina_por_ejercicio': angina_eje,
                    'viejo_pico_ST': fields[11],
                    'st_slope': st,
                    'tags': tag_int,
                    'medico':fields[0]
                })
                if serializador_cardio.is_valid():
                    serializador_cardio.save()
                else:
                    return Response(serializador_cardio.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"mensaje": "Datos guardados correctamente."}, status=status.HTTP_201_CREATED)