<template>
  <div class="bg-white shadow-md rounded-lg p-4 mb-4 border border-gray-200 hover:shadow-lg transition-shadow">
    <div class="flex justify-between items-start">
      <!-- Titel und Beschreibung -->
      <div>
        <h3 class="text-lg font-semibold text-gray-800">{{ task.title }}</h3>
        <p class="text-gray-600 mt-1 text-sm">{{ task.description }}</p>
        
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
const emit = defineEmits(['edit', 'delete']);
</script>
