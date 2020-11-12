
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
  
  let elements = document.getElementsByClassName("conf-content");
  for (let i = 0; i < elements.length; i++) {
    elements[i].style.marginLeft = "250px";
  }
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
  
  let elements = document.getElementsByClassName("conf-content");
  for (let i = 0; i < elements.length; i++) {
    elements[i].style.marginLeft = "0";
  }
}
