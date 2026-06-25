const themeToggle = document.getElementById("themeToggle");
const THEME_KEY = "csTheme";
const DEFAULT_THEME = "dark";

function showToast(message) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  window.setTimeout(() => toast.classList.remove("show"), 3200);
}

function getStoredTheme() {
  return localStorage.getItem(THEME_KEY) || DEFAULT_THEME;
}

function applyTheme(theme) {
  document.body.classList.toggle("light", theme === "light");
  document.body.classList.toggle("dark", theme !== "light");
  if (themeToggle) {
    themeToggle.textContent = theme === "light" ? "Switch to Dark" : "Switch to Light";
  }
  localStorage.setItem(THEME_KEY, theme);
}

function toggleTheme() {
  const nextTheme = getStoredTheme() === "dark" ? "light" : "dark";
  applyTheme(nextTheme);
}

document.addEventListener("DOMContentLoaded", () => {
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
  }
  applyTheme(getStoredTheme());
});
