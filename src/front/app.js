document.addEventListener('DOMContentLoaded', () => {
    // --- URLs da API Flask ---
    const API_BASE_URL = 'http://127.0.0.1:5000/api';

    // --- State ---
    let currentUser = null;
    let popularesData = [];
    let userHistory = [];

    // --- DOM Elements ---
    const loginContainer = document.getElementById('login-container');
    const userInfo = document.getElementById('user-info');
    const userIdInput = document.getElementById('user-id');
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const welcomeMessage = document.getElementById('welcome-message');
    
    const rowPopular = document.getElementById('row-popular');
    
    const sectionConnected = document.getElementById('section-connected');
    const rowConnected = document.getElementById('row-connected');
    const instructionMsg = document.getElementById('instruction-msg');

    // --- Render Functions ---
    function renderCards(container, data, isLoggedIn = false) {
        container.innerHTML = '';
        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card';
            
            const idFilme = item.id_filme || item.id;
            
            const titleSpan = document.createElement('span');
            titleSpan.textContent = item.titulo || item.title;
            card.appendChild(titleSpan);
            
            if (isLoggedIn) {
                const btn = document.createElement('button');
                btn.className = 'btn-assisti';
                
                if (userHistory.includes(idFilme)) {
                    btn.textContent = 'Assistido';
                    btn.disabled = true;
                    btn.classList.add('disabled-btn');
                } else {
                    btn.textContent = '✔️ Já Assisti';
                    btn.addEventListener('click', async (e) => {
                        e.stopPropagation();
                        await handleAssistir(btn, idFilme);
                    });
                }
                card.appendChild(btn);
            }
            
            container.appendChild(card);
        });
    }

    // --- API Calls ---
    async function carregarPopulares() {
        try {
            const response = await fetch(`${API_BASE_URL}/populares`);
            if (!response.ok) throw new Error('Erro ao buscar filmes populares');
            
            const json = await response.json();
            popularesData = json.data;
            
            // Renderiza na tela sem interatividade (pois o utilizador ainda não fez login)
            renderCards(rowPopular, popularesData, false);
        } catch (error) {
            console.error('Falha na API (Populares):', error);
            rowPopular.innerHTML = '<p class="info-msg" style="color: red;">Erro ao carregar os filmes. O servidor Flask está a correr?</p>';
        }
    }

    async function buscarRecomendacoes() {
        if (!currentUser) return;
        
        try {
            // Remove a mensagem de instrução
            instructionMsg.style.display = 'none';
            // Mostra mensagem de carregamento (opcional, mas bom para UX)
            rowConnected.innerHTML = '<p class="info-msg">O Grafo está a calcular as afinidades...</p>';

            const response = await fetch(`${API_BASE_URL}/recomendacoes/${currentUser}`);
            if (!response.ok) throw new Error('Erro ao buscar recomendações do Grafo Bipartido');
            
            const json = await response.json();
            const recomendacoesData = json.data;
            
            if (recomendacoesData.length === 0) {
                // Caso de Cold Start (Utilizador sem arestas no grafo)
                instructionMsg.textContent = "Não encontramos interações suficientes! Clique num filme popular acima para vermos o que os utilizadores com gostos parecidos estão a assistir!";
                instructionMsg.style.display = 'block';
                rowConnected.innerHTML = '';
                rowConnected.appendChild(instructionMsg);
            } else {
                // Renderiza os filmes recomendados com sucesso
                renderCards(rowConnected, recomendacoesData, false);
            }
            
        } catch (error) {
            console.error('Falha na API (Recomendações):', error);
            rowConnected.innerHTML = '<p class="info-msg" style="color: red;">Erro ao contactar o servidor.</p>';
        }
    }

    async function carregarHistorico(userId) {
        try {
            const response = await fetch(`${API_BASE_URL}/historico/${userId}`);
            if (response.ok) {
                const json = await response.json();
                userHistory = json.data || [];
            }
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }

    // --- Handlers ---
    async function handleLogin() {
        const userId = userIdInput.value.trim();
        if (userId) {
            currentUser = parseInt(userId);
            
            // Busca o histórico antes de renderizar
            await carregarHistorico(currentUser);
            
            loginContainer.classList.add('hidden');
            welcomeMessage.textContent = `Logado como Utilizador ${currentUser}`;
            userInfo.classList.remove('hidden');
            
            // Mostra a fileira 2 (Conectados)
            sectionConnected.classList.remove('hidden');

            // Torna a fileira 1 interativa (mostra os botões)
            renderCards(rowPopular, popularesData, true);
            
            // Busca as recomendações iniciais se existirem interações
            buscarRecomendacoes();
        }
    }

    function handleLogout() {
        currentUser = null;
        userHistory = [];
        userIdInput.value = '';
        
        userInfo.classList.add('hidden');
        loginContainer.classList.remove('hidden');
        
        // Esconde a fileira 2
        sectionConnected.classList.add('hidden');

        // Volta a mostrar o texto de instrução original
        instructionMsg.textContent = "Clique em algum filme popular acima para vermos o que os usuários com gosto parecido estão assistindo.";
        instructionMsg.style.display = 'block';
        rowConnected.innerHTML = '';
        rowConnected.appendChild(instructionMsg);

        // Tira interatividade da fileira 1
        renderCards(rowPopular, popularesData, false);
    }

    async function handleAssistir(btn, idFilme) {
        if (!currentUser) return;

        // Atualização Otimista no UI
        btn.textContent = 'Assistido';
        btn.disabled = true;
        btn.classList.add('disabled-btn');
        userHistory.push(idFilme);
        
        try {
            const response = await fetch(`${API_BASE_URL}/assistir`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id_usuario: currentUser, id_filme: idFilme })
            });
            
            if (response.ok) {
                // Atualiza a fileira de populares para espelhar o botão cinzento nela também (caso estivesse lá)
                renderCards(rowPopular, popularesData, true);
                
                // Recalcula o Grafo Bipartido e atualiza recomendações
                buscarRecomendacoes();
            }
        } catch (error) {
            console.error('Erro ao registar interação:', error);
        }
    }

    // --- Init ---
    // Assim que a página carrega, vai buscar os dados ao Heap
    carregarPopulares();

    // Events
    loginBtn.addEventListener('click', handleLogin);
    userIdInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLogin();
    });
    logoutBtn.addEventListener('click', handleLogout);
});
