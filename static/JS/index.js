const hamburger = document.getElementById("js_hamburger");
const navlinks = document.getElementById("js_navlinks");

hamburger.addEventListener("click", function() {
  navlinks.classList.toggle("active")
})