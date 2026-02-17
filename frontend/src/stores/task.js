import { defineStore } from 'pinia';
import api from '../api/axios';
import { ref } from 'vue';

export const useTaskStore = defineStore('task', () => {
    // State: Reaktive Daten für Aufgaben
    const tasks = ref([]);
    const isLoading = ref(false);
    const error = ref(null);

    // Actions: Methoden zur Interaktion mit dem Backend 

    // 1. Alle Aufgaben abrufen (GET /tasks)
    const fetchTasks = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await api.get('/tasks/');
            tasks.value = response.data;
        } catch (err) {
            console.error('Fehler beim Laden der Aufgaben:', err);
            error.value = 'Aufgaben konnten nicht geladen werden.';
        } finally {
            isLoading.value = false;
        }
    };

    // 2. Neue Aufgabe erstellen (POST /tasks)
    const createTask = async (taskData) => {
        isLoading.value = true;
        error.value = null;
        try {
            const response = await api.post('/tasks/', taskData);
            // Neue Aufgabe zur Liste hinzufügen (optimistisches UI-Update wäre auch möglich)
            tasks.value.push(response.data);
            return { success: true };
        } catch (err) {
            console.error('Fehler beim Erstellen der Aufgabe:', err);
            error.value = err.response?.data?.detail || 'Aufgabe konnte nicht erstellt werden.';
            return { success: false, error: error.value };
        } finally {
            isLoading.value = false;
        }
    };

    // 3. Aufgabe aktualisieren (PUT /tasks/{id})
    const updateTask = async (id, updateData) => {
        isLoading.value = true;
        try {
            const response = await api.put(`/tasks/${id}`, updateData);
            // Lokale Liste aktualisieren
            const index = tasks.value.findIndex(t => t.id === id);
            if (index !== -1) {
                tasks.value[index] = response.data;
            }
            return { success: true };
        } catch (err) {
            console.error('Fehler beim Aktualisieren:', err);
            return { success: false, error: err.response?.data?.detail };
        } finally {
            isLoading.value = false;
        }
    };

    // 4. Aufgabe löschen (DELETE /tasks/{id})
    const deleteTask = async (id) => {
        isLoading.value = true;
        try {
            await api.delete(`/tasks/${id}`);
            // Aus lokaler Liste entfernen
            tasks.value = tasks.value.filter(t => t.id !== id);
            return { success: true };
        } catch (err) {
            console.error('Fehler beim Löschen:', err);
            return { success: false, error: err.response?.data?.detail };
        } finally {
            isLoading.value = false;
        }
    };

    // 5. Datei hochladen (POST /upload/)
    const uploadFile = async (file) => {
        // FormData erstellen (für Datei-Upload zwingend erforderlich)
        const formData = new FormData();
        formData.append('file', file); // 'file' muss mit Backend-Parameter übereinstimmen

        try {
            // Wichtig: Content-Type nicht manuell setzen, Axios macht das bei FormData automatisch
            const response = await api.post('/upload/', formData);
            return { success: true, data: response.data }; // Gibt { id: ..., filename: ... } zurück
        } catch (err) {
            console.error('Fehler beim Hochladen:', err);
            return { success: false, error: err.response?.data?.detail || 'Upload fehlgeschlagen' };
        }
    };

    return { 
        tasks, 
        isLoading, 
        error, 
        fetchTasks, 
        createTask, 
        updateTask, 
        deleteTask,
        uploadFile
    };
});
