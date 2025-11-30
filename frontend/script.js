function getPriorityClass(score) {
  if (score >= 120) return "priority-high";
  if (score >= 80) return "priority-medium";
  return "priority-low";
}

function displayResults(tasks) {
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  if (!tasks || tasks.length === 0) {
    resultsDiv.textContent = "No tasks returned.";
    return;
  }

  tasks.forEach((task) => {
    const card = document.createElement("div");
    card.classList.add("task-card", getPriorityClass(task.score || 0));

    const titleEl = document.createElement("div");
    titleEl.className = "task-title";
    titleEl.textContent = task.title || "Untitled Task";

    const metaEl = document.createElement("div");
    metaEl.className = "task-meta";
    metaEl.innerHTML = `
      <div><strong>Due:</strong> ${task.due_date || "N/A"}</div>
      <div><strong>Importance:</strong> ${task.importance}</div>
      <div><strong>Estimated Hours:</strong> ${task.estimated_hours}</div>
      <div class="task-score"><strong>Score:</strong> ${task.score}</div>
    `;

    const expl = task.explanations || {};
    const explEl = document.createElement("div");
    explEl.className = "task-expl";
    explEl.textContent =
      `Urgency: ${expl.urgency || ""} | ` +
      `Importance: ${expl.importance || ""} | ` +
      `Effort: ${expl.effort || ""} | ` +
      `Dependencies: ${expl.dependencies || ""}`;

    card.appendChild(titleEl);
    card.appendChild(metaEl);
    card.appendChild(explEl);

    resultsDiv.appendChild(card);
  });
}

function addTaskFromForm() {
  const title = document.getElementById("formTitle").value.trim();
  const dueDate = document.getElementById("formDueDate").value;
  const importance = document.getElementById("formImportance").value;
  const estimatedHours = document.getElementById("formEstimatedHours").value;
  const depsRaw = document.getElementById("formDependencies").value;

  if (!title || !dueDate) {
    alert("Title and Due Date are required.");
    return;
  }

  const task = {
    title,
    due_date: dueDate,
    importance: importance ? Number(importance) : 5,
    estimated_hours: estimatedHours ? Number(estimatedHours) : 1,
  };

  if (depsRaw.trim()) {
    task.dependencies = depsRaw
      .split(",")
      .map((v) => v.trim())
      .filter((v) => v !== "")
      .map((v) => Number(v));
  } else {
    task.dependencies = [];
  }

  const inputEl = document.getElementById("taskInput");

  let current;
  try {
    current = inputEl.value ? JSON.parse(inputEl.value) : [];
    if (!Array.isArray(current)) current = [];
  } catch (e) {
    current = [];
  }

  current.push(task);
  inputEl.value = JSON.stringify(current, null, 2);

  document.getElementById("taskForm").reset();
}

async function analyzeTasks() {
  const statusEl = document.getElementById("status");
  const inputEl = document.getElementById("taskInput");
  const strategySelect = document.getElementById("strategySelect");

  let tasks;
  try {
    tasks = inputEl.value ? JSON.parse(inputEl.value) : [];
  } catch (e) {
    alert("Invalid JSON in textarea. Please fix it.");
    return;
  }

  if (!Array.isArray(tasks)) {
    alert("JSON must be an array of tasks.");
    return;
  }

  statusEl.textContent = "Analyzing...";

  try {
    const res = await fetch("/api/tasks/analyze/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        strategy: strategySelect.value,
        tasks,
      }),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      statusEl.textContent = "Error analyzing tasks.";
      console.error("Error:", errData);
      alert(errData.error || "Failed to analyze tasks.");
      return;
    }

    const data = await res.json();
    displayResults(data.tasks || []);
    statusEl.textContent = `Analyzed ${data.tasks.length} task(s) with "${strategySelect.value}" strategy.`;
  } catch (e) {
    console.error(e);
    statusEl.textContent = "Error contacting server.";
    alert("Error contacting server. Check console.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("analyzeBtn").addEventListener("click", analyzeTasks);
});
