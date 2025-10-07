// static/js/app.js
const chat = document.getElementById("chat");
const textInput = document.getElementById("textInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

function appendMessage(who, text) {
  const el = document.createElement("div");
  el.className = "msg " + who;
  el.innerText = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

sendBtn.onclick = async () => {
  const text = textInput.value.trim();
  if (!text) return;
  appendMessage("user", text);
  textInput.value = "";
  const r = await fetch("/api/command", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });
  const data = await r.json();
  appendMessage("assistant", data.text);
  // speak using browser TTS:
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(data.text);
    speechSynthesis.speak(utter);
  }
};

// Web Speech API for browser microphone
let recognition;
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = async (event) => {
    const txt = event.results[0][0].transcript;
    appendMessage("user", txt);
    const r = await fetch("/api/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({text: txt})
    });
    const data = await r.json();
    appendMessage("assistant", data.text);
    if ('speechSynthesis' in window) {
      const utter = new SpeechSynthesisUtterance(data.text);
      speechSynthesis.speak(utter);
    }
  };
  recognition.onerror = (e) => console.error("Speech recognition error", e);
} else {
  micBtn.disabled = true;
}

micBtn.onclick = () => {
  if (recognition) recognition.start();
};
