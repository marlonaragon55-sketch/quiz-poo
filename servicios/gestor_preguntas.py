from modelos import Pregunta, PreguntaMultiple, PreguntaVerdaderoFalso


class GestorPreguntas:
    """Agrega objetos Pregunta (agregación): ellas existen sin el gestor."""

    def __init__(self, preguntas=None):
        self._preguntas = []
        for p in preguntas or []:
            self.agregar(p)

    def agregar(self, pregunta):
        if not isinstance(pregunta, Pregunta):
            raise TypeError("Solo se pueden agregar objetos Pregunta.")
        self._preguntas.append(pregunta)

    def filtrar(self, categoria=None, dificultad=None):
        return [p for p in self._preguntas
                if (categoria is None or p.categoria == categoria)
                and (dificultad is None or p.dificultad == dificultad)]

    def categorias(self):
        return sorted({p.categoria for p in self._preguntas})


def preguntas_iniciales():
    M, V = PreguntaMultiple, PreguntaVerdaderoFalso
    return [
        M("¿Qué palabra clave define una clase en Python?", "Python", "facil", ["def", "class", "object", "self"], 1),
        V("En Python, una lista es inmutable.", "Python", "facil", False),
        M("¿Qué función invoca al constructor de la clase padre?", "Python", "media", ["parent()", "base()", "super()", "init()"], 2),
        M("¿Cuál es el método constructor en Python?", "POO", "facil", ["__new__", "__init__", "__str__", "__main__"], 1),
        V("La herencia permite reutilizar atributos y métodos de otra clase.", "POO", "facil", True),
        M("¿Qué módulo permite crear clases abstractas?", "POO", "media", ["abc", "oop", "typing", "enum"], 0),
        M("Un mismo método con comportamientos distintos según el objeto es...", "POO", "dificil", ["Herencia", "Encapsulamiento", "Polimorfismo", "Composición"], 2),
        M("¿Cuál es la capital de Colombia?", "Cultura General", "facil", ["Medellín", "Bogotá", "Cali", "Barranquilla"], 1),
        V("El río Magdalena desemboca en el mar Caribe.", "Cultura General", "media", True),
    ]
