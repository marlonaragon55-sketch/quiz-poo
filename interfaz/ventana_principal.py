import tkinter as tk
from tkinter import ttk, messagebox

from modelos import Pregunta, PreguntaMultiple
from servicios import GestorPreguntas, Partida, Ranking, preguntas_iniciales


class VentanaPrincipal(tk.Tk):
    """Solo presenta datos y reacciona a eventos; las reglas viven en Partida."""

    def __init__(self):
        super().__init__()
        self.title("Quiz POO")
        self.geometry("580x470")
        self.resizable(False, False)
        self.gestor = GestorPreguntas(preguntas_iniciales())
        self.ranking = Ranking()
        self.partida = None
        self._jugador = ""
        self._marco = None
        self._job = None
        self._restante = 0
        self._mostrar_menu()

    # ---------- utilidades ----------
    def _nuevo_marco(self):
        self._cancelar_timer()
        if self._marco:
            self._marco.destroy()
        self._marco = ttk.Frame(self, padding=20)
        self._marco.pack(fill="both", expand=True)
        return self._marco

    def _cancelar_timer(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None

    # ---------- menú ----------
    def _mostrar_menu(self):
        m = self._nuevo_marco()
        ttk.Label(m, text="Quiz de Programación", font=("Arial", 20, "bold")).pack(pady=10)
        ttk.Label(m, text="Nombre del jugador:").pack()
        self._nombre = ttk.Entry(m, width=30)
        self._nombre.pack(pady=4)
        ttk.Label(m, text="Categoría:").pack()
        self._cat = ttk.Combobox(m, values=["Todas"] + self.gestor.categorias(), state="readonly")
        self._cat.set("Todas")
        self._cat.pack(pady=4)
        ttk.Label(m, text="Dificultad:").pack()
        self._dif = ttk.Combobox(m, values=["Todas"] + list(Pregunta.DIFICULTADES), state="readonly")
        self._dif.set("Todas")
        self._dif.pack(pady=4)
        ttk.Button(m, text="Jugar", command=self._iniciar).pack(pady=8)
        ttk.Button(m, text="Agregar pregunta", command=self._dialogo_agregar).pack(pady=2)
        ttk.Button(m, text="Ver ranking", command=self._ver_ranking).pack(pady=2)

    def _iniciar(self):
        nombre = self._nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Falta el nombre", "Escribe tu nombre para jugar.")
            return
        cat = None if self._cat.get() == "Todas" else self._cat.get()
        dif = None if self._dif.get() == "Todas" else self._dif.get()
        try:
            self.partida = Partida(self.gestor.filtrar(cat, dif))
        except ValueError as e:
            messagebox.showwarning("Sin preguntas", str(e))
            return
        self._jugador = nombre
        self._mostrar_pregunta()

    # ---------- juego ----------
    def _mostrar_pregunta(self):
        p = self.partida.pregunta_actual
        m = self._nuevo_marco()
        ttk.Label(m, text=f"Pregunta {self.partida.progreso}  |  Puntaje: {self.partida.puntaje}").pack()
        self._lbl_tiempo = ttk.Label(m, font=("Arial", 14, "bold"))
        self._lbl_tiempo.pack(pady=6)
        ttk.Label(m, text=p.enunciado, wraplength=500, font=("Arial", 13)).pack(pady=14)
        for i, texto in enumerate(p.opciones):
            ttk.Button(m, text=texto, width=40, command=lambda i=i: self._responder(i)).pack(pady=3)
        self._restante = self.partida.tiempo_limite
        self._tick()

    def _tick(self):
        self._lbl_tiempo.config(text=f"Tiempo: {self._restante}s")
        if self._restante <= 0:
            self._job = None
            self.partida.tiempo_agotado()
            messagebox.showinfo("Tiempo", "¡Se acabó el tiempo!")
            self._siguiente()
        else:
            self._restante -= 1
            self._job = self.after(1000, self._tick)

    def _responder(self, indice):
        self._cancelar_timer()
        ok = self.partida.responder(indice)
        messagebox.showinfo("Resultado", "¡Correcto!" if ok else "Incorrecto")
        self._siguiente()

    def _siguiente(self):
        if self.partida.terminada:
            self._mostrar_resultados()
        else:
            self._mostrar_pregunta()

    def _mostrar_resultados(self):
        self.ranking.registrar(self._jugador, self.partida.puntaje)
        m = self._nuevo_marco()
        ttk.Label(m, text="Fin de la partida", font=("Arial", 20, "bold")).pack(pady=10)
        ttk.Label(m, text=f"Jugador: {self._jugador}").pack()
        ttk.Label(m, text=f"Puntaje: {self.partida.puntaje}").pack()
        ttk.Label(m, text=f"Aciertos: {self.partida.aciertos}   Errores: {self.partida.errores}").pack(pady=6)
        ttk.Button(m, text="Ver ranking", command=self._ver_ranking).pack(pady=4)
        ttk.Button(m, text="Menú principal", command=self._mostrar_menu).pack(pady=4)

    def _ver_ranking(self):
        m = self._nuevo_marco()
        ttk.Label(m, text="Ranking (sesión actual)", font=("Arial", 18, "bold")).pack(pady=10)
        top = self.ranking.top()
        if not top:
            ttk.Label(m, text="Aún no hay partidas jugadas.").pack()
        for pos, (nombre, pts) in enumerate(top, 1):
            ttk.Label(m, text=f"{pos}. {nombre} — {pts} pts").pack()
        ttk.Button(m, text="Menú principal", command=self._mostrar_menu).pack(pady=14)

    # ---------- agregar pregunta ----------
    def _dialogo_agregar(self):
        d = tk.Toplevel(self)
        d.title("Nueva pregunta")
        d.grab_set()
        campos = {}
        for etiqueta in ("Enunciado", "Categoría", "Opción 1", "Opción 2", "Opción 3", "Opción 4"):
            ttk.Label(d, text=etiqueta).pack(padx=10, anchor="w")
            campos[etiqueta] = ttk.Entry(d, width=50)
            campos[etiqueta].pack(padx=10, pady=2)
        ttk.Label(d, text="Dificultad").pack(padx=10, anchor="w")
        dif = ttk.Combobox(d, values=list(Pregunta.DIFICULTADES), state="readonly")
        dif.set("facil")
        dif.pack(padx=10, pady=2)
        ttk.Label(d, text="Número de la opción correcta (1-4)").pack(padx=10, anchor="w")
        correcta = ttk.Entry(d, width=5)
        correcta.pack(padx=10, pady=2)

        def guardar():
            try:
                idx = int(correcta.get()) - 1
            except ValueError:
                messagebox.showerror("Datos inválidos", "La opción correcta debe ser un número.", parent=d)
                return
            try:
                opciones = [campos[f"Opción {i}"].get() for i in range(1, 5)]
                nueva = PreguntaMultiple(campos["Enunciado"].get(), campos["Categoría"].get(),
                                         dif.get(), opciones, idx)
                self.gestor.agregar(nueva)
            except ValueError as e:
                messagebox.showerror("Datos inválidos", str(e), parent=d)
                return
            messagebox.showinfo("Listo", "Pregunta agregada.", parent=d)
            d.destroy()
            self._mostrar_menu()

        ttk.Button(d, text="Guardar", command=guardar).pack(pady=10)
