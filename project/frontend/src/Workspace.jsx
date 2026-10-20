import { useState } from "react";

export async function requestJson(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 45000);
  try {
    const response = await fetch(path, {
      ...options,
      signal: controller.signal,
    });
    const data = await response.json();
    if (!response.ok)
      throw new Error(
        data.error ||
          "Check your input and try again. The service may be unavailable.",
      );
    return data;
  } catch (error) {
    if (error.name === "AbortError")
      throw new Error(
        "The request took too long. Your input is preserved; retry manually.",
      );
    if (error instanceof TypeError || error instanceof SyntaxError)
      throw new Error(
        "The local service is unavailable. Your input is preserved; retry manually.",
      );
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

export function PackForm({ onSave, onClose }) {
  const [error, setError] = useState("");
  function submit(event) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const title = data.get("title").trim();
    const role = data.get("role").trim();
    const questions = data
      .get("questions")
      .split(/\r?\n/)
      .map((text) => text.trim())
      .filter(Boolean);
    if (!title || !role || !questions.length)
      return setError("Enter a title, target role, and at least one question.");
    if (questions.length > 30 || questions.some((text) => text.length > 1000))
      return setError("Use at most 30 questions, each up to 1,000 characters.");
    const id = crypto.randomUUID();
    const pack = {
      id,
      title,
      role,
      description: "Your personal question pack.",
      tags: [
        ...new Set(
          data
            .get("tags")
            .split(",")
            .map((tag) => tag.trim())
            .filter(Boolean),
        ),
      ],
      questions: questions.map((text, index) => ({
        id: `${id}-${index}`,
        text,
        hint: "Use a truthful example and explain your own contribution.",
      })),
    };
    const failure = onSave(pack);
    if (failure) setError(failure);
  }
  return (
    <section className="workspace" aria-labelledby="create-heading">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">MAKE IT YOURS</p>
          <h2 id="create-heading">Create a question pack.</h2>
        </div>
        <button className="secondary-button" onClick={onClose}>
          Cancel
        </button>
      </div>
      <form onSubmit={submit} className="field-grid">
        <label>
          Pack title
          <input name="title" required maxLength={120} autoFocus />
        </label>
        <label>
          Target role
          <input name="role" required maxLength={120} />
        </label>
        <label className="full-width">
          Tags, separated by commas
          <input name="tags" maxLength={300} />
        </label>
        <label className="full-width">
          Questions, one per line
          <textarea name="questions" required rows={5} maxLength={30000} />
        </label>
        <p className="fine-print full-width">
          Saved in this browser only. Clearing browser storage removes your
          personal packs. Avoid private information.
        </p>
        {error && (
          <p className="inline-error full-width" role="alert">
            {error}
          </p>
        )}
        <button className="primary-button" type="submit">
          Save pack
        </button>
      </form>
    </section>
  );
}

