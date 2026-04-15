// Chat Service - Integración con API FastAPI
class ChatManager {
    constructor(apiEndpoint = '/api/chat') {
        this.apiEndpoint = apiEndpoint;
        this.messages = [];
        this.isLoading = false;
        this.provider = 'gemini'; // Provider por defecto
        this.loadPreferences();
    }

    /**
     * Cargar preferencias guardadas
     */
    loadPreferences() {
        const prefs = window.dataManager?.loadPreferences() || {};
        this.provider = prefs.provider || 'gemini';
    }

    /**
     * Guardar preferencias
     */
    savePreferences() {
        if (window.dataManager) {
            window.dataManager.savePreferences({ provider: this.provider });
        }
    }

    /**
     * Enviar mensaje al servidor
     */
    async sendMessage(userMessage) {
        if (!userMessage.trim()) return null;

        // Agregar mensaje del usuario al historial
        this.messages.push({
            role: 'user',
            content: userMessage
        });

        // Preparar formato de historial
        const history = this.messages.slice(0, -1).map(msg => ({
            role: msg.role,
            content: msg.content
        }));

        this.isLoading = true;

        try {
            const response = await window.api?.sendChatMessage(userMessage, this.provider, history) || 
                            await this._fallbackFetch(userMessage, history);

            // Agregar respuesta del asistente
            this.messages.push({
                role: 'assistant',
                content: response.respuesta
            });

            this.isLoading = false;
            
            // Emitir evento
            window.eventDispatcher?.emit('message-received', response);
            
            return response;
        } catch (error) {
            console.error('Error comunicándose con el servidor:', error);
            this.isLoading = false;
            throw error;
        }
    }

    /**
     * Fallback para fetch en caso de que api no esté disponible
     */
    async _fallbackFetch(userMessage, history) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pregunta: userMessage,
                provider: this.provider,
                historial: history
            })
        });

        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return await response.json();
    }

    /**
     * Obtener historial formateado
     */
    getHistory() {
        return this.messages;
    }

    /**
     * Limpiar historial
     */
    clearHistory() {
        this.messages = [];
        if (window.dataManager) {
            window.dataManager.clearAll();
        }
    }

    /**
     * Obtener último mensaje
     */
    getLastMessage() {
        return this.messages[this.messages.length - 1];
    }

    /**
     * Cambiar provider
     */
    setProvider(provider) {
        this.provider = provider;
        this.savePreferences();
        window.eventDispatcher?.emit('provider-changed', { provider });
    }
}

// UI Manager para Chat Desktop
class ChatUIManager {
    constructor(options = {}) {
        this.containerId = options.containerId || 'chat-container';
        this.inputId = options.inputId || 'chat-input';
        this.sendBtnId = options.sendBtnId || 'chat-send';
        
        this.container = document.getElementById(this.containerId);
        this.input = document.getElementById(this.inputId);
        this.sendBtn = document.getElementById(this.sendBtnId);
        this.chatManager = new ChatManager('/api/chat');
        
        this.setupEventListeners();
        this.loadChatHistory();
        this.setupGlobalListeners();
    }

