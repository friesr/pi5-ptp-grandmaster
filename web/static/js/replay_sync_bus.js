const ReplaySyncBus = {
    listeners: [],

    subscribe(fn) {
        this.listeners.push(fn);
    },

    emit(timestamp) {
        this.listeners.forEach(fn => fn(timestamp));
    }
};
