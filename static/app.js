const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

function appendMessage(html, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = sender === 'user' ? 'user-msg' : 'bot-msg';
    messageElement.innerHTML = html;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const msg = userInput.value;
    if (!msg.trim()) return; // Don't send empty messages

    appendMessage(msg, 'user');
    userInput.value = '';

    // Send to backend
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });
        const data = await response.json();

        if (data.greeting) {
            appendMessage(data.greeting, 'bot');
        } 
        else if (data.profile_prompt) {
            appendMessage(data.profile_prompt, 'bot');
        } 
        else if (data.recommendation_msg && data.recommended_product) {
            let recommendationHTML = `<p>${data.recommendation_msg}</p>`;
            const product = data.recommended_product.product;
            recommendationHTML += `
                <div class="product-card">
                    <h4>${product.name}</h4>
                    <p><strong>Description:</strong> ${product.description}</p>
                    <p><strong>Features:</strong> ${product.features.join(', ')}</p>
                    <p><strong>Benefits:</strong> ${product.benefits.join(', ')}</p>
                </div>
            `;
            if (data.transition_msg) {
                recommendationHTML += `<p>${data.transition_msg}</p>`;
            }
            appendMessage(recommendationHTML, 'bot');
            // Must also handle the calculator prompt that comes with the recommendation
            if (data.calculator_prompt) {
                appendMessage(data.calculator_prompt, 'bot');
            }
        } 
        else if (data.calculator_prompt) {
            appendMessage(data.calculator_prompt, 'bot');
        } 
        else if (data.calculator_result) {
            appendMessage(data.calculator_result, 'bot');
        } 
        else if (data.message) {
            appendMessage(data.message, 'bot');
        } 
        else if (Object.keys(data).length === 0) {
            appendMessage('No suitable products found. Please provide more information about your age and risk tolerance (e.g., "I am 55 and prefer low risk").', 'bot');
        }
    } catch (err) {
        console.error('Error:', err);
        appendMessage('Error contacting backend.', 'bot');
    }
}

// Allow Enter to send, Shift+Enter for newline
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage();
});
