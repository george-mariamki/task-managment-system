<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Anmelden</h2>
      
      <!-- Fehlermeldung anzeigen -->
      <div v-if="errorMessage" class="mb-4 rounded bg-red-100 p-3 text-red-700">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin">
        <!-- E-Mail Feld -->
        <div class="mb-4">
          <label class="mb-2 block text-sm font-bold text-gray-700" for="email">
            E-Mail Adresse
          </label>
          <input
            v-model="email"
            class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
            id="email"
            type="email"
            placeholder="E-Mail eingeben"
            required
          />
        </div>

        <!-- Passwort Feld -->
        <div class="mb-6">
          <label class="mb-2 block text-sm font-bold text-gray-700" for="password">
            Passwort
          </label>
          <input
            v-model="password"
            class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
            id="password"
            type="password"
            placeholder="******************"
            required
          />
        </div>

        <!-- Submit Button -->
        <div class="flex items-center justify-between">
          <button
            class="focus:shadow-outline rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700 focus:outline-none"
            type="submit"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Laden...' : 'Einloggen' }}
          </button>
        </div>
      </form>

      <p class="mt-4 text-center text-sm text-gray-600">
        Noch kein Konto? <router-link to="/register" class="text-blue-500 hover:text-blue-800">Registrieren</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

// Store und Router initialisieren 
const authStore = useAuthStore();
const router = useRouter();

// Reaktive Variablen
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

// Login-Handler
const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // Login-Aktion aus dem Store aufrufen 
    const result = await authStore.login(email.value, password.value);
    
    if (!result.success) {
      errorMessage.value = result.error;
    } else {
      // Bei Erfolg weiterleiten (wird bereits im Store behandelt, aber zur Sicherheit)
      // router.push('/dashboard'); 
    }
  } catch (error) {
    console.error('Unerwarteter Fehler:', error);
    errorMessage.value = 'Ein unerwarteter Fehler ist aufgetreten.';
  } finally {
    isLoading.value = false;
  }
};
</script>
