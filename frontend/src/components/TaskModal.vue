<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
    <!-- Modal Container mit Scroll (overflow-y-auto) -->
    <div class="bg-white rounded-lg shadow-xl w-full max-w-lg relative flex flex-col max-h-[90vh]">
      
      <!-- Header (Fixed) -->
      <div class="flex justify-between items-center p-6 border-b">
        <h2 class="text-2xl font-bold text-gray-800">
          {{ isEditing ? 'Aufgabe bearbeiten' : 'Neue Aufgabe erstellen' }}
        </h2>
        <button 
          @click="$emit('close')" 
          class="text-gray-500 hover:text-gray-700 text-xl font-bold p-2"
        >
          ✕
        </button>
      </div>

      <!-- Content (Scrollable Area) -->
      <div class="p-6 overflow-y-auto">
        <form @submit.prevent="handleSubmit" id="taskForm">
          
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

          <!-- Status Checkbox (nur beim Bearbeiten) -->
          <div v-if="isEditing" class="mb-6 flex items-center">
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

          <hr class="my-6 border-gray-200">

          <!-- Bereich: Bestehende Anhänge (nur Edit) -->
          <div v-if="isEditing && form.attachments && form.attachments.length > 0" class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2">Aktuelle Anhänge:</label>
            <ul class="space-y-2 bg-gray-50 p-3 rounded border border-gray-200">
              <li v-for="att in form.attachments" :key="att.id" class="flex justify-between items-center text-sm group">
                <span class="text-gray-700 truncate flex-1" :title="att.filename">{{ att.filename }}</span>
                <button 
                  type="button"
                  @click="removeExistingAttachment(att.id)" 
                  class="text-gray-400 hover:text-red-600 font-bold ml-2 px-2 py-1 rounded transition-colors"
                  title="Diesen Anhang löschen"
                >
                  ✕
                </button>
              </li>
            </ul>
          </div>

          <!-- Bereich: Neue Anhänge -->
          <div class="mb-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Neue Anhänge hinzufügen
            </label>
            
            <!-- File Input (Hidden, gesteuert durch Button) -->
            <input 
              ref="fileInputRef"
              @change="handleFileSelect"
              type="file" 
              multiple 
              class="hidden"
              :accept="acceptValue"
            >
            
            <!-- Custom Upload Button -->
            <button 
              type="button"
              @click="$refs.fileInputRef.click()"
              class="w-full border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:bg-gray-50 transition-colors focus:outline-none focus:border-blue-500"
            >
              <span class="text-gray-500 text-sm">
                Klicken zum Auswählen oder Dateien hierher ziehen
              </span>
              <p class="text-xs text-gray-400 mt-1">
                Erlaubte Formate: {{ allowedExts.join(', ') }}
              </p>
              <p class="text-xs text-gray-400 mt-1">
                Maximale Größe: {{ maxSizeMB }}MB
              </p>

            </button>

            <!-- Fehlermeldung für ungültige Dateien -->
            <div v-if="fileError" class="mt-2 text-xs text-red-600 bg-red-50 p-2 rounded border border-red-200 flex items-center animate-pulse">
              <span class="mr-1 font-bold">⚠️</span>
              {{ fileError }}
            </div>

            <!-- Liste der wartenden Dateien -->
            <div v-if="pendingFiles.length > 0" class="mt-4">
              <p class="text-xs font-bold text-gray-500 mb-2 uppercase tracking-wide">Bereit zum Hochladen ({{ pendingFiles.length }}):</p>
              <ul class="space-y-2 bg-blue-50 p-3 rounded border border-blue-100 max-h-40 overflow-y-auto">
                <li v-for="(file, index) in pendingFiles" :key="index" class="flex justify-between items-center text-sm">
                  <div class="flex items-center truncate flex-1">
                    <span class="mr-2 text-lg">📄</span>
                    <span class="text-blue-900 font-medium truncate">{{ file.name }}</span>
                    <span class="text-xs text-gray-500 ml-2 whitespace-nowrap">({{ (file.size / 1024 / 1024).toFixed(2) }} MB)</span>
                  </div>
                  <button 
                    type="button"
                    @click="removePendingFile(index)"
                    class="text-blue-300 hover:text-red-500 ml-2 font-bold px-2 text-lg transition-colors"
                    title="Aus Liste entfernen"
                  >
                    ✕
                  </button>
                </li>
              </ul>
            </div>
          </div>

        </form>
      </div>

      <!-- Footer (Fixed Buttons) -->
      <div class="p-6 border-t bg-gray-50 rounded-b-lg flex justify-end space-x-3">
        <button 
          type="button" 
          @click="$emit('close')" 
          class="bg-white border border-gray-300 text-gray-700 font-semibold py-2 px-4 rounded hover:bg-gray-100 transition focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200"
        >
          Abbrechen
        </button>
        <button 
          type="submit" 
          form="taskForm"
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded shadow-md transition focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Speichern...
          </span>
          <span v-else>Speichern</span>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, watch, computed  } from 'vue';
import { useTaskStore } from '../stores/task';

const maxSizeMB = parseInt(import.meta.env.VITE_UPLOAD_MAX_SIZE_MB || '5')
const rawExts = import.meta.env.VITE_UPLOAD_ALLOWED_EXTS || '[".jpg",".jpeg",".png",".gif",".pdf",".doc",".docx",".txt"]'
//const allowedExts = ref(allowedExtsRaw.split(',').map(e => e.trim().toLowerCase()).filter(Boolean))

