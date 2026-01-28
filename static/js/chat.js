// =======================
// GLOBAL ELEMENTS
// =======================
const msg = document.getElementById("msg");
const reply = document.getElementById("reply");

let recognition = null;

// =======================
// SEND MESSAGE
// =======================
function send() {
  const userMessage = msg.value.trim();
  if (!userMessage) return;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: userMessage,
      mode: currentMode
    })
  })
    .then(r => r.json())
    .then(d => {
      reply.innerText = d.reply;

      // 🔊 AI बोलेगा
      speak(d.reply);
    })
    .catch(err => console.error("Chat error:", err));

  msg.value = "";
}

// =======================
// 🎤 VOICE INPUT (REPAIRED)
// =======================
function voice() {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("❌ Voice input not supported in this browser");
    return;
  }

  if (!recognition) {
    recognition = new SpeechRecognition();
    recognition.lang = currentMode === "english" ? "en-US" : "hi-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (e) => {
      msg.value = e.results[0][0].transcript;
    };

    recognition.onerror = (e) => {
      console.error("Mic error:", e.error);
    };
  }

  recognition.start();
}

// =======================
// 🔊 TEXT TO SPEECH (REPAIRED)
// =======================
function speak(text) {
  if (!("speechSynthesis" in window)) return;

  speechSynthesis.cancel(); // important fix

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = currentMode === "english" ? "en-US" : "hi-IN";
  utterance.rate = 1;
  utterance.pitch = 1;

  speechSynthesis.speak(utterance);
}
