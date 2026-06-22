# Usa os dois grafos para gerar recomendações.

class Recomendador:

    def __init__(self, grafo_usuarios, grafo_series):
        self.grafo_u = grafo_usuarios
        self.grafo_s = grafo_series

    # Recomenda as séries que compartilham mais palavras-chave com a maior quantidade de outras séries
    def recomendar_mais_conectadas(self, top_n=10):
        pontuacoes = {}
        # Para cada série, soma o peso das arestas de cada vértice adjacente
        for serie, vizinhos in self.grafo_s.adj.items():
            pontuacoes[serie] = sum(vizinhos.values())
            
        # Ordena as séries em ordem decrescente (reverse = True)
        # O 'key=lambda x: x[1]' é para indicar que as séries devem ser ordenadas pela pontuação
        series_ordenadas = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
        return series_ordenadas[:top_n]

    def recomendar_para_usuario(self, usuario, top_n=10):
        assistidas = self.grafo_u.series_do_usuario(usuario)
        # Caso o usuário não tenha nenhuma série assistida, irá retornar um dicionário vazio
        if not assistidas:
            return []
            
        candidatas = {}
        
        # Para cada série assistida pelo usuário, calcula a similaridade com outras séries existentes
        for serie_assistida in assistidas:
            
            similares = self.grafo_s.adj.get(serie_assistida, {})
            
            for serie_similar, similaridade in similares.items():
                
                # Pula as que ele já viu
                if serie_similar in assistidas:
                    continue
                
                if serie_similar not in candidatas:
                    candidatas[serie_similar] = 0
                
                # Apenas soma a similaridade de Jaccard vinda do GrafoSeries
                candidatas[serie_similar] += similaridade
                
        recomendacoes = sorted(candidatas.items(), key=lambda x: x[1], reverse=True)
        return recomendacoes[:top_n]