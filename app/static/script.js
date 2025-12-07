document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const messagesArea = document.getElementById('messagesArea');

    // Generate a random user name for this session if not set
    const userName = "User_" + Math.floor(Math.random() * 1000);

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const question = userInput.value.trim();
        if (!question) return;

        // Add User Message
        addMessage(question, 'user');
        userInput.value = '';

        // Show Typing Indicator
        const loadingId = addLoadingMessage();

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: question,
                    user_name: userName
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Remove Loading Message
            removeMessage(loadingId);

            // Add AI Message
            addMessage(data.answer, 'system');

        } catch (error) {
            console.error('Error:', error);
            removeMessage(loadingId);
            addMessage('Sorry, something went wrong. Please try again.', 'system');
        }
    });

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'system-message');

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = sender === 'user' ? 'U' : 'AI';

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');

        const textP = document.createElement('p');
        textP.textContent = text;

        bubbleDiv.appendChild(textP);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);

        messagesArea.appendChild(messageDiv);
        scrollToBottom();
    }

    function addLoadingMessage() {
        const id = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'system-message');
        messageDiv.id = id;

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = 'AI';

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');

        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingIndicator.appendChild(dot);
        }

        bubbleDiv.appendChild(typingIndicator);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(bubbleDiv);

        messagesArea.appendChild(messageDiv);
        scrollToBottom();

        return id;
    }

    function removeMessage(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
});
