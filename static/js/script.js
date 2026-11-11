document.addEventListener('DOMContentLoaded', () => {
    // 1. Widget Toggle Logic
    const chatHeader = document.getElementById('chat-header');
    const chatBody = document.getElementById('chat-body');
    const chatToggle = document.getElementById('chat-toggle');

    if (chatHeader && chatBody && chatToggle) {
        chatHeader.addEventListener('click', () => {
            // Check computed style to handle initial CSS states correctly
            const isHidden = window.getComputedStyle(chatBody).display === 'none';
            if (isHidden) {
                chatBody.style.display = 'flex';
                chatToggle.textContent = '−';
            } else {
                chatBody.style.display = 'none';
                chatToggle.textContent = '+';
            }
        });
    } else {
        console.error("Chatbot elements not found in the DOM.");
    }

    // 2. Initialize SocketIO
    // Only initialize if io is defined (prevents errors if CDN fails to load)
    if (typeof io !== 'undefined') {
        const socket = io();

        const chatInput = document.getElementById('chat-input');
        const chatSendBtn = document.getElementById('chat-send');
        const chatMessages = document.getElementById('chat-messages');

        function appendMessage(text, sender) {
            if (!chatMessages) return;
            
            const msgDiv = document.createElement('div');
            msgDiv.style.padding = '8px 12px';
            msgDiv.style.maxWidth = '80%';
            msgDiv.style.marginBottom = '8px';
            
            if (sender === 'user') {
                // Securely render user input as raw text to prevent XSS
                msgDiv.textContent = text;
                msgDiv.style.backgroundColor = 'var(--aviation-blue)';
                msgDiv.style.color = 'white';
                msgDiv.style.borderRadius = '12px 12px 0 12px';
                msgDiv.style.alignSelf = 'flex-end';
            } else {
                // Render bot response as HTML to allow line breaks and bolding
                msgDiv.innerHTML = text;
                msgDiv.style.backgroundColor = '#e2e8f0';
                msgDiv.style.color = 'var(--ink)';
                msgDiv.style.borderRadius = '12px 12px 12px 0';
                msgDiv.style.alignSelf = 'flex-start';
            }
            
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendMessage() {
            if (!chatInput) return;
            const text = chatInput.value.trim();
            if (text) {
                appendMessage(text, 'user');
                socket.emit('user_message', { message: text });
                chatInput.value = '';
            }
        }

        if (chatSendBtn) {
            chatSendBtn.addEventListener('click', sendMessage);
        }
        
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        }

        socket.on('bot_response', (data) => {
            appendMessage(data.message, 'bot');
        });
    } else {
         console.error("Socket.io library not loaded.");
    }
});