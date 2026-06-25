const timelineList = document.getElementById("timelineList");
const skillsList = document.getElementById("skillsList");
const certificationsList = document.getElementById("certificationsList");
const projectsList = document.getElementById("projectsList");
const resourcesList = document.getElementById("resourcesList");
const downloadRoadmap = document.getElementById("downloadRoadmap");

async function fetchRoadmap() {
  const stored = JSON.parse(localStorage.getItem("careerSyncAnalysis") || "null");
  if (!stored) {
    showToast("Please analyze your resume first.");
    return;
  }
  const response = await fetch("http://localhost:5000/api/roadmap", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      role: stored.role,
      summary: stored.analysis.summary,
      missing_skills: stored.analysis.missing_skills || [],
    }),
  });
  const data = await response.json();
  if (!response.ok) {
    showToast(data.error || "Failed to generate roadmap.");
    return;
  }
  renderRoadmap(data);
}

function renderList(element, items) {
  element.innerHTML = "";
  if (!items || !items.length) {
    const li = document.createElement("li");
    li.textContent = "No items available yet.";
    element.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  });
}

function renderRoadmap(data) {
  renderList(timelineList, data.timeline);
  renderList(skillsList, data.skills);
  renderList(certificationsList, data.certifications);
  renderList(projectsList, data.projects);
  renderList(resourcesList, data.resources);
  localStorage.setItem("careerSyncRoadmap", JSON.stringify(data));
}

function downloadRoadmapFile() {
  const stored = JSON.parse(localStorage.getItem("careerSyncRoadmap") || "null");
  if (!stored) {
    showToast("No roadmap data to download.");
    return;
  }
  const content = `Timeline:\n${stored.timeline.join("\n")}\n\nSkills:\n${stored.skills.join("\n")}\n\nCertifications:\n${stored.certifications.join("\n")}\n\nProjects:\n${stored.projects.join("\n")}\n\nResources:\n${stored.resources.join("\n")}`;
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "careersync_roadmap.txt";
  anchor.click();
  URL.revokeObjectURL(url);
}

if (downloadRoadmap) {
  downloadRoadmap.addEventListener("click", downloadRoadmapFile);
}

fetchRoadmap();
