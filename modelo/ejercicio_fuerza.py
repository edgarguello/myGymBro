from modelo.ejercicio import Ejercicio

class EjercicioFuerza(Ejercicio):
    """
    Representa un ejercicio de fuerza regular.
    Atributos:
        subtipo (str): Tipo de ejercicio de fuerza (por defecto, "Fuerza Regular").
        peso_maximo (float): Peso máximo utilizado en el ejercicio en kilogramos.
        repeticiones (int): Número de repeticiones por serie.
        sets (int): Número de series del ejercicio.
        descanso (int): Tiempo de descanso entre series en minutos.
    """

    subtipo = "Fuerza Regular"

    def __init__(self, nombre_ejercicio, peso_maximo, repeticiones, sets, descanso):
        """
        Inicializa un ejercicio de fuerza regular.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
            peso_maximo (float): Peso utilizado en kg.
            repeticiones (int): Número de repeticiones por serie.
            sets (int): Número de series.
            descanso (int): Descanso entre series en minutos.
        """
        super().__init__(nombre_ejercicio)
        self.peso_maximo = peso_maximo
        self.repeticiones = repeticiones
        self.sets = sets
        self.descanso = descanso

    def descripcion(self):
        """
        Devuelve una descripción textual del ejercicio de fuerza regular.
        Returns:
            str: Descripción del ejercicio.
        """
        return (
            f"Ejercicio de {self.subtipo} {self.nombre_ejercicio}: "
            f"{self.sets} sets de {self.repeticiones} reps con {self.peso_maximo}kg, "
            f"descanso de {self.descanso} minuto/s"
        )

    def estimar_calorias(self):
        """
        Estima la cantidad de calorías que se generan durante el ejercicio.
        Returns:
            float: Calorías estimadas.
        """
        return self.sets * self.repeticiones * self.peso_maximo * 0.1


class EjercicioFuerzaDropSet(EjercicioFuerza):
    """
    Representa un ejercicio de fuerza tipo drop set (reducción progresiva de peso e incremento de repeticiones).
    Atributos:
        subtipo (str): Tipo de ejercicio (por defecto, "Drop Set").
        variacion_peso (float): Cantidad de peso a disminuir entre sets en kg.
        variacion_reps (int): Cantidad de repeticiones a aumentar entre sets.
    """

    subtipo = "Drop Set"

    def __init__(self, nombre_ejercicio, peso_maximo, repeticiones, descanso, sets, variacion_peso, variacion_repeticiones):
        """
        Inicializa un ejercicio de fuerza tipo drop set.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
            peso_maximo (float): Peso inicial en kg.
            repeticiones (int): Repeticiones iniciales.
            descanso (int): Descanso entre sets en minutos.
            sets (int): Número total de sets (drops).
            variacion_peso (float): Peso que se reduce en cada set.
            variacion_repeticiones (int): Repeticiones que se incrementan en cada set.
        """
        super().__init__(nombre_ejercicio, peso_maximo, repeticiones, sets, descanso)
        self.variacion_peso = variacion_peso
        self.variacion_reps = variacion_repeticiones

    def descripcion(self):
        """
        Devuelve una descripción textual del ejercicio de tipo drop set.
        Returns:
            str: Descripción del ejercicio.
        """

        return f"{self.subtipo} - {self.nombre_ejercicio}: empieza con {self.peso_maximo}kg y {self.repeticiones} reps. Disminuye {self.variacion_peso}kg, aumenta {self.variacion_reps} reps. Descanso de {self.descanso} minuto/s por {self.sets} serie/s."

    def estimar_calorias(self):
        """
        Estima la cantidad de calorías gastadas considerando todos los sets.
        Returns:
            float: Calorías estimadas.
        """
        total_calorias = 0
        peso = self.peso_maximo
        reps = self.repeticiones

        for _ in range(self.sets):
            total_calorias += reps * peso * 0.1
            peso = max(0, peso - self.variacion_peso)
            reps += self.variacion_reps

        return total_calorias
