from django.db import models
from django.core.exceptions import ValidationError

####################################################################
# En este archivo de establece el modelo para almacenar el conocimiento
#############

# Varaibles para almacenar los tipos de ejercicios que están códificados
# Se declaran como variables para posibles modificaciones en el futuro
# con el fin de hacer un sólo cambio en un solo lugar
tipoAbierto = "Abierto"
tipoOpMultiple = "Opción múltiple"
tipoEjercicios = [tipoAbierto,tipoOpMultiple]

# # # # # # # # # # # # # # # #
#   Tabla para las lecciones  
class Lecciones(models.Model):
    # --> Campos de la tabla
    numero = models.IntegerField(unique=True,verbose_name="Número de lección")
    titulo = models.CharField(max_length=200,verbose_name="Título de lección")
    descripcion = models.TextField(max_length=10000,verbose_name="Descripción de lección")
    
    # --> Validación extra de campos    
    def clean_fields(self, exclude=None):
        # Validar que el número no sea negativo o cero
        if self.numero or self.numero==0: # valida que el campo numero existe 
            if self.numero < 1:
                raise ValidationError({'numero': f'El Número de la Lección no puede ser negativo o cero'}) 

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="una Lección"
        verbose_name_plural="1) Lecciones"
        ordering = ['numero']
     
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Lección {self.numero}: {self.titulo}'


# # # # # # # # # # # # # # # #
#   Tabla para Temas  
class Temas (models.Model):
    # --> Campos de la tabla
    idLeccion = models.ForeignKey(Lecciones, on_delete=models.PROTECT,verbose_name="Lección perteneciente")
    numero = models.CharField(max_length=20,unique=True,verbose_name="Número de Tema",help_text="Ejemplo: 1.1")
    titulo = models.CharField(max_length=200,verbose_name="Título")
    teoria = models.TextField(max_length=10000,verbose_name="Teoría")
    numMinEjemplos = models.IntegerField(verbose_name="Número minímo de ejemplos a consultar")
    numMinEjercicios = models.IntegerField(verbose_name="Número minímo de ejercicios a resolver")
   
    # --> Validación extra de campos    
    def clean_fields(self, exclude=None):

        if self.numMinEjemplos or self.numMinEjemplos==0: # valida que el campo numero existe 
            if self.numMinEjemplos < 1:
                raise ValidationError({'numMinEjemplos': f'El Número minímo de ejemplos a consultar no puede ser negativo o cero'})

        if self.numMinEjercicios or self.numMinEjercicios==0: # valida que el campo numero existe 
            if self.numMinEjercicios < 1:
                raise ValidationError({'numMinEjercicios': f'El Número minímo de ejercicios a resolver no puede ser negativo o cero'}) 

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Tema"
        verbose_name_plural="2) Temas"
        ordering = ['idLeccion',"numero"]
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Tema {self.numero} {self.titulo}'
   

# # # # # # # # # # # # # # # #
#   Tabla para las Ejemplos  
class Ejemplos (models.Model):
    # --> Campos de la tabla
    idTema = models.ForeignKey(Temas,on_delete=models.PROTECT,verbose_name="Tema al que pertenece")
    numero = models.IntegerField(verbose_name="Número de Ejemplo")
    explicacion = models.TextField(max_length=10000,verbose_name="Explicación")
    ejemplo = models.TextField(max_length=10000,verbose_name="Ejemplo")
    
    
    # --> Validación extra de campos    
    def clean_fields(self, exclude=None):
        # Validar que el número no sea negativo o cero
        if self.numero or self.numero==0: # valida que el campo numero existe 
            if self.numero < 1:
                raise ValidationError({'numero': f'El Número del Ejemplo no puede ser negativo o cero'}) 

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="un Ejemplo"
        verbose_name_plural="3) Ejemplos"
        ordering = ['idTema',"numero"]
        unique_together = ['numero', 'idTema']

    # --> Representación de la tabla en un String
    def __str__(self):    
        return f' Tema  {self.idTema.numero}: Ejemplo {self.numero}'


# # # # # # # # # # # # # # # # # # # #
#   Tabla para los Tipos de ejercicios 
class TipoEjercicio (models.Model):
    # --> Campos de la tabla
    tipoEjercicio = models.CharField(max_length=200,verbose_name="Tipo de ejercicio")
    descripcion = models.TextField(max_length=10000,verbose_name="Descripción")
    
    # --> Validación extra de campos    
    def clean_fields(self, exclude=None): 
        if self.tipoEjercicio: # Verifica que el campo no este vacio    
            # Validación Para limitar valores en tipo ejercicio
            if not self.tipoEjercicio in tipoEjercicios:
                tipos = ""
                for tipo in tipoEjercicios:
                    tipos += tipo + ", "
                raise ValidationError({'tipoEjercicio': f'Favor de ingresar unicamente estos valores (deben escribirse tal cual se muestra): {tipos} .'}) 

            # Validación Para limitar un unico registro por tipo de ejercicio
            tiposRegistrados = TipoEjercicio.objects.all()
            listaId_TiposRegistrados=[]
            listaTiposRegistrados=[]
            # Obtener todos los tipos resgitrados y almacenarlos
            for tipo in tiposRegistrados:
                listaId_TiposRegistrados.append(tipo.id)
                listaTiposRegistrados.append(tipo.tipoEjercicio)

            if  self.tipoEjercicio in listaTiposRegistrados:
                if not self.id in listaId_TiposRegistrados: # Esta validación es para permitir modificar un registro
                    raise ValidationError({'tipoEjercicio': f'El tipo de ejercicio {self.tipoEjercicio} ya ha sido registrado.'}) 

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="Tipo Ejercicio"
        verbose_name_plural="5) Tipos de Ejercicios"
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'{self.tipoEjercicio}'

        

