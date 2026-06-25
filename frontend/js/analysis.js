const matchScoreEl = document.getElementById("matchScore");
const atsScoreEl = document.getElementById("atsScore");
const strengthsList = document.getElementById("strengthsList");
const missingSkillsList = document.getElementById("missingSkillsList");
const suggestionsList = document.getElementById("suggestionsList");
const summaryText = document.getElementById("summaryText");
const downloadReport = document.getElementById("downloadReport");

function renderList(element, items) {
  element.innerHTML = "";
  if (!items || !items.length) {
    const li = document.createElement("li");
    li.textContent = "No items found.";
    element.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  });
}

function formatAnalysis() {
  const stored = localStorage.getItem("careerSyncAnalysis");
  if (!stored) return null;
  return JSON.parse(stored);
}

function populateAnalysis() {
  const payload = formatAnalysis();
  if (!payload) {
    showToast("No analysis data available.");
    return;
  }
  const { analysis } = payload;
  matchScoreEl.textContent = `${analysis.match_score || 0}%`;
  atsScoreEl.textContent = `${analysis.ats_score || 0}%`;
  renderList(strengthsList, analysis.strengths || []);
  renderList(missingSkillsList, analysis.missing_skills || []);
  renderList(suggestionsList, analysis.suggestions || []);
  summaryText.textContent = analysis.summary || "Your resume summary will appear here after analysis.";
}

function downloadPDFReport() {
  const payload = formatAnalysis();
  if (!payload) {
    showToast("No analysis data found.");
    return;
  }

  const { role, analysis } = payload;
  const content = `CareerSync AI Resume Analysis\n\nRole: ${role}\n\nMatch Score: ${analysis.match_score}%\nATS Score: ${analysis.ats_score}%\n\nStrengths:\n${(analysis.strengths || []).map((item) => `- ${item}`).join("\n")}\n\nMissing Skills:\n${(analysis.missing_skills || []).map((item) => `- ${item}`).join("\n")}\n\nSuggestions:\n${(analysis.suggestions || []).map((item) => `- ${item}`).join("\n")}\n\nSummary:\n${analysis.summary || "N/A"}`;

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "careersync_analysis_report.txt";
  anchor.click();
  URL.revokeObjectURL(url);
}

if (downloadReport) {
  downloadReport.addEventListener("click", downloadPDFReport);
}

populateAnalysis();
