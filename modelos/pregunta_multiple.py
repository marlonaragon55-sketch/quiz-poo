from .pregunta import Pregunta


class PreguntaMultiple(Pregunta):
    def __init__(self, enunciado, categoria, dificultad, opciones, indice_correcto):
        super().__init__(enunciado, categoria, dificultad)
        limpias = [o.strip() for o in opciones if o and o.strip()]
        if len(limpias) < 2:
            raise ValueError("Se necesitan al menos 2 opciones.")
        if not 0 <= indice_correcto < len(limpias):
            raise ValueError("La opción correcta no existe en la lista de opciones.")
        self._opciones = limpias
        self._indice_correcto = indice_correcto

    @property
    def opciones(self):
        return list(self._opciones)

    def evaluar(self, indice):
        return indice == self._indice_correcto
