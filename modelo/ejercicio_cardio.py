from modelo.ejercicio import Ejercicio

class EjercicioCardio(Ejercicio):
    """
    Representa un ejercicio de cardio regular.
    Atributos:
        subtipo (str): Tipo de ejercicio cardio (por defecto, "Cardio Regular").
        velocidad_regular (float): Velocidad constante del ejercicio en km/h.
        tiempo (int): Duración del ejercicio en minutos.
    """

    subtipo = "Cardio Regular"

    def __init__(self, nombre_ejercicio, velocidad_regular, tiempo):
        """
        Inicializa un ejercicio de cardio regular.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
            velocidad_regular (float): Velocidad constante en km/h.
            tiempo (int): Tiempo total del ejercicio en minutos.
        """

        super().__init__(nombre_ejercicio)
        self.velocidad_regular = velocidad_regular
        self.tiempo = tiempo

    def descripcion(self):
        """
        Devuelve una descripción textual del ejercicio de cardio.
        Returns:
            str: Descripción del ejercicio.
        """
        return f"Ejercicio de cardio {self.nombre_ejercicio}: {self.tiempo} min a {self.velocidad_regular} km/h"


class EjercicioCardioHIIT(EjercicioCardio):
    """
    Representa un ejercicio de cardio tipo HIIT (intervalos de alta intensidad).
    Atributos:
        subtipo (str): Tipo de ejercicio (por defecto, "Cardio HIIT").
        velocidad_intensa (float): Velocidad de alta intensidad en km/h.
        intervalo (int): Duración de cada intervalo en minutos.
    """

    subtipo = "Cardio HIIT"
    
    def __init__(self, nombre_ejercicio, velocidad_regular, velocidad_intensa, intervalo, tiempo):
        """
        Inicializa un ejercicio de cardio HIIT.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
            velocidad_regular (float): Velocidad baja en km/h.
            velocidad_intensa (float): Velocidad alta en km/h.
            intervalo (int): Duración de cada intervalo en minutos.
            tiempo (int): Tiempo total del ejercicio en minutos.
        """

        super().__init__(nombre_ejercicio, velocidad_regular, tiempo)
        self.velocidad_intensa = velocidad_intensa
        self.intervalo = intervalo

    def descripcion(self):
        """
        Devuelve una descripción textual del ejercicio HIIT.
        Returns:
            str: Descripción del ejercicio.
        """

        return f"{self.subtipo}: alternar {self.velocidad_regular}/{self.velocidad_intensa} km/h cada {self.intervalo} minuto/s por {self.tiempo} min"
