from .pregunta import Pregunta


class PreguntaVerdaderoFalso(Pregunta):
    def __init__(self, enunciado, categoria, dificultad, es_verdadera):
        super().__init__(enunciado, categoria, dificultad)
        self._es_verdadera = bool(es_verdadera)

    @property
    def opciones(self):
        return ["Verdadero", "Falso"]

    def evaluar(self, indice):
        return (indice == 0) == self._es_verdadera