    setupEventListeners() {
        // Enviar mensaje con botón
        if (this.sendBtn) {
            this.sendBtn.addEventListener('click', () => this.handleSendMessage());
        }
        
        // Enviar mensaje con Enter
        if (this.input) {
            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSendMessage();
                }
            });
        }

        // Botones de sugerencias
        document.querySelectorAll('[data-suggestion]').forEach(btn => {
            btn.addEventListener('click', () => {
                const suggestion = btn.getAttribute('data-suggestion');
                if (this.input) {
                    this.input.value = suggestion;
                    this.handleSendMessage();
                }
            });
        });

        // Selector de provider
        document.querySelectorAll('[data-provider]').forEach(btn => {
            btn.addEventListener('click', () => {
                const provider = btn.getAttribute('data-provider');
                this.chatManager.setProvider(provider);
                
                // Actualizar UI
                document.querySelectorAll('[data-provider]').forEach(b => {
                    b.classList.remove('active', 'bg-primary', 'text-on-primary');
                    b.classList.add('bg-surface-container-lowest', 'text-on-surface');
                });
                btn.classList.add('bg-primary', 'text-on-primary');
                btn.classList.remove('bg-surface-container-lowest', 'text-on-surface');
            });
        });
    }

    /**
     * Setup de listeners globales para eventos
     */
    setupGlobalListeners() {
        if (window.eventDispatcher) {
            window.eventDispatcher.on('message-received', (data) => {
                this.scrollToBottom();
            });
        }
    }

    async handleSendMessage() {
        const message = this.input.value.trim();
        if (!message || this.chatManager.isLoading) return;

        // Limpiar input
        this.input.value = '';
        if (this.input) this.input.focus();

        // Mostrar mensaje del usuario
        this.appendMessage(message, 'user');

        // Mostrar indicador de carga
        const loadingId = this.appendMessage('Pensando...', 'assistant', true);

        try {
            const response = await this.chatManager.sendMessage(message);
            
            // Reemplazar mensaje de carga con respuesta real
            const loadingElement = document.getElementById(loadingId);
            if (loadingElement) {
                loadingElement.innerHTML = this.formatResponse(response.respuesta);
            }

            // Guardar historial
            this.saveChatHistory();

            // Scroll a último mensaje
            this.scrollToBottom();
        } catch (error) {
            console.error('Error:', error);
            const loadingElement = document.getElementById(loadingId);
            if (loadingElement) {
                loadingElement.innerHTML = '<strong>Error:</strong> No se pudo obtener respuesta del servidor. Por favor, intenta de nuevo.';
                loadingElement.parentElement.classList.add('opacity-70');
            }
        }
    }

    appendMessage(content, role, isLoading = false) {
        const messageId = `msg-${Date.now()}-${Math.random()}`;
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex flex-col items-${role === 'user' ? 'end' : 'start'} max-w-[85%]`;
        messageDiv.id = messageId;

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = role === 'user' 
            ? 'bg-secondary text-on-secondary p-6 rounded-lg rounded-tr-none shadow-sm'
            : 'bg-surface-container-low border border-outline-variant/15 p-6 rounded-lg rounded-tl-none shadow-sm';
        
        bubbleDiv.innerHTML = isLoading 
            ? `<p class="font-body animate-pulse">${content}</p>`
            : `<p class="font-body text-base leading-relaxed">${content}</p>`;

        messageDiv.appendChild(bubbleDiv);

        const labelSpan = document.createElement('span');
        labelSpan.className = 'font-label text-[9px] uppercase tracking-widest text-stone-400 mt-2 ' + 
                            (role === 'user' ? 'ml-auto mr-1' : 'ml-1');
        labelSpan.textContent = role === 'user' ? 'Tú' : 'Asistente Virtual';

        messageDiv.appendChild(labelSpan);
        
        if (this.container) {
            this.container.appendChild(messageDiv);
        }

        return messageId;
    }

    formatResponse(text) {
        // Escapar HTML
        let formatted = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');

        // Convertir URLs a links
        formatted = formatted.replace(
            /https?:\/\/[^\s]+/g,
            url => `<a href="${url}" target="_blank" class="text-primary underline hover:opacity-80">${url}</a>`
        );

        // Negritas **texto**
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Cursivas *texto*
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // Preservar saltos de línea
        formatted = formatted.replace(/\n/g, '<br/>');

        return formatted;
    }

    scrollToBottom() {
        if (this.container) {
            // Usar requestAnimationFrame para asegurar que el DOM esté completamente renderizado
            requestAnimationFrame(() => {
                this.container.scrollTop = this.container.scrollHeight;
            });
        }
    }

    saveChatHistory() {
        const history = this.chatManager.getHistory();
        if (window.dataManager) {
            window.dataManager.saveChatHistory(history);
        }
    }

    loadChatHistory() {
        if (window.dataManager) {
            const saved = window.dataManager.loadChatHistory();
            if (saved.length > 0) {
                this.chatManager.messages = saved;
                saved.forEach(msg => {
                    this.appendMessage(msg.content, msg.role, false);
                });
                this.scrollToBottom();
            }
        }
    }

    clearChat() {
        if (this.container) {
            this.container.innerHTML = '';
        }
        this.chatManager.clearHistory();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.querySelector('[data-chat-container]');
    if (chatContainer) {
        window.chatUI = new ChatUIManager({
            containerId: 'chat-container',
            inputId: 'chat-input',
            sendBtnId: 'chat-send'
        });
    }
});
