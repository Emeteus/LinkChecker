document.querySelector(".hamburger").addEventListener("click", function () {
    document.querySelector(".header").classList.toggle("mobile");
    document.querySelector("body").classList.toggle("hidden");
  });
