# Shared InterviewCoach app and Design Review evidence

The repository previously contained individual homework prototypes without a
shared practice app. This change adds the product in `project/`: pack browsing
and browser-local custom packs, question-by-question written practice with free
AI feedback, job-advert extraction with human correction, and document-grounded
guidance with checked citations and refusal.

The Python gateway enforces free model selection and zero advertised pricing,
bounded requests and no automatic paid fallback/retry. Local CPU embeddings build
a model-tagged index from ten versioned preparation guides. Root course documents
link to real tests, live evaluations and sanitized usage. The existing contract
is renamed to the required path without changing signatures.

Validation: 28 offline tests passed; frontend build passed; real browser checks
covered custom-pack persistence, practice/draft navigation and feedback, cited
guidance/refusal, and degraded-image review/correction. Latest live golden run is
**4/5**; image routing is **4/4 synthetic cases**. Earlier failures are retained.

Review the remaining false refusal, corpus content, $0 quota assumptions, pending
signature and proposed risk owners/dates. No mobile or ten-trial latency success,
historical lab gates, teammate approval, remote CI, merge, tags or form completion
is claimed. See `docs/DESIGN-REVIEW.md` and `docs/SUBMISSION-CHECKLIST.md`.
