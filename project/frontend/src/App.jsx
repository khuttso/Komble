import { useEffect, useRef, useState } from "react";
import { AdvertImport, Guidance, PackForm, Practice } from "./Workspace.jsx";

const STORAGE_KEY = "interviewcoach.shared.packs.v1";

function loadPersonalPacks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { packs: [], error: "" };
    const value = JSON.parse(raw);
    if (!Array.isArray(value)) throw new Error("Invalid saved packs");
    return { packs: value.length === 0 ? [] : validatePacks(value), error: "" };
  } catch {
    return {
      packs: [],
      error:
        "Personal packs could not be read. Check browser storage; existing stored data has not been overwritten.",
    };
  }
}

function validatePacks(value) {
  if (!Array.isArray(value) || value.length === 0)
    throw new Error("Invalid library");
  const ids = new Set();
  for (const pack of value) {
    if (
      !pack ||
      typeof pack.id !== "string" ||
      ids.has(pack.id) ||
      !["title", "role", "description"].every(
        (key) => typeof pack[key] === "string",
      ) ||
      !Array.isArray(pack.tags) ||
      !pack.tags.every((tag) => typeof tag === "string") ||
      !Array.isArray(pack.questions) ||
      !pack.questions.length ||
      !pack.questions.every(
        (question) =>
          question &&
          typeof question.id === "string" &&
          typeof question.text === "string",
      )
    ) {
      throw new Error("Invalid library");
    }
    ids.add(pack.id);
  }
  return value;
}

