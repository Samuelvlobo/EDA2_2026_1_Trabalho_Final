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
   source venv/bin/activate
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
   *(Nota: O NLTK precisa dos pacotes básicos de PLN. Se for a primeira vez, execute: `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')" `)*

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