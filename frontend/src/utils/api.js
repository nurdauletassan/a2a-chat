import axios from 'axios';

const api = axios.create({
    baseURL: 'http://167.172.160.167:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Добавляем перехватчик для обработки ошибок
api.interceptors.response.use(
    response => response,
    error => {
        console.error('API Error:', error.response || error);
        return Promise.reject(error);
    }
);

export const sendPrompt = async (prompt, dialogId = null) => {
    try {
        const response = await api.post('/a2a', { prompt, dialog_id: dialogId });
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        throw new Error('Failed to send prompt');
    }
};

export const getDialogs = async () => {
    try {
        const response = await api.get('/dialogs');
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        throw new Error('Failed to get dialogs');
    }
};

export const getDialog = async (dialogId) => {
    try {
        const response = await api.get(`/dialogs/${dialogId}`);
        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        // Если ошибка 404, возвращаем пустой диалог
        if (error.response && error.response.status === 404) {
            return { id: dialogId, messages: [] };
        }
        throw new Error('Failed to get dialog');
    }
};

export const deleteDialog = async (dialogId) => {
    try {
        await api.delete(`/dialogs/${dialogId}`);
    } catch (error) {
        console.error('API Error:', error);
        throw new Error('Failed to delete dialog');
    }
};

export const updateDialogTitle = async (dialogId, title) => {
    try {
        await api.patch(`/dialogs/${dialogId}`, { title: title });
    } catch (error) {
        console.error('API Error:', error);
        throw new Error('Failed to update dialog title');
    }
}; 