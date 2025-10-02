from datetime import datetime
from django.shortcuts import render
from conocimiento.models import *
from conocimiento.models import tipoAbierto,tipoOpMultiple
from estudiante.models import *
import time

#   /////////////////////////////////////////////
#   Funciones para almacenar las lecciones y 
#   temas vistas por el estudiante
#   /////////////////////////////////////////////

# # # # # # # # # # # # # # # #
# Realiza la relación entre estudiante y lecciones estudiadas, si el usuario está
# registrado unicamente en el modelo User y no en Estudiante, no se podra hacer la relación
def relacionarLeccion(request,leccion):
    leccionEstudiada = LeccionesEstudiadas()
    estudiante = Estudiante.objects.filter(nombreUsuario = request.user.id).first()

    if estudiante:
        if not LeccionesEstudiadas.objects.filter(idLeccion=leccion.id,idEstudiante = estudiante.id):
            leccionEstudiada.idLeccion = leccion
            leccionEstudiada.idEstudiante = estudiante
            leccionEstudiada.avance = 0
            leccionEstudiada.terminada = False
            leccionEstudiada.save()
    else:
        return render(request,"error.html",{'mensaje':"Al parecer no estás registrado como estudiante, decir al administrador que te registre."})

# # # # # # # # # # # # # # # #
# realiza la relación entre lecciones estudiadas y temas estudiados
def relacionarTema(request,leccion,tema):
    temaEstudiado = TemasEstudiados()
    estudiante = Estudiante.objects.filter(nombreUsuario = request.user.id).first()
    
    if estudiante:
        leccionEstudiada = LeccionesEstudiadas.objects.filter(idLeccion=leccion.id,idEstudiante = estudiante.id).first()
        
        if not TemasEstudiados.objects.filter(idTema=tema.id,idLeccionesEstudiadas = leccionEstudiada.id):
            temaEstudiado.idTema = tema
            temaEstudiado.idLeccionesEstudiadas = leccionEstudiada
            temaEstudiado.terminada = False
            temaEstudiado.avanceEjemplos = 0
            temaEstudiado.avanceEjercicios = 0
            temaEstudiado.ejemplosExtra = 0
            temaEstudiado.ejerciciosExtra = 0
            temaEstudiado.save()
    else:
        return render(request,"error.html",{'mensaje':"Al parecer no estás registrado como estudiante, decir al administrador que te registre."})


#   ////////////////////////////////////////////////////////////
#   Funciones para las operaciones en ejemplos
#   ////////////////////////////////////////////////////////////

# Crea y reinicia los valores de las variables de ejemplo
def riniciarVaraiblesEjemplo(request):
    request.session['idTemaEstudiadoEjemplo'] = -1
    request.session['idEjemplo'] = -1
    request.session['tiempoI_Ejemplo'] = 0

# # # # # # # # # # # # # # # #
# Verifica si hay un ejemplo visto por el usuario cuando va a otra página que no sea 
# la del ejemplo siguiente al visto. Almacena el ejercicio estudiado en caso de haber visto uno
def verificarEjemplo(request):
    if request.session.get('idTemaEstudiadoEjemplo') and request.session.get('idTemaEstudiadoEjemplo') != -1 :
        registrarEjemploEstudiado(request)

# # # # # # # # # # # # # # # #
# Inicia los valores para después poder insertar un registro
# en ejermplos estudiados
def iniciarVariblesEjemplo(request,idLeccion,idTtema,idEjemplo):
    estudiante = Estudiante.objects.filter(nombreUsuario = request.user.id).first()

    if estudiante:
        leccionEstudiada = LeccionesEstudiadas.objects.filter(idLeccion=idLeccion,idEstudiante=estudiante.id).first()
        temaEstudiado = TemasEstudiados.objects.filter(idLeccionesEstudiadas=leccionEstudiada.id,idTema = idTtema).first()

        request.session['idTemaEstudiadoEjemplo'] = temaEstudiado.id
        request.session['idEjemplo'] = idEjemplo
        request.session['tiempoI_Ejemplo'] = time.time()
    else:
        return render(request,"error.html",{'mensaje':"Al parecer no estás registrado como estudiante, decir al administrador que te registre."})

