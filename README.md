# Sistema de Recomendação Baseado em Grafos Bipartidos

Este projeto consiste em um Sistema de Recomendação de Textos desenvolvido para a disciplina de Estruturas de Dados 2. O sistema utiliza um grafo bipartido (Usuários-Textos) e projeção de grafos para sugerir novos conteúdos relevantes.

## 📋 Domínio Escolhido
* **Área de Aplicação:** [Definir Ex: Recomendação de Artigos Médicos / Notícias de Esporte]
* **Objetivo:** Resolver o problema de [Ex: sobrecarga de informação para pesquisadores médicos].

## 🛠️ Tecnologias e Estruturas de Dados
* **Linguagem:** [Python / C++ / C]
* **Estruturas Principais:** Grafo Bipartido (Implementação Própria) e [Tabela Hash / Árvore Binária - Escolher uma].

## 👥 Integrantes do Grupo
* Integrante 1 - GitHub: @username1 (Contribuição: ...)
* Integrante 2 - GitHub: @username2 (Contribuição: ...)
* Integrante 3 - GitHub: @username3 (Contribuição: ...)

## ⚙️ Como executar o projeto localmente

Para testar este MVP na sua máquina, siga os passos exatos abaixo:

1. **Ativar o ambiente virtual**:
   - No **Linux/Mac**:
   ```bash
   python -m venv venv/bin/activate
   ```
   - No **Windows**:
   ```bash
   venv\Scripts\activate
   ```

2. **Instalar dependências**:
   Com o ambiente ativado, instale os pacotes (Flask, Pandas, Rake-NLTK):
   ```bash
   pip install -r requirements.txt
   ```
   *Nota 1: talvez seja necessário fazer um override do pip, porque pode ser que o gerenciador de pacotes exija a instalação dos requisitos por ele ao invés do gerenciador pip. Basta executar: `pip install -r requirements.txt --break-system-packages`*
   *Nota 2: O NLTK precisa dos pacotes básicos de PLN. Se for a primeira vez, execute: `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')" `*

3. **Iniciar o servidor (Back-end)**:
   Inicie a nossa API REST em Flask que vai carregar o Grafo e o Heap para a memória RAM:
   ```bash
   python src/back/api.py
   ```
   *Deixe este terminal aberto.*

4. **Abrir a Interface (Front-end)**:
   Como não usamos frameworks de Front-end, não precisamos de NPM. Basta abrir o ficheiro diretamente no seu navegador padrão (ou usar uma extensão como o Live Server):
   ```bash
   # No Linux, basta rodar noutro terminal:
   xdg-open src/front/index.html
   ```
5. **Criar um usuário**
   Basta designar um número de ID ao usuário e escolher os filmes que o usuário já assistiu. Desta forma, os filmes mais similares ao gosto do usuário aparecerão primeiro. Os usuários de 0 a 50 já tem gostos definidos. Para adicionar um usuário sem gosto pré-definido, basta designar um ID de número maior que 50 no arquivo "usuarios.csv" localizado na pasta "data".
