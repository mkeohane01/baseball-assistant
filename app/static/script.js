document.getElementById('send-btn').addEventListener('click', sendMessage);

document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = userInput;
        document.getElementById('messages').appendChild(messageElement);

        document.getElementById('user-input').value = "";

        // Handle the request to the Flask backend here
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userInput }),
        })
        .then(response => response.json())
        .then(data => {
            const responseMessageElement = document.createElement('div');
            responseMessageElement.className = 'message bot-message';
            responseMessageElement.textContent = data.answer;
            document.getElementById('messages').appendChild(responseMessageElement);
        });
    }
}
