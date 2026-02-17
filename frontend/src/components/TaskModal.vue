<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-lg p-6 relative">
      <!-- Schließen Button (X) -->
      <button 
        @click="$emit('close')" 
        class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
      >
        ✕
      </button>

      <h2 class="text-2xl font-bold mb-4 text-gray-800">
        {{ isEditing ? 'Aufgabe bearbeiten' : 'Neue Aufgabe erstellen' }}
      </h2>

      <form @submit.prevent="handleSubmit">
        <!-- Titel Feld -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="title">
            Titel
          </label>
          <input 
            v-model="form.title" 
            id="title" 
            type="text" 
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
            placeholder="Aufgabentitel eingeben" 
            required
          >
        </div>

        <!-- Beschreibung Feld -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="description">
            Beschreibung
          </label>
          <textarea 
            v-model="form.description" 
            id="description" 
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-32" 
            placeholder="Details zur Aufgabe..."
          ></textarea>
        </div>

        <!-- Status Checkbox (nur beim Bearbeiten sichtbar) -->
        <div v-if="isEditing" class="mb-4 flex items-center">
          <input 
            v-model="form.is_completed" 
            id="status" 
            type="checkbox" 
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          >
          <label for="status" class="ml-2 block text-sm text-gray-900">
            Als erledigt markieren
          </label>
        </div>

        <!-- Datei Upload Feld -->
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="file">
            Anhang (Optional)
          </label>
          <input 
            @change="handleFileChange"
            id="file" 
            type="file" 
            class="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          >
          <!-- Zeige ausgewählten Dateinamen -->
          <p v-if="selectedFile" class="mt-2 text-sm text-gray-600">
            Ausgewählt: {{ selectedFile.name }}
          </p>
        </div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-3 mt-6">
          <button 
            type="button" 
            @click="$emit('close')" 
            class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Abbrechen
          </button>
          <button 
            type="submit" 
            class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Speichern...' : 'Speichern' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';
import { useTaskStore } from '../stores/task';

// Props: Task-Daten (optional für Edit) und Loading-Status
const props = defineProps({
  taskToEdit: {
    type: Object,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'save']);

// Reaktives Formular-Objekt
const form = reactive({
  title: '',
  description: '',
  is_completed: false
});

// Computed Property für den Modus (Erstellen oder Bearbeiten)
const isEditing = ref(false);

// Watcher: Wenn sich props.taskToEdit ändert, Formular füllen
watch(() => props.taskToEdit, (newTask) => {
  if (newTask) {
    isEditing.value = true;
    form.title = newTask.title;
    form.description = newTask.description;
    form.is_completed = newTask.is_completed;
  } else {
    // Reset für neue Aufgabe
    isEditing.value = false;
    form.title = '';
    form.description = '';
    form.is_completed = false;
  }
}, { immediate: true });

// Formular absenden
//const handleSubmit = () => {
  // Daten an Eltern-Komponente senden (DashboardView)
 // emit('save', { ...form });
//};

// Store nutzen
const taskStore = useTaskStore();

// Neuer State für Datei
const selectedFile = ref(null);

// Datei-Auswahl Handler
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
};

// Update handleSubmit
const handleSubmit = async () => {
  let attachmentId = null;

  // 1. Wenn Datei ausgewählt, zuerst hochladen
  if (selectedFile.value) {
    const uploadResult = await taskStore.uploadFile(selectedFile.value);
    if (uploadResult.success) {
        attachmentId = uploadResult.data.id; // ID vom Backend erhalten
    } else {
        alert('Fehler beim Dateiupload: ' + uploadResult.error);
        return; // Abbrechen
    }
  }

  // 2. Daten vorbereiten (mit Attachment ID wenn vorhanden)
  const taskData = { ...form };
  if (attachmentId) {
      taskData.attachment_ids = [attachmentId]; // Backend erwartet Liste von IDs
  }

  // 3. An Eltern-Komponente senden
  emit('save', taskData);
  
  // Reset
  selectedFile.value = null;
};

</script>
