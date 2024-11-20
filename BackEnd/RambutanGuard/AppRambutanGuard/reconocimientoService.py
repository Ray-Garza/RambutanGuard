#Reconocimiento facial
import base64
import face_recognition
from PIL import Image
from io import BytesIO
import numpy as np
import os
from .models import Empleado, Empleo_detalle, Puesto, Horario


# Función para almacenar datos biométricos en archivo .npy
def almacenar_datos_biometricos(empleado, imagen):
    # Obtener la codificación del rostro
    print("Almacenando datos biométricos...")
    imagen_codificada = obtener_codificacion_rostro(imagen)

    if imagen_codificada is not None and len(imagen_codificada) > 0:
        print("Generando archivo...")
        # Crear el archivo para almacenar la codificación (por ejemplo, archivo .npy)
        archivo_datos = f"media/biometricos/{empleado.nombre_Empleado}_biometricos.npy"
        os.makedirs(os.path.dirname(archivo_datos), exist_ok=True)
        
        # Guardar la codificación en un archivo numpy
        np.save(archivo_datos, imagen_codificada[0])  # Guardar la primera codificación
        print("Guardando datos..")
        # Guardar la ruta del archivo en el modelo
        empleado.datos_biometricos = archivo_datos

        #Guarda los datos del empleado
        empleado.save()
    else:
        raise ValueError("No se detectó un rostro en la imagen proporcionada.")
    


def obtener_codificacion_rostro(imagen):
            
    # Decodificar y Cargar la imagen
    image = Image.open(BytesIO(base64.b64decode(imagen)))
    
    # Convertir la imagen a un formato que face_recognition pueda procesar
    image_np = np.array(image)

    # Detectar los rostros en la imagen
    rostros = face_recognition.face_locations(image_np)

    # Si se detectan rostros, obtenemos la codificación del primer rostro
    if len(rostros) > 0:
        codificacion_rostro = face_recognition.face_encodings(image_np, known_face_locations=rostros)
        return codificacion_rostro
    else:
        # Si no se detectan rostros, retornar None
        return None
    
def verificar_rostro_empleado(imagen_base64):
    #Obtener la codificación de la imagen
    print("Codificando imagen...")
    imagen_codificada = obtener_codificacion_rostro(imagen_base64)

    #Devolver False si no hay un rostro
    if imagen_codificada is None:
        return False, "No se detectó un rostro en la imagen proporcionada."
    
    #Obtener todos los empleados que tengan datos biométricos
    print("Obteniendo registro de empleados...")
    empleados = Empleado.objects.filter(datos_biometricos__isnull=False)

    rostros_empleados = []
    empleados_lista = []
    
    #Guarda las codificaciones de los rostros de los empleados en una lista
    #Guarda también los empleados en una lista
    for empleado in empleados:
        print("Cargando datos de archivos biometricos...")
        rostro_empleado = np.load(empleado.datos_biometricos)
        rostros_empleados.append(rostro_empleado)
        empleados_lista.append(empleado)
    
    #Busca coincidencias de rostro
    print("Comparando rostros...")
    coincidencias = face_recognition.compare_faces(rostros_empleados, imagen_codificada[0])
    
    #Devuelve si hay coincidencias
    for i, coincidencia in enumerate(coincidencias):
        if coincidencia:
            return True, empleados_lista[i]

    return False, "No se encontró un empleado con esa imagen."
