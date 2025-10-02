from django.contrib import admin
from .models import *


class PersonalizacionGenero(admin.ModelAdmin):
    list_display=("genero",)

class PersonalizacionGradoMaximo(admin.ModelAdmin):
    list_display=("grado",)

class PersonalizacionEstudiante(admin.ModelAdmin): 
    list_display=("nombreUsuario","correo","genero","edad","gradoMaximoEstudios","ocupacion")
    list_filter=("gradoMaximoEstudios","genero","edad","ocupacion")

class PersonalizacionLeccionesEstudiadas(admin.ModelAdmin):
    list_display=("idLeccion","idEstudiante","avance","terminada")
    search_fields=("idLeccion__titulo","idEstudiante__nombreUsuario__username","avance") 
    list_filter=("idLeccion","idEstudiante","avance","terminada")

class PersonalizacionTemasEstudiados(admin.ModelAdmin):
    list_display=("idLeccionesEstudiadas","idTema","avanceEjemplos","avanceEjercicios","ejemplosExtra","ejerciciosExtra","terminada")
    search_fields=("idTema__titulo","idLeccionesEstudiadas__idEstudiante__nombreUsuario__username") 
    list_filter=("idLeccionesEstudiadas__idLeccion","idTema","terminada")

class PersonalizacionEjemplosEstudiados(admin.ModelAdmin):
    list_display=("idEjemplo","idTemasEstudiados","tiempo","fecha")
    list_filter=("idEjemplo","idTemasEstudiados","tiempo","fecha") 

class PersonalizacionEjerciciosEstudiados(admin.ModelAdmin):
    list_display=("idEjercicio","idTemaEstudiado","tiempo","fecha","bien_o_Mal","pidioAyuda")
    list_filter=("idEjercicio","idTemaEstudiado","tiempo","fecha","bien_o_Mal","pidioAyuda") 

# tablas de Datos
admin.site.register(Estudiante,PersonalizacionEstudiante)
admin.site.register(LeccionesEstudiadas,PersonalizacionLeccionesEstudiadas)
admin.site.register(TemasEstudiados,PersonalizacionTemasEstudiados) 
admin.site.register(EjemplosEstudiados,PersonalizacionEjemplosEstudiados) 
admin.site.register(EjerciciosEstudiados,PersonalizacionEjerciciosEstudiados) 

admin.site.register(Genero,PersonalizacionGenero)
admin.site.register(GradoMaximoEstudios,PersonalizacionGradoMaximo) 