export default function App() {
  const [packs, setPacks] = useState([]);
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState(null);
  const [status, setStatus] = useState("loading");
  const [attempt, setAttempt] = useState(0);
  const previewHeading = useRef(null);
  const [personal, setPersonal] = useState(loadPersonalPacks);
  const [workspace, setWorkspace] = useState(null);
  const [practicePack, setPracticePack] = useState(null);
  const [notice, setNotice] = useState("");
  const workspaceAnchor = useRef(null);

  useEffect(() => {
    if (workspace)
      workspaceAnchor.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
  }, [workspace]);

  function savePack(pack) {
    if (personal.error) return personal.error;
    const next = [...personal.packs, pack];
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    } catch {
      return "Your browser could not save the pack. Check available storage and try again.";
    }
    setPersonal({ packs: next, error: "" });
    setWorkspace(null);
    setQuery("");
    setNotice(`“${pack.title}” was added to this browser’s library.`);
    return "";
  }

  function startPractice(pack) {
    setPracticePack(pack);
    setWorkspace("practice");
  }

  useEffect(() => {
    const controller = new AbortController();
    let active = true;
    const deadline = setTimeout(() => controller.abort(), 10000);
    async function load() {
      setStatus("loading");
      try {
        const response = await fetch("/api/packs", {
          signal: controller.signal,
          cache: "no-store",
        });
        if (!response.ok) throw new Error("Library unavailable");
        const data = validatePacks(await response.json());
        if (active) {
          setPacks(data);
          setStatus("ready");
        }
      } catch {
        if (active) setStatus("error");
      } finally {
        clearTimeout(deadline);
      }
    }
    load();
    return () => {
      active = false;
      clearTimeout(deadline);
      controller.abort();
    };
  }, [attempt]);

  useEffect(() => {
    if (selectedId) previewHeading.current?.focus();
  }, [selectedId]);

  const term = query.trim().toLocaleLowerCase();
  const allPacks = [...packs, ...personal.packs];
  const visible = allPacks.filter((pack) =>
    [pack.title, pack.role, ...pack.tags].some((value) =>
      value.toLocaleLowerCase().includes(term),
    ),
  );
  const selected = allPacks.find((pack) => pack.id === selectedId);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="site-header">
        <a href="/" className="brand" aria-label="InterviewCoach home">
          <span className="brand-icon" aria-hidden="true">
            ic
          </span>
          Interview<span>Coach</span>
        </a>
        <span className="header-label">YOUR PREPARATION SPACE</span>
        <span className="local-badge">
          <i aria-hidden="true" />
          Local library
        </span>
      </header>
      <main id="main">
        <section className="hero">
          <div>
            <p className="eyebrow">A LITTLE PRACTICE. A CLEARER NEXT STEP.</p>
            <h1>
              Make room for
              <br />
              your <em>next opportunity.</em>
            </h1>
            <p className="hero-description">
              Find questions for the role you want.
              <br />
              Start with what you know. Build from there.
            </p>
            <a className="primary-button" href="#library">
              Explore the questions <span aria-hidden="true">↗</span>
            </a>
          </div>
          <aside className="hero-note" aria-label="Preparation reminder">
            <span className="note-label">BEFORE YOUR NEXT INTERVIEW</span>
            <p>
              You have a story
              <br />
              worth <em>practising.</em>
            </p>
            <span className="note-line" />
            <p className="note-caption">
              Coursework. Side projects. Helping someone.
              <br />
              Your experience has a starting point.
            </p>
            <span className="note-star" aria-hidden="true">
              ✳
            </span>
          </aside>
        </section>
        <div ref={workspaceAnchor} className="workspace-anchor">
          {workspace === "create" && (
            <PackForm onSave={savePack} onClose={() => setWorkspace(null)} />
          )}
          {workspace === "practice" && practicePack && (
            <Practice
              key={practicePack.id}
              pack={practicePack}
              onClose={() => {
                setWorkspace(null);
                setPracticePack(null);
              }}
            />
          )}
          {workspace === "import" && (
            <AdvertImport
              onClose={() => setWorkspace(null)}
              onUse={(role, requirements) => {
                const terms = [role, ...requirements]
                  .join(" ")
                  .toLowerCase()
                  .split(/\W+/)
                  .filter((term) => term.length > 2);
                const matching = allPacks.filter((pack) =>
                  terms.some((term) =>
                    [pack.title, pack.role, ...pack.tags]
                      .join(" ")
                      .toLowerCase()
                      .includes(term),
                  ),
                );
                setQuery(matching[0]?.role || role);
                setWorkspace(null);
                setNotice(
                  matching.length
                    ? `Showing a pack matching your confirmed advert: ${role}.`
                    : `No existing pack matches ${role}. Clear search to browse, or create your own pack.`,
                );
              }}
            />
          )}
          {workspace === "guidance" && (
            <Guidance onClose={() => setWorkspace(null)} />
          )}
        </div>
        <section
          className="library"
          id="library"
          aria-labelledby="library-heading"
        >
          <div className="section-heading">
            <div>
              <p className="eyebrow">THE QUESTION LIBRARY</p>
              <h2 id="library-heading">Find your starting point.</h2>
            </div>
            <p>
              Thoughtful questions.
              <br />
              One role at a time.
            </p>
          </div>
          {!workspace && (
            <div className="tool-actions">
              <button
                className="secondary-button"
                onClick={() => setWorkspace("create")}
                disabled={Boolean(personal.error)}
              >
                ＋ Create a pack
              </button>
              <button
                className="secondary-button"
                onClick={() => setWorkspace("import")}
              >
                Read a job advert
              </button>
              <button
                className="secondary-button"
                onClick={() => setWorkspace("guidance")}
              >
                Ask the preparation guides
              </button>
            </div>
          )}
          {notice && (
            <p className="notice" role="status">
              {notice}
            </p>
          )}
          {personal.error && (
            <p className="inline-error" role="alert">
              {personal.error}
            </p>
          )}
          {status === "loading" && (
            <p className="state-box" role="status">
              Getting your question library ready…
            </p>
          )}
          {status === "error" && (
            <div className="state-box error" role="alert">
              <h3>We couldn’t load your library.</h3>
              <p>Check that the local service is running, then try again.</p>
              <button
                className="secondary-button"
                onClick={() => setAttempt((value) => value + 1)}
              >
                Try again
              </button>
            </div>
          )}
          {status === "ready" && (
            <>
              <div className="search-row">
                <label className="search-label">
                  <span className="sr-only">
                    Search packs by title, role, or tag
                  </span>
                  <span aria-hidden="true">⌕</span>
                  <input
                    type="search"
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    placeholder="Search by role, title, or tag…"
                  />
                </label>
                <span className="result-count" role="status">
                  {visible.length} of {allPacks.length} packs
                </span>
              </div>
              <div className="pack-grid">
                {visible.map((pack) => (
                  <article className="pack-card" key={pack.id}>
                    <div className="card-top">
                      <span className="pack-number">
                        {String(allPacks.indexOf(pack) + 1).padStart(2, "0")}
                      </span>
                      <span className="question-count">
                        {pack.questions.length} questions
                      </span>
                    </div>
                    <p className="pack-role">{pack.role}</p>
                    <h3>{pack.title}</h3>
                    <p className="pack-description">{pack.description}</p>
                    <div className="tags">
                      {pack.tags.map((tag) => (
                        <span key={tag}>{tag}</span>
                      ))}
                    </div>
                    <button
                      className="card-action"
                      onClick={() => setSelectedId(pack.id)}
                      aria-expanded={selectedId === pack.id}
                      aria-controls={selected ? "pack-preview" : undefined}
                    >
                      View questions <span aria-hidden="true">↗</span>
                      <span className="sr-only"> for {pack.title}</span>
                    </button>
                    {!workspace && (
                      <button
                        className="start-practice"
                        onClick={() => startPractice(pack)}
                      >
                        Practise this pack <span aria-hidden="true">→</span>
                        <span className="sr-only"> {pack.title}</span>
                      </button>
                    )}
                  </article>
                ))}
              </div>
              {!visible.length && (
                <div className="state-box">
                  <h3>No packs found.</h3>
                  <p>Try another role, title, or tag.</p>
                  <button
                    className="secondary-button"
                    onClick={() => setQuery("")}
                  >
                    Clear search
                  </button>
                </div>
              )}
              {selected && (
                <section
                  className="preview"
                  id="pack-preview"
                  aria-labelledby="preview-heading"
                >
                  <div className="preview-top">
                    <div>
                      <p className="eyebrow">INSIDE THE PACK</p>
                      <h2
                        id="preview-heading"
                        tabIndex={-1}
                        ref={previewHeading}
                      >
                        {selected.title}
                      </h2>
                      <p>
                        {selected.role} · {selected.questions.length} questions
                      </p>
                    </div>
                    <button
                      className="secondary-button"
                      onClick={() => {
                        const button = [
                          ...document.querySelectorAll(".card-action"),
                        ].find(
                          (item) =>
                            item.getAttribute("aria-expanded") === "true",
                        );
                        setSelectedId(null);
                        button?.focus();
                      }}
                    >
                      Close preview
                    </button>
                  </div>
                  <ol className="question-list">
                    {selected.questions.map((question) => (
                      <li key={question.id}>
                        <p>{question.text}</p>
                        <span>{question.hint}</span>
                      </li>
                    ))}
                  </ol>
                </section>
              )}
            </>
          )}
          <p className="library-note">
            <span aria-hidden="true">◇</span> A good answer starts with a real
            example.
          </p>
        </section>
      </main>
      <footer>
        <span>
          InterviewCoach <span aria-hidden="true">/</span> Your preparation
          library
        </span>
        <span>A little more ready for what’s next.</span>
      </footer>
    </div>
  );
}
