import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import RegisterEmpleadoSerializer  
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Empleado, Empleo_detalle, Puesto, Horario
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .reconocimientoService import verificar_rostro_empleado
import base64
from io import BytesIO
from PIL import Image


#Método para registrar empleado
#Ejemplo JSON esperado:
"""
    {   
        "nombre": "Ray",
        "apellidos": "Garza Garza",
        "correo": "ray@gmail.com",
        "celular": "5555555555",
        "direccion": "Champiñones #555",
        "puesto": "Gerente",
        "hora_entrada": "8:00",
        "hora_salida": "14:00", 
        "foto": "UklGRmYzBQBXRUJQVlA4IFozBQCwQw+dASqdBNwFPjEWiUOiISEhJdRrgEAGCWdqw..." 

    }

"""
class RegisterEmpleadoView(generics.CreateAPIView): 
    serializer_class = RegisterEmpleadoSerializer #El serializador que utilizaremos
    def create(self, request, *args, **kwargs): #Funcion de crear para el POST
        serializer = self.get_serializer(data=request.data) #Obtiene el serializador y le pasamos los datos del request
        serializer.is_valid(raise_exception=True) #Se validan los datos
        empleado = serializer.save() #En caso de ser validados se guardan en la base de datos
        response_data = { #Esto es simplemente un response data que nos sirve para comprobar que si se mando correctamente
            "empleado": empleado.nombre_Empleado, #nombre
            "apellidos": empleado.apellidos, #Apellido
            "correo": empleado.correo,#correo
        }
        return Response(response_data, status=status.HTTP_201_CREATED) #Se regresa el response data, es decir los 3 campos y un estado HTTP 201

    
@method_decorator(csrf_exempt, name='dispatch') #Necesite colocar el method decorator para el csrf, debido a que no jalaba los Delete en POSTMAN al menos.
class EliminarEmpleadoView(View): 
    def delete(self, request, nombre, apellido): #funcion para el DELETE
        try:
            empleado = Empleado.objects.get(nombre_Empleado=nombre, apellidos=apellido) #Se busca el empleado que coincida con los campos otorgados, es decir, nombre y apellido.
            empleado.delete() #Si se encuentra se elimina de la BD
            return JsonResponse({"message": "Empleado eliminado correctamente"}, status=200) #Notificacion de que fue eliminado correctamente
        except Empleado.DoesNotExist:
            return JsonResponse({"error": "Empleado no encontrado"}, status=404) #Si no existe el mpleado, se informa que no se encontro

class ListarEmpleadosView(View):
    def get(self, request):  # Función para el GET
        empleados = Empleado.objects.all()  #Se trae a todos los empleados
        empleados_data = []  #Se crea una lista para almacenar a toos los empleados

        for empleado in empleados:
            #Se intenta obtener el empleo detalle para cada empleado
            try:
                empleo_detalle = Empleo_detalle.objects.get(empleado=empleado) #Se obtiene el respectivo empleo detalle
                puesto = empleo_detalle.puesto.nombre_Puesto  # nombre del puesto
                horario = {
                    "entrada": empleo_detalle.horario.hora_entrada.strftime("%H:%M"), #Su entrada
                    "salida": empleo_detalle.horario.hora_salida.strftime("%H:%M"), #Su salida
                }
            except Empleo_detalle.DoesNotExist: 
                puesto = None
                horario = None

            # La informacion que tendra la respuesta
            empleados_data.append({  
                "nombre": empleado.nombre_Empleado,
                "apellido": empleado.apellidos,
                "correo": empleado.correo,
                "celular": empleado.celular,
                "direccion": empleado.direccion,
                "puesto": puesto, 
                "horario": horario,  
            })

        return JsonResponse({"empleados": empleados_data}, status=200)#Se regresa el empleado

class ObtenerPuestosView(View):
    def get(self, request):  # Funcion para el GET
        puestos = Puesto.objects.all()  # Obtener todos los puestos
        puestos_data = [] #Para guardar todos los puestos en la respuesta

        for puesto in puestos: #Se recorre cada puesto
            puestos_data.append({ #Se agrega a los puestos
                "id": puesto.id,  # el ID del puesto
                "nombre": puesto.nombre_Puesto,  # y su nombre del puesto
            })

        return JsonResponse({"puestos": puestos_data}, status=200)  #Regresamos el formato de respuesta

class ObtenerHorariosView(View):
    def get(self, request):  # Funcion para el GET
        horarios = Horario.objects.all()  # Obtener todos los horarios
        horarios_data = [] #Para guarda todos los horarios

        for horario in horarios: #Se recorre cada horario
            horarios_data.append({ #Se agrega a los horarios
                "id": horario.id,  # ID del horario
                "horario": f"{horario.hora_entrada.strftime('%H:%M')} - {horario.hora_salida.strftime('%H:%M')}",  # Y aca se saca
                #la entrada y salida, con un guion en medio de cada uno.
            })

        return JsonResponse({"horarios": horarios_data}, status=200)#Respuesta JSON de los horarios


def home(request):
    return HttpResponse("<h1>Página de Inicio</h1><p>BackEnd RambutanGuard</p>")




#Método para validar asistencia
#Ejemplo JSON esperado: {
#           
#                  "foto": "UklGRmYzBQBXRUJQVlA4IFozBQCwQw+dASqdBNwFPjEWiUOiISEhJdRrgEAGCWdqw..."            
#   
#               }
@method_decorator(csrf_exempt, name='dispatch')
class ValidarAsistenciaView(View):
    def post(self, request, *args, **kwargs):
        # Obtener la imagen
        print("Obteniendo imagen en base 64")
        data = json.loads(request.body)
        imagen_base64 = data.get('foto')
        
        if not imagen_base64:
            return JsonResponse({"error": "No se proporciono una imagen."}, status=400)

        """try:
            # Decodificar la imagen base64
            imagen_decodificada = base64.b64decode(imagen_base64)
            imagen = Image.open(BytesIO(imagen_decodificada))  # Convertir a un objeto de imagen de PIL
        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la imagen: {str(e)}"}, status=400)"""
                
        
        # Verificar si la imagen pertenece a algún empleado
        is_empleado, empleado = verificar_rostro_empleado(imagen_base64)
        
        if is_empleado:
            return JsonResponse({"message": f"Asistencia registrada de {empleado.nombre_Empleado}"}, status=200)
        else:
            return JsonResponse({"error": "No se encontró."}, status=404)