# # # # # # # # # # # # # # # #
#   Tabla para los Ejercicios  
class Ejercicios (models.Model):
    # --> Campos de la tabla
    idTema = models.ForeignKey(Temas,on_delete=models.PROTECT,verbose_name="Tema al que pertenece")
    idTipoEjercicio = models.ForeignKey(TipoEjercicio,on_delete=models.PROTECT,verbose_name="Tipo de ejercicio")
    numero = models.IntegerField(verbose_name="Número de ejercicio")
    instruccionEjercicio = models.TextField(max_length=10000,verbose_name="Instrucción de ejercicio")
    ejercicio = models.TextField(max_length=10000,verbose_name="Ejercicio")
    ayuda = models.TextField(max_length=10000,verbose_name="Ayuda")
    
    
    # --> Validación extra de campos    
    def clean_fields(self, exclude=None): 
        # Validar que el número no sea negativo o cero
        if self.numero or self.numero==0: # valida que el campo numero existe 
            if self.numero < 1:
                raise ValidationError({'numero': f'El Número del Ejercicio no puede ser negativo o cero'}) 


    # --> Metadatos de la tabla
    class Meta:
        verbose_name="Ejercicio"
        verbose_name_plural="4) Ejercicios"
        unique_together = ['numero', 'idTema']
        ordering = ['idTema',"numero"]
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Tema {self.idTema.numero} || Ejercicio {self.numero} -> {self.idTipoEjercicio}' # {self.idTipoEjercicio.tipoEjercicio}'

# # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Tabla para Tipo de Ejercicios Respuestas Abiertas
class RespuestasAbiertas (models.Model):
    # --> Campos de la tabla
    idEjercicio = models.OneToOneField(Ejercicios,on_delete=models.PROTECT,verbose_name="Respuesta de Ejercicio")
    respuesta = models.TextField(max_length=10000,verbose_name="Respuesta")

    # --> Validación extra de campos
    def clean_fields(self, exclude=None):
        
        try: # Try para capturar excepcion de AttributeError al no existir el objeto idEjercicio 
            # Validación Para saber si el ejercicio es de respuesta multiple
            tipoActual = self.idEjercicio.idTipoEjercicio.tipoEjercicio # obtiene el tipo de ejercicio del ejercicio seleccionado en el input
            if  tipoActual != tipoAbierto:
                raise ValidationError({'idEjercicio': f'El ejercicio seleccionado es de tipo {self.idEjercicio.idTipoEjercicio}. Para ingresar la respuesta a este ejercicio vaya a la tabla correcta de respuestas o modifique el tipo de ejercicio de este ejercicio a {tipoAbierto}'}) 
        except AttributeError:
            pass

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="una Respuesta abierta"
        verbose_name_plural="6) Respuestas Abiertas"
        ordering = ['idEjercicio',]
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Respuesta a ejercicio {self.idEjercicio}'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Tabla para Tipo de Ejercicios Respuestas Opcion Multiple
class RespuestasOpcionMultiple (models.Model):
    # --> Campos de la tabla
    idEjercicio = models.ForeignKey(Ejercicios,on_delete=models.PROTECT,verbose_name="Ejercicio")
    numero = models.IntegerField(verbose_name="Número de respuesta")
    respuesta = models.TextField(max_length=10000,verbose_name="Respuesta")
    correctoIncorrecto = models.BooleanField(verbose_name="¿Es la respuesta correcta?")
    
    # --> Validación extra de campos
    def clean_fields(self, exclude=None):         
        # Validar que el número no sea negativo o cero
        if self.numero or self.numero==0: # valida que el campo numero existe 
            # Validar que el número no sea negativo o cero
            if self.numero < 1:
                raise ValidationError({'numero': f'El Número de la Respuesta no puede ser negativo o cero'}) 

        try: # Try para capturar excepcion de AttributeError al no existir el objeto idEjercicio
            
            # Validación Para saber si el ejercicio es de respuesta multiple
            tipoActual = self.idEjercicio.idTipoEjercicio.tipoEjercicio # obtiene el tipo de ejercicio del ejercicio seleccionado en el input
            if  tipoActual and tipoActual != tipoOpMultiple:
                raise ValidationError({'idEjercicio': f'El ejercicio seleccionado es de tipo {self.idEjercicio.idTipoEjercicio}. Para ingresar la respuesta a este ejercicio vaya a la tabla correcta de respuestas o modifique el tipo de ejercicio de este ejercicio a {tipoOpMultiple}'}) 
                
            # Validación para campo correctoIncorrecto
            listaRespuestas = RespuestasOpcionMultiple.objects.filter(idEjercicio=self.idEjercicio)

            for respuesta in listaRespuestas:
                if respuesta.correctoIncorrecto and self.correctoIncorrecto and self.id != respuesta.id:
                    raise ValidationError({'correctoIncorrecto': 'La respuesta correcta ya existe para este ejercicio seleccionado.'})
        
        except AttributeError:
            pass

    # --> Metadatos de la tabla
    class Meta:
        verbose_name="Respuestas Opcion Multiple"
        verbose_name_plural="7) Respuestas Opcion Multiple"
        unique_together = ['numero', 'idEjercicio']
        ordering = ['idEjercicio',"numero"]
    
    # --> Representación de la tabla en un String
    def __str__(self):    
        return f'Respuesta a ejercicio {self.idEjercicio}'