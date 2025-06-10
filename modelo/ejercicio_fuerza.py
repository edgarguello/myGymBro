from modelo.ejercicio import Ejercicio

class EjercicioFuerza(Ejercicio):
    """
    Representa un ejercicio de fuerza regular.
    Atributos:
        subtipo (str): Tipo de ejercicio de fuerza (por defecto, "Fuerza Regular").
        peso_maximo (float): Peso máximo utilizado en el ejercicio en kilogramos.
        repeticiones (int): Número de repeticiones por serie.
        descanso (int): Tiempo de descanso entre series en minutos.
    """

    subtipo = "Fuerza Regular"

    def __init__(self, nombre_ejercicio, peso_maximo, repeticiones, descanso):
        """
        Inicializa un ejercicio de fuerza regular.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
            peso_maximo (float): Peso utilizado en kg.
            repeticiones (int): Número de repeticiones.
            descanso (int): Descanso entre series en minutos.
        """
        super().__init__(nombre_ejercicio)
        self.peso_maximo = peso_maximo
        self.repeticiones = repeticiones
        self.descanso = descanso

    def descripcion(self):
        """
        Devuelve una descripción textual del ejercicio de fuerza regular.
        Returns:
            str: Descripción del ejercicio.
        """

        return f"Ejercicio de {self.subtipo} {self.nombre_ejercicio}: {self.repeticiones} reps con {self.peso_maximo}kg, descanso de {self.descanso} minuto/s"


class EjercicioFuerzaDropSet(EjercicioFuerza):
    """
    Representa un ejercicio de fuerza tipo drop set (reducción progresiva de peso e incremento de repeticiones).
    Atributos:
        subtipo (str): Tipo de ejercicio (por defecto, "Drop Set").
        variacion_peso (float): Cantidad de peso a disminuir entre sets en kg.
        variacion_reps (int): Cantidad de repeticiones a aumentar entre sets.
    """

    subtipo = "Drop Set"

    def __init__(self, nombre_ejercicio, peso_maximo, repeticiones, descanso, variacion_peso, variacion_repeticiones):
        """
        Inicializa un ejercicio de fuerza tipo drop set.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
            peso_maximo (float): Peso inicial en kg.
            repeticiones (int): Repeticiones iniciales.
            descanso (int): Descanso entre sets en minutos.
            variacion_peso (float): Peso que se reduce en cada set.
            variacion_repeticiones (int): Repeticiones que se incrementan en cada set.
        """

        super().__init__(nombre_ejercicio, peso_maximo, repeticiones, descanso)
        self.variacion_peso = variacion_peso
        self.variacion_reps = variacion_repeticiones

    def descripcion(self):
        """
        Devuelve una descripción textual del ejercicio de tipo drop set.
        Returns:
            str: Descripción del ejercicio.
        """

        return f"{self.subtipo}: empieza con {self.peso_maximo}kg y {self.repeticiones} reps. Disminuye {self.variacion_peso}kg, aumenta {self.variacion_reps} reps. Descanso de {self.descanso} minuto/s"
