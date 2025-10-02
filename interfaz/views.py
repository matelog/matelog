from django.http.request import QueryDict
from django.urls import reverse
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from conocimiento.models import *
from conocimiento.models import tipoAbierto,tipoOpMultiple
from estudiante.models import *
import time
from .opereaciones import *


# # # # # # # # # # # # # # # # 
# Vista: Página para ver vídeo de explicación de la plataforma
def tutorial(request):
    return render(request,"tutorial.html")


# # # # # # # # # # # # # # # # 
# Vista: Página para errores 404
def error_404_view(request, exception):
    return render(request,"error_404.html")

# # # # # # # # # # # # # # # # 
# Vista: Página principal, muestra todas las lecciones
@login_required
def home (request):
    verificarEjemplo(request)# Verificar si hay un ejemplo estudiado que guardar en caso de haber saltado a esta vista
    verificarEjercicio(request)# Verificar si hay un ejercicio estudiado que no fue resuelto para borrar datos 
    lecciones = Lecciones.objects.all() #obtener todas las lecciones para mostrarlas
    
    # Procedimiento para crear una lista de diccionarios con datos de la lección
    # cada diccionrario tendra una lección, si esta está terminada y su avance
    # {leccion,terminada,avance}
    listaLecciones =[]
    try:
        idEstudiante = Estudiante.objects.filter(nombreUsuario=request.user.id).first().id
    except:
        return render(request,'home.html',{'mensaje':"Estás registrado como usuario y no como estudiante, pide al administrado que te agrege como estudiante."} )

    for leccion in lecciones:
        leccionEstudiada = LeccionesEstudiadas.objects.filter(idEstudiante = idEstudiante, idLeccion = leccion.id)
        esTerminada = False
        estadoLeccion = "Lección no iniciada"
        clase = "" 
        avance = 0
        
        if leccionEstudiada:
            estadoLeccion = "Lección en curso"
            clase = "enCurso" 
            esTerminada = leccionEstudiada.first().terminada
            avance = leccionEstudiada.first().avance
             
            if esTerminada:
                estadoLeccion = "Lección completada"
                clase = "completada" # ocupada para saber que clase css debe tener en caso de haber terminado la lección

        listaLecciones.append({"leccion":leccion,"terminada":esTerminada,"avance":avance,"clase":clase,"estadoLeccion":estadoLeccion})


    if lecciones: 
        # Crear contexto a llevar a la plantilla
        contexto = {
            "listaLecciones":listaLecciones,
        }
        return render(request,'home.html',contexto)
    else:
        return render(request,'home.html',{'mensaje':"No hay lecciones "} )


