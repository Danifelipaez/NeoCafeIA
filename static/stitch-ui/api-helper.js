/**
 * API Helper - Gestiona todas las peticiones al backend
 */
class APIHelper {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
        };
    }

    /**
     * Enviar pregunta al chat
     */
    async sendChatMessage(pregunta, provider = 'gemini', historial = []) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: this.defaultHeaders,
                body: JSON.stringify({
                    pregunta,
                    provider,
                    historial
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw new Error(`Error al enviar mensaje: ${error.message}`);
        }
    }

    /**
     * Obtener estado del servidor
     */
    async healthCheck() {
        try {
            const response = await fetch('/health');
            return response.ok;
        } catch {
            return false;
        }
    }

    /**
     * Obtener información del proyecto
     */
    async getProjectInfo() {
        try {
            const response = await fetch(`${this.baseURL}/info`);
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch {
            return null;
        }
    }

    /**
     * Obtener menú completo
     */
    async getMenu() {
        try {
            const response = await fetch(`${this.baseURL}/menu`);
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`HTTP ${response.status}`);
        } catch (error) {
            throw new Error(`Error al obtener menú: ${error.message}`);
        }
    }

    /**
     * Obtener recomendaciones personalizadas
     */
    async getRecommendations(preference = null) {
        try {
            const url = preference 
                ? `${this.baseURL}/recommendations?preference=${preference}`
                : `${this.baseURL}/recommendations`;
            
            const response = await fetch(url);
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`HTTP ${response.status}`);
        } catch (error) {
            throw new Error(`Error al obtener recomendaciones: ${error.message}`);
        }
    }

    /**
     * Obtener horarios de atención
     */
    async getHours() {
        try {
            const response = await fetch(`${this.baseURL}/horarios`);
            if (response.ok) {
                return await response.json();
            }
            throw new Error(`HTTP ${response.status}`);
        } catch (error) {
            throw new Error(`Error al obtener horarios: ${error.message}`);
        }
    }

/**
 * Data Manager - Gestiona almacenamiento local de datos
 */
class DataManager {
    constructor(storageKey = 'neocafeIA') {
        this.storageKey = storageKey;
    }

    /**
     * Guardar historial de chat
     */
    saveChatHistory(messages) {
        try {
            localStorage.setItem(`${this.storageKey}_history`, JSON.stringify(messages));
        } catch (e) {
            console.warn('No se pudo guardar historial:', e);
        }
    }

    /**
     * Cargar historial de chat
     */
    loadChatHistory() {
        try {
            const saved = localStorage.getItem(`${this.storageKey}_history`);
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            console.warn('No se pudo cargar historial:', e);
            return [];
        }
    }

    /**
     * Guardar preferencias del usuario
     */
    savePreferences(preferences) {
        try {
            localStorage.setItem(`${this.storageKey}_prefs`, JSON.stringify(preferences));
        } catch (e) {
            console.warn('No se pudo guardar preferencias:', e);
        }
    }

    /**
     * Cargar preferencias del usuario
     */
    loadPreferences() {
        try {
            const saved = localStorage.getItem(`${this.storageKey}_prefs`);
            return saved ? JSON.parse(saved) : { provider: 'gemini' };
        } catch (e) {
            console.warn('No se pudo cargar preferencias:', e);
            return { provider: 'gemini' };
        }
    }

    /**
     * Limpiar todos los datos
     */
    clearAll() {
        try {
            localStorage.removeItem(`${this.storageKey}_history`);
            localStorage.removeItem(`${this.storageKey}_prefs`);
        } catch (e) {
            console.warn('No se pudo limpiar datos:', e);
        }
    }
}

/**
 * Event Dispatcher - Gestor de eventos global
 */
class EventDispatcher {
    constructor() {
        this.listeners = {};
    }

    /**
     * Suscribirse a evento
     */
    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    /**
     * Desuscribirse de evento
     */
    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    }

    /**
     * Emit evento
     */
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }
}

// Instancias globales
window.api = new APIHelper();
window.dataManager = new DataManager();
window.eventDispatcher = new EventDispatcher();
