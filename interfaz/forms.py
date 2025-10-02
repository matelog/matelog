# Este archivo se crearan todos los formularios necesarios para la aplicación

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from estudiante.models import Genero
from estudiante.models import GradoMaximoEstudios

# Formulario para el registro de alumnos
class FormRegistrarUsuario(UserCreationForm):
    # Lista de tuplas para almacenar los elementos de la lista desplegable, se agrega opción en blanco como primer elemento
    listaGeneros = [('','--------')] 
    listaGrados = [('','--------')]
    
    # Obtener generos y grados de estudio registrados en la DB para hacer lista desplegable
    try:
        generos = Genero.objects.all()
        grados = GradoMaximoEstudios.objects.all()
        # agregar los elementos a las listas
        for g in generos:
            listaGeneros.append((g.genero,g.genero))
        for gr in grados: 
            listaGrados.append((gr.grado,gr.grado))
    except:
        pass

    #Campos del formulario
    correo = forms.EmailField(label="Correo eléctronico",)
    edad = forms.IntegerField(label="Edad",min_value=1,max_value=122)
    genero = forms.ChoiceField(label="Género",choices=listaGeneros)
    grado = forms.ChoiceField(label="Grado máximo de estudios",choices=listaGrados)
    ocupacion = forms.CharField(label="Ocupación",)
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme Contraseña",widget=forms.PasswordInput)

    # Se utiliza el modelo user de django y estos campos para poder aprovechar su implementación de registro e inicio de sesión 
    class Meta:
        model = User
        fields = ['username','password1','password2']

    
# Formulari0 para las respuestas de los ejercicios opcion abierta
class FormRespuestaAbierta(forms.Form):
    respuesta = forms.CharField(label="Ingresa tu respuesta",) 


# Formulari0 para las respuestas de los ejercicios opcion multiple
class FormRespuestaOpMultiple(forms.Form):
 
    def __init__(self, *args, **kwargs):
        respuestas = kwargs.pop('extra')
        super(FormRespuestaOpMultiple, self).__init__(*args, **kwargs)

        op = []
        for res in respuestas:
            op.append((res,res))
        
        self.fields['Respuesta'] = forms.CharField(label='Respuestas', widget=forms.RadioSelect(choices=op),error_messages={'required': 'Por favor eliga una respuesta'},required=True)
        