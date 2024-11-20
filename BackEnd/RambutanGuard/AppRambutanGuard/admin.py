from django.contrib import admin
from .models import Rol, Usuario, Horario, Puesto, Empleado, Empleo_detalle, Reporte_Mensual, Asistencia

# Register your models here.

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Horario)
admin.site.register(Puesto)
admin.site.register(Empleado)
admin.site.register(Empleo_detalle)
admin.site.register(Reporte_Mensual)
admin.site.register(Asistencia)
