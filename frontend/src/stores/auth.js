import { defineStore } from 'pinia';
import api from '../api/axios';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
    // State: Zustand der Anwendung
    const user = ref(null);
    const token = ref(localStorage.getItem('token') || null);
    const router = useRouter();

    // Getters: Berechnete Eigenschaften 
    const isAuthenticated = computed(() => !!token.value);

    // Actions: Methoden zum Ändern des Zustands 
    
    // 1. Login-Funktion 
    const login = async (email, password) => {
        try {
            // Anfrage an das Backend senden (form-urlencoded für OAuth2)
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await api.post('/token', formData);
            
            // Token speichern
            token.value = response.data.access_token;
            localStorage.setItem('token', token.value);
            
            // Benutzerdaten abrufen (nach erfolgreichem Login)
            await fetchUser();
            
            // Weiterleitung zum Dashboard
            router.push('/dashboard');
            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            return { success: false, error: error.response?.data?.detail || 'Login fehlgeschlagen' };
        }
    };

    // 2. Benutzerdaten abrufen 
    const fetchUser = async () => {
        if (!token.value) return;
        try {
            const response = await api.get('/users/me');
            user.value = response.data;
        } catch (error) {
            console.error('Fetch user error:', error);
            logout(); // Wenn Token ungültig, ausloggen
        }
    };

    // 3. Logout-Funktion 
    const logout = () => {
        user.value = null;
        token.value = null;
        localStorage.removeItem('token');
        router.push('/login');
    };

    return { user, token, isAuthenticated, login, fetchUser, logout };
});
