from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView,LogoutView
from django.conf.urls import handler404

# Registro de URLs 
urlpatterns = [
    #URL de home, muestra todas las lecciones
    path('', home,name='/'),
    
    #URLs para el manejo de sesiones de usuario
    path('registro/',registrarse, name="registro"),
    path('login/',LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/',LogoutView.as_view(template_name='logout.html'), name="logout"),
    
    #URLs para Navegacion del conocimiento 
    path('leccion/<int:id_leccion>/',leccion,name='leccion'), # para mostrar la lista de temas de una leccion
    path('leccion/<int:id_leccion>/<int:id_tema>/',tema,name='tema'), # para mostrar un tema de una leccion
    path('ejemplo/<int:id_leccion>/<int:id_tema>/<int:id_ejemplo>',ejemplo, name="ejemplo"),  # para mostrar un ejemplo de un tema
    path('ejercicio/<int:id_leccion>/<int:id_tema>/<int:id_ejercicio>',ejercicio, name="ejercicio"),  # para mostrar un ejercicio de un tema

    #URLs para ver explicacion de la plataforma
    path('tutorial/',tutorial, name="tutorial"),

]

#URLs para errores 404 y 500
handler404 = 'interfaz.views.error_404_view'