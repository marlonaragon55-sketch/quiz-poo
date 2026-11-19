class Ranking:
    """Ranking en memoria (no se persiste, como lo permite el enunciado)."""

    def __init__(self):
        self._registros = []

    def registrar(self, nombre, puntaje):
        self._registros.append((nombre, puntaje))

    def top(self, n=5):
        return sorted(self._registros, key=lambda r: r[1], reverse=True)[:n]
