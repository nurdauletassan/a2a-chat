import React, { useState, useEffect, useRef } from 'react';
import { sendPrompt, getDialogs, getDialog, deleteDialog, updateDialogTitle } from '../utils/api';
import '../styles/Chatbot.css';

const TypingIndicator = () => (
    <div className="typing-indicator">
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
    </div>
);

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dialogs, setDialogs] = useState([]);
    const [currentDialogId, setCurrentDialogId] = useState(null);
    const [editingDialogId, setEditingDialogId] = useState(null);
    const [editingTitle, setEditingTitle] = useState('');
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [dialogToDelete, setDialogToDelete] = useState(null);
    const [isSidebarVisible, setIsSidebarVisible] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const sidebarRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        loadDialogs();
    }, []);

    useEffect(() => {
        if (currentDialogId) {
            loadDialog(currentDialogId);
            setIsSidebarVisible(false);
        }
    }, [currentDialogId]);

    // Закрытие сайдбара при клике вне его
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (sidebarRef.current && !sidebarRef.current.contains(event.target) && 
                !event.target.closest('.mobile-menu-button')) {
                setIsSidebarVisible(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const loadDialogs = async () => {
        try {
            const data = await getDialogs();
            setDialogs(data);
        } catch (error) {
            setError('Failed to load dialogs');
        }
    };

    const loadDialog = async (dialogId) => {
        try {
            const dialog = await getDialog(dialogId);
            setMessages(dialog.messages || []);
        } catch (error) {
            setError('Failed to load dialog');
        }
    };

    const generateDialogTitle = (message) => {
        // Ограничиваем длину сообщения до 30 символов
        const maxLength = 30;
        let title = message.trim();
        
        // Если сообщение длиннее maxLength, обрезаем и добавляем многоточие
        if (title.length > maxLength) {
            title = title.substring(0, maxLength) + '...';
        }
        
        return title;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { prompt: userMessage, response: '' }]);
        setLoading(true);
        setError(null);

        try {
            const response = await sendPrompt(userMessage, currentDialogId);
            setMessages(prev => prev.map(msg => 
                msg.prompt === userMessage ? { ...msg, response: response.response } : msg
            ));
            if (!currentDialogId) {
                setCurrentDialogId(response.dialog_id);
                // Если это новый диалог, обновляем его название
                const title = generateDialogTitle(userMessage);
                await updateDialogTitle(response.dialog_id, title);
                await loadDialogs();
            }
        } catch (error) {
            setError('Failed to send message');
            setMessages(prev => prev.filter(msg => msg.prompt !== userMessage));
        } finally {
            setLoading(false);
        }
    };

    const handleNewDialog = () => {
        setCurrentDialogId(null);
        setMessages([]);
        setInput('');
        setError(null);
        setIsSidebarVisible(false);
        inputRef.current?.focus();
    };

    const handleDialogClick = (dialogId) => {
        setCurrentDialogId(dialogId);
        setEditingDialogId(null);
    };

    const handleEditClick = (e, dialogId, title) => {
        e.stopPropagation();
        setEditingDialogId(dialogId);
        setEditingTitle(title || '');
    };

    const handleDeleteClick = (e, dialogId) => {
        e.stopPropagation();
        setDialogToDelete(dialogId);
        setShowDeleteModal(true);
    };

    const handleDeleteConfirm = async () => {
        try {
            await deleteDialog(dialogToDelete);
            if (currentDialogId === dialogToDelete) {
                setCurrentDialogId(null);
                setMessages([]);
            }
            await loadDialogs();
        } catch (error) {
            setError('Failed to delete dialog');
        } finally {
            setShowDeleteModal(false);
            setDialogToDelete(null);
        }
    };

    const handleTitleSubmit = async (e, dialogId) => {
        e.preventDefault();
        try {
            await updateDialogTitle(dialogId, editingTitle);
            await loadDialogs();
            setEditingDialogId(null);
        } catch (error) {
            setError('Failed to update dialog title');
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="chatbot-container">
            <div className="chatbot-header">
                <button 
                    className="mobile-menu-button"
                    onClick={() => setIsSidebarVisible(!isSidebarVisible)}
                    title="Меню"
                >
                    ☰
                </button>
                <h2>AI Assistant</h2>
                <button className="new-dialog-button" onClick={handleNewDialog}>
                    ➕ Новый диалог
                </button>
            </div>

            <div className="chatbot-content">
                <div 
                    ref={sidebarRef}
                    className={`dialogs-sidebar ${isSidebarVisible ? 'visible' : ''}`}
                >
                    <h3>Диалоги</h3>
                    <div className="dialogs-list">
                        {dialogs.map(dialog => (
                            <div
                                key={dialog.id}
                                className={`dialog-item ${currentDialogId === dialog.id ? 'active' : ''}`}
                                onClick={() => handleDialogClick(dialog.id)}
                            >
                                {editingDialogId === dialog.id ? (
                                    <form 
                                        className="edit-title-form"
                                        onSubmit={(e) => handleTitleSubmit(e, dialog.id)}
                                        onClick={e => e.stopPropagation()}
                                    >
                                        <input
                                            type="text"
                                            value={editingTitle}
                                            onChange={(e) => setEditingTitle(e.target.value)}
                                            placeholder="Введите название"
                                            autoFocus
                                        />
                                        <div className="edit-buttons">
                                            <button type="submit" title="Сохранить">
                                                ✓
                                            </button>
                                            <button 
                                                type="button" 
                                                onClick={() => setEditingDialogId(null)}
                                                title="Отмена"
                                            >
                                                ✕
                                            </button>
                                        </div>
                                    </form>
                                ) : (
                                    <>
                                        <span className="dialog-name">
                                            {dialog.title || formatDate(dialog.created_at)}
                                        </span>
                                        <div className="dialog-buttons">
                                            <button
                                                className="edit-dialog-button"
                                                onClick={(e) => handleEditClick(e, dialog.id, dialog.title)}
                                                title="Редактировать"
                                            >
                                                ✎
                                            </button>
                                            <button
                                                className="delete-dialog-button"
                                                onClick={(e) => handleDeleteClick(e, dialog.id)}
                                                title="Удалить"
                                            >
                                                🗑️
                                            </button>
                                        </div>
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                <div className="chat-area">
                    {error && <div className="error-message">{error}</div>}
                    <div className="messages-container">
                        {messages.length === 0 && !loading ? (
                            <div className="welcome-message">
                                <h1>Добро пожаловать!</h1>
                                <p>Начните новый диалог, отправив сообщение ниже.</p>
                            </div>
                        ) : (
                            messages.map((message, index) => (
                                <div key={index} className="message-pair">
                                    <div className="user-message">{message.prompt}</div>
                                    {message.response ? (
                                        <div className="assistant-message">{message.response}</div>
                                    ) : loading && index === messages.length - 1 ? (
                                        <div className="assistant-message">
                                            <TypingIndicator />
                                        </div>
                                    ) : null}
                                </div>
                            ))
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <form className="chatbot-form" onSubmit={handleSubmit}>
                        <input
                            ref={inputRef}
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Введите сообщение..."
                            disabled={loading}
                        />
                        <button type="submit" disabled={loading || !input.trim()}>
                            ➤
                        </button>
                    </form>
                </div>
            </div>

            {showDeleteModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Удалить диалог?</h3>
                        <p>Это действие нельзя отменить. Все сообщения в этом диалоге будут удалены.</p>
                        <div className="modal-buttons">
                            <button className="cancel-button" onClick={() => setShowDeleteModal(false)}>
                                Отмена
                            </button>
                            <button className="confirm-button" onClick={handleDeleteConfirm}>
                                Удалить
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot; 