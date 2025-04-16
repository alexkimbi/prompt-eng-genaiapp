document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const clearChatButton = document.getElementById('clear-chat');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorToast = new bootstrap.Toast(document.getElementById('error-toast'));
    const errorMessage = document.getElementById('error-message');

    // Focus on input field when page loads
    userInput.focus();

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input field
        userInput.value = '';
        
        // Show loading spinner
        loadingSpinner.classList.remove('d-none');
        
        // Send message to server
        sendMessage(message);
    });

    // Handle clear chat button
    clearChatButton.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear the conversation?')) {
            clearChat();
        }
    });

    // Function to add a message to the chat
    function addMessageToChat(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(role === 'user' ? 'user-message' : 'ai-message');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = content;
        
        messageDiv.appendChild(messageContent);
        chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to send message to server
    function sendMessage(message) {
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading spinner
            loadingSpinner.classList.add('d-none');
            
            // Add AI response to chat
            addMessageToChat('assistant', data.response);
        })
        .catch(error => {
            // Hide loading spinner
            loadingSpinner.classList.add('d-none');
            
            // Show error toast
            errorMessage.textContent = error.message || 'An error occurred while processing your request';
            errorToast.show();
            
            console.error('Error:', error);
        });
    }

    // Function to clear chat
    function clearChat() {
        fetch('/clear_conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Clear chat container
            chatContainer.innerHTML = '';
            
            // Add welcome message
            const welcomeMessage = document.createElement('div');
            welcomeMessage.classList.add('welcome-message');
            welcomeMessage.innerHTML = `
                <h3>Welcome to Career Advisor!</h3>
                <p>Hi, I'm Joe, your AI career coach. How can I help you with your career today?</p>
                <p>Try asking me questions like:</p>
                <ul>
                    <li>What careers are good for someone with a sociology degree?</li>
                    <li>How can I transition from marketing to data science?</li>
                    <li>What skills should I develop for a career in healthcare?</li>
                </ul>
            `;
            chatContainer.appendChild(welcomeMessage);
        })
        .catch(error => {
            // Show error toast
            errorMessage.textContent = error.message || 'An error occurred while clearing the conversation';
            errorToast.show();
            
            console.error('Error:', error);
        });
    }

    // Handle Enter key in textarea
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
}); 