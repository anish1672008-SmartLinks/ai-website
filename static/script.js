let currentMode = "hindi";

function setMode(mode) {
  currentMode = mode;
  document.getElementById("modeText").innerText =
    mode === "english" ? "Current Mode: English AI" : "Current Mode: Hindi AI";

  console.log("Mode:", currentMode);
}

function send() {
  const message = document.getElementById("msg").value.trim();
  if (!message) return;

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: message,
      mode: currentMode
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("reply").innerText = data.reply;
    document.getElementById("msg").value = "";
  })
  .catch(err => {
    console.error(err);
    document.getElementById("reply").innerText = "Error connecting to AI.";
  });
}
