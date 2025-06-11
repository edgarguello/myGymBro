import os
import pickle
from modelo.rutina import Rutina
from modelo.ejercicio_fuerza import EjercicioFuerza, EjercicioFuerzaDropSet
from modelo.ejercicio_cardio import EjercicioCardio, EjercicioCardioHIIT

class Controlador:
    """
    Clase Controlador que gestiona el flujo principal de la aplicación de rutinas.
    Se encarga de crear, iniciar, guardar y cargar rutinas.
    """

    ARCHIVO_RUTINAS = os.path.join("datos", "rutinas.pkl")

    def __init__(self, vista):
        """
        Inicializa el controlador con una vista y una lista de rutinas vacía.
        :param vista: Objeto que representa la vista (interfaz de usuario).
        """
        self.vista = vista
        self.rutinas = []

    def iniciar(self):
        """
        Inicia el ciclo principal de la aplicación.
        Carga las rutinas guardadas y muestra el menú principal.
        """
        self.cargar_rutinas()
        while True:
            opcion = self.vista.mostrar_menu()
            if opcion == "1":
                self.empezar_rutina()
            elif opcion == "2":
                self.crear_rutina()
            elif opcion == "3":
                break

    def crear_rutina(self):
        """
        Crea una nueva rutina solicitando datos desde la vista.
        Permite agregar múltiples ejercicios a la rutina.
        Guarda la rutina al finalizar.
        """
        nombre = self.vista.pedir_nombre_rutina()
        rutina = Rutina(nombre)

        while True:
            clase_base = self.vista.seleccionar_tipo_ejercicio(rutina)
            if clase_base is None:
                self.vista.mostrar_mensaje("Tipo inválido.")
                continue

            clase = self.vista.seleccionar_subtipo(clase_base)
            if clase is None:
                self.vista.mostrar_mensaje("Subtipo inválido.")
                continue

            datos = self.vista.pedir_datos(clase)
            ejercicio = clase(**datos)
            rutina.agregar_ejercicio(ejercicio)

            if not self.vista.preguntar_otro_ejercicio():
                break
        self.rutinas.append(rutina)
        self.guardar_rutinas()
        self.vista.mostrar_rutina(rutina)

    def empezar_rutina(self):
        """
        Permite al usuario seleccionar una rutina existente para realizarla.
        Si no hay rutinas, ofrece crear una nueva.
        """
        if not self.rutinas:
            desea_crear = self.vista.preguntar_si_desea_cargar_rutina()
            if desea_crear:
                self.crear_rutina()
            else:
                return

        rutina = self.vista.seleccionar_rutina(self.rutinas)
        if rutina:
            self.realizar_rutina(rutina)

    def realizar_rutina(self, rutina):
        """
        Ejecuta los ejercicios de una rutina, mostrando instrucciones y descansos por set.
        :param rutina: Objeto de tipo Rutina a ejecutar.
        """
        self.vista.mostrar_inicio_rutina(rutina.nombre)

        for ejercicio in rutina.ejercicios:
            sets = int(getattr(ejercicio, 'sets', 1))

            for numero_set in range(1, sets + 1):
                self.vista.mostrar_ejercicio(ejercicio,numero_set)
                self.vista.esperar_fin_ejercicio()

                descanso = getattr(ejercicio, 'descanso', None)
                if isinstance(descanso, (int, float)) and descanso > 0 and numero_set < sets:
                    self.vista.mostrar_descanso(descanso)

        self.vista.mostrar_fin_rutina(rutina.nombre)

    def guardar_rutinas(self):
        """
        Guarda la lista de rutinas actuales en un archivo utilizando pickle.
        Crea la carpeta si no existe.
        """
        try:
            os.makedirs(os.path.dirname(self.ARCHIVO_RUTINAS), exist_ok=True)
            with open(self.ARCHIVO_RUTINAS, 'wb') as f:
                pickle.dump(self.rutinas, f)
        except Exception as e:
            self.vista.mostrar_mensaje(f"❌ Error al guardar las rutinas: {e}")
    
    def cargar_rutinas(self):
        """
        Carga las rutinas guardadas desde un archivo utilizando pickle.
        Si hay error al leer, muestra un mensaje y deja la lista vacía.
        """
        if os.path.exists(self.ARCHIVO_RUTINAS):
            try:
                with open(self.ARCHIVO_RUTINAS, 'rb') as f:
                    self.rutinas = pickle.load(f)
            except Exception as e:
                self.vista.mostrar_mensaje(f"⚠️ No se pudo cargar las rutinas guardadas: {e}")
                self.rutinas = []
