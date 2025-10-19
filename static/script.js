document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');

    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // 显示用户消息
        const userMsg = document.createElement('div');
        userMsg.className = 'user-message';
        userMsg.textContent = `你：${message}`;
        chatHistory.appendChild(userMsg);
        messageInput.value = '';

        // 调用后端接口
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(res => res.json())
        .then(data => {
            const botMsg = document.createElement('div');
            botMsg.className = 'bot-message';
            botMsg.textContent = `星火：${data.reply}`;
            chatHistory.appendChild(botMsg);
        })
        .catch(err => console.error('接口调用失败：', err));
    }
});