<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Registrieren</h2>
      
      <!-- Fehlermeldung anzeigen -->
      <div v-if="errorMessage" class="mb-4 rounded bg-red-100 p-3 text-red-700 text-sm">
        {{ errorMessage }}
      </div>
      <!-- Erfolgsmeldung anzeigen -->
      <div v-if="successMessage" class="mb-4 rounded bg-green-100 p-3 text-green-700 text-sm">
        {{ successMessage }}
      </div>

      <form @submit.prevent="handleRegister">
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
        <div class="mb-4">
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

        <!-- Passwort Bestätigen -->
        <div class="mb-6">
          <label class="mb-2 block text-sm font-bold text-gray-700" for="passwordConfirm">
            Passwort bestätigen
          </label>
          <input
            v-model="passwordConfirm"
            class="focus:shadow-outline w-full appearance-none rounded border px-3 py-2 leading-tight text-gray-700 shadow focus:outline-none"
            id="passwordConfirm"
            type="password"
            placeholder="******************"
            required
          />
        </div>

        <!-- Submit Button -->
        <div class="flex items-center justify-between">
          <button
            class="w-full focus:shadow-outline rounded bg-green-500 px-4 py-2 font-bold text-white hover:bg-green-700 focus:outline-none"
            type="submit"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Laden...' : 'Registrieren' }}
          </button>
        </div>
      </form>

      <p class="mt-4 text-center text-sm text-gray-600">
        Bereits ein Konto? <router-link to="/login" class="text-blue-500 hover:text-blue-800">Anmelden</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/axios'; // Direkter API-Aufruf 

const router = useRouter();

// Reaktive Variablen 
const email = ref('');
const password = ref('');
const passwordConfirm = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isLoading = ref(false);

// Registrierungs-Handler
const handleRegister = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  isLoading.value = true;

  // Validierung: Passwortübereinstimmung
  if (password.value !== passwordConfirm.value) {
    errorMessage.value = 'Die Passwörter stimmen nicht überein.'; // كلمات المرور غير متطابقة
    isLoading.value = false;
    return;
  }

  try {
    // Anfrage an das Backend senden 
    // Hinweis: Pfad muss mit Backend übereinstimmen (/users/ oder /auth/register)
    await api.post('/users/', {
      email: email.value,
      password: password.value
    });

    successMessage.value = 'Registrierung erfolgreich! Weiterleitung zum Login...';
    
    // Nach 2 Sekunden zum Login leiten
    setTimeout(() => {
      console.log('Redirecting to login...'); // 
      router.push('/login');
    }, 2000);

  } catch (error) {
    console.error('Registrierung fehlgeschlagen:', error);
    if (error.response && error.response.data && error.response.data.detail) {
        // Backend-Fehlermeldung anzeigen 
        errorMessage.value = error.response.data.detail;
    } else {
        errorMessage.value = 'Registrierung fehlgeschlagen. Bitte versuchen Sie es später erneut.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