# # # # # # # # # # # # # # # #
# Vista : Muestra el contenido de la lección y todos sus temas
@login_required
def leccion (request,id_leccion):
    verificarEjemplo(request)
    verificarEjercicio(request)
    
    leccion = Lecciones.objects.filter(id=id_leccion).first() # obtener la lección elegida por el usuario
    temas = Temas.objects.filter(idLeccion=id_leccion) # obtener temas de la lección 
    
    # Almacenar datos del estudiante
    resultado = relacionarLeccion(request,leccion) # Agrega la relación entre Lecciones estudiadas y estudiante, si hay un error se almacena en la variable
    if resultado: # si resultado contine un objeto render, se renderizara.
        return resultado

    
    # Procedimiento para crear una lista de diccionarios con datos del tema
    # cada diccionrario tendra un tema, si esta está terminado y su avance
    # {tema,terminado,avance}
    listaTemas =[]
    idEstudiante = Estudiante.objects.filter(nombreUsuario=request.user.id).first().id
    idleccionEstudiada = LeccionesEstudiadas.objects.filter(idEstudiante = idEstudiante, idLeccion = id_leccion).first().id
    ejemplosHechos = ""

    
    for tema in temas:
        temaEstudiado = TemasEstudiados.objects.filter(idLeccionesEstudiadas=idleccionEstudiada,idTema = tema.id)
        esTerminada = False
        estadoTema = "Tema no iniciado"
        clase = "" 
        numMinEjemplos = tema.numMinEjemplos
        numMinEjercicios = tema.numMinEjercicios
        ejemplosExtra = Ejemplos.objects.filter(idTema = tema.id).count() - numMinEjemplos
        ejerciciosExtra = Ejercicios.objects.filter(idTema = tema.id).count() - numMinEjercicios
        avance = {
                'tema': 0,
                'ejemplos': 0,
                'ejercicios': 0,
                'ejemplosExtra': 0,
                'ejerciciosExtra': 0,
                
                'numMinEjemplos': numMinEjemplos,
                'ejemplosHechos': 0,
                'numMinEjercicios': numMinEjercicios,
                'ejerciciosHechos': 0,

                'numEjemplosExtra': ejemplosExtra,
                'numEjemplosExtrasHechos': 0,
                'numEjerciciosExtra': ejerciciosExtra,
                'numEjerciciosExtrasHechos': 0,
            }

        ejemplosHechos = ""
        
        if temaEstudiado:
            estadoTema = "Cursando tema"      
            clase = "enCurso" 
            temaEstudiado = temaEstudiado.first()                  
            if temaEstudiado.terminada:
                esTerminada = True
                clase = "completada" # ocupada para saber que clase css debe tener en caso de haber terminado la lección
                estadoTema = "Tema terminado"  
        
            #calcular avance
            ejemplosHechos = temaEstudiado.avanceEjemplos
            ejerciciosHechos = temaEstudiado.avanceEjercicios
            
            ejemplosExtrasHechos = temaEstudiado.ejemplosExtra
            ejerciciosExtrasHechos = temaEstudiado.ejerciciosExtra
            
            avanceTema = 0
            avanceEjemplos = 0
            avanceEjercicios = 0
            avanceEjemplosExtra = 0
            avanceEjerciciosExtra = 0
            
            if numMinEjemplos + numMinEjercicios != 0:
                avanceTema = int( ( (ejemplosHechos + ejerciciosHechos) * 100) / (numMinEjemplos + numMinEjercicios))
            
            if numMinEjemplos != 0:
                avanceEjemplos = int( (ejemplosHechos * 100) / numMinEjemplos )

            if numMinEjercicios != 0:
                avanceEjercicios = int( (ejerciciosHechos * 100) / numMinEjercicios )
            
            if ejemplosExtra != 0:
                avanceEjemplosExtra = int( (ejemplosExtrasHechos * 100) / ejemplosExtra )

            if ejerciciosExtra != 0:
                avanceEjerciciosExtra = int( (ejerciciosExtrasHechos * 100) / ejerciciosExtra)

            avance = {
                'tema': avanceTema,
                'ejemplos': avanceEjemplos,
                'ejercicios': avanceEjercicios,
                'ejemplosExtra': avanceEjemplosExtra,
                'ejerciciosExtra': avanceEjerciciosExtra,
                
                'numMinEjemplos': numMinEjemplos,
                'ejemplosHechos': ejemplosHechos,
                'numMinEjercicios': numMinEjercicios,
                'ejerciciosHechos': ejerciciosHechos,

                'numEjemplosExtra': ejemplosExtra,
                'numEjemplosExtrasHechos': ejemplosExtrasHechos,
                'numEjerciciosExtra': ejerciciosExtra,
                'numEjerciciosExtrasHechos': ejerciciosExtrasHechos,
            }

        listaTemas.append({"tema":tema,"terminado":esTerminada,"avance":avance,"clase":clase,"estadoTema":estadoTema})

    
    # Crear contexto a llevar a la plantilla
    contexto = {
            "leccion":leccion,
        }

    if temas: # verificar si hay temas
        contexto['listaTemas'] = listaTemas # se agrega al contexto los temas
        return render(request,'leccion.html',contexto)
    else:
        contexto['mensaje'] = 'Aún no hay temas para esta lección 😰'# mensaje si no hay temas
        return render(request,'leccion.html',contexto)
    

