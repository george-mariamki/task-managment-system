<template>
  <div class="bg-white shadow-md rounded-lg p-4 mb-4 border border-gray-200 hover:shadow-lg transition-shadow">
    <div class="flex justify-between items-start">
      <!-- Titel und Beschreibung -->
      <div>
        <h3 class="text-lg font-semibold text-gray-800">{{ task.title }}</h3>
        <p class="text-gray-600 mt-1 text-sm">{{ task.description }}</p>
        
        <!-- Anhänge -->
        <div v-if="task.attachments && task.attachments.length > 0" class="mt-3 border-t pt-2">
            <p class="text-xs font-semibold text-gray-500 mb-1">Anhänge:</p>
            <ul class="space-y-1">
                <li 
                v-for="attachment in task.attachments" 
                :key="attachment.id" 
                class="flex items-center justify-between bg-gray-50 px-2 py-1 rounded text-sm"
                >
                <!-- Dateiname (Link zum Öffnen) -->
                <a 
                    :href="getFileUrl(attachment.file_path)" 
                    target="_blank" 
                    class="text-blue-600 hover:underline truncate max-w-[150px]"
                    title="Datei öffnen"
                >
                    📎 {{ attachment.filename }}
                </a>
                
                <!-- Löschen Button (X) -->
                <button 
                    @click="$emit('delete-attachment', attachment.id)" 
                    class="text-gray-400 hover:text-red-500 ml-2"
                    title="Anhang entfernen"
                >
                    ✕
                </button>
                </li>
            </ul>
        </div>

        <!-- Status Anzeige  -->
        <span 
          class="inline-block mt-2 px-2 py-1 text-xs font-semibold rounded-full"
          :class="task.is_completed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
        >
          {{ task.is_completed ? 'Erledigt' : 'Offen' }}
        </span>
      </div>

      <!-- Aktionen  -->
      <div class="flex space-x-2">
        <button 
          @click="$emit('edit', task)" 
          class="text-blue-500 hover:text-blue-700 p-1 rounded hover:bg-blue-50"
          title="Bearbeiten"
        >
          ✏️
        </button>
        <button 
          @click="$emit('delete', task.id)" 
          class="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-50"
          title="Löschen"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Props definieren 
const props = defineProps({
  task: {
    type: Object,
    required: true
  }
});

// Emits definieren 
const emit = defineEmits(['edit', 'delete', 'delete-attachment']);

// Hilfsfunktion: URL für Datei generieren
const origin = import.meta.env.VITE_BACKEND_ORIGIN || "http://localhost:8000";

const getFileUrl = (filePath) => {
  if (!filePath) return "#";
  if (filePath.startsWith("http://") || filePath.startsWith("https://")) return filePath;
  const p = filePath.startsWith("/") ? filePath : `/${filePath}`;
  return `${origin}${p}`;
};
</script>
