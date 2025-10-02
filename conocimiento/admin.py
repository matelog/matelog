from django.contrib import admin
from conocimiento.models import *
# Register your models here.

# class ListaDeRespuestasAbiertas(admin.StackedInline):
#     model = Temas
#     extra = 5

# class MostrarRespuestas(admin.ModelAdmin):
#     respuesta = [ListaDeRespuestasAbiertas]

class PersonalizacionLecciones(admin.ModelAdmin):
    list_display=("numero","titulo")
    search_fields=("numero","titulo")
    

class PersonalizacionTemas(admin.ModelAdmin):
    list_display=("idLeccion","numero","titulo","numMinEjemplos","numMinEjercicios")
    search_fields=("idLeccion__titulo","numero","titulo")
    list_filter=("idLeccion",) 

class PersonalizacionEjemplos(admin.ModelAdmin):
    list_display=("idTema","numero","ejemplo")
    search_fields=("idTema__titulo","numero","ejemplo")
    list_filter=("idTema__idLeccion","idTema")

class PersonalizacionEjercicios(admin.ModelAdmin):
    list_display=("idTema","numero","instruccionEjercicio","idTipoEjercicio")
    search_fields=("idTema__titulo","numero","instruccionEjercicio","idTipoEjercicio__tipoEjercicio")
    list_filter=("idTema__idLeccion","idTema","idTipoEjercicio") 

class PersonalizacionTipoEjercicio(admin.ModelAdmin):
    list_display=("tipoEjercicio","descripcion")

class PersonalizacionRespuestasOpcionMultiple(admin.ModelAdmin):
    list_display=("idEjercicio","numero","correctoIncorrecto")
    search_fields=("idEjercicio__idTema","numero","correctoIncorrecto")
    list_filter=("idEjercicio__idTema","idEjercicio","correctoIncorrecto")

class PersonalizacionRespuestasAbiertas(admin.ModelAdmin):
    list_display=("idEjercicio",)
    search_fields=("idEjercicio__idTema",)  
    list_filter=("idEjercicio__idTema","idEjercicio")

# tablas de Conocimiento
admin.site.register(Lecciones,PersonalizacionLecciones)
admin.site.register(Temas,PersonalizacionTemas)
admin.site.register(Ejemplos,PersonalizacionEjemplos)
admin.site.register(Ejercicios,PersonalizacionEjercicios)
admin.site.register(TipoEjercicio,PersonalizacionTipoEjercicio)
admin.site.register(RespuestasAbiertas,PersonalizacionRespuestasAbiertas)
admin.site.register(RespuestasOpcionMultiple,PersonalizacionRespuestasOpcionMultiple)


