# Representa o relacionamento entre usuários e séries.
# Adiciona usuários
# Adiciona séries
# Adiciona interações
# Consulta séries de um usuário
# Consulta usuários de uma série

class GrafoBipartido:

    def __init__(self):
        self.usuarios = set()
        self.series = set()

        # usuario -> {serie: peso}
        self.adj_usuario = {}

        # serie -> {usuario: peso}
        self.adj_serie = {}

    def adicionar_usuario(self, usuario):
        if usuario not in self.usuarios:
            self.usuarios.add(usuario)
            self.adj_usuario[usuario] = {}

    def adicionar_serie(self, serie):
        if serie not in self.series:
            self.series.add(serie)
            self.adj_serie[serie] = {}

    def adicionar_interacao(self, usuario, serie, peso):

        self.adicionar_usuario(usuario)
        self.adicionar_serie(serie)

        self.adj_usuario[usuario][serie] = peso
        self.adj_serie[serie][usuario] = peso

    def series_do_usuario(self, usuario):
        return self.adj_usuario.get(usuario, {})

    def usuarios_da_serie(self, serie):
        return self.adj_serie.get(serie, {})