const socket = io('ws://localhost:3500');

function sendMessage(e) {
    e.preventDefault();
    const input = document.getElementById('messageInput');
    if (input.value) {
      socket.emit('message', input.value);
      input.value = '';
    }
    input.focus();
  }
  
  document.getElementById('messageForm').addEventListener('submit', sendMessage);
  
  socket.on('messageAdded', (data) => {
    const li = document.createElement('li');
    li.textContent = data;
    document.getElementById('messageList').appendChild(li);
  });
  
