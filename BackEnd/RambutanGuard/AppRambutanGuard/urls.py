"""
URL configuration for RambutanGuard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppRambutanGuard.views import RegisterEmpleadoView, EliminarEmpleadoView, ValidarAsistenciaView, ListarEmpleadosView,ObtenerHorariosView,ObtenerPuestosView


urlpatterns = [
    path('crear-empleado/',RegisterEmpleadoView.as_view(), name='crear_empleado'), #Ruta para crear empleado
    path('eliminar-empleado/<str:nombre>/<str:apellido>/', EliminarEmpleadoView.as_view(), name='eliminar_empleado'),#Ruta para eliminar emplaedo en base a su nombre
    path('validar-asistencia/', ValidarAsistenciaView.as_view(), name='validar-asistencia'),
    path('listar-empleados/', ListarEmpleadosView.as_view(), name='listar_empleados'), #Ruta para listar empleados
    path('get-puestos/', ObtenerPuestosView.as_view(), name='get-puestos'), #Ruta para obtener puestos
    path('get-horarios/', ObtenerHorariosView.as_view(), name='get-horarios'), #Ruta para obtener horarios

]