# # # # # # # # # # # # # # # #
# Vista : Muestra un tema seleccionado
@login_required
def tema (request,id_leccion,id_tema):
    verificarEjemplo(request)
    verificarEjercicio(request)
        
    # obtener datos del tema y lección
    temaActual = Temas.objects.filter(id=id_tema).first()
    leccionActual = Lecciones.objects.filter(id=id_leccion).first()

    # Almacenar datos del estudiante
    resultado = relacionarTema(request,leccionActual,temaActual) # Agrega la relación entre Temas estudiados y Lecciones Estudiadas, si hay un error se almacena en la variable
    if resultado: # si resultado contine un objeto render, se renderizara.
        return resultado
    
    # Crear contexto a llevar a la plantilla
    contexto = {
            'leccion':leccionActual,
            'tema':temaActual,
            'idPrimerEjemplo': -1
            }

    # Obtener ejemplos del tema
    listaEjemplos = Ejemplos.objects.filter(idTema=id_tema) # lista de ejemplos del tema
    idEjemplos = [] # lista para los Id de los ejemplos
        
    if listaEjemplos: # se vérifica la existencia de ejemplos
        for ejemplo in listaEjemplos: # se obtienen todos los id de los ejemplos del tema
            idEjemplos.append(ejemplo.id)
       
        request.session['id_ejemplos'] = idEjemplos # se almacenan todos los id en una variable de sesión para poder mostrar los ejemplos uno por uno
        contexto['idPrimerEjemplo'] = idEjemplos[0] # se sobrescribe el primer ejemplo en el contexto al primer ejemplo de la lista obtenida
    else:
        contexto['mensaje'] = "No hay ejemplos que ver 😥"

    return render(request,'tema.html',contexto)

# # # # # # # # # # # # # # # #
# Vista : Muestra un ejemplo y contiene la lógica para almacenar los datos del estudiante-ejemplos
@login_required
def ejemplo (request,id_leccion,id_tema, id_ejemplo):
    verificarEjercicio(request)

    # Obtener la lista de id de ejemplos guardos en la variable de sesión
    id_ejemplos = request.session.get('id_ejemplos')

    if not id_ejemplos: # Error si entra directo sin haber pasado por un tema
        return render(request,"error.html",{'mensaje':"Ups. por favor vuelva a la página principal"})

    # Crea las variables de sesión necesarias para almacenar los datos si  estás no existen
    if not request.session.get('idTemaEstudiadoEjemplo'):
        riniciarVaraiblesEjemplo(request)

    # Almacena los datos si se ha visto el ejemplo y reinicia las variables
    if request.session.get('idTemaEstudiadoEjemplo') != -1 :
        registrarEjemploEstudiado(request)
        resultado = iniciarVariblesEjemplo(request,id_leccion,id_tema,id_ejemplo)
        if resultado:
            return resultado
    else: # en caso contrario sólo reinicia las variables
        resultado = iniciarVariblesEjemplo(request,id_leccion,id_tema,id_ejemplo)
        if resultado:
            return resultado

    # obtener el id del siguiente ejemplo 
    indiceSiguiente = id_ejemplos.index(id_ejemplo)+1 # se obtiene el indice del id del ejercicio actual, y se suma 1 para obtener el indice del siguiente id del ejemplo
    # obtener el id del anterior ejemplo 
    indiceAnterior = id_ejemplos.index(id_ejemplo)-1 # se obtiene el indice del id del ejercicio actual, y se resta 1 para obtener el indice del siguiente id del ejemplo


    # Datos necesarios para la vista
    try:
        idEstudiante = Estudiante.objects.filter(nombreUsuario=request.user.id).first().id
    except:
        return render(request,'home.html',{'mensaje':"Estás registrado como usuario y no como estudiante, pide al administrado que te agrege como estudiante."} )

    idleccionEstudiada = LeccionesEstudiadas.objects.filter(idEstudiante = idEstudiante, idLeccion = id_leccion).first().id
    temasEstudiado =  TemasEstudiados.objects.filter(idLeccionesEstudiadas=idleccionEstudiada,idTema=id_tema).first()

    leccion = Lecciones.objects.filter(id=id_leccion).first()
    tema = Temas.objects.filter(id=id_tema).first()
    ejemplo = Ejemplos.objects.filter(id=id_ejemplo).first() # se obtiene el ejemplo actual
    numTotalEjemplos = Ejemplos.objects.filter(idTema=id_tema).count()
    numMinEjemplos = tema.numMinEjemplos
    numEjemplosVistos = temasEstudiado.avanceEjemplos

    # Crear contexto a llevar a la plantilla
    contexto = {
        'leccion':leccion,
        'tema':tema ,
        'ejemplo':ejemplo,
        "numTotalEjemplos": numTotalEjemplos,
        }

    if  indiceAnterior >= 0: # se verifica que el indice del anterior ejemplo no sea menor a cero
        contexto['id_ejemplo_anterior'] = id_ejemplos[indiceAnterior] # se obtiene el id del anterior ejemplo con ayuda del idice obtenido al restar 1

    if  indiceSiguiente < len(id_ejemplos): # se verifica que el indice del siguiente ejemplo no sea mayor al ultimo indice de la lista, para no provocar una exceptcion
        contexto['id_ejemplo_siguiente'] = id_ejemplos[indiceSiguiente] # se obtiene el id del siguiente ejemplo con ayuda del idice obtenido al sumar 1

        if numEjemplosVistos == numMinEjemplos or ejemplo.numero == numMinEjemplos:
            contexto['ejemplosMinCumplidos'] = True
            
            listaEjercicios(request,id_tema,contexto)

    else: # si ya no hay ejemplos se obtienen los ejercios del tema
        listaEjercicios(request,id_tema,contexto)

    return render(request,'ejemplo.html',contexto)


