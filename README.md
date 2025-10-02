# Matelog

Este proyecto es un ambiente de aprendizaje para apoyo en la enseñanza de lógica matemática. 
Se tiene el objetivo de recabar los datos generados por el estudiante con la interacción del ambiente de aprendizaje: lecciones terminadas, temas terminados, avance en ejemplos y en ejercicios, las respuestas correctas y el número total de intentos que sean realizados en cada ejercicio, así como el tiempo en segundos que ha tardado en resolver el ejercicio o en estudiar un ejemplo. A través de este ambiente de aprendizaje se realizará investigación de sistemas tutores inteligentes en el CENIDET.
.

## Construido con 🛠️
* Django 3.2.7
* Python 3.9
* HTML 5
* CSS 3
* Bootstrap 5
* SQLite

## Ocupar MateLog de manera local

### Prerrequisitos
Antes de comenzar, asegúrate de tener instalado:
  - VisualStudioCode (VSC)
  - Python 3.9 (https://www.python.org/ftp/python/3.9.0/python-3.9.0.exe)
  - Git
    
### 1. En VSC, abre una nueva terminal CMD:
  - Presiona Ctrl + Shift  + Ñ
  - Cuando aparezca la terminal haz clic en la flecha hacia abajo al lado del signo "+" y selecciona "Command Prompt" o "Símbolo del sistema"
   <img width="351" height="382" alt="image" src="https://github.com/user-attachments/assets/77da6291-c1ed-4fb5-b2cf-4e8811360946" />
   
### 2. Dentro de la terminal de VSC coloca la dirección donde van a almacenar la carpeta de MateLog, con "cd" (change directory) y la dirección de la ubicación, por ejemplo:
  cd C:\Users\Victor\Documents 

### 3. Hacer un git clone de https://github.com/matelog/matelog:
     git clone https://github.com/matelog/matelog.git

### 4. El paso anterior va a crear una carpeta con el nombre "matelog" dentro de la dirección que eligiron, así que ahora tienen que entrar a la carpeta, otra vez con cd y el nombre de la carpeta
```bash
cd matelog
```
### 5. Crea un entorno virtual con la instrucción:
```bash
 python -m venv venv 
```

### 6. Activa el entorno virtual con la instrucción:
```bash
venv\Scripts\activate
```
### 7. Verifica que la versión que está activa de Python sea la 3.9 con la instrucción:
```bash
python --version
```
### 8. Instala las dependencias que se encuentran en el archivo requerimientos.txt
```bash
pip install -r requirements.txt
```
### 9. Ejecuta el servidor de desarrollo con la instrucción:
```bash
python manage.py runserver
```
### 10. Abre en un navegador la dirección:
```bash
http://127.0.0.1:8000/
```

## Autor ✒️

* **Miguel Ángel** - *Proyecto de Residencias* - [Miguel-AngelRC](https://github.com/Miguel-AngelRC)
