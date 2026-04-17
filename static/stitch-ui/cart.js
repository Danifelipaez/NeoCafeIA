class CartManager {
    constructor(storageKey = 'neocafeIA_cart') {
        this.storageKey = storageKey;
        this.items = [];
        this.load();
    }

    normalizeItem(item) {
        return {
            id: String(item.id || item.name || Date.now()),
            name: String(item.name || 'Producto'),
            price: Number(item.price || 0),
            quantity: Math.max(1, Number(item.quantity || 1)),
            category: String(item.category || 'General')
        };
    }

    addItem(item) {
        const normalized = this.normalizeItem(item);
        const existing = this.items.find((entry) => entry.id === normalized.id);

        if (existing) {
            existing.quantity += normalized.quantity;
        } else {
            this.items.push(normalized);
        }

        this.save();
        this.emit('cart-item-added', { item: normalized, items: this.items });
        this.emitUpdated();
    }

    removeItem(id) {
        this.items = this.items.filter((item) => item.id !== String(id));
        this.save();
        this.emitUpdated();
    }

    updateQuantity(id, qty) {
        const parsedQty = Number(qty);
        const item = this.items.find((entry) => entry.id === String(id));

        if (!item) {
            return;
        }

        if (parsedQty <= 0 || Number.isNaN(parsedQty)) {
            this.removeItem(id);
            return;
        }

        item.quantity = parsedQty;
        this.save();
        this.emitUpdated();
    }

    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    getCount() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    }

    clear() {
        this.items = [];
        this.save();
        this.emit('cart-cleared', { items: [] });
        this.emitUpdated();
    }

    save() {
        const payload = {
            items: this.items,
            updatedAt: new Date().toISOString()
        };

        try {
            if (window.dataManager && window.dataManager.storageKey) {
                localStorage.setItem(this.storageKey, JSON.stringify(payload));
            } else {
                localStorage.setItem(this.storageKey, JSON.stringify(payload));
            }
        } catch (error) {
            console.warn('No se pudo guardar carrito:', error);
        }
    }

    load() {
        try {
            const raw = localStorage.getItem(this.storageKey);
            if (!raw) {
                this.items = [];
                return;
            }

            const parsed = JSON.parse(raw);
            this.items = Array.isArray(parsed.items)
                ? parsed.items.map((item) => this.normalizeItem(item))
                : [];
        } catch (error) {
            console.warn('No se pudo cargar carrito:', error);
            this.items = [];
        }
    }

    emit(eventName, data) {
        if (window.eventDispatcher && typeof window.eventDispatcher.emit === 'function') {
            window.eventDispatcher.emit(eventName, data);
        }
    }

    emitUpdated() {
        this.emit('cart-updated', {
            items: this.items,
            total: this.getTotal(),
            count: this.getCount()
        });
    }
}

window.cartManager = window.cartManager || new CartManager();
