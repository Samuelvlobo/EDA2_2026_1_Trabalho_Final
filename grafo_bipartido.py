# Representa o relacionamento entre usuários e séries (sem peso).

class GrafoBipartido:

    def __init__(self):
        self.usuarios = set()
        self.series = set()

        # usuario -> set(series)
        self.adj_usuario = {}

        # serie -> set(usuarios)
        self.adj_serie = {}

    def adicionar_usuario(self, usuario):
        if usuario not in self.usuarios:
            self.usuarios.add(usuario)
            self.adj_usuario[usuario] = set()

    def adicionar_serie(self, serie):
        if serie not in self.series:
            self.series.add(serie)
            self.adj_serie[serie] = set()

    def adicionar_interacao(self, usuario, serie):
        self.adicionar_usuario(usuario)
        self.adicionar_serie(serie)

        self.adj_usuario[usuario].add(serie)
        self.adj_serie[serie].add(usuario)

    def series_do_usuario(self, usuario):
        return self.adj_usuario.get(usuario, set())

    def usuarios_da_serie(self, serie):
        return self.adj_serie.get(serie, set())