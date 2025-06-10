import os
import time
import sys
from modelo.ejercicio_fuerza import EjercicioFuerza
from modelo.ejercicio_fuerza import EjercicioFuerzaDropSet
from modelo.ejercicio_cardio import EjercicioCardio
from modelo.ejercicio_cardio import EjercicioCardioHIIT

class VistaCLI:
    """Vista de línea de comandos para la interacción con el usuario."""

    def mostrar_menu(self):
        """Muestra el menú principal y solicita una opción al usuario.
        Returns:
            str: Opción seleccionada por el usuario.
        """

        self.limpiar_pantalla()
        print("1. Seleccionar rutina \n2. Crear rutina\n3. Salir")
        return self.pedir_texto("Seleccione una opción: ")

    def pedir_nombre_rutina(self):
        """Solicita al usuario el nombre de una nueva rutina.
        Returns:
            str: Nombre de la rutina introducido por el usuario.
        """

        self.limpiar_pantalla()
        print("Creando nueva Rutina...")
        return self.pedir_texto("Nombre de la rutina: ")

    def seleccionar_tipo_ejercicio(self, rutina):
        """Solicita al usuario seleccionar el tipo de ejercicio.
        Args:
            rutina: Objeto Rutina actual.
        Returns:
            class: Clase del tipo de ejercicio seleccionado.
        """

        self.limpiar_pantalla()
        print(f"Rutina : {rutina.nombre}")
        print("Tipo de ejercicio\n1- Ejercicio de Fuerza\n2- Ejercicio de Cardio\n")
        tipo = self.pedir_int("Seleccione una opción: ")
        if tipo == 1:
            return EjercicioFuerza
        elif tipo == 2:
            return EjercicioCardio
        return None

    def seleccionar_subtipo(self, clase_base):
        """Permite al usuario seleccionar un subtipo de ejercicio.
        Args:
            clase_base (class): Clase base del ejercicio.

        Returns:
            class: Subclase seleccionada del ejercicio.
        """

        subtipos = [clase_base] + clase_base.__subclasses__()
        self.limpiar_pantalla()
        print("Tipos disponibles:")
        for idx, clase in enumerate(subtipos, start=1):
            nombre_legible = getattr(clase, "subtipo", clase.__name__)
            print(f"{idx} - {nombre_legible}")

        opcion = self.pedir_int("Seleccione subtipo: ")
        try:
            return subtipos[int(opcion) - 1]
        except (ValueError, IndexError):
            return None

    def pedir_float(self, mensaje):
        """Solicita un número decimal al usuario.
        Args:
            mensaje (str): Mensaje a mostrar.
        Returns:
            float: Valor introducido por el usuario.
        """

        while True:
            try:
                return float(input(mensaje))
            except ValueError:
                print("Por favor, introduzca un número válido.")

    def pedir_int(self, mensaje):
        """Solicita un número entero al usuario.
        Args:
            mensaje (str): Mensaje a mostrar.
        Returns:
            int: Valor introducido por el usuario.
        """

        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Por favor, introduzca un número entero válido.")

    def pedir_texto(self, mensaje):
        """Solicita un texto no vacío al usuario.
        Args:
            mensaje (str): Mensaje a mostrar.
        Returns:
            str: Texto introducido.
        """

        valor = input(mensaje).strip()
        while not valor:
            print("Este campo no puede estar vacío.")
            valor = input(mensaje).strip()
        return valor

    def pedir_datos(self, clase_modelo):
        """Solicita al usuario los datos necesarios para crear un ejercicio.
        Args:
            clase_modelo (class): Clase del modelo de ejercicio.
        Returns:
            dict: Diccionario con los datos introducidos.
        """

        datos = {}
        if clase_modelo.__name__ == "EjercicioFuerza":
            datos["nombre_ejercicio"] = self.pedir_texto("Nombre del ejercicio: ")
            datos["peso_maximo"] = self.pedir_float("Peso máximo (kg): ")
            datos["repeticiones"] = self.pedir_int("Repeticiones: ")
            datos["descanso"] = self.pedir_float("Descanso (minutos): ")

        elif clase_modelo.__name__ == "EjercicioFuerzaDropSet":
            datos["nombre_ejercicio"] = self.pedir_texto("Nombre del ejercicio: ")
            datos["peso_maximo"] = self.pedir_float("Peso máximo inicial (kg): ")
            datos["repeticiones"] = self.pedir_int("Repeticiones iniciales: ")
            datos["descanso"] = self.pedir_float("Descanso (minutos): ")
            datos["variacion_peso"] = self.pedir_float("Disminución de peso (kg): ")
            datos["variacion_repeticiones"] = self.pedir_int("Aumento de repeticiones: ")

        elif clase_modelo.__name__ == "EjercicioCardio":
            datos["nombre_ejercicio"] = self.pedir_texto("Nombre del ejercicio: ")
            datos["velocidad_regular"] = self.pedir_float("Velocidad del ejercicio (km/h): ")
            datos["tiempo"] = self.pedir_int("Tiempo total del ejercicio (min): ")

        elif clase_modelo.__name__ == "EjercicioCardioHIIT":
            datos["nombre_ejercicio"] = self.pedir_texto("Nombre del ejercicio: ")
            datos["velocidad_regular"] = self.pedir_float("Velocidad mínima (km/h): ")
            datos["velocidad_intensa"] = self.pedir_float("Velocidad máxima (km/h): ")
            datos["intervalo"] = self.pedir_float("Intervalo entre velocidades (min): ")
            datos["tiempo"] = self.pedir_float("Tiempo total del ejercicio (min): ")

        self.limpiar_pantalla()
        return datos

    def preguntar_otro_ejercicio(self):
        """Pregunta al usuario si desea añadir otro ejercicio.
        Returns:
            bool: True si desea añadir otro, False en caso contrario.
        """

        otro = input("Ingrese (s) para agregar otro ejercicio u otro carácter para salir: ").strip().lower()
        return otro == "s"

    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje por pantalla.
        Args:
            mensaje (str): Mensaje a mostrar.
        """

        print(mensaje)

    def mostrar_rutina(self, rutina):
        """Muestra la rutina completa con sus ejercicios.
        Args:
            rutina: Objeto Rutina a mostrar.
        """

        self.limpiar_pantalla()
        print(f"Rutina: {rutina.nombre}")
        for linea in rutina.obtener_descripciones():
            print(f"  {linea}")
        self.esperar_confirmacion()

    def esperar_confirmacion(self):
        """Pide al usuario que presione una tecla para continuar."""

        input("Presione enter para volver al menú principal...")

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""

        os.system('cls' if os.name == 'nt' else 'clear')

    def preguntar_si_desea_cargar_rutina(self):
        """Pregunta si se desea crear una nueva rutina si no hay ninguna.
        Returns:
            bool: True si el usuario responde afirmativamente.
        """

        respuesta = input("No hay rutinas cargadas. ¿Desea crear una nueva? (s/n): ").lower()
        return respuesta == "s"

    def seleccionar_rutina(self, rutinas):
        """Permite al usuario seleccionar una rutina de la lista.
        Args:
            rutinas (list): Lista de rutinas disponibles.
        Returns:
            Rutina o None: Rutina seleccionada o None si no se elige ninguna válida.
        """

        self.limpiar_pantalla()
        print("📋 Rutinas disponibles:\n")

        for idx, rutina in enumerate(rutinas, 1):
            print(f"{idx}. {rutina.nombre}")
            if rutina.ejercicios:
                for ej_idx, ejercicio in enumerate(rutina.ejercicios, 1):
                    print(f"   {ej_idx}. {ejercicio.descripcion()}") 
            else:
                print("   (Sin ejercicios)")
            print()

        try:
            seleccion = int(input("Selecciona una rutina por número: "))
            if 1 <= seleccion <= len(rutinas):
                return rutinas[seleccion - 1]
        except ValueError:
            pass

        print("❌ Selección inválida.")
        return None

    def mostrar_inicio_rutina(self, nombre_rutina):
        """Informa del inicio de una rutina.
        Args:
            nombre_rutina (str): Nombre de la rutina.
        """

        self.limpiar_pantalla()
        print(f"🏋️‍♂️ Realizando rutina: '{nombre_rutina}'\n")
        self._mostrar_timer_con_barra(3)

    def esperar_fin_ejercicio(self):
        """Espera que el usuario indique que ha terminado el ejercicio."""

        input("✅ Presiona cualquier tecla cuando termines este ejercicio...")

    def mostrar_descanso(self, minutos):
        """Muestra un temporizador de descanso.
        Args:
            minutos (float): Duración del descanso en minutos.
        """

        segundos = minutos * 60
        print(f"\n🛌 Descanso de {minutos} minutos")
        self._mostrar_timer_con_barra(segundos)

    def _temporizador_cardio(self, ejercicio):
        """Muestra un temporizador para un ejercicio de cardio regular.
        Args:
            ejercicio (EjercicioCardio): Ejercicio a realizar.
        """

        segundos = int(ejercicio.tiempo * 60)
        print(f"\n⏱ Iniciando cardio regular durante {ejercicio.tiempo} minutos a {ejercicio.velocidad_regular} km/h")
        self._mostrar_timer_con_barra(segundos)
        print("\n✅ Ejercicio de cardio regular finalizado.")

    def _temporizador_cardio_hiit(self, ejercicio):
        """Muestra un temporizador para un ejercicio de cardio HIIT.
        Args:
            ejercicio (EjercicioCardioHIIT): Ejercicio a realizar.
        """

        total_segundos = int(ejercicio.tiempo * 60)
        intervalo_segundos = int(ejercicio.intervalo * 60)
        velocidad_actual = ejercicio.velocidad_regular
        velocidad_intensa = ejercicio.velocidad_intensa
        velocidad_suave = ejercicio.velocidad_regular

        tiempo_transcurrido = 0
        toggle = True  

        print(f"\n🔥 Iniciando Cardio HIIT por {ejercicio.tiempo} minutos con intervalos de {ejercicio.intervalo} min.")

        while tiempo_transcurrido < total_segundos:
            velocidad_actual = velocidad_intensa if toggle else velocidad_suave
            velocidad_texto = f"Velocidad actual: {velocidad_actual:.1f} km/h".center(60)
            print(f"\n{velocidad_texto}")
            segundos_restantes = min(intervalo_segundos, total_segundos - tiempo_transcurrido)
            self._mostrar_timer_con_barra(segundos_restantes)
            tiempo_transcurrido += segundos_restantes
            toggle = not toggle

        print("\n✅ Ejercicio HIIT completado.")

    def mostrar_fin_rutina(self, nombre_rutina):
        """Informa de que la rutina ha finalizado.
        Args:
            nombre_rutina (str): Nombre de la rutina.
        """

        self.limpiar_pantalla()
        print(f"🎉 Rutina '{nombre_rutina}' completada. ¡Bien hecho!\n")
        input("🔙 Presiona cualquier tecla para volver al menú principal...")

    def _mostrar_timer_con_barra(self, segundos):
        """Muestra una barra de progreso con temporizador.
        Args:
            segundos (int): Duración total en segundos.
        """

        barra_total = 30
        print("⏳", end=" ", flush=True)
        for i in range(barra_total):
            time.sleep(segundos / barra_total)
            print("█", end="", flush=True)
        print("\n")

    def mostrar_ejercicio(self, ejercicio):
        """Muestra la información del ejercicio actual y lanza su temporizador si aplica.
        Args:
            ejercicio: Objeto del ejercicio a mostrar.
        """

        self.limpiar_pantalla()
        print(f"➡️ Realizando: {getattr(ejercicio, 'nombre_ejercicio', 'N/A')}\n")
        self._mostrar_detalles_ejercicio(ejercicio)

        if isinstance(ejercicio, EjercicioCardioHIIT):
            self._temporizador_cardio_hiit(ejercicio)

        elif isinstance(ejercicio, EjercicioCardio):
            self._temporizador_cardio(ejercicio)

    def _mostrar_detalles_ejercicio(self, ejercicio):
        """Muestra los detalles del ejercicio según su tipo.
        Args:
            ejercicio: Objeto ejercicio.
        """
        
        print("📋 Detalles del ejercicio:\n")

        if isinstance(ejercicio, EjercicioFuerza):
            print("🧱 Tipo: Fuerza regular")
            print(f"📦 Peso máximo: {ejercicio.peso_maximo} kg")
            print(f"🔁 Repeticiones: {ejercicio.repeticiones}")
            print(f"🕒 Descanso: {ejercicio.descanso} min")

        elif isinstance(ejercicio, EjercicioFuerzaDropSet):
            print("🧱 Tipo: Fuerza Drop Set")
            print(f"📦 Peso inicial: {ejercicio.peso_maximo} kg")
            print(f"📉 Disminución de peso: {ejercicio.variacion_peso} kg")
            print(f"🔁 Repeticiones iniciales: {ejercicio.repeticiones}")
            print(f"🔁 Aumento de repeticiones: {ejercicio.variacion_repeticiones}")
            print(f"🕒 Descanso: {ejercicio.descanso} min")

        elif isinstance(ejercicio, EjercicioCardio):
            print("🏃 Tipo: Cardio regular")
            print(f"🚶 Velocidad: {ejercicio.velocidad_regular} km/h")
            print(f"⏱ Tiempo: {ejercicio.tiempo} min")

        elif isinstance(ejercicio, EjercicioCardioHIIT):
            print("🔥 Tipo: Cardio HIIT")
            print(f"🚶 Velocidad regular: {ejercicio.velocidad_regular} km/h")
            print(f"🏃 Velocidad intensa: {ejercicio.velocidad_intensa} km/h")
            print(f"🔁 Intervalo: {ejercicio.intervalo} min")
            print(f"⏱ Tiempo total: {ejercicio.tiempo} min")

        else:
            print("⚠️ Tipo de ejercicio no reconocido.")

        print()