def listaEjercicios(request,id_tema,contexto):
    ejercicios = Ejercicios.objects.filter(idTema = id_tema)

    if ejercicios: # se verifiva la existencia de ejercicios
        id_ejercicios = [] # lista para id de ejercicios
        # llenar lista con todos los id
        for ejercicio in ejercicios:
            id_ejercicios.append(ejercicio.id)

        request.session['id_ejercicios'] = id_ejercicios # se almacena la lista de id en una variable de sesión

        contexto['id_ejercicio_actual'] = id_ejercicios[0] # el id del ejercicio actual es el primero en la lista
    else:
        contexto['mensaje'] = "No hay ejercios que realizar 😥" # mensaje en caso de no haber ejercicios

# # # # # # # # # # # # # # # #
# Vista : Muestra un ejercicio y contiene la lógica para almacenar los datos del estudiante-ejercicio y validar la respuesta
@login_required
def ejercicio (request,id_leccion,id_tema, id_ejercicio):
    verificarEjemplo(request)
    
    # Obtener la lista de id de ejercicios guardos en la variable de sesión
    id_ejercicios = request.session.get('id_ejercicios')
    if not id_ejercicios: # Error si entra directo sin haber pasado por un tema
        return render(request,"error.html",{'mensaje':"Ups. por favor vuelva a la página principal"})

    # Crea las variables de sesión necesarias para almacenar los datos si  estás no existen
    if not request.session.get('idTemaEstudiadoEjercicio'):
        reiniciarVaraiblesEjercicio(request)

    # Inicia las variables de sesión en caso de haber cambiado de ejercicio
    if id_ejercicio != request.session.get('idEjercicio') :
        reiniciarVaraiblesEjercicio(request)
        resultado = iniciarVariblesEjercicio(request,id_leccion,id_tema,id_ejercicio)
        if resultado:
            return resultado
          
    # Datos necesarios para la vista
    try:
        idEstudiante = Estudiante.objects.filter(nombreUsuario=request.user.id).first().id
    except:
        return render(request,'home.html',{'mensaje':"Estás registrado como usuario y no como estudiante, pide al administrado que te agrege como estudiante."} )

    idleccionEstudiada = LeccionesEstudiadas.objects.filter(idEstudiante = idEstudiante, idLeccion = id_leccion).first().id
    temasEstudiado =  TemasEstudiados.objects.filter(idLeccionesEstudiadas=idleccionEstudiada,idTema=id_tema).first()


    # Datos del ejercicio
    ejercicio = Ejercicios.objects.filter(id=id_ejercicio).first()
    tipoEjercicio = TipoEjercicio.objects.filter(id=ejercicio.idTipoEjercicio.id).first().tipoEjercicio
    numTotalEjercicios = Ejercicios.objects.filter(idTema=id_tema).count()

    leccion = Lecciones.objects.filter(id=id_leccion).first()
    tema = Temas.objects.filter(id=id_tema).first()
    numMinEjercicios = tema.numMinEjercicios
    numEjerciciosCorrectos = temasEstudiado.avanceEjercicios

    # se valida si se pide ayuda
    ayuda = ""
    bAyuda = False
    if request.GET:
        bAyuda = True 
        ayuda = ejercicio.ayuda

    # Crear contexto a llevar a la plantilla
    contexto = {
        'leccion':leccion,
        'tema':tema ,
        'ejercicio':ejercicio,
        'ayuda': ayuda,
        'numTotalEjercicios':numTotalEjercicios,
    }

    # obtener el id del siguiente ejercicio  
    indiceSiguiente = id_ejercicios.index(id_ejercicio)+1 # se obtiene el indice del id del ejercicio actual, y se suma 1 para obtener el indice del siguiente id del ejercicio
    # obtener el id del anterior ejercicio  
    indiceAnterior = id_ejercicios.index(id_ejercicio)-1 # se obtiene el indice del id del ejercicio actual, y se resta 1 para obtener el indice del anterior id del ejercicio


    if  indiceAnterior >= 0: # se verifica que el indice del anterior ejemplo no sea menor a cero
        contexto['id_ejercicio_anterior'] = id_ejercicios[indiceAnterior] # se obtiene el id del anterior ejemplo con ayuda del idice obtenido al restar 1


    if  indiceSiguiente < len(id_ejercicios): 
        contexto['id_ejercicio_siguiente']= id_ejercicios[indiceSiguiente]
        
        if numEjerciciosCorrectos == numMinEjercicios :
            contexto['ejerciciosMinCumplidos'] = True
            

    # Si hubo una petición Post
    if request.method == 'POST':
        
        # 1) verificar si es un reintento
        try:
            reintentar = request.POST['reintentar'] # ocurrira una excepción en caso de no ser un reintento
            request.POST = QueryDict()
            if reintentar:
                reiniciarVaraiblesEjercicio(request) # reiniciar variables 
                resultado = iniciarVariblesEjercicio(request,id_leccion,id_tema,id_ejercicio)
                if resultado:
                    return resultado
            
                return redirect(reverse('ejercicio',args=(id_leccion,id_tema,id_ejercicio))) # recargar ejercicio
        except:
            pass

        # 2) si no es un reintento, entonces es una respuesta
        if tipoEjercicio == tipoAbierto: # Tipo ejercicio abierto
            
            respuestaCorrecta = RespuestasAbiertas.objects.filter(idEjercicio=id_ejercicio).first().respuesta # Obtener respuesta

            form = FormRespuestaAbierta (request.POST)
            if form.is_valid(): 
                respuestaEstudiante = form.cleaned_data['respuesta']
                
                if respuestaEstudiante.strip().lower() == respuestaCorrecta.strip().lower():
                    request.session['bienOMal'] = True
                    messages.success(request, f'Su respuesta es correcta!! 😄')
                else:
                    messages.error(request, f'Ups esa no es la respuesta correcta 😥')
                    
                # guardar datos en variables de sesión para poder registrarlas
                request.session['pidioAyuda'] = bAyuda
                request.session['respuestaEjercicio'] = respuestaEstudiante

                # Registrar intento 
                registrarEjercicioEstudiado(request)

                # recargar ejercicio
                return redirect(reverse('ejercicio',args=(id_leccion,id_tema,id_ejercicio)))
        
        else: # Tipo ejercicio opción múltiple
            # guardar datos en variables de sesión para poder registrarlas
            respuestaEstudiante = request.POST['Respuesta']
            request.session['respuestaEjercicio'] = respuestaEstudiante
            request.session['pidioAyuda'] = bAyuda
            
            # Obtener la respuesta correcta
            respuestaCorrecta = ""
            consulta = RespuestasOpcionMultiple.objects.filter(idEjercicio=id_ejercicio)

            for respuesta in consulta:
                if respuesta.correctoIncorrecto:
                    respuestaCorrecta = respuesta.respuesta
                    break
            
            # Saber si fue correcta la respuesta
            if respuestaCorrecta == respuestaEstudiante :
                request.session['bienOMal'] = True
                messages.success(request, f'Su respuesta es correcta!! 😄')    
            else:
                 messages.error(request, f'Ups esa no es la respuesta correcta 😥')

            # Registrar intento
            registrarEjercicioEstudiado(request)

            # Recargar ejercicio
            return redirect(reverse('ejercicio',args=(id_leccion,id_tema,id_ejercicio)))            
    
    
    # Si no hay petición POST llegara a esta parte
    # se determina como se mostrará el formulario, si como ejercicio de respuesta abierta o opción múltiple

    if tipoEjercicio == tipoAbierto: # Tipo ejercicio abierto
        respuestaCorrecta = RespuestasAbiertas.objects.filter(idEjercicio=id_ejercicio) # Obtener respuesta
        if respuestaCorrecta:
            form = FormRespuestaAbierta()
            contexto['form']=form
        else:
            contexto['mensaje']= "Ups no han agregado la respuesta a este ejercicio 😥"

    else: # Tipo Opción múltiple
        respuestas = []
        consulta = RespuestasOpcionMultiple.objects.filter(idEjercicio=id_ejercicio)

        if consulta:
            for respuesta in consulta:
                respuestas.append(respuesta.respuesta)
            
            form = FormRespuestaOpMultiple(extra=respuestas)
            contexto['form']=form
        else:
            contexto['mensaje']= "Ups no han agregado respuestas a este ejercicio 😥"

    return render(request,'ejercicio.html',contexto)