const parseExts = (raw) => {
  if (!raw) return []
  try {
    const arr = JSON.parse(raw)
    if (Array.isArray(arr)) {
      return arr.map(e => String(e).trim().toLowerCase()).filter(Boolean)
    }
  } catch (e) {
    // fallback: ".jpg,.png" → split(',')
    return raw.split(',').map(e => e.trim().toLowerCase()).filter(Boolean)
  }
  return []
}

const allowedExts = ref(parseExts(rawExts))
const acceptValue = computed(() => allowedExts.value.join(','))

// Props
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
const taskStore = useTaskStore();
const fileError = ref(''); 

// State
const form = reactive({
  title: '',
  description: '',
  is_completed: false,
  attachments: [] // Nur für Anzeige im Edit-Modus
});

const isEditing = ref(false);
const pendingFiles = ref([]); // Warteschlange für Uploads
const fileInputRef = ref(null); // Ref für File Input Element

// Watcher: Formular füllen bei Edit
watch(() => props.taskToEdit, (newTask) => {
  pendingFiles.value = []; // Immer resetten beim Öffnen
  if (newTask) {
    isEditing.value = true;
    form.title = newTask.title;
    form.description = newTask.description;
    form.is_completed = newTask.is_completed;
    form.attachments = newTask.attachments ? [...newTask.attachments] : [];
  } else {
    isEditing.value = false;
    form.title = '';
    form.description = '';
    form.is_completed = false;
    form.attachments = [];
  }
}, { immediate: true });

// --- File Handling Logic ---

// Datei-Auswahl Handler (Professional Validation)
const handleFileSelect = (event) => {
  fileError.value = ''; // Reset error message
  const newFiles = Array.from(event.target.files);
  
  // Konfiguration für erlaubte Dateien
  //const MAX_SIZE = 5 * 1024 * 1024; // 5MB
  //const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
  const MAX_SIZE_BYTES = maxSizeMB * 1024 * 1024; // 5MB 
  const validFiles = [];
  const invalidFiles = [];

  // Validierungsschleife
  newFiles.forEach(file => {
    //  Extension validation (wie Backend!)
    const fileExt = file.name.split('.').pop()?.toLowerCase()
    if (!allowedExts.value.includes('.' + fileExt)) {
      invalidFiles.push(`${file.name}: Ungültiges Format`)
      return
    }

    // Check 2: Dateigröße
    if (file.size > MAX_SIZE_BYTES) {
      invalidFiles.push(`${file.name}: Zu groß`)
      return
    }

    // Check 3: Duplikate vermeiden
  const isDuplicate = pendingFiles.value.some(f => f.name === file.name && f.size === file.size)
    if (isDuplicate) return

    validFiles.push(file)
  });


  // Erfolgreiche Dateien hinzufügen
  if (validFiles.length > 0) {
    pendingFiles.value = [...pendingFiles.value, ...validFiles];
  }
  if (invalidFiles.length > 0) {
    fileError.value = invalidFiles.join('; ')
    setTimeout(() => fileError.value = '', 5000)
  }

  event.target.value = ''; // Reset Input
};

// Datei aus Warteschlange entfernen
const removePendingFile = (index) => {
  pendingFiles.value.splice(index, 1);
};

// Bestehenden Anhang vom Server löschen
const removeExistingAttachment = async (attachmentId) => {
  if (confirm('Diesen Anhang unwiderruflich löschen?')) {
    const result = await taskStore.deleteAttachment(attachmentId);
    if (result.success) {
      // Aus lokaler Liste entfernen für sofortiges UI-Feedback
      form.attachments = form.attachments.filter(att => att.id !== attachmentId);
    } else {
      alert('Fehler beim Löschen: ' + (result.error || 'Unbekannt'));
    }
  }
};

// --- Submit Logic (Der Kern der Sache) ---

const handleSubmit = async () => {
  try {
    let newAttachmentIds = [];

    // 1. Alle Dateien in der Warteschlange hochladen
    if (pendingFiles.value.length > 0) {
      // Parallel oder sequenziell hochladen? Sequenziell ist sicherer für Fehlerbehandlung.
      for (const file of pendingFiles.value) {
        const uploadResult = await taskStore.uploadFile(file);
        
        if (uploadResult.success) {
          newAttachmentIds.push(uploadResult.data.id);
        } else {
          // Fehlerbehandlung: Abbruch oder Warnung?
          // Hier: Warnung und wir machen weiter (oder return um abzubrechen)
          console.error(`Upload failed for ${file.name}:`, uploadResult.error);
          alert(`Fehler beim Upload von ${file.name}. Speichern abgebrochen.`);
          return; // Sicherheitsabbruch, damit wir keine inkonsistenten Daten speichern
        }
      }
    }

    // 2. Task Daten vorbereiten
    const taskData = {
      title: form.title,
      description: form.description,
      is_completed: form.is_completed
    };

    // 3. Attachment IDs hinzufügen (falls neue Dateien hochgeladen wurden)
    if (newAttachmentIds.length > 0) {
      if (isEditing.value) {
        // Backend erwartet beim Update 'new_attachment_ids'
        taskData.new_attachment_ids = newAttachmentIds;
      } else {
        // Backend erwartet beim Create 'attachment_ids'
        taskData.attachment_ids = newAttachmentIds;
      }
    }

    // 4. Alles an DashboardView senden
    emit('save', taskData);

    // 5. Aufräumen (wird eigentlich durch Modal-Close erledigt, aber zur Sicherheit)
    pendingFiles.value = [];

  } catch (error) {
    console.error('Unerwarteter Fehler im Submit:', error);
    alert('Ein unerwarteter Fehler ist aufgetreten.');
  }
};
</script>
