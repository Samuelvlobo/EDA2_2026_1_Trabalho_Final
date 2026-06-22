import pandas as pd
import os

def gerar_dados():
    # Caminho absoluto para a pasta /data/
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(base_dir, 'data')
    
    # Cria o diretório se não existir
    os.makedirs(data_dir, exist_ok=True)
    
    print("Iniciando geração de dados...")

    # 1. Gerar utilizadores.csv
    utilizadores_data = {
        'id_utilizador': [1, 2, 3, 4, 5],
        'nome': ['Tiago', 'Sofia', 'Carlos', 'Mariana', 'Pedro']
    }
    df_utilizadores = pd.DataFrame(utilizadores_data)
    caminho_utilizadores = os.path.join(data_dir, 'utilizadores.csv')
    df_utilizadores.to_csv(caminho_utilizadores, index=False)
    print(f"Salvo: {caminho_utilizadores}")

    # 2. Gerar filmes.csv
    filmes_data = {
        'id_filme': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'titulo': [
            'Matrix', 'A Origem (Inception)', 'O Padrinho', 'Interestelar', 
            'Pulp Fiction', 'Clube da Luta', 'Forrest Gump', 
            'Blade Runner 2049', 'O Senhor dos Anéis', 'Vingadores'
        ],
        'sinopse': [
            'Um hacker descobre a verdade sobre a simulação que vive.',
            'Ladrão invade mentes para plantar ideias.',
            'História de uma das maiores famílias mafiosas de Nova York.',
            'Exploradores viajam pelo espaço para salvar a humanidade.',
            'Vidas cruzadas de assassinos e bandidos em Los Angeles.',
            'Clube secreto de luta para aliviar frustrações modernas.',
            'Um homem simples vivendo momentos históricos dos EUA.',
            'Um caçador de androides descobre um segredo perigoso.',
            'Jornada épica para destruir um anel mágico.',
            'Super-heróis se unem para salvar a Terra.'
        ],
        'popularidade': [95, 92, 98, 90, 88, 85, 94, 82, 97, 89]
    }
    df_filmes = pd.DataFrame(filmes_data)
    caminho_filmes = os.path.join(data_dir, 'filmes.csv')
    df_filmes.to_csv(caminho_filmes, index=False)
    print(f"Salvo: {caminho_filmes}")

    # 3. Gerar interacoes.csv
    # Padrão: Tiago e Sofia (Sci-Fi), Carlos e Mariana (Ação/Drama)
    interacoes_data = {
        'id_utilizador': [
            # Tiago (Sci-fi)
            1, 1, 1, 1,
            # Sofia (Sci-fi)
            2, 2, 2,
            # Carlos (Drama/Clássicos)
            3, 3, 3, 3,
            # Mariana (Drama/Clássicos)
            4, 4, 4,
            # Pedro (Tudo um pouco)
            5, 5, 5, 5
        ],
        'id_filme': [
            # Tiago
            101, 102, 104, 108,
            # Sofia
            101, 102, 104,
            # Carlos
            103, 105, 106, 107,
            # Mariana
            103, 105, 107,
            # Pedro
            101, 103, 109, 110
        ]
    }
    df_interacoes = pd.DataFrame(interacoes_data)
    caminho_interacoes = os.path.join(data_dir, 'interacoes.csv')
    df_interacoes.to_csv(caminho_interacoes, index=False)
    print(f"Salvo: {caminho_interacoes}")
    
    print("\nCSV gerados com sucesso na pasta /data/!")

if __name__ == "__main__":
    gerar_dados()
