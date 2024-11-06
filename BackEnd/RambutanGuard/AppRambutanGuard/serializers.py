from rest_framework import serializers
from .models import Empleado, Empleo_detalle, Puesto, Horario
import os
from datetime import datetime

class RegisterEmpleadoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=128)  #Nombre, con apellidos
    correo = serializers.EmailField() #Correo 
    password = serializers.CharField(write_only=True) #contraseña
    puesto = serializers.PrimaryKeyRelatedField(queryset=Puesto.objects.all()) #Puesto, habra una boxlist pero se manejaran los ids como respuesta (ints)
    horario = serializers.PrimaryKeyRelatedField(queryset=Horario.objects.all()) #Igual que puesto
    foto = serializers.ListField(child=serializers.FileField(), write_only=True) #La foto a mandar que sera una lista en caso que ocupamos mandar N en un futuro

    def create(self, validated_data): 
        #El proceso de separar nombre y apellidos
        nombreCompleto = validated_data['nombre'].split() #Spliteamos en dos el nombre completo
        nombreEmpleado = nombreCompleto[0] #Primera parte seria el nombre
        apellidos = ' '.join(nombreCompleto[1:]) if len(nombreCompleto) > 1 else '' #Segunda seria el apellido, al menos que sea menor que 1, entonces no tendria apellido.

        #Se crea el empleado como tal
        empleado = Empleado.objects.create(
            nombre_Empleado=nombreEmpleado, 
            apellidos=apellidos,
            correo=validated_data['correo'], 
            datos_biometricos='',  #Inicializa vacio
            celular='',  # De momento vacio, esperando front end
            direccion=''  # Igual
        )

        #Como funcionan las imagenes
        image_paths = [] #Inicializamos lista vacia para las rutas
        for i, image in enumerate(validated_data['foto']): #Se itera sobre cada imagen en el conjunto de 
            image_path = f"media/{empleado.nombre_Empleado}/imagen_{i + 1}.png" #Se agrega a la carpeta media con la ruta de cada imagen, nombre de empleado y su indice respectivo
            os.makedirs(os.path.dirname(image_path), exist_ok=True) #Crea directorio especificado en caso de no existir.
            with open(image_path, 'wb+') as f: #Abre el archivo en modo binario de escritura
                for chunk in image.chunks(): # Divide la imagen en chunks para que sea mas eficiente
                    f.write(chunk) #Se escribe cada chunk en dicho archivo.
            image_paths.append(image_path) #Agrega la ruta de la imagen a la lista de image paths

        empleado.datos_biometricos = image_paths[0]# Guardar la ruta de la primera imagen en datos_biometricos
        empleado.save()#Guarda los cambios realizados en la base de datos

        # Crear el empleo_detalle 
        #Debido a que en el formulario se maneja lo de puesto y horario, debemos de llenar empleado detalle tambien
        empleo_detalle = Empleo_detalle.objects.create(
            empleado=empleado,
            puesto=validated_data['puesto'],
            horario=validated_data['horario'],
            fecha_inicio=datetime.now().date(),  # Usa la fecha actual, la de hoy pues
            fecha_fin=None #No contiene fin
        )
        
        return empleado