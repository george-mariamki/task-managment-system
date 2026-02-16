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
            // Nutzung von URLSearchParams für application/x-www-form-urlencoded Format
            // Dies ist zwingend erforderlich für OAuth2PasswordRequestForm im Backend
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);

            // Anfrage senden
            const response = await api.post('/login/access-token', params);    

            // Token speichern
            token.value = response.data.access_token;
            localStorage.setItem('token', token.value);
            
            // Benutzerprofil laden
            await fetchUser();
            
            // Weiterleitung zum Dashboard
            router.push('/dashboard');
            
            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            return { 
                success: false, 
                error: error.response?.data?.detail || 'Anmeldung fehlgeschlagen' 
            };
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
