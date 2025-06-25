# My Gym Bro

Aplicación académica construida en Python con arquitectura MVC para la gestión de rutinas de entrenamiento personal. Permite crear, almacenar y ejecutar rutinas con ejercicios de fuerza (regular y drop set) y cardio (regular y HIIT), calculando además las calorías estimadas por cada ejercicio.

## Cómo ejecutar el sistema

### Requisitos

* Python 3.10 o superior
* Biblioteca estándar `tkinter` (para la interfaz gráfica)
* Sistema operativo: macOS, Linux o Windows

### Instrucciones por sistema operativo

#### Linux (Ubuntu, Debian, etc.)


python3 mygymbro_ig.py


Asegúrate de tener `python3-tk` instalado:

 
sudo apt install python3-tk


#### macOS (M1/M2/M3 con Homebrew)

1. Instalar Homebrew si no está instalado: https://brew.sh 
2. Ejecutar el programa con:

 
/opt/homebrew/bin/python3 /ruta/al/proyecto/mygymbro_ig.py


Esto es necesario porque la versión de Python que viene por defecto con macOS o Visual Studio Code no siempre incluye correctamente `tkinter`.

#### Windows

1. Instalar Python desde python.org
2. Seleccionar la opción "Add Python to PATH" durante la instalación.
3. Ejecutar:

 
python mygymbro_ig.py


Si aparece un error relacionado a `tkinter`, asegurarse de que el instalador de Python incluya esa librería (suele venir por defecto).

## Estructura del Proyecto

El proyecto está dividido en cuatro módulos principales, siguiendo el patrón MVC (Modelo - Vista - Controlador):

### modelo/

Contiene toda la lógica de negocio del sistema. Incluye:

* Clase abstracta `Ejercicio`
* Subclases `EjercicioFuerza`, `EjercicioFuerzaDropSet`
* Subclases `EjercicioCardio`, `EjercicioCardioHIIT`
* Clase `Rutina` que actúa como contenedor de ejercicios

Cada tipo de ejercicio implementa su propia lógica para descripción y estimación calórica.

### controlador.py

Actúa como intermediario entre la vista y el modelo. Se encarga de:

* Crear rutinas y ejercicios
* Almacenar y recuperar datos usando pickle
* Coordinar la interacción con la vista

### vista/ (contenido en mygymbro\_ig.py)

Contiene la interfaz gráfica desarrollada con Tkinter. Incluye varias pantallas:

* `MenuFrame`: menú principal
* `SeleccionFrame`: seleccionar una rutina guardada
* `CrearFrame`: formulario para crear rutinas
* `RealizarFrame`: ejecución paso a paso de una rutina

### datos/

Contiene los datos persistentes del sistema. Guarda las rutinas en un archivo binario `rutinas.pkl` utilizando pickle.

## Autor

Edgar Jesús Arguello Contessi
edgar.arguello@fpuna.edu.py
