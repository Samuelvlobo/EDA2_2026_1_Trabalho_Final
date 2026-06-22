# Lê os CSVs e monta os grafos.

import csv

from grafo_bipartido import GrafoBipartido
from grafo_series import GrafoSeries

def carregar_interacoes(caminho):

    grafo = GrafoBipartido()

    with open(caminho, encoding="utf-8") as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:

            usuario = linha["usuario"]
            serie = linha["titulo"]

            grafo.adicionar_interacao(
                usuario,
                serie,
            )

    return grafo

def carregar_series(caminho):

    grafo = GrafoSeries()

    with open(caminho, encoding="utf-8") as arquivo:

        leitor = csv.DictReader(arquivo)

        for linha in leitor:

            grafo.adicionar_serie(
                linha["serie"],
                linha["palavras_chave"]
            )

    grafo.construir_similaridades()

    return grafo