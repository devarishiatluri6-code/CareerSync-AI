const technicalList = document.getElementById("technicalList");
const behavioralList = document.getElementById("behavioralList");
const hrList = document.getElementById("hrList");
const downloadQuestions = document.getElementById("downloadQuestions");

async function fetchInterviewQuestions() {
  const stored = JSON.parse(localStorage.getItem("careerSyncAnalysis") || "null");
  if (!stored) {
    showToast("Please analyze your resume first.");
    return;
  }
  const response = await fetch("http://localhost:5000/api/interview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role: stored.role, summary: stored.analysis.summary }),
  });
  const data = await response.json();
  if (!response.ok) {
    showToast(data.error || "Failed to generate questions.");
    return;
  }
  renderQuestions(data);
}

function renderList(element, items) {
  element.innerHTML = "";
  if (!items || !items.length) {
    const li = document.createElement("li");
    li.textContent = "No questions available yet.";
    element.appendChild(li);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  });
}

function renderQuestions(data) {
  renderList(technicalList, data.technical_questions);
  renderList(behavioralList, data.behavioral_questions);
  renderList(hrList, data.hr_questions);
  localStorage.setItem("careerSyncInterview", JSON.stringify(data));
}

function copySection(type) {
  const stored = JSON.parse(localStorage.getItem("careerSyncInterview") || "null");
  if (!stored) {
    showToast("No interview content available.");
    return;
  }
  const content = (stored[`${type}_questions`] || []).join("\n");
  navigator.clipboard.writeText(content).then(() => {
    showToast("Questions copied to clipboard.");
  });
}

function downloadQuestionFile() {
  const stored = JSON.parse(localStorage.getItem("careerSyncInterview") || "null");
  if (!stored) {
    showToast("No interview questions to download.");
    return;
  }
  const content = `Technical Questions:\n${stored.technical_questions.join("\n")}\n\nBehavioral Questions:\n${stored.behavioral_questions.join("\n")}\n\nHR Questions:\n${stored.hr_questions.join("\n")}`;
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "careersync_interview_questions.txt";
  anchor.click();
  URL.revokeObjectURL(url);
}

document.querySelectorAll("button[data-copy]").forEach((button) => {
  button.addEventListener("click", () => copySection(button.dataset.copy));
});

if (downloadQuestions) {
  downloadQuestions.addEventListener("click", downloadQuestionFile);
}

fetchInterviewQuestions();
