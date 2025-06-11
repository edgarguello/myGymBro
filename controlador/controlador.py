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
        self.cargar_rutinas()

    def obtener_rutinas(self):
        return self.rutinas

    def crear_rutina(self, nombre, lista_ejercicios):
        rutina = Rutina(nombre)
        for ej in lista_ejercicios:
            rutina.agregar_ejercicio(ej)
        self.rutinas.append(rutina)
        self.guardar_rutinas()

    def realizar_rutina(self, rutina):
        # Simplemente delega a la vista RealizarFrame con rutina cargada
        self.vista.mostrar_realizar(rutina)

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
            self.vista.mostrar_error(f"❌ Error al guardar las rutinas: {e}")

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
                self.vista.mostrar_error(f"⚠️ No se pudo cargar las rutinas guardadas: {e}")
                self.rutinas = []

    def obtener_subtipos(self, tipo):
        if tipo == "Fuerza":
            return ["Regular", "DropSet"]
        elif tipo == "Cardio":
            return ["Regular", "HIIT"]
        return []

    def obtener_campos_para(self, tipo, subtipo):
        if tipo == "Fuerza":
            if subtipo == "Regular":
                return ["nombre_ejercicio", "peso_maximo", "repeticiones", "sets", "descanso"]
            elif subtipo == "DropSet":
                return ["nombre_ejercicio", "peso_maximo", "repeticiones", "descanso", "sets", "variacion_peso", "variacion_repeticiones"]
        elif tipo == "Cardio":
            if subtipo == "Regular":
                return ["nombre_ejercicio", "velocidad_regular", "tiempo"]
            elif subtipo == "HIIT":
                return ["nombre_ejercicio", "velocidad_regular", "velocidad_intensa", "intervalo", "tiempo"]
        return []

    def crear_ejercicio(self, tipo, subtipo, datos):
        try:
            if tipo == "Fuerza":
                if subtipo == "Regular":
                    return EjercicioFuerza(
                        datos["nombre_ejercicio"],
                        float(datos["peso_maximo"]),
                        int(datos["repeticiones"]),
                        int(datos["sets"]),
                        int(datos["descanso"])
                    )
                elif subtipo == "DropSet":
                    return EjercicioFuerzaDropSet(
                        datos["nombre_ejercicio"],
                        float(datos["peso_maximo"]),
                        int(datos["repeticiones"]),
                        int(datos["descanso"]),
                        int(datos["sets"]),
                        float(datos["variacion_peso"]),
                        int(datos["variacion_repeticiones"])
                    )
            elif tipo == "Cardio":
                if subtipo == "Regular":
                    return EjercicioCardio(
                        datos["nombre_ejercicio"],
                        float(datos["velocidad_regular"]),
                        int(datos["tiempo"])
                    )
                elif subtipo == "HIIT":
                    return EjercicioCardioHIIT(
                        datos["nombre_ejercicio"],
                        float(datos["velocidad_regular"]),
                        float(datos["velocidad_intensa"]),
                        int(datos["intervalo"]),
                        int(datos["tiempo"])
                    )
        except (ValueError, KeyError) as e:
            self.vista.mostrar_error(f"❌ Error al crear ejercicio: {e}")
            return None
