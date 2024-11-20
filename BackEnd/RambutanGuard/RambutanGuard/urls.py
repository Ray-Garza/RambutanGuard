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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from AppRambutanGuard.views import home


urlpatterns = [
    path("admin/", admin.site.urls), #Ruta para acceder al panel de admin
    path('', home, name='home'), #Casa predefinida
    path('app/', include('AppRambutanGuard.urls')), #Se agregan las rutas de urls.py de AppRambutanGuard

]
if settings.DEBUG: #Checa si esta en modo debug
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Agrega las rutas para servir archivos de media