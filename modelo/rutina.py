class Rutina:
    """
    Representa una rutina de ejercicios.
    Atributos:
        nombre (str): Nombre de la rutina.
        ejercicios (list): Lista de objetos ejercicio agregados a la rutina.
    """

    def __init__(self, nombre):
        """
        Inicializa una nueva instancia de la clase Rutina.
        Args:
            nombre (str): El nombre de la rutina.
        """
        self.nombre = nombre
        self.ejercicios = []

    def agregar_ejercicio(self, ejercicio):
        """
        Agrega un ejercicio a la rutina.
        Args:
            ejercicio (object): Instancia de un ejercicio que se agregará a la rutina.
        """
        self.ejercicios.append(ejercicio)

    def obtener_descripciones(self):
        """
        Obtiene una lista de descripciones de todos los ejercicios en la rutina.
        Cada descripción está numerada en formato "n. descripción".
        Returns:
            list de str: Lista con las descripciones numeradas de los ejercicios.
        """
        return [f"{i + 1}. {e.descripcion()}" for i, e in enumerate(self.ejercicios)]
