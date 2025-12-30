<script>
function sendMsg() {
  const msgInput = document.getElementById("msg");
  const replyBox = document.getElementById("reply");

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: msgInput.value
    })
  })
  .then(res => {
    if (!res.ok) {
      throw new Error("Chat API error: " + res.status);
    }
    return res.json();
  })
  .then(data => {
    replyBox.innerText = data.reply || "No reply received";
  })
  .catch(err => {
    console.error(err);
    alert("Chat failed");
  });
}

console.log("RAW RESPONSE:", data);
</script>
