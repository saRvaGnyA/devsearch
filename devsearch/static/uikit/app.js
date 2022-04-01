// Invoke Functions Call on Document Loaded
document.addEventListener("DOMContentLoaded", function () {
  hljs.highlightAll();
});

let body = document.getElementsByTagName("body")[0];

body.addEventListener("click", (e) => {
  if (e.target.classList.contains("alert__close")) {
    document.querySelector(".alert").style.display = "none";
    console.log("clicked");
  }
});