export function Practice({ pack, onClose }) {
  const [index, setIndex] = useState(0);
  const [drafts, setDrafts] = useState({});
  const [results, setResults] = useState({});
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [complete, setComplete] = useState(false);
  const [consent, setConsent] = useState(false);
  const question = pack.questions[index];
  const text = drafts[question.id] || "";
  const feedback =
    results[question.id]?.answer === text
      ? results[question.id].feedback
      : null;

  async function submit(event) {
    event.preventDefault();
    if (busy) return;
    if (!text.trim() || text.trim().length > 3000)
      return setError("Enter an answer between 1 and 3,000 characters.");
    if (!consent)
      return setError(
        "Confirm external AI processing before requesting feedback.",
      );
    setBusy(true);
    setError("");
    try {
      const result = await requestJson("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question.text, answer: text.trim() }),
      });
      if (
        !["strengths", "improvements", "suggestion"].every(
          (key) => typeof result[key] === "string" && result[key].trim(),
        )
      )
        throw new Error("Feedback was incomplete. Your answer is still here.");
      setResults((previous) => ({
        ...previous,
        [question.id]: { answer: text, feedback: result },
      }));
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy(false);
    }
  }

  function navigate(next) {
    setIndex(next);
    setError("");
  }
  return (
    <section className="workspace" aria-labelledby="practice-heading">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">{pack.title}</p>
          <h2 id="practice-heading">
            {complete
              ? "A little more prepared."
              : "One question. Your own story."}
          </h2>
        </div>
        <button className="secondary-button" onClick={onClose} disabled={busy}>
          End session
        </button>
      </div>
      {complete ? (
        <div>
          <p>
            You reached the end of this pack. {Object.keys(results).length} of{" "}
            {pack.questions.length} questions received feedback.
          </p>
          <p>
            Your answers stay only in this page session and are discarded when
            you leave it.
          </p>
          <button className="primary-button" onClick={() => setComplete(false)}>
            Review your answers
          </button>
        </div>
      ) : (
        <>
          <div className="question-prompt">
            <span className="eyebrow">
              QUESTION {index + 1} OF {pack.questions.length}
            </span>
            <h3>{question.text}</h3>
            <p>{question.hint}</p>
          </div>
          <div className="practice-grid">
            <form onSubmit={submit}>
              <label className="field">
                Your answer
                <textarea
                  value={text}
                  onChange={(event) => {
                    setDrafts((previous) => ({
                      ...previous,
                      [question.id]: event.target.value,
                    }));
                    setError("");
                  }}
                  readOnly={busy}
                  rows={8}
                  maxLength={3100}
                  placeholder="Describe a real example: the situation, what you did, and what happened."
                />
              </label>
              <p className="character-count">
                {text.trim().length.toLocaleString()} / 3,000 characters
              </p>
              <label className="consent">
                <input
                  type="checkbox"
                  checked={consent}
                  onChange={(event) => setConsent(event.target.checked)}
                  disabled={busy}
                />
                <span>
                  I understand my answer is sent through OpenRouter to an
                  external AI provider. I will omit sensitive information.
                </span>
              </label>
              {error && (
                <p className="inline-error" role="alert">
                  {error}
                </p>
              )}
              <button className="primary-button" type="submit" disabled={busy}>
                {busy ? "Reading your answer…" : "Get feedback"}
              </button>
              {busy && (
                <p role="status" className="fine-print">
                  Preparing feedback. Your answer is preserved if the provider
                  is unavailable.
                </p>
              )}
            </form>
            <aside
              className="feedback-panel"
              aria-live="polite"
              aria-busy={busy}
            >
              <p className="eyebrow">YOUR FEEDBACK</p>
              {feedback ? (
                <>
                  {[
                    ["strengths", "Strengths"],
                    ["improvements", "Areas for improvement"],
                    ["suggestion", "One next step"],
                  ].map(([key, label]) => (
                    <div key={key}>
                      <h4>{label}</h4>
                      <p>{feedback[key]}</p>
                    </div>
                  ))}
                </>
              ) : (
                <p>
                  Write an answer to get specific feedback on relevance,
                  clarity, and completeness.
                </p>
              )}
              <p className="fine-print">
                Practice guidance, not a hiring prediction. Check suggestions
                against your real experience.
              </p>
            </aside>
          </div>
          <div className="session-navigation">
            <button
              className="secondary-button"
              disabled={index === 0 || busy}
              onClick={() => navigate(index - 1)}
            >
              Previous question
            </button>
            <button
              className="primary-button"
              disabled={busy}
              onClick={() =>
                index + 1 === pack.questions.length
                  ? setComplete(true)
                  : navigate(index + 1)
              }
            >
              {index + 1 === pack.questions.length
                ? "Finish pack"
                : "Next question"}{" "}
              <span aria-hidden="true">→</span>
            </button>
          </div>
        </>
      )}
    </section>
  );
}

