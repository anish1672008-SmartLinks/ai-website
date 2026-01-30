/**************** GLOBAL ****************/
let currentSessionId = null;
let currentMode = "hindi";

/**************** ADD MESSAGE ****************/
function addMessage(text, role) {
  const box = document.getElementById("chatBox");
  if (!box) return;

  if (role === "assistant") role = "ai";

  const div = document.createElement("div");
  div.className = "msg " + role;
  div.innerText = text;

  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

/**************** SEND ****************/
function send() {
  const input = document.getElementById("msg");
  const userMessage = input.value.trim();
  if (!userMessage) return;

  if (!currentSessionId) {
    alert("Click New Chat first");
    return;
  }

  addMessage(userMessage, "user");

  fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      message: userMessage,
      mode: currentMode,
      session_id: currentSessionId
    })
  })
  .then(r => r.json())
  .then(d => addMessage(d.reply, "ai"))
  .catch(() => addMessage("Server error", "ai"));

  input.value = "";
}

/**************** LANGUAGE ****************/
function changeLanguage() {
  currentMode = document.getElementById("languageSelect").value;
}

/**************** NEW CHAT ****************/
function newChat() {
  fetch("/new_chat", {method: "POST"})
    .then(r => r.json())
    .then(d => {
      currentSessionId = d.chat_id;

      document.getElementById("chatBox").innerHTML = "";
      loadHistory();
    });
}

/**************** HISTORY ****************/
function loadHistory() {
  fetch("/history")
    .then(r => r.json())
    .then(data => {
      const box = document.getElementById("history");
      box.innerHTML = "";

      data.forEach(chat => {
        const div = document.createElement("div");
        div.className = "chat-item";

        const title = document.createElement("span");
        title.innerText = chat.title;
        title.onclick = () => loadChat(chat.id);

        const renameBtn = document.createElement("button");
        renameBtn.innerText = "✏";
        renameBtn.onclick = e => {
          e.stopPropagation();
          renameChat(chat.id);
        };

        const deleteBtn = document.createElement("button");
        deleteBtn.innerText = "🗑";
        deleteBtn.onclick = e => {
          e.stopPropagation();
          deleteChat(chat.id);
        };

        div.appendChild(title);
        div.appendChild(renameBtn);
        div.appendChild(deleteBtn);

        box.appendChild(div);
      });
    });
}

/**************** LOAD CHAT ****************/
function loadChat(id) {
  currentSessionId = id;

  const box = document.getElementById("chatBox");
  box.innerHTML = "";

  fetch("/load_chat/" + id)
    .then(r => r.json())
    .then(data => {
      data.forEach(m => addMessage(m.content, m.role));
    });
}

/**************** DELETE ****************/
function deleteChat(id) {
  if (!confirm("Delete chat?")) return;

  fetch("/delete_chat/" + id, {method: "POST"})
    .then(() => {
      if (currentSessionId === id) {
        currentSessionId = null;
        document.getElementById("chatBox").innerHTML = "";
      }
      loadHistory();
    });
}

/**************** RENAME ****************/
function renameChat(id) {
  const name = prompt("New chat name:");
  if (!name) return;

  fetch("/rename_chat/" + id, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({title: name})
  }).then(() => loadHistory());
}

/**************** THEME ****************/
function toggleTheme() {
  document.body.classList.toggle("light-mode");
}

/**************** INIT ****************/
loadHistory();
newChat();