# # # # # # # # # # # # # # # #
# Vista : Registro de estudiantes, se crea un nuevo registro en el modelo User y otro en Estudiantes
def registrarse(request):

    # Verificar si hubo un POST
    if request.method == 'POST':
        form = FormRegistrarUsuario (request.POST)
        # verificar que el formulario es correcto
        if form.is_valid():
            form.save() # Guardar nombre y contraseña en el modelo User
                    
            try:
                # Proceso para insertar datos en el modelo Estudiantes
                nombre = request.POST.get("username")
                correo = request.POST.get("correo")
                edad = request.POST.get("edad")
                genero = request.POST.get("genero")
                grado = request.POST.get("grado")
                ocupacion = request.POST.get("ocupacion")
                
                estudiante = Estudiante() #nuevo objeto estudiante
                
                # Agregar valores al objeto estudiante (campos de la tabla)
                estudiante.nombreUsuario = User.objects.filter(username=nombre).first()
                estudiante.correo = correo
                estudiante.edad = edad
                estudiante.genero = Genero.objects.filter(genero=genero).first()
                estudiante.gradoMaximoEstudios = GradoMaximoEstudios.objects.filter(grado=grado).first()
                estudiante.ocupacion = ocupacion
                 
                estudiante.save() # insertar el nuevo estudiante registrado
                #relacionarLeccionesTemasEstudiante(estudiante) 
                
                messages.success(request, f'Usuario {nombre} creado, por favor inicia sesión 😁')
                return redirect('login')
            except:
                usuario = User.objects.filter(username=nombre)
                usuario.delete()
                messages.error(request, f'Algo salio mal, por favor intentalo de nuevo 😕')
                form = FormRegistrarUsuario()
    else:
        form = FormRegistrarUsuario()
    
    context = {'form':form}

    return render(request,'registro.html', context )