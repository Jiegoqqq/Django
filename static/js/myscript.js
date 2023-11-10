var toggleBtn1 = document.getElementById("toggleBtn1");
var content1 = document.getElementById("content1");

toggleBtn1.addEventListener("click", function() {
  if (content1.style.display === "none") {
    content1.style.display = "block";
  } else {
    content1.style.display = "none";
  }
});

var toggleBtn2 = document.getElementById("toggleBtn2");
var content2 = document.getElementById("content2");

toggleBtn2.addEventListener("click", function() {
  if (content2.style.display === "none") {
    content2.style.display = "block";
  } else {
    content2.style.display = "none";
  }
});

var toggleBtn3 = document.getElementById("toggleBtn3");
var content3 = document.getElementById("content3");

toggleBtn3.addEventListener("click", function() {
  if (content3.style.display === "none") {
    content3.style.display = "block";
  } else {
    content3.style.display = "none";
  }
});