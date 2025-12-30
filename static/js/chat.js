function send(){
 fetch("/chat",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({message:msg.value})
 }).then(r=>r.json()).then(d=>{
  reply.innerText=d.reply;
  speak(d.reply);
 });
}

function voice(){
 let r=new webkitSpeechRecognition();
 r.lang="hi-IN";
 r.onresult=e=>msg.value=e.results[0][0].transcript;
 r.start();
}

function speak(t){
 let s=new SpeechSynthesisUtterance(t);
 s.lang="hi-IN";
 speechSynthesis.speak(s);
}