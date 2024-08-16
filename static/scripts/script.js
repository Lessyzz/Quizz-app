var socket = io();

socket.on('connect', function() {
    console.log('Connected to the server');
});

socket.on('chat_message', function(msg) {
    var messages = document.getElementById('messages');
    var messageItem = document.createElement('div');
    messageItem.textContent = msg;
    messages.appendChild(messageItem);
});

function sendMessage() {
    var messageInput = document.getElementById('message');
    var message = messageInput.value;
    socket.emit('chat_message', message); 
    messageInput.value = '';
}