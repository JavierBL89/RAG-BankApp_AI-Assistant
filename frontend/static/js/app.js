let timeoutMessageShown = false;
let timeoutMessageDiv = null;
let timeoutHandle = null;

const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const chatbox = document.getElementById('chatbox');

const md = window.markdownit({
  breaks: true,
  html: false,
  linkify: true,
  typographer: true
});

window.addEventListener('DOMContentLoaded', async () => {
  typeBotResponse("Hey, this is Banky! 👋\n  How can I assist you?", "bot");
});

function createBotBubbleWithSpinner() {
  const div = document.createElement('div');
  div.className = 'bot';

  const span = document.createElement('span');
  span.id = 'bot-reply-content';
  span.style.display = 'inline-block';

  const spinner = document.createElement('div');
  spinner.className = 'spinner';
  spinner.id = 'loading-spinner';

  div.appendChild(spinner);
  div.appendChild(span);
  chatbox.appendChild(div);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function removeLoading() {
  const spinner = document.getElementById('loading-spinner');
  if (spinner) spinner.remove();
}

function displayMessage(message, sender) {
  const div = document.createElement('div');
  div.className = sender;
  chatbox.appendChild(div);
  div.textContent = message;
}


form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value;
  console.log("user input:"+ message);
  displayMessage(message, 'user');
  input.value = '';

  createBotBubbleWithSpinner();

  const timeOutMessage = setTimeout(() => {
    if (!timeoutMessageShown) {
      timeoutMessageDiv = document.createElement('div');
      timeoutMessageDiv.className = 'bot';
      timeoutMessageDiv.id = 'timeout-hint';
      timeoutMessageDiv.textContent = "⏳ This is taking longer... bot server might be busy.";
      chatbox.appendChild(timeoutMessageDiv);
      chatbox.scrollTop = chatbox.scrollHeight;
      timeoutMessageShown = true;
    }
  }, 5000);

  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: message }),
    });

    if (!response.ok) throw new Error(await response.text());

    const data = await response.json();

    clearTimeout(timeOutMessage);
    removeLoading();

    if (timeoutMessageDiv) {
      timeoutMessageDiv.remove();
      timeoutMessageDiv = null;
      timeoutMessageShown = false;
    }
    console.log(data.choices[0].message.content, 'bot');
    typeBotResponse(data.choices[0].message.content, 'bot');
    
  } catch (err) {
    clearTimeout(timeOutMessage);
    if (timeoutMessageDiv) {
      timeoutMessageDiv.remove();
      timeoutMessageDiv = null;
      timeoutMessageShown = false;
    }
    removeLoading();
    console.error("❌ Error talking to server:", err);
    typeBotResponse('Ey sorry, something went wrong or connection to server was lost\n Please try once again!', 'bot');
  }
});


function typeBotResponse(message, sender) {
  const div = document.createElement('div');
  div.className = sender;

  const span = document.createElement('span');
  div.appendChild(span);
  chatbox.appendChild(div);

  chatbox.scrollTop = chatbox.scrollHeight;

  // Step 1: Clean raw markdown string
  const cleaned = message.replace(/\\n/g, '\n').trim();

  // Step 2: Split raw markdown into character chunks
  const charChunks = cleaned.match(/.{1,19}/gs);  // 19-char chunks
  let index = 0;
  let current = "";

  const type = () => {
    if (index < charChunks.length) {
      current += charChunks[index];         // Append raw text
      span.innerHTML = md.render(current);  // Render complete visible part
      chatbox.scrollTop = chatbox.scrollHeight;
      index++;
      setTimeout(type, 50);                 // Typing delay
    }
  };

  type();
}