export function AdvertImport({ onUse, onClose }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [consent, setConsent] = useState(false);
  const [fields, setFields] = useState({
    role_title: "",
    seniority: "",
    requirements: "",
  });
  async function submit(event) {
    event.preventDefault();
    if (!file || file.size > 2 * 1024 * 1024)
      return setError("Choose a JPEG or PNG under 2 MB.");
    if (!consent)
      return setError("Confirm external AI processing before uploading.");
    setBusy(true);
    setError("");
    setResult(null);
    const body = new FormData();
    body.append("image", file);
    try {
      const data = await requestJson("/api/extract", { method: "POST", body });
      setResult(data);
      setFields({
        role_title: data.decision.fields.role_title || "",
        seniority: data.decision.fields.seniority || "",
        requirements: (data.decision.fields.requirements || []).join(", "),
      });
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy(false);
    }
  }
  function useFields(event) {
    event.preventDefault();
    if (!fields.role_title.trim() || !fields.requirements.trim())
      return setError("Enter a role title and requirements before continuing.");
    onUse(
      fields.role_title.trim(),
      fields.requirements
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
    );
  }
  return (
    <section className="workspace" aria-labelledby="import-heading">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">PREPARE FOR A ROLE</p>
          <h2 id="import-heading">Start with the job advert.</h2>
        </div>
        <button className="secondary-button" onClick={onClose} disabled={busy}>
          Close
        </button>
      </div>
      <p className="workspace-intro">
        Extract the visible role and requirements, then check them yourself.
        Uncertain fields stay empty.
      </p>
      <form onSubmit={submit}>
        <label className="field">
          Advert screenshot (JPEG or PNG, under 2 MB)
          <input
            type="file"
            accept="image/jpeg,image/png"
            disabled={busy}
            onChange={(event) => {
              setFile(event.target.files[0] || null);
              setResult(null);
              setError("");
            }}
          />
        </label>
        <label className="consent">
          <input
            type="checkbox"
            checked={consent}
            onChange={(event) => setConsent(event.target.checked)}
            disabled={busy}
          />
          <span>
            This image will be sent through OpenRouter to an external AI
            provider. It contains no private information.
          </span>
        </label>
        <button className="primary-button" disabled={busy} type="submit">
          {busy ? "Reading the advert…" : "Read advert"}
        </button>
      </form>
      {error && (
        <p className="inline-error" role="alert">
          {error}
        </p>
      )}
      {result && (
        <div className="extraction-result">
          <h3>
            {
              {
                accept: "Check the extracted details",
                confirm: "Please confirm the uncertain details",
                review: "This advert needs your review",
                reject: "Try another image",
              }[result.decision.route]
            }
          </h3>
          <ul>
            {result.decision.reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
          {result.decision.route !== "reject" && (
            <form onSubmit={useFields} className="field-grid">
              {[
                ["role_title", "Role title"],
                ["seniority", "Seniority (optional)"],
                ["requirements", "Requirements, separated by commas"],
              ].map(([name, label]) => (
                <label
                  key={name}
                  className={name === "requirements" ? "full-width" : ""}
                >
                  {label}
                  <input
                    value={fields[name]}
                    maxLength={name === "requirements" ? 1000 : 120}
                    required={name !== "seniority"}
                    onChange={(event) =>
                      setFields((previous) => ({
                        ...previous,
                        [name]: event.target.value,
                      }))
                    }
                  />
                  <small>
                    {result.evidence[name]
                      ? `Visible evidence: ${result.evidence[name]}`
                      : "No supported value was prefilled. Any value you enter is your own correction."}
                  </small>
                </label>
              ))}
              <button className="primary-button" type="submit">
                Confirm and find packs
              </button>
            </form>
          )}
        </div>
      )}
    </section>
  );
}

export function Guidance({ onClose }) {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [consent, setConsent] = useState(false);
  async function submit(event) {
    event.preventDefault();
    if (question.trim().length < 3)
      return setError("Enter a more specific preparation question.");
    if (!consent)
      return setError("Confirm external AI processing before asking.");
    setBusy(true);
    setError("");
    setResult(null);
    try {
      setResult(
        await requestJson("/api/guidance", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: question.trim() }),
        }),
      );
    } catch (failure) {
      setError(failure.message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="workspace" aria-labelledby="guidance-heading">
      <div className="workspace-heading">
        <div>
          <p className="eyebrow">FROM OUR PREPARATION GUIDES</p>
          <h2 id="guidance-heading">A little guidance, with sources.</h2>
        </div>
        <button className="secondary-button" disabled={busy} onClick={onClose}>
          Close
        </button>
      </div>
      <p className="workspace-intro">
        Ask about interview preparation. Answers cite our team-authored guides.
        If those guides don’t support an answer, we’ll say so.
      </p>
      <form onSubmit={submit}>
        <label className="field">
          Your preparation question
          <textarea
            value={question}
            onChange={(event) => {
              setQuestion(event.target.value);
              setResult(null);
            }}
            rows={3}
            maxLength={1000}
            readOnly={busy}
            placeholder="How can I answer a teamwork question without work experience?"
          />
        </label>
        <label className="consent">
          <input
            type="checkbox"
            checked={consent}
            disabled={busy}
            onChange={(event) => setConsent(event.target.checked)}
          />
          <span>
            My question and relevant guide passages may be sent to an external
            AI provider. I will omit sensitive information.
          </span>
        </label>
        <button className="primary-button" type="submit" disabled={busy}>
          {busy ? "Checking the guides…" : "Ask the guides"}
        </button>
      </form>
      {error && (
        <p className="inline-error" role="alert">
          {error}
        </p>
      )}
      {result && (
        <div className="guidance-result" aria-live="polite">
          <p className="eyebrow">
            {result.grounded ? "ANSWER WITH SOURCES" : "INSUFFICIENT SUPPORT"}
          </p>
          <p>{result.answer}</p>
          {result.citations.map((citation) => (
            <details key={citation.number}>
              <summary>
                [{citation.number}]{" "}
                {citation.document.replace(".md", "").replaceAll("-", " ")}
              </summary>
              <p>{citation.excerpt}</p>
            </details>
          ))}
          <p className="fine-print">
            Team-authored preparation guidance; review pending. Check the cited
            passages. Practice guidance does not predict hiring outcomes.
          </p>
        </div>
      )}
    </section>
  );
}
