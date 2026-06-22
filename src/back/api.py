# ==============================================================================
# INSTRUÇÕES DE INSTALAÇÃO:
# 1. Certifique-se de que o ambiente virtual está ativado
# 2. Execute: pip install flask flask-cors pandas
# ==============================================================================

import os
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

# Importa as estruturas de dados criadas manualmente
from meu_heap import MaxHeap
from meu_grafo import GrafoBipartido

app = Flask(__name__)
# Habilita o CORS para permitir requisições do front-end local (index.html)
CORS(app)

# Instancia as estruturas globais
heap_populares = MaxHeap()
grafo_recomendacao = GrafoBipartido()

def carregar_dados():
    """
    Função chamada ao iniciar o servidor para ler os CSVs
    e popular as estruturas de dados na memória RAM.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(base_dir, 'data')
    
    print("Iniciando a carga de dados na memória...")

    # 1. LER E POPULAR FILMES NO HEAP E NO GRAFO
    caminho_filmes = os.path.join(data_dir, 'filmes.csv')
    if os.path.exists(caminho_filmes):
        df_filmes = pd.read_csv(caminho_filmes)
        for _, row in df_filmes.iterrows():
            id_filme = int(row['id_filme'])
            titulo = row['titulo']
            popularidade = int(row['popularidade'])
            
            # Adiciona o nó do filme no Grafo (Conjunto V)
            grafo_recomendacao.adicionar_filme(id_filme, titulo)
            
            # Insere no Max-Heap (a chave de ordenação no código do meu_heap.py é 'popularidade')
            heap_populares.inserir({
                'id': id_filme,
                'titulo': titulo,
                'popularidade': popularidade
            })
        print(f"-> {len(df_filmes)} Filmes carregados no Heap e no Grafo.")

    # 2. LER E POPULAR UTILIZADORES NO GRAFO
    caminho_utilizadores = os.path.join(data_dir, 'usuarios.csv')
    if os.path.exists(caminho_utilizadores):
        df_users = pd.read_csv(caminho_utilizadores)
        for _, row in df_users.iterrows():
            id_user = int(row['id_usuario'])
            nome = row['nome']
            
            # Adiciona o nó do utilizador no Grafo (Conjunto U)
            grafo_recomendacao.adicionar_utilizador(id_user, nome)
        print(f"-> {len(df_users)} Utilizadores carregados no Grafo.")

    # 3. LER E POPULAR INTERAÇÕES (ARESTAS) NO GRAFO
    caminho_interacoes = os.path.join(data_dir, 'interacoes.csv')
    if os.path.exists(caminho_interacoes):
        df_interacoes = pd.read_csv(caminho_interacoes)
        for _, row in df_interacoes.iterrows():
            id_user = int(row['id_usuario'])
            id_filme = int(row['id_filme'])
            
            # Cria a aresta não direcionada entre Utilizador e Filme
            grafo_recomendacao.adicionar_aresta(id_user, id_filme)
        print(f"-> {len(df_interacoes)} Interações (Arestas) carregadas no Grafo.")

    print("Carga de dados concluída com sucesso!\n")


@app.route('/api/populares', methods=['GET'])
def get_populares():
    """
    Retorna os top 5 filmes mais populares utilizando a nossa implementação de Max-Heap.
    """
    top_5 = []
    
    # Extrai (remove) os maiores da raiz um por um
    for _ in range(5):
        if heap_populares.tamanho() > 0:
            filme = heap_populares.extrair_max()
            if filme:
                top_5.append(filme)
                
    # Como extrair_max REMOVE os itens da árvore, precisamos reinseri-los
    # para que a próxima requisição também consiga vê-los
    for filme in top_5:
        heap_populares.inserir(filme)
        
    # Retorna o JSON para o frontend
    return jsonify({
        "status": "success",
        "data": top_5
    })

@app.route('/api/recomendacoes/<int:id_usuario>', methods=['GET'])
def get_recomendacoes(id_usuario):
    """
    Dada a identificação do utilizador, projeta o Grafo Bipartido
    para sugerir filmes baseados em filtragem colaborativa.
    """
    titulos_recomendados = grafo_recomendacao.recomendar_para_utilizador(id_usuario)
    
    # Prepara a formatação da resposta esperada pelo app.js (mock)
    # Transformando a lista de strings em lista de dicionários com id (simulado) e titulo
    recomendacoes_formatadas = []
    for idx, titulo in enumerate(titulos_recomendados):
        recomendacoes_formatadas.append({
            "id": 900 + idx,  # ID fictício só para não quebrar o frontend atual
            "title": titulo
        })
        
    return jsonify({
        "status": "success",
        "data": recomendacoes_formatadas
    })

@app.route('/api/historico/<int:id_usuario>', methods=['GET'])
def get_historico(id_usuario):
    """
    Retorna a lista de IDs de filmes que o utilizador já assistiu.
    """
    # adj_utilizadores é um dicionário: chave = ID do utilizador, valor = set() com IDs dos filmes
    filmes_assistidos = grafo_recomendacao.adj_utilizadores.get(id_usuario, set())
    return jsonify({
        "status": "success",
        "data": list(filmes_assistidos)
    })

@app.route('/api/assistir', methods=['POST'])
def post_assistir():
    """
    Regista que um utilizador assistiu a um filme.
    Atualiza o Grafo na memória e persiste no ficheiro interacoes.csv.
    """
    dados = request.get_json()
    if not dados or 'id_usuario' not in dados or 'id_filme' not in dados:
        return jsonify({"status": "error", "message": "Dados inválidos. Requer id_usuario e id_filme."}), 400
        
    id_usuario = int(dados['id_usuario'])
    id_filme = int(dados['id_filme'])
    
    # 1. Atualizar o Grafo na memória RAM
    grafo_recomendacao.adicionar_aresta(id_usuario, id_filme)
    
    # 2. Fazer o append no CSV para persistência
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    caminho_interacoes = os.path.join(base_dir, 'data', 'interacoes.csv')
    
    try:
        with open(caminho_interacoes, 'a', encoding='utf-8') as f:
            # A base do script gerador colocou o CSV com cabeçalho id_usuario,id_filme,assistiu
            # Então devemos manter 3 colunas se o CSV tiver 3 colunas, ou as 2 que o Python requer
            # O gerador anterior criou: 'id_usuario', 'id_filme', 'assistiu'
            f.write(f"{id_usuario},{id_filme},1\n")
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erro ao salvar: {str(e)}"}), 500
        
    return jsonify({
        "status": "success",
        "message": "Aresta adicionada e persistida com sucesso!"
    })


if __name__ == '__main__':
    # Antes de subir o servidor web, dispara a carga pesada dos CSVs para a memória RAM
    carregar_dados()
    
    # Sobe o servidor na porta padrão do Flask
    app.run(debug=True, port=5000)
