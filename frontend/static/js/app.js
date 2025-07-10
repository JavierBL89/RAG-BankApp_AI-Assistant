async function sendMessage() {
    const input = document.getElementById('user-input').value;
    const response = await fetch('http://localhost:3000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input })
    });
    const data = await response.json();
    document.getElementById('chat-response').innerText = data.response;
  }