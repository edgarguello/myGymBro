from abc import ABC, abstractmethod

class Ejercicio(ABC):
    """
    Clase base abstracta para representar un ejercicio.
    Esta clase debe ser extendida por ejercicios concretos (fuerza, cardio, etc.).
    Define la interfaz común que todas las subclases deben implementar.
    Atributos:
        nombre_ejercicio (str): Nombre del ejercicio.
    """

    def __init__(self, nombre_ejercicio):
        """
        Inicializa un ejercicio con su nombre.
        Args:
            nombre_ejercicio (str): Nombre del ejercicio.
        """

        self.nombre_ejercicio = nombre_ejercicio

    @abstractmethod
    def descripcion(self):
        """
        Método abstracto que debe ser implementado por las subclases.
        Debe devolver una descripción textual del ejercicio.
        Returns:
            str: Descripción del ejercicio.
        """

        pass

    @abstractmethod
    def estimar_calorias(self):
        """
        Método polimórfico que estima las calorías quemadas.
        Cada subclase implementa su propia fórmula.
        """
        pass