from abc import ABC, abstractmethod


class Pregunta(ABC):
    """Clase abstracta: define el contrato común de cualquier tipo de pregunta."""

    DIFICULTADES = ("facil", "media", "dificil")
    PUNTOS = {"facil": 10, "media": 20, "dificil": 30}

    def __init__(self, enunciado, categoria, dificultad):
        self.enunciado = enunciado      # usa los setters con validación
        self.categoria = categoria
        self.dificultad = dificultad

    @property
    def enunciado(self):
        return self._enunciado

    @enunciado.setter
    def enunciado(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El enunciado no puede estar vacío.")
        self._enunciado = valor.strip()

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        if not valor or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor.strip().title()

    @property
    def dificultad(self):
        return self._dificultad

    @dificultad.setter
    def dificultad(self, valor):
        if valor not in self.DIFICULTADES:
            raise ValueError(f"Dificultad inválida. Use: {', '.join(self.DIFICULTADES)}.")
        self._dificultad = valor

    @property
    def puntos(self):
        return self.PUNTOS[self._dificultad]

    @property
    @abstractmethod
    def opciones(self):
        """Textos que la interfaz muestra como alternativas."""

    @abstractmethod
    def evaluar(self, indice):
        """Devuelve True si la opción elegida (por índice) es correcta."""
