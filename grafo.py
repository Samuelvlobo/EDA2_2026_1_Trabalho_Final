from collections import namedtuple

Grafo = namedtuple("Grafo", ["nodes", "arestas", "id_direcao"])


def __init__(self, direcionado=False):
    self.direcionado = direcionado


def matriz(grafo):
    matriz_adj = [[0 for node in grafo.nodes] for node in grafo.nodes]
    for aresta in grafo.arestas:
        node1, node2 = aresta[0], aresta[1]
        matriz_adj[node1][node2] += 1
        if not grafo.id_direcao:
            matriz_adj[node2][node1] += 1
    return matriz_adj
