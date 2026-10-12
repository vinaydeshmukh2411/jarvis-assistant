const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const micButton = document.getElementById('micButton');

const localResponses = {
  hello: 'Hello! I am Jarvis. How may I assist you?',
  hi: 'Hi there! I am ready to help.',
  time: 'Checking the current time...',
  date: 'Here is today\'s date...',
  weather: 'I can help with weather if you tell me the city.',
  name: 'I am Jarvis, your virtual assistant.',
  default: 'I heard you. Please tell me what you want me to do.'
};

function addMessage(text, type) {
  const msg = document.createElement('div');
  msg.className = `message ${type}`;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function getLocalResponse(input) {
  const text = input.toLowerCase();

  if (text.includes('hello') || text.includes('hi') || text.includes('hey')) return localResponses.hello;
  if (text.includes('time')) return `The current time is ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}.`;
  if (text.includes('date')) return `Today is ${new Date().toLocaleDateString()}.`;
  if (text.includes('weather')) return 'I can check the weather for a city. For example: "Weather in London".';
  if (text.includes('your name') || text.includes('who are you')) return localResponses.name;
  if (text.includes('thank')) return 'You are welcome.';
  return localResponses.default;
}

async function sendMessage(inputText) {
  const text = inputText.trim();
  if (!text) return;

  addMessage(text, 'user');
  userInput.value = '';

  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    if (response.ok) {
      const data = await response.json();
      addMessage(data.reply, 'bot');
      if ('speechSynthesis' in window) {
        const utter = new SpeechSynthesisUtterance(data.reply);
        speechSynthesis.cancel();
        speechSynthesis.speak(utter);
      }
      return;
    }
  } catch (error) {
    console.warn('Backend unavailable, using local mode:', error);
  }

  const fallback = getLocalResponse(text);
  addMessage(fallback, 'bot');
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(fallback);
    speechSynthesis.cancel();
    speechSynthesis.speak(utter);
  }
}

sendButton.addEventListener('click', () => sendMessage(userInput.value));
userInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') sendMessage(userInput.value);
});

micButton.addEventListener('click', () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    addMessage('Speech recognition is not supported in this browser.', 'bot');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    userInput.value = transcript;
    sendMessage(transcript);
  };

  recognition.onerror = () => {
    addMessage('I could not hear you clearly. Please try again.', 'bot');
  };
});

addMessage('Jarvis online. Ask me anything.', 'bot');
