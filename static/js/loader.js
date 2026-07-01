window.addEventListener("load", () => {
  const loader = document.querySelector(".page-loader");

  if (loader) {
    loader.classList.add("hide-loader");

    setTimeout(() => {
      loader.style.display = "none";
    }, 500);
  }
});