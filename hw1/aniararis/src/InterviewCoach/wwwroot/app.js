"use strict";

const byId = (id) => document.getElementById(id);
const form = byId("answer-form");
const answer = byId("answer");
const submit = byId("submit-answer");
let questionId = null;
let busy = false;

function showError(id, message) {
  const element = byId(id);
  element.textContent = message;
  element.hidden = !message;
}

async function loadQuestion() {
  submit.disabled = true;
  byId("reload-question").hidden = true;
  showError("question-error", "");
  try {
    const response = await fetch("/api/question", { cache: "no-store" });
    if (!response.ok) throw new Error("Question unavailable");
    const question = await response.json();
    questionId = question.id;
    byId("question").textContent = question.text;
    byId("question-hint").textContent = question.hint;
    submit.disabled = false;
  } catch {
    byId("question").textContent = "Let's get your question ready.";
    showError("question-error", "We couldn't load the question. Check that the app is running and try again.");
    byId("reload-question").hidden = false;
  }
}

function updateCount() {
  const length = answer.value.trim().length;
  byId("character-count").textContent = `${length.toLocaleString("en-US")} / 3,000`;
  byId("character-count").classList.toggle("over-limit", length > 3000);
  answer.removeAttribute("aria-invalid");
  showError("form-error", "");
  // Feedback describes the submitted answer; hide it when that answer changes.
  byId("feedback-result").hidden = true;
  byId("feedback-placeholder").hidden = false;
  byId("request-status").textContent = "";
}

answer.addEventListener("input", updateCount);
byId("reload-question").addEventListener("click", loadQuestion);
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy || !questionId) return;
  showError("form-error", "");
  const text = answer.value.trim();
  if (text.length < 1 || text.length > 3000) {
    answer.setAttribute("aria-invalid", "true");
    showError("form-error", "Enter an answer between 1 and 3,000 characters after trimming spaces.");
    answer.focus();
    return;
  }

  busy = true;
  submit.disabled = true;
  answer.readOnly = true;
  byId("button-label").textContent = "Reading your answer…";
  byId("request-status").textContent = "Preparing feedback. This may take up to 20 seconds.";
  document.querySelector(".feedback-card").setAttribute("aria-busy", "true");
  byId("feedback-result").hidden = true;
  byId("feedback-placeholder").hidden = false;
  const started = performance.now();
  const controller = new AbortController();
  // Slightly longer than the server deadline so its readable timeout can arrive first.
  const deadline = setTimeout(() => controller.abort(), 25000);
  try {
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ questionId, answer: text }),
      signal: controller.signal
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Feedback is unavailable. Your answer is still here; try again manually.");
    if (!["strengths", "improvements", "suggestion"].every((key) => typeof data.feedback?.[key] === "string" && data.feedback[key].trim()))
      throw new Error("The feedback was incomplete. Your answer is still here; try again manually.");

    // Plain text rendering prevents model-supplied HTML from executing.
    for (const key of ["strengths", "improvements", "suggestion"]) byId(key).textContent = data.feedback[key];
    byId("feedback-placeholder").hidden = true;
    byId("feedback-result").hidden = false;
    await new Promise(requestAnimationFrame);
    const elapsed = ((performance.now() - started) / 1000).toFixed(2);
    byId("elapsed").textContent = `Displayed in ${elapsed} seconds · measured from submission`;
    byId("request-status").textContent = "Your feedback is ready. You can edit your answer and practise again.";
  } catch (error) {
    const message = error.name === "AbortError"
      ? "The request took too long. Your answer is still here; you can try again manually."
      : error instanceof TypeError || error instanceof SyntaxError
        ? "We couldn't get feedback. Your answer is still here; check your connection and try again manually."
        : error.message;
    showError("form-error", message);
    byId("request-status").textContent = "";
  } finally {
    clearTimeout(deadline);
    busy = false;
    submit.disabled = false;
    answer.readOnly = false;
    byId("button-label").textContent = "Get feedback";
    document.querySelector(".feedback-card").setAttribute("aria-busy", "false");
  }
});

loadQuestion();
