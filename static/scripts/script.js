var socket = io();

socket.on('connect', function() {
    console.log('Connected to the server');
});

socket.on('chat_message', function(msg) { // Gelen mesajları dinle
    messageItem.textContent = msg;
});

function sendMessage() { // Mesaj gönderme fonksiyonu
    socket.emit('chat_message', "mesaj"); 
    messageInput.value = '';
}