import axios from 'axios';

// API-Instanz erstellen
const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1', // Basis-URL des Backends
});

// Request-Interceptor: Token hinzufügen 
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response-Interceptor: Fehlerbehandlung 
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Wenn 401 (Unauthorized), Token löschen und zum Login leiten
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