# # # # # # # # # # # # # # # #
# Hace el registro del ejemplo estudiado
def registrarEjemploEstudiado(request):
    idTemaEstudiadoEjemplo = request.session.get('idTemaEstudiadoEjemplo')
    
    if idTemaEstudiadoEjemplo != -1:
        idEjemplo = request.session.get('idEjemplo')

        if idEjemplo != -1:
            tiempoI_Ejemplo = request.session.get('tiempoI_Ejemplo')
            tiempoF_Ejemplo = time.time()
            
            if tiempoI_Ejemplo !=0:
                ejemploEstudiado = EjemplosEstudiados()

                ejemplo = Ejemplos.objects.filter(id=idEjemplo).first()
                temaEstudiado = TemasEstudiados.objects.filter(id=idTemaEstudiadoEjemplo)

                ejemploEstudiado.idEjemplo = ejemplo
                ejemploEstudiado.idTemasEstudiados = temaEstudiado.first()
                ejemploEstudiado.tiempo = round(tiempoF_Ejemplo - tiempoI_Ejemplo,3)
                ejemploEstudiado.fecha = datetime.today()
                ejemploEstudiado.save()
                incrementarEjemplos(temaEstudiado,ejemplo.id,temaEstudiado.first().idTema.id)
                riniciarVaraiblesEjemplo(request)


def incrementarEjemplos(temaEstudiado,id_Ejemplo,id_tema):
    registroUnico = EjemplosEstudiados.objects.filter(idTemasEstudiados = temaEstudiado.first().id,idEjemplo = id_Ejemplo).count()

    if registroUnico == 1 :
        tema = Temas.objects.filter(id=id_tema).first()
        numMinEjemplos = tema.numMinEjemplos

        avance = temaEstudiado.first().avanceEjemplos + 1 

        if avance <= numMinEjemplos:
            temaEstudiado.update(avanceEjemplos=avance)
            temaTerminado(temaEstudiado,tema)
        else:
            avance = temaEstudiado.first().ejemplosExtra + 1 
            temaEstudiado.update(ejemplosExtra=avance)
            

        


#   /////////////////////////////////////////////
#   Funciones para las operaciones en ejercicios
#   /////////////////////////////////////////////

# Crea y reinicia los valores de las variables de ejercicios
def reiniciarVaraiblesEjercicio(request):
    request.session['idTemaEstudiadoEjercicio'] = -1
    request.session['idEjercicio'] = -1
    request.session['bienOMal'] = False
    request.session['pidioAyuda'] = False
    request.session['tiempoI_Ejercicio'] = 0
    request.session['respuestaEjercicio'] = None

# # # # # # # # # # # # # # # #
# Verifica si hay un ejercicio visto por el usuario cuando va a otra página sin haberlo resuelto
# para borrar los datos dado que no lo resolvio
def verificarEjercicio(request):
    if request.session.get('idTemaEstudiadoEjercicio') and request.session.get('idTemaEstudiadoEjercicio') != -1 :
        reiniciarVaraiblesEjercicio(request)

# # # # # # # # # # # # # # # #
# Inicia los valores para después poder insertar un registro
# en ejercicios estudiados
def iniciarVariblesEjercicio (request,idLeccion,idTtema,idEjercicio):
    estudiante = Estudiante.objects.filter(nombreUsuario = request.user.id).first()

    if estudiante:
        leccionEstudiada = LeccionesEstudiadas.objects.filter(idLeccion=idLeccion,idEstudiante=estudiante.id).first()
        temaEstudiado = TemasEstudiados.objects.filter(idLeccionesEstudiadas=leccionEstudiada.id,idTema = idTtema).first()

        request.session['idTemaEstudiadoEjercicio'] = temaEstudiado.id
        request.session['idEjercicio'] = idEjercicio
        request.session['tiempoI_Ejercicio'] = time.time()
    else:
        return render(request,"error.html",{'mensaje':"Al parecer no estás registrado como estudiante, decir al administrador que te registre."})


