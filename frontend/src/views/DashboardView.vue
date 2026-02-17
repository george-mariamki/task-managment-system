<template>
  <!-- Layout Container: Volle Höhe, Flex-Spalte, kein Scroll am Body -->
  <div class="h-screen flex flex-col bg-gray-50 overflow-hidden">
    
    <!-- 1. Fixierter Header (Bleibt immer oben) -->
    <header class="bg-white shadow-sm z-10 p-6 flex-shrink-0">
      <div class="max-w-7xl mx-auto flex justify-between items-center w-full">
        <!-- Begrüßung -->
        <div>
          <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Meine Aufgaben</h1>
          <div class="flex items-center mt-1 text-gray-500 text-sm">
            <span class="mr-2">👋</span>
            <span class="font-medium">Willkommen zurück, {{ user?.email }}!</span>
          </div>
        </div>
        
        <!-- Aktionen -->
        <div class="flex space-x-3">
          <button 
            @click="openCreateModal"
            class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 px-5 rounded-lg shadow-md hover:shadow-lg transition-all transform hover:-translate-y-0.5 flex items-center"
          >
            <span class="mr-2 text-xl leading-none">+</span> Neue Aufgabe
          </button>
          
          <button 
            @click="handleLogout"
            class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 hover:text-red-600 font-semibold py-2.5 px-5 rounded-lg shadow-sm transition-colors flex items-center"
          >
            <span class="mr-2">🚪</span> Abmelden
          </button>
        </div>
      </div>
    </header>

    <!-- 2. Scrollbarer Inhalt (Nimmt restlichen Platz ein) -->
    <main class="flex-1 overflow-y-auto p-6 md:p-8">
      <div class="max-w-7xl mx-auto w-full">
        
        <!-- Loading State -->
        <div v-if="taskStore.isLoading && !taskStore.tasks.length" class="flex flex-col items-center justify-center py-20 h-64">
          <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-100 border-t-blue-600 mb-4"></div>
          <p class="text-gray-500 font-medium animate-pulse">Lade Ihre Aufgaben...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="taskStore.error" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-sm mb-6 max-w-2xl mx-auto" role="alert">
          <div class="flex">
            <div class="py-1"><svg class="fill-current h-6 w-6 text-red-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"/></svg></div>
            <div>
              <p class="font-bold">Ein Fehler ist aufgetreten</p>
              <p class="text-sm">{{ taskStore.error }}</p>
            </div>
          </div>
        </div>

        <!-- Task Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-12">
          <TaskCard 
            v-for="task in taskStore.tasks" 
            :key="task.id" 
            :task="task" 
            @edit="openEditModal"
            @delete="confirmDelete"
            @delete-attachment="handleDeleteAttachment"
          />
          
          <!-- Empty State (Zentriert und schön gestaltet) -->
          <div v-if="taskStore.tasks.length === 0" class="col-span-full flex flex-col items-center justify-center py-20 bg-white rounded-xl border-2 border-dashed border-gray-300 text-center">
            <div class="bg-blue-50 p-4 rounded-full mb-4">
              <span class="text-4xl">📝</span>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Keine Aufgaben gefunden</h3>
            <p class="text-gray-500 max-w-md mb-6">Starten Sie produktiv in den Tag und erstellen Sie Ihre erste Aufgabe!</p>
            <button 
              @click="openCreateModal" 
              class="text-blue-600 hover:text-blue-800 font-semibold hover:underline flex items-center"
            >
              Jetzt Aufgabe erstellen →
            </button>
          </div>
        </div>
      
      </div>
    </main>

    <!-- Modal Komponente (Außerhalb des Flows) -->
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

// Lokaler State
const showModal = ref(false);
const currentTask = ref(null);
const user = authStore.user;

// Lifecycle
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  taskStore.fetchTasks();
});

// Actions
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

const openCreateModal = () => {
  currentTask.value = null;
  showModal.value = true;
};

const openEditModal = (task) => {
  currentTask.value = task;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  currentTask.value = null;
};

const handleSaveTask = async (formData) => {
  let result;
  if (currentTask.value) {
    result = await taskStore.updateTask(currentTask.value.id, formData);
  } else {
    result = await taskStore.createTask(formData);
  }

  if (result.success) {
    closeModal();
    // Optional: Erfolgsmeldung anzeigen (Toast)
  } else {
    alert('Fehler beim Speichern: ' + (result.error || 'Unbekannter Fehler'));
  }
};

const confirmDelete = async (id) => {
  if (confirm('Möchten Sie diese Aufgabe wirklich löschen?')) {
    await taskStore.deleteTask(id);
  }
};

const handleDeleteAttachment = async (attachmentId) => {
  if (confirm('Möchten Sie diesen Anhang wirklich löschen?')) {
    const result = await taskStore.deleteAttachment(attachmentId);
    if (!result.success) {
      alert('Fehler: ' + result.error);
    }
  }
};
</script>
