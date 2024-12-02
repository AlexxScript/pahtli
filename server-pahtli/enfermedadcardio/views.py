from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#LIBRERIA PARA CARGAR EL MODELO Y ESCALADOR
import joblib

#LLAMADA DEL MODELO PACIENTE Y ESCALADOR
from .models import Paciente, Cardio
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

class PacienteUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, id_paciente):
        paciente = Paciente.objects.get(id=id_paciente)
        serializador = PacienteSerializer(paciente)
        return Response({"User":serializador.data},status=status.HTTP_200_OK)

    def put(self ,request , id_paciente):
        paciente = Paciente.objects.get(id = id_paciente)
        serializador = PacienteSerializer(paciente,data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id_paciente):
        # Recuperar los datos del paciente por id y alguna condición adicional, como el médico
        try:
            datos_paciente = Paciente.objects.get(id=id_paciente)
        except Cardio.DoesNotExist:
            return Response({"error": "Datos del paciente no encontrados"}, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminar la instancia
        datos_paciente.delete()
        return Response({"mensaje": "Datos eliminados correctamente"}, status=status.HTTP_204_NO_CONTENT)

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
            # paciente = request.data['paciente']
            # patient = Paciente.objects.get(id=paciente)
            angina_map = {
                "ASINTOMATICO": 0,
                "ANGINA ATIPICA": 1,
                "SIN DOLOR ANGINAL": 2,
                "ANGINA TIPICA": 3
            }
            electro_map = {
                "ANOMALIA DEL SEGMENTO ST": 0,
                "NORMAL": 1,
                "HIPERTROFIA VENTRICULAR IZQUIERDA": 2
            }
            st_map = {
                "DESCENDENTE": 0,
                "PLANO": 1,
                "ASCENDENTE": 2
            }
            print(request.data['genero'])
            angina = angina_map.get(request.data['tipo_dolor_pecho'])
            print(request.data['tipo_dolor_pecho'])
            electro = electro_map.get(request.data['electrogardiograma_reposo'].upper(), 2)
            st = st_map.get(request.data['st_slope'].upper(), 2)
            fasting_bs = 1 if float(request.data['azucar_sangre_ayuno']) > 120 else 0
            ang_ejercicio = 1 if request.data['angina_por_ejercicio'].upper() == "SI" else 0
            genero = 1 if request.data['genero'].upper() == "M" else 0

            #ESCALAMOS Y PREDECIMOS
            # x = escalador.transform([[patient.edad,patient.genero,angina, request.data['presion_arterial_reposo'],request.data['colesterol'],fasting_bs,electro,request.data['frecuencia_cardiaca_maxima'],ang_ejercicio,request.data['viejo_pico_ST'],st]])
            x = escalador.transform([[int(request.data['edad']),genero,angina, float(request.data['presion_arterial_reposo']),request.data['colesterol'],fasting_bs,electro,request.data['frecuencia_cardiaca_maxima'],ang_ejercicio,request.data['viejo_pico_ST'],st]])
            # prediccion = modelo.predict([[patient.edad,patient.genero,angina,request.data['presion_arterial_reposo'],request.data['colesterol'],fasting_bs,electro,request.data['frecuencia_cardiaca_maxima'],ang_ejercicio,request.data['viejo_pico_ST'],st]])
            prediccion = modelo.predict(x)
            print(prediccion)
            return Response({"prediccion":prediccion[0]},status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
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

        angina_map = {
            "ASINTOMATICO": 0,
            "ANGINA ATIPICA": 1,
            "SIN DOLOR ANGINAL": 2,
            "ANGINA TIPICA": 3
        }

        st_map = {
            "DESCENDENTE": 0,
            "PLANO": 1,
            "ASCENDENTE": 2
        }

        electro_map = {
            "ANOMALIA DEL SEGMENTO ST": 0,
            "NORMAL": 1,
            "HIPERTROFIA VENTRICULAR IZQUIERDA": 2
        }

        for line in lines:
            #SE TOMA EL STRING LINE Y POR CADA COMA QUE ENCUENTRE EN EL STRING SE CONVIERTE EN UN ELEMENTO DE LA LISTA QUE SE CREA
            fields = line.split(",")
            #ELIMINA LOS ESPACIOS EN BLANCO DEL INICIO Y FINAL DEL STRING
            fields[-1] = fields[-1].strip()

            angina = angina_map.get(fields[2], 3)  # Default a 3 si no encuentra valor
            st = st_map.get(fields[10].upper(), 2) # Default a 2
            electro = electro_map.get(fields[6].upper(), 2) # Default a 2
            angina_eje = 1 if fields[8].upper() == "SI" else 0
            azucar = 1 if float(fields[5]) > 120 else 0
            genero = 1 if fields[1].upper() == "M" else 0

            x = escalador.transform([[int(fields[0]), genero, angina, float(fields[3]), float(fields[4]), float(azucar), electro, int(fields[7]), angina_eje, float(fields[9]), st]])
            prediccion = modelo.predict(x)
            predicciones.append({"edad":fields[0],"genero":fields[1],"angina":fields[2],"presionA":fields[3],"colesterol":fields[4],"azucar":fields[5],"electrocardio":fields[6].upper(),"FrecuenciaMaxima":fields[7],"anginaEjercicio":fields[8],"ViejoPico":fields[9],"stslope":fields[10],"prediccion": prediccion[0]})
        return Response({"predicciones":predicciones},status=status.HTTP_200_OK)
 
#CREANDO VISTA O ENDPOINT PARA ALMACENAR DATOS DE ENTRENAMIENTO (TAG O RESULTADO) EN LA BASE DE DATOS
class EntrenarCardio(APIView):
    #TIPO DE AUTENTICACION QUE SE ESTA UTILIZANDO
    authentication_classes = [TokenAuthentication]
    #QUIENES PODRAN ACCEDER A ESTE ENDPOINT
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            datos = Cardio.objects.all()
            datos_paciente = Paciente.objects.all()
            serializador_paciente = PacienteSerializer(datos_paciente,many=True)
            serializador = CardioGuardarSerializer(datos,many=True)
            return Response({"datos":serializador.data,"paciente":serializador_paciente.data},status=status.HTTP_200_OK)
        except Cardio.DoesNotExist:
            return Response({"error": "Datos de cardio no encontrados"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        csv_file = request.FILES['archivo']
        
        file_data = csv_file.read().decode("utf-8")
        #CADA VEZ QUE VEA UN SALTO DE LINEA CREA UN NUEVO ELEMENTO EN LA LISTA, ES DECIR LA
        #LISTA VA A CONTENER CADA ELEMENTO DE LA FILA DEL CSV
        lines = file_data.split("\n")
        #ELIMINA LA ULTIMA LINEA DE LA LISTA
        # lines = lines[:-1]
        #ELIMINA LA PRIMERA LINEA DE LA LISTA
        lines = lines[1:]

        angina_map = {
            "ASINTOMATICO": 0,
            "ANGINA ATIPICA": 1,
            "SIN DOLOR ANGINAL": 2,
            "ANGINA TIPICA": 3
        }
        st_map = {
            "DESCENDENTE": 0,
            "PLANO": 1,
            "ASCENDENTE": 2
        }
        electro_map = {
            "ANOMALIA DEL SEGMENTO ST": 0,
            "NORMAL": 1,
            "HIPERTROFIA VENTRICULAR IZQUIERDA": 2
        }

        for line in lines:
            #SE TOMA EL STRING LINE Y POR CADA COMA QUE ENCUENTRE EN EL STRING SE CONVIERTE EN UN ELEMENTO DE LA LISTA QUE SE CREA
            fields = line.split(",")
            genero = 1 if fields[3].upper() == 'M' else 0

            serializador_paciente = PacienteSerializer(data={
                'nombre_paciente': fields[1],
                'edad': int(fields[2]),
                'genero': genero
            })
            if not serializador_paciente.is_valid():
                return Response(serializador_paciente.errors, status=status.HTTP_400_BAD_REQUEST)
            
            paciente = serializador_paciente.save()

            # Mapeo de valores categóricos
            angina = angina_map.get(fields[4], 3)
            azucar = 1 if float(fields[7]) > 120 else 0
            angina_eje = 1 if fields[10].upper() == "SI" else 0
            st = st_map.get(fields[12].upper(), 2)
            electro = electro_map.get(fields[8].upper(), 2)
            tag_int = 0 if fields[13].upper() == 'NORMAL' else 1

            # Guardamos el paciente y seguimos con los datos de Cardio
            serializador_cardio = CardioGuardarSerializer(data = {
                'paciente': paciente.id,
                'tipo_dolor_pecho': angina,  # Aquí asociamos el paciente creado
                'presion_arterial_reposo': fields[5],
                'colesterol': fields[6],
                'azucar_sangre_ayuno': float(fields[7]),
                'azucar_sangre_cat': azucar,
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
    
#ELIMINACIÓN Y ACTUALIZACIÓN DE DATOS INDIVIDUALES
class EntrenarCardioActualizarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id_paciente):
        try:
            datos_paciente = Paciente.objects.get(id=id_paciente)
            serializador_paciente = PacienteSerializer(datos_paciente)
            angina_map = {
                0:"ASINTOMATICO",
                1:"ANGINA ATIPICA",
                2:"SIN DOLOR ANGINAL",
                3:"ANGINA TIPICA"
            }
            st_map = {
                0:"DESCENDENTE",
                1:"PLANO",
                2:"ASCENDENTE"
            }
            electro_map = {
                0:"ANOMALIA DEL SEGMENTO ST",
                1:"NORMAL",
                2:"HIPERTROFIA VENTRICULAR IZQUIERDA"
            }
            datos_cardio = Cardio.objects.get(paciente=id_paciente, medico=request.user)
            datos_cardio.tipo_dolor_pecho = angina_map.get(datos_cardio.tipo_dolor_pecho)
            datos_cardio.electrogardiograma_reposo = electro_map.get(datos_cardio.electrogardiograma_reposo)
            datos_cardio.st_slope = st_map.get(datos_cardio.st_slope)
            datos_cardio.angina_por_ejercicio = "SI" if datos_cardio.angina_por_ejercicio == 1 else "NO"
            target = "NORMAL" if datos_cardio.target == 0 else "SI"
            serializador = CardioGuardarSerializer(datos_cardio)
            return Response({"paciente":serializador_paciente.data,"datos":serializador.data,"target":target},status=status.HTTP_200_OK)
        except Cardio.DoesNotExist:
            return Response({"error": "Datos de cardio no encontrados"}, status=status.HTTP_404_NOT_FOUND)

    def put(self,request,id_paciente):
        print(request.user)
        try:
            datos_cardio = Cardio.objects.get(paciente=id_paciente, medico=request.user)
        except Cardio.DoesNotExist:
            return Response({"error": "Datos de cardio no encontrados"}, status=status.HTTP_404_NOT_FOUND)

        dolor_pecho_map = {
            "ASINTOMATICO": 0,
            "ANGINA ATIPICA": 1,
            "SIN DOLOR ANGINAL": 2,
            "DOLOR ANGINAL": 3  # ejemplo por defecto, ajusta según tus datos
        }

        st_slope_map = {
            "DESCENDENTE": 0,
            "PLANO": 1,
            "ASCENDENTE": 2  # ejemplo por defecto
        }

        electro_map = {
            "ANOMALIA DEL SEGMENTO ST": 0,
            "NORMAL": 1,
            "HIPERTROFIA VENTRICULAR": 2  # ejemplo por defecto
        }

        tags_map = {
            'NORMAL': 0,
            'SI': 1
        }

        angina = dolor_pecho_map.get(request.data['tipo_dolor_pecho'].upper(), 3)  # Valor por defecto 3 si no coincide
        st = st_slope_map.get(request.data['st_slope'].upper(), 2)
        electro = electro_map.get(request.data['electrogardiograma_reposo'].upper(), 2)
        tag_int = tags_map.get(request.data['tags'].upper(), 1)

        azucar = 1 if float(request.data['azucar_sangre_ayuno']) > 120 else 0
        angina_eje = 1 if request.data['angina_por_ejercicio'].upper() == "SI" else 0

        serializador = CardioGuardarSerializer(datos_cardio,data = {
            'tipo_dolor_pecho': angina,  # Aquí asociamos el paciente creado
            'presion_arterial_reposo': request.data['presion_arterial_reposo'],
            'colesterol': request.data['colesterol'],
            'azucar_sangre_ayuno': azucar,
            'electrogardiograma_reposo': electro,
            'frecuencia_cardiaca_maxima': request.data['frecuencia_cardiaca_maxima'],
            'angina_por_ejercicio': angina_eje,
            'viejo_pico_ST': request.data['viejo_pico_ST'],
            'st_slope': st,
            'tags': tag_int,
            "medico":request.data["medico"],
            "paciente":request.data["paciente"],
        })

        if serializador.is_valid():
            serializador.save()
        else:
            return Response(serializador.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"mensaje":"editado correctamente"},status=status.HTTP_201_CREATED)

    def delete(self, request, id_paciente):
        # Recuperar los datos del paciente por id y alguna condición adicional, como el médico
        try:
            datos_cardio = Cardio.objects.get(paciente=id_paciente, medico=request.user)
        except Cardio.DoesNotExist:
            return Response({"error": "Datos de Cardio no encontrados"}, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminar la instancia
        datos_cardio.delete()
        return Response({"mensaje": "Datos eliminados correctamente"}, status=status.HTTP_204_NO_CONTENT)