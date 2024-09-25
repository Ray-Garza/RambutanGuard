from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=120)
    correo = models.EmailField(unique=True)
    rol = models.ForeignKey('Rol', on_delete= models.CASCADE)
    contrasenia = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.contrasenia = make_password(raw_password)
    
    def __str__(self):
        return self.nombre_usuario

class Horario(models.Model):
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()

    def __str__(self):
        return f"{self.hora_entrada.strftime('%H:%M')} - {self.hora_salida.strftime('%H:%M')}"

class Puesto(models.Model):
    nombre_Puesto = models.CharField(max_length=128)
    def __str__(self):
        return self.nombre_Puesto

class Empleado(models.Model):
    nombre_Empleado = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128)
    correo = models.EmailField()
    estado = models.BooleanField(default=True)
    datos_biometricos = models.CharField(max_length=300)
    celular = models.CharField(max_length=15)
    direccion = models.CharField(max_length=300)    

    def __str__(self):
        return self.nombre_Empleado + " "+ self.apellidos

class Empleo_detalle(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    puesto = models.ForeignKey('Puesto', on_delete=models.CASCADE)
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE)
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)

    def __str__(self):
        if self.fecha_fin is None:
            return self.fecha_inicio.strftime('%Y-%m-%d') + " - " + " ---"
        else:
            return self.fecha_inicio.strftime('%Y-%m-%d') + " - " + self.fecha_fin.strftime('%Y-%m-%d')

class Asistencia(models.Model):
    fecha = models.DateField()
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    empleo_detalle = models.ForeignKey('Empleo_detalle', on_delete=models.CASCADE)

    def __str__(self):
        return self.hora_entrada.strftime('%H:%M') + " - "+ self.hora_salida.strftime('%H:%M')
    
class Reporte_Mensual(models.Model):
    fecha = models.DateField()    
    retardos = models.IntegerField()
    salidas_anticipadas = models.IntegerField()
    horas_trabajadas = models.IntegerField()
    horas_extra = models.IntegerField()
    faltas = models.IntegerField()
    empleo_detalle = models.ForeignKey('Empleo_detalle', on_delete=models.CASCADE)

    def __str__(self):
        return "Retardos: "+str(self.retardos)+" Salidas Anticipadas: "+ str(self.salidas_anticipadas)+" Horas Trabajadas:" + str(self.horas_trabajadas)+" Horas Extra: "+str(self.horas_extra) + " Faltas: "+str(self.faltas)
