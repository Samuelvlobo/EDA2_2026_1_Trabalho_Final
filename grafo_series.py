# Representa a similaridade entre séries usando palavras-chave.
# Armazena palavras-chave
# Calcula similaridade
# Constrói arestas entre séries semelhantes

class GrafoSeries:

    def __init__(self):
        self.tags = {}
        self.adj = {}

    def adicionar_serie(self, nome, palavras_chave):

        tags = {
            tag.strip().lower()
            for tag in palavras_chave.split(";")
        }

        self.tags[nome] = tags
        self.adj[nome] = {}

    def similaridade_jaccard(self, serie1, serie2):

        a = self.tags[serie1]
        b = self.tags[serie2]

        intersecao = len(a & b)
        uniao = len(a | b)

        if uniao == 0:
            return 0

        return intersecao / uniao
    
    def construir_similaridades(self):

        series = list(self.tags.keys())

        for i in range(len(series)):

            for j in range(i + 1, len(series)):

                s1 = series[i]
                s2 = series[j]

                peso = self.similaridade_jaccard(s1, s2)

                if peso > 0:

                    self.adj[s1][s2] = peso
                    self.adj[s2][s1] = peso

def vizinhos(self, serie):

    return self.adj.get(serie, {})

def mostrar_grafo(self):

    for serie, vizinhos in self.adj.items():

        print(f"\n{serie}")

        for vizinho, peso in vizinhos.items():
            print(f"  -> {vizinho}: {peso:.2f}")