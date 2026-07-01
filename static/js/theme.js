document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.querySelector("#themeToggle");
  const savedTheme = localStorage.getItem("studymate_theme");

  if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-theme");

      const theme = document.body.classList.contains("dark-theme")
        ? "dark"
        : "light";

      localStorage.setItem("studymate_theme", theme);
    });
  }
});