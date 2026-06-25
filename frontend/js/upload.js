const resumeInput = document.getElementById("resumeInput");
const browseButton = document.getElementById("browseButton");
const uploadArea = document.getElementById("uploadArea");
const selectedFile = document.getElementById("selectedFile");
const analyzeButton = document.getElementById("analyzeButton");
const roleSelect = document.getElementById("roleSelect");
const progressBlock = document.getElementById("progressBlock");
const progressText = document.getElementById("progressText");

let currentFile = null;

if (browseButton) {
  browseButton.addEventListener("click", () => resumeInput.click());
}

if (resumeInput) {
  resumeInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      currentFile = file;
      selectedFile.textContent = file.name;
    }
  });
}

if (uploadArea) {
  ["dragenter", "dragover"].forEach((eventName) => {
    uploadArea.addEventListener(eventName, (event) => {
      event.preventDefault();
      event.stopPropagation();
      uploadArea.classList.add("dragging");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    uploadArea.addEventListener(eventName, (event) => {
      event.preventDefault();
      event.stopPropagation();
      uploadArea.classList.remove("dragging");
    });
  });

  uploadArea.addEventListener("drop", (event) => {
    const file = event.dataTransfer.files[0];
    if (file) {
      currentFile = file;
      selectedFile.textContent = file.name;
    }
  });
}

async function analyzeResume() {
  if (!currentFile) {
    showToast("Select a resume file first.");
    progressBlock.hidden = true;
    return;
  }

  const formData = new FormData();
  formData.append("resume", currentFile);
  formData.append("role", roleSelect.value);

  progressBlock.hidden = false;
  progressText.textContent = "Uploading resume...";

  try {
    const response = await fetch("http://localhost:5000/api/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      showToast(data.error || "Analysis failed.");
      progressBlock.hidden = true;
      return;
    }

    localStorage.setItem("careerSyncAnalysis", JSON.stringify({ role: roleSelect.value, analysis: data }));
    showToast("Resume analyzed successfully.");
    window.location.href = "analysis.html";
  } catch (error) {
    showToast("Unable to connect to backend.");
    progressBlock.hidden = true;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (progressBlock) {
    progressBlock.hidden = true;
  }

  if (analyzeButton) {
    analyzeButton.addEventListener("click", analyzeResume);
  }
});
