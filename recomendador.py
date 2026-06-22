# Usa os dois grafos para gerar recomendações.

class Recomendador:

    def __init__(self, grafo_usuarios, grafo_series):

        self.grafo_u = grafo_usuarios
        self.grafo_s = grafo_series