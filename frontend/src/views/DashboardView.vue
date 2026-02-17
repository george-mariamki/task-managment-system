<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <!-- Header -->
    <header class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Meine Aufgaben</h1>
        <p class="text-gray-500 mt-1">Willkommen zurück, {{ user?.email }}!</p>
      </div>
      
      <div class="flex space-x-4">
        <!-- Neue Aufgabe Button -->
        <button 
          @click="openCreateModal"
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow transition"
        >
          + Neue Aufgabe
        </button>
        
        <!-- Logout Button -->
        <button 
          @click="handleLogout"
          class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-100 font-semibold py-2 px-4 rounded shadow-sm transition"
        >
          Abmelden
        </button>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="taskStore.isLoading && !taskStore.tasks.length" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-500">Lade Aufgaben...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="taskStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6" role="alert">
      <strong class="font-bold">Fehler!</strong>
      <span class="block sm:inline"> {{ taskStore.error }}</span>
    </div>

    <!-- Task List -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <TaskCard 
        v-for="task in taskStore.tasks" 
        :key="task.id" 
        :task="task" 
        @edit="openEditModal"
        @delete="confirmDelete"
        @delete-attachment="handleDeleteAttachment" 
      />
      
      <!-- Empty State -->
      <div v-if="taskStore.tasks.length === 0" class="col-span-full text-center py-12 bg-white rounded-lg border border-dashed border-gray-300">
        <p class="text-gray-500 text-lg">Keine Aufgaben gefunden.</p>
        <button @click="openCreateModal" class="mt-4 text-blue-600 hover:underline">Erstellen Sie Ihre erste Aufgabe!</button>
      </div>
    </div>

    <!-- Modal für Erstellen/Bearbeiten -->
    <TaskModal 
      v-if="showModal" 
      :taskToEdit="currentTask" 
      :isLoading="taskStore.isLoading"
      @close="closeModal"
      @save="handleSaveTask"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useTaskStore } from '../stores/task';
import { useAuthStore } from '../stores/auth';
import TaskCard from '../components/TaskCard.vue';
import TaskModal from '../components/TaskModal.vue';
import { useRouter } from 'vue-router';

// Stores initialisieren
const taskStore = useTaskStore();
const authStore = useAuthStore();
const router = useRouter();

// Lokaler State für UI
const showModal = ref(false); // Modal Sichtbarkeit
const currentTask = ref(null); // Aktuelle Aufgabe zum Bearbeiten (null = neu)
const user = authStore.user;

// Lifecycle Hook
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  taskStore.fetchTasks();
});

// Logout Handler
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

// --- Modal Logic ---

// Öffnet das Modal für eine neue Aufgabe
const openCreateModal = () => {
  currentTask.value = null; // Reset für neue Aufgabe
  showModal.value = true;
};

// Öffnet das Modal zum Bearbeiten einer existierenden Aufgabe
const openEditModal = (task) => {
  currentTask.value = task; // Task-Daten übergeben
  showModal.value = true;
};

// Schließt das Modal
const closeModal = () => {
  showModal.value = false;
  currentTask.value = null;
};

// Speichert die Aufgabe (Create oder Update)
const handleSaveTask = async (formData) => {
  let result;
  
  if (currentTask.value) {
    // Update-Logik: ID der aktuellen Aufgabe nutzen
    result = await taskStore.updateTask(currentTask.value.id, formData);
  } else {
    // Create-Logik: Neue Aufgabe erstellen
    result = await taskStore.createTask(formData);
  }

  // Wenn erfolgreich, Modal schließen
  if (result.success) {
    closeModal();
  } else {
    alert('Fehler beim Speichern: ' + (result.error || 'Unbekannter Fehler'));
  }
};

// Löschen bestätigen
const confirmDelete = async (id) => {
  if (confirm('Möchten Sie diese Aufgabe wirklich löschen?')) {
    await taskStore.deleteTask(id);
  }
};

// Anhang löschen
const handleDeleteAttachment = async (attachmentId) => {
  if (confirm('Möchten Sie diesen Anhang wirklich löschen?')) {
    // API-Aufruf (direkt über axios oder besser: neue Action im Store)
    try {
      await api.delete(`/attachments/${attachmentId}`);
      // UI aktualisieren: Task neu laden (einfachste Lösung)
      await taskStore.fetchTasks(); 
    } catch (error) {
      alert('Fehler beim Löschen des Anhangs: ' + (error.response?.data?.detail || 'Unbekannt'));
    }
  }
};
</script>
