from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import RegisterEmpleadoSerializer  # Asegúrate de usar el nombre correcto
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Empleado
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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

def home(request):
    return HttpResponse("<h1>Página de Inicio</h1><p>BackEnd RambutanGuard</p>")