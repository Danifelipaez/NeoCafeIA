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

    async healthCheck() {
        try {
            const response = await fetch('/health');
            return response.ok;
        } catch {
            return false;
        }
    }

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

    async getRecommendations(preference = null) {
        try {
            const url = preference
                ? `${this.baseURL}/recommendations?preference=${encodeURIComponent(preference)}`
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

    async createOrder(orderPayload) {
        try {
            const response = await fetch(`${this.baseURL}/orders`, {
                method: 'POST',
                headers: this.defaultHeaders,
                body: JSON.stringify(orderPayload)
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw new Error(`Error al crear pedido: ${error.message}`);
        }
    }
}

/**
 * Data Manager - Gestiona almacenamiento local de datos
 */
class DataManager {
    constructor(storageKey = 'neocafeIA') {
        this.storageKey = storageKey;
    }

    saveChatHistory(messages) {
        try {
            localStorage.setItem(`${this.storageKey}_history`, JSON.stringify(messages));
        } catch (e) {
            console.warn('No se pudo guardar historial:', e);
        }
    }

    loadChatHistory() {
        try {
            const saved = localStorage.getItem(`${this.storageKey}_history`);
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            console.warn('No se pudo cargar historial:', e);
            return [];
        }
    }

    savePreferences(preferences) {
        try {
            localStorage.setItem(`${this.storageKey}_prefs`, JSON.stringify(preferences));
        } catch (e) {
            console.warn('No se pudo guardar preferencias:', e);
        }
    }

    loadPreferences() {
        try {
            const saved = localStorage.getItem(`${this.storageKey}_prefs`);
            return saved ? JSON.parse(saved) : { provider: 'gemini' };
        } catch (e) {
            console.warn('No se pudo cargar preferencias:', e);
            return { provider: 'gemini' };
        }
    }

    setValue(key, value) {
        try {
            localStorage.setItem(`${this.storageKey}_${key}`, JSON.stringify(value));
        } catch (e) {
            console.warn(`No se pudo guardar ${key}:`, e);
        }
    }

    getValue(key, fallback = null) {
        try {
            const raw = localStorage.getItem(`${this.storageKey}_${key}`);
            return raw ? JSON.parse(raw) : fallback;
        } catch (e) {
            console.warn(`No se pudo cargar ${key}:`, e);
            return fallback;
        }
    }

    removeValue(key) {
        try {
            localStorage.removeItem(`${this.storageKey}_${key}`);
        } catch (e) {
            console.warn(`No se pudo eliminar ${key}:`, e);
        }
    }

    clearAll() {
        try {
            localStorage.removeItem(`${this.storageKey}_history`);
            localStorage.removeItem(`${this.storageKey}_prefs`);
            localStorage.removeItem('neocafeIA_cart');
            localStorage.removeItem(`${this.storageKey}_last_order`);
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

    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter((cb) => cb !== callback);
        }
    }

    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach((callback) => callback(data));
        }
    }
}

window.api = new APIHelper();
window.dataManager = new DataManager();
window.eventDispatcher = new EventDispatcher();