# # # # # # # # # # # # # # # #
# Hace el registro del ejercicio estudiado
def registrarEjercicioEstudiado(request):
    idTemaEstudiadoEjercicio = request.session.get('idTemaEstudiadoEjercicio')
    
    if idTemaEstudiadoEjercicio != -1:
        idEjercicio = request.session.get('idEjercicio')

        if idEjercicio != -1:
            tiempoI_Ejercicio = request.session.get('tiempoI_Ejercicio')
            tiempoF_Ejercicio = time.time()
            
            if tiempoI_Ejercicio !=0:
                ejercicioEstudiado = EjerciciosEstudiados()

                ejercicio = Ejercicios.objects.filter(id=idEjercicio).first()
                temaEstudiado = TemasEstudiados.objects.filter(id=idTemaEstudiadoEjercicio)

                ejercicioEstudiado.idEjercicio = ejercicio
                ejercicioEstudiado.idTemaEstudiado = temaEstudiado.first()
                ejercicioEstudiado.bien_o_Mal = request.session.get('bienOMal')
                ejercicioEstudiado.pidioAyuda = request.session.get('pidioAyuda')
                ejercicioEstudiado.tiempo = round(tiempoF_Ejercicio - tiempoI_Ejercicio,3)
                ejercicioEstudiado.fecha = datetime.today()
                ejercicioEstudiado.save()
                if request.session.get('bienOMal'):
                    incrementarEjercicios(temaEstudiado,ejercicio.id,temaEstudiado.first().idTema.id)

def incrementarEjercicios(temaEstudiado,id_Ejercicio,id_tema):
    registroUnico = EjerciciosEstudiados.objects.filter(idTemaEstudiado = temaEstudiado.first().id,idEjercicio = id_Ejercicio,bien_o_Mal=True).count()

    if registroUnico == 1 :
        tema = Temas.objects.filter(id=id_tema).first()
        numMinEjercicios = tema.numMinEjercicios

        avance = temaEstudiado.first().avanceEjercicios + 1 

        if avance <= numMinEjercicios:
            temaEstudiado.update(avanceEjercicios=avance)
            temaTerminado(temaEstudiado,tema)
        else:
            avance = temaEstudiado.first().ejerciciosExtra + 1 
            temaEstudiado.update(ejerciciosExtra=avance)

def temaTerminado(temaEstudiado,tema):
    numMinEjercicios = tema.numMinEjercicios
    numMinEjemplos = tema.numMinEjemplos
    avanceEjemplos = temaEstudiado.first().avanceEjemplos
    avanceEjercicios = temaEstudiado.first().avanceEjercicios
    
    if numMinEjemplos == avanceEjemplos and numMinEjercicios == avanceEjercicios:
        temaEstudiado.update(terminada=True)
        avanceLeccion(temaEstudiado,tema)

def avanceLeccion(temaEstudiado,tema):
    temaEstudiado = temaEstudiado.first()
    leccionEstudiada = LeccionesEstudiadas.objects.filter(id=temaEstudiado.idLeccionesEstudiadas.id)

    numTemas = Temas.objects.filter(idLeccion = tema.idLeccion).count()
    numTemasCompletados = TemasEstudiados.objects.filter(idLeccionesEstudiadas = temaEstudiado.idLeccionesEstudiadas.id,idTema = tema.id,terminada=True).count()
    avance = int (numTemasCompletados * 100 / numTemas) + leccionEstudiada.first().avance

    leccionEstudiada.update(avance=avance)

    if avance == 100:
        leccionEstudiada.update(terminada=True)