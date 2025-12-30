function toggleTheme(){
 document.body.className =
 document.body.className==="dark"?"light":"dark";
 localStorage.setItem("theme",document.body.className);
}
document.body.className = localStorage.getItem("theme") || "dark";
