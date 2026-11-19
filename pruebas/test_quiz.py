import pytest
from modelos import PreguntaMultiple, PreguntaVerdaderoFalso, Pregunta
from servicios import Partida, GestorPreguntas


def test_polimorfismo_evaluar():
    m = PreguntaMultiple("¿2+2?", "mate", "facil", ["3", "4"], 1)
    v = PreguntaVerdaderoFalso("El sol es una estrella", "ciencia", "facil", True)
    assert m.evaluar(1) and v.evaluar(0) and not v.evaluar(1)


def test_partida_puntaje_y_tiempo_agotado():
    p = PreguntaMultiple("¿2+2?", "mate", "media", ["3", "4"], 1)
    q = PreguntaVerdaderoFalso("Falso", "mate", "facil", False)
    partida = Partida([p, q])
    for _ in range(2):
        if partida.pregunta_actual is p:
            partida.responder(1)
        else:
            partida.tiempo_agotado()
    assert partida.terminada and partida.puntaje == 20 and partida.errores == 1


def test_entradas_invalidas():
    with pytest.raises(ValueError):
        PreguntaMultiple("", "x", "facil", ["a", "b"], 0)
    with pytest.raises(ValueError):
        PreguntaMultiple("¿?", "x", "facil", ["a", "b"], 5)
    with pytest.raises(TypeError):
        GestorPreguntas().agregar("no soy pregunta")
    with pytest.raises(TypeError):
        Pregunta("a", "b", "facil")   # clase abstracta
