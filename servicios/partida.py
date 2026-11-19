import random


class Partida:
    """Controla el estado de un juego. La interfaz solo consulta y avisa eventos."""

    def __init__(self, preguntas, tiempo_por_pregunta=15):
        if not preguntas:
            raise ValueError("No hay preguntas para esa selección.")
        if tiempo_por_pregunta <= 0:
            raise ValueError("El tiempo por pregunta debe ser positivo.")
        self._preguntas = random.sample(preguntas, len(preguntas))
        self._tiempo = tiempo_por_pregunta
        self._indice = 0
        self._puntaje = 0
        self._aciertos = 0
        self._errores = 0

    @property
    def puntaje(self):
        return self._puntaje

    @property
    def aciertos(self):
        return self._aciertos

    @property
    def errores(self):
        return self._errores

    @property
    def tiempo_limite(self):
        return self._tiempo

    @property
    def terminada(self):
        return self._indice >= len(self._preguntas)

    @property
    def pregunta_actual(self):
        return None if self.terminada else self._preguntas[self._indice]

    @property
    def progreso(self):
        return f"{min(self._indice + 1, len(self._preguntas))}/{len(self._preguntas)}"

    def responder(self, indice):
        pregunta = self._exigir_pregunta()
        if not 0 <= indice < len(pregunta.opciones):
            raise ValueError("Opción fuera de rango.")
        correcta = pregunta.evaluar(indice)   # polimorfismo
        if correcta:
            self._puntaje += pregunta.puntos
            self._aciertos += 1
        else:
            self._errores += 1
        self._indice += 1
        return correcta

    def tiempo_agotado(self):
        self._exigir_pregunta()
        self._errores += 1
        self._indice += 1

    def _exigir_pregunta(self):
        if self.terminada:
            raise RuntimeError("La partida ya terminó.")
        return self._preguntas[self._indice]
