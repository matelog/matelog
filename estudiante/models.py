from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint
from django.db.models.query_utils import Q
from conocimiento.models import * # importando tablas de la app Comocimiento

####################################################################
# Este archivo se establece el modelo para almacenar los Datos
#############

# Lista para almacenar los generos están códificados
# con el fin de hacer un sólo cambio en un solo lugar
listaGeneros = ["Mujer","Hombre","Otro","Prefiero no decirlo"]

# Varaibles para almacenar los generos están códificados
# con el fin de hacer un sólo cambio en un solo lugar
listaGrados = ["Primaria","Secundaria","Preparatoria","Técnico","Licenciatura","Maestría","Doctorado"]

# # # # # # # # # # # # # # # # # # #
#   Tabla para genero del estudiante
class Genero (models.Model):
    # --> Campos de la tabla
    genero = models.CharField(max_length=50,verbose_name="Genero")

    # --> Validación extra de campos    
    def clean_fields(self, exclude=None): 
        if self.genero: # Verifica que el campo no este vacio

            # Validación Para limitar valores en genero
            if not self.genero in listaGeneros:
                generos = ""
                for gen in listaGeneros:
                    generos += gen + ", "
                raise ValidationError({'genero': f'Favor de ingresar unicamente estos valores (deben escribirse tal cual se muestra): {generos} .'}) 

            # Validación Para limitar un unico registro por genero
            generosRegistrados = Genero.objects.all()
            listaId_GenerosRegistrados=[]
            lista_GenerosRegistrados=[]
            
            for gen in generosRegistrados: # Obtener todos generos resgitrados y almacenarlos
                listaId_GenerosRegistrados.append(gen.id)
                lista_GenerosRegistrados.append(gen.genero)

            if  self.genero in lista_GenerosRegistrados:
                if not self.id in listaId_GenerosRegistrados: # Esta validación es para permitir modificar un registro
                    raise ValidationError({'genero': f'El genero {self.genero} ya ha sido registrado.'}) 

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Genero"
        verbose_name_plural="6) Genero"
        

    # --> Representación de la tabla en un String 
    def __str__(self):    
        return f'{self.genero}'


# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Tabla para grado máximo de estudios del estudiante
class GradoMaximoEstudios (models.Model):
    # --> Campos de la tabla
    grado = models.CharField(max_length=100,verbose_name="Grado máximo de estudios")

    # --> Validación extra de campos    
    def clean_fields(self, exclude=None): 
        if self.grado: # Verifica que el campo no este vacio

            # Validación Para limitar valores en genero
            if not self.grado in listaGrados:
                grados = ""
                for gra in listaGrados:
                    grados += gra + ", "
                raise ValidationError({'grado': f'Favor de ingresar unicamente estos valores (deben escribirse tal cual se muestra): {grados}.'}) 

            # Validación Para limitar un unico registro por genero
            grdaosRegistrados = GradoMaximoEstudios.objects.all()
            listaId_GradosRegistrados=[]
            lista_GradosRegistrados=[]
            
            for gen in grdaosRegistrados: # Obtener todos generos resgitrados y almacenarlos
                listaId_GradosRegistrados.append(gen.id)
                lista_GradosRegistrados.append(gen.grado)

            if  self.grado in lista_GradosRegistrados:
                if not self.id in listaId_GradosRegistrados: # Esta validación es para permitir modificar un registro
                    raise ValidationError({'grado': f'El grado {self.grado} ya ha sido registrado.'}) 

    
    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Grado Máximo Estudios"
        verbose_name_plural="7) Grado Máximo Estudios"
        ordering = ['id',]
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'{self.grado}'


# # # # # # # # # # # # # # # #
# Tabla para estudiante
class Estudiante(models.Model):
    # --> Campos de la tabla
    nombreUsuario = models.OneToOneField(User,on_delete=models.PROTECT,verbose_name="Nombre del estudiante")
    correo = models.EmailField(verbose_name="Correo eléctronico")
    edad = models.IntegerField(verbose_name="Edad")
    genero = models.ForeignKey(Genero,on_delete=models.PROTECT,verbose_name="Genero del estudiante")
    gradoMaximoEstudios = models.ForeignKey(GradoMaximoEstudios,on_delete=models.PROTECT,verbose_name="Grado máximo de estudios")
    ocupacion = models.CharField(max_length=200,verbose_name="Ocupación del estudiante")

    # --> Validación extra de campos    
    def clean_fields(self, exclude=None):
        # Validar que la edad no sea negativa o cero
        if self.edad or self.edad==0: # valida que el campo numero existe 
            if self.edad < 1:
                raise ValidationError({'edad': f'La edad no puede ser negativa o cero'})
            if self.edad > 122:
                raise ValidationError({'edad': f'Favor de ingresar una edad válida'}) 

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Estudiante"
        verbose_name_plural="1) Estudiantes"
        ordering = ['nombreUsuario']
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f' {self.nombreUsuario}'


