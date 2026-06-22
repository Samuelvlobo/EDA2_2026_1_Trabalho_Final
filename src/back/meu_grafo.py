"""
Módulo Didático: Implementação de Grafo Bipartido
Criado para fins educacionais - Disciplina de Estruturas de Dados 2

Este grafo separa logicamente utilizadores e filmes e é armazenado
por meio de Lista de Adjacência utilizando dicionários do Python.
"""

class GrafoBipartido:
    def __init__(self):
        # Listas de adjacência separadas para clareza didática.
        # adj_utilizadores[id_user] = set(id_filmes_assistidos)
        self.adj_utilizadores = {}
        
        # adj_filmes[id_filme] = set(id_users_que_assistiram)
        self.adj_filmes = {}
        
        # Armazenamento de metadados para facilitar buscas nominais (O(1))
        self.meta_utilizadores = {}
        self.meta_filmes = {}

    def adicionar_utilizador(self, id_utilizador, nome):
        """Adiciona um nó no conjunto U (Utilizadores). Complexidade: O(1)."""
        if id_utilizador not in self.adj_utilizadores:
            self.adj_utilizadores[id_utilizador] = set()
            self.meta_utilizadores[id_utilizador] = nome

    def adicionar_filme(self, id_filme, titulo):
        """Adiciona um nó no conjunto V (Filmes). Complexidade: O(1)."""
        if id_filme not in self.adj_filmes:
            self.adj_filmes[id_filme] = set()
            self.meta_filmes[id_filme] = titulo

    def adicionar_aresta(self, id_utilizador, id_filme):
        """
        Cria uma ligação não-direcionada entre Utilizador e Filme.
        Como é implementado com Sets, a inserção não duplica arestas.
        Complexidade: O(1) médio.
        """
        # Garante que os nós existam no grafo antes de criar a aresta
        if id_utilizador not in self.adj_utilizadores:
            self.adicionar_utilizador(id_utilizador, f"Utilizador {id_utilizador}")
        if id_filme not in self.adj_filmes:
            self.adicionar_filme(id_filme, f"Filme {id_filme}")

        self.adj_utilizadores[id_utilizador].add(id_filme)
        self.adj_filmes[id_filme].add(id_utilizador)

    def recomendar_para_utilizador(self, id_utilizador):
        """
        Projeção de Grafo Bipartido (Filtragem Colaborativa).
        Descobre utilizadores com gostos similares para inferir filmes.
        
        Complexidade: O(F * U * f), onde:
        F = filmes assistidos pelo alvo
        U = utilizadores que também assistiram F
        f = filmes que esses utilizadores U assistiram
        """
        if id_utilizador not in self.adj_utilizadores:
            return [] # Utilizador inexistente

        filmes_assistidos_pelo_alvo = self.adj_utilizadores[id_utilizador]
        
        if not filmes_assistidos_pelo_alvo:
            # Caso de "Cold Start": O utilizador ainda não interagiu com o sistema
            return []

        # Dicionário para contar a frequência de recomendações (Grau da aresta virtual na projeção)
        frequencia_recomendacao = {}

        # 1. Para cada filme que o alvo assistiu
        for id_filme_assistido in filmes_assistidos_pelo_alvo:
            
            # 2. Descobre quem mais assistiu a esse mesmo filme (Nós adjacentes no grafo)
            vizinhos_similares = self.adj_filmes[id_filme_assistido]
            
            for id_vizinho in vizinhos_similares:
                # Evita que o algoritmo se auto-recomende
                if id_vizinho == id_utilizador:
                    continue
                
                # 3. Para cada vizinho similar, analisa quais filmes ELE assistiu
                filmes_do_vizinho = self.adj_utilizadores[id_vizinho]
                
                for filme_sugestao in filmes_do_vizinho:
                    # Só recomenda filmes que o alvo AINDA NÃO ASSISTIU
                    if filme_sugestao not in filmes_assistidos_pelo_alvo:
                        if filme_sugestao in frequencia_recomendacao:
                            frequencia_recomendacao[filme_sugestao] += 1
                        else:
                            frequencia_recomendacao[filme_sugestao] = 1

        # Transforma o dicionário num formato de lista de tuplas para poder ordenar
        # formato: [(id_filme, score_frequencia), ...]
        sugestoes_ordenadas = sorted(
            frequencia_recomendacao.items(), 
            key=lambda x: x[1], # Ordena pelo valor da contagem (score)
            reverse=True        # Ordem decrescente (mais recomendados primeiro)
        )

        # Seleciona os Top 3 melhores IDs de filmes
        top_3_ids = [sugestao[0] for sugestao in sugestoes_ordenadas[:3]]
        
        # Converte os IDs nos nomes descritivos para melhor visualização (Retorna os Títulos)
        top_3_titulos = [self.meta_filmes.get(f_id, f"Desconhecido ({f_id})") for f_id in top_3_ids]

        return top_3_titulos
