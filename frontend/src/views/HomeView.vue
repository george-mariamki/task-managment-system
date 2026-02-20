<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 text-gray-900">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
      <h1 class="text-2xl font-bold mb-3 text-center">Willkommen!</h1>
      <p class="text-sm text-gray-600 mb-6 text-center">
        Bitte melden Sie sich an oder registrieren Sie sich, um fortzufahren.
      </p>

      <div class="flex gap-3">
        <router-link
          to="/login"
          class="flex-1 text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded"
        >
          Anmelden
        </router-link>

        <router-link
          to="/register"
          class="flex-1 text-center bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded"
        >
          Registrieren
        </router-link>
      </div>
    </div>
  </div>
</template>