# # # # # # # # # # # # # # # # # # #
# Tabla para Lecciones Estudiadas
class LeccionesEstudiadas(models.Model):
    # --> Campos de la tabla
    idLeccion = models.ForeignKey(Lecciones,on_delete=models.PROTECT,verbose_name="Lección")
    idEstudiante = models.ForeignKey(Estudiante,on_delete=models.PROTECT,verbose_name="Estudiante")   
    avance = models.IntegerField(verbose_name="Avance en la Lección")
    terminada = models.BooleanField(verbose_name="¿Está terminada?")
    
    # --> Validación extra de campos    
    def clean_fields(self, exclude=None):
        # Validar que el avance no sea negativo o cero
        if self.avance or self.avance==0: # valida que el campo avance existe 
            if self.avance < 0:
                raise ValidationError({'avance': f'El avance no puede ser negativo'})
    
    # --> Metadatos de la tabla
    class Meta:
        verbose_name="una Lección Estudiada"
        verbose_name_plural="2) Lecciones Estudiadas"
        unique_together = ['idLeccion', 'idEstudiante']
        ordering = ['idLeccion','avance']

    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Lección {self.idLeccion.numero} -> {self.idEstudiante}'

# # # # # # # # # # # # # # # # # # #
# Tabla para Temas Estudiados
class TemasEstudiados(models.Model):
    # --> Campos de la tabla
    idTema = models.ForeignKey(Temas,on_delete=models.PROTECT,verbose_name="Tema")
    idLeccionesEstudiadas = models.ForeignKey(LeccionesEstudiadas,on_delete=models.PROTECT,verbose_name="Relación de Lección con Estudiante")   
    avanceEjemplos = models.IntegerField(verbose_name="Avance en ejemplos")
    avanceEjercicios = models.IntegerField(verbose_name="Avance en ejercicios")
    ejemplosExtra = models.IntegerField(verbose_name="Ejemplos extra")
    ejerciciosExtra = models.IntegerField(verbose_name="Ejercicios extra")
    terminada = models.BooleanField(verbose_name=       "¿Está terminado?")

    # --> Validación extra de campos    
    def clean_fields(self, exclude=None):
        # Validar que el avanceEjemplos no sea negativo o cero
        if self.avanceEjemplos or self.avanceEjemplos==0: # valida que el campo numero existe 
            if self.avanceEjemplos < 0:
                raise ValidationError({'avanceEjemplos': f'El avance de ejemplos no puede ser negativo'})

        # Validar que el avanceEjercicios no sea negativo o cero
        if self.avanceEjercicios or self.avanceEjercicios==0: # valida que el campo numero existe 
            if self.avanceEjercicios < 0:
                raise ValidationError({'avanceEjercicios': f'El avance de ejercicios no puede ser negativo'})

        # Validar que el ejemplosExtra no sea negativo o cero
        if self.ejemplosExtra or self.ejemplosExtra==0: # valida que el campo numero existe 
            if self.ejemplosExtra < 0:
                raise ValidationError({'ejemplosExtra': f'Los ejemplos extras no pueden ser negativos'})

        # Validar que el avanceEjercicios no sea negativo o cero
        if self.ejerciciosExtra or self.ejerciciosExtra==0: # valida que el campo numero existe 
            if self.ejerciciosExtra < 0:
                raise ValidationError({'avanceEjercicios': f'Los ejercicios extras no pueden ser negativos'})

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Tema Estudiado"
        verbose_name_plural="3) Temas Estudiados"
        unique_together = ['idTema', 'idLeccionesEstudiadas']
        ordering = ['idTema',]

    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Lección {self.idLeccionesEstudiadas.idLeccion.numero} -> Tema {self.idTema.numero} -> {self.idLeccionesEstudiadas.idEstudiante}'


# # # # # # # # # # # # # # # # # # #
# Tabla para Ejemplos Estudiados
class EjemplosEstudiados(models.Model):
    # --> Campos de la tabla
    idEjemplo = models.ForeignKey(Ejemplos,on_delete=models.PROTECT,verbose_name="Ejemplo")
    idTemasEstudiados = models.ForeignKey(TemasEstudiados,on_delete=models.PROTECT,verbose_name="Relación de Lección y Tema con Estudiante")   
    tiempo = models.IntegerField(verbose_name="Tiempo en segundos")
    fecha = models.DateTimeField(verbose_name="Fecha")
    
    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Ejemplo Estudiado"
        verbose_name_plural="4) Ejemplos Estudiados"
        ordering = ['idEjemplo','fecha','tiempo']

    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'{self.idEjemplo} y {self.idTemasEstudiados}'

# # # # # # # # # # # # # # # # # # #
# Tabla para Ejercicios Estudiados
class EjerciciosEstudiados(models.Model):
    # --> Campos de la tabla
    idTemaEstudiado = models.ForeignKey(TemasEstudiados,on_delete=models.PROTECT,verbose_name="Relación de Lección y Tema con Estudiante")
    idEjercicio = models.ForeignKey(Ejercicios,on_delete=models.PROTECT,verbose_name="Ejercicio")   
    bien_o_Mal = models.BooleanField(verbose_name="Bien o mal")
    pidioAyuda = models.BooleanField(verbose_name="Pidio ayuda")
    tiempo = models.IntegerField(verbose_name="Tiempo en segundos")
    fecha = models.DateTimeField(verbose_name="Fecha")

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Ejercicio Estudiado"
        verbose_name_plural="5) Ejercicios Estudiados"
        ordering = ['idEjercicio','fecha','tiempo',"bien_o_Mal"]

    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'{self.idEjercicio} y {self.idTemaEstudiado}'
