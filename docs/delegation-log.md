# Shared application delegation log

## 20 October 2026: foundation

User approved the detailed roadmap, specified `project/` for product source, asked
for incremental work, and authorized **free models only / $0 total**. Codex drafted
the shared spec, roadmap, agent instructions, role transcription, multimodal and
retrieval specifications, and ADR 001. Codex is implementing the foundation API
and React pack library. No teammate review, merge, tags or live model evidence is
claimed. Individual `hw1/` submissions are outside this work.

Initial environment finding: `py --list-paths` reported no installed Python, but a
direct Python 3.13.5 executable was found under the user's Programs directory.
No OpenRouter key is configured in the agent process.

Corrections: virtual-environment bootstrap hit a sandbox temporary-directory
permission failure; running the project-local setup outside that restriction
succeeded. Offline TestClient/server processes also hung in the sandbox; the
approved normal execution completed. Existing ports 5173/5174 were occupied, so
the shared app uses 5190/5191. No existing homework server was stopped.

Verification: 4 offline API tests passed; frontend production build passed; real
browser search, preview, empty-result recovery and service outage/retry passed.
One dependency deprecation warning remains visible. Mobile inspection and model
access are unverified. [Full record and screenshot](verification.md).
The initial slice is implemented on local branch `codex/shared-app-foundation`;
it is not committed, pushed, merged, tagged or claimed to be teammate-reviewed.

## 20 October 2026: practice, multimodal, grounding and review

Codex implemented the approved subsequent slices inside `project/` and drafted
the ten clearly labeled AI-assisted preparation guides. The user supplied a local
key and confirmed the $0/free-only policy. Its misplaced `project.env` file was
moved to ignored `project/.env`; the key was not printed. Generation verifies
zero-price/schema support; embeddings use the documented local CPU model.

Corrections and evidence: the first feedback swapped strengths/improvements;
field descriptions and instructions were clarified, retaining the first result.
Initial golden 2/5 and image 0/4 runs showed truncation. Optional reasoning was
disabled only when advertised. Citation punctuation was corrected without
allowing uncited sentences. Retrieval k increased to 5 after the required
reasoning source ranked fourth. Selected golden result is 4/5, images 4/4;
failed cases remain. This is not a controlled single-variable experiment.

Codex ran 22 offline checks and real browser creation/persistence, practice/draft
navigation, feedback, cited guidance, refusal and degraded-image manual review.
Usage export excludes earlier mocked events; test logs are now isolated. A
full-corpus external comparison was rejected by automatic approval review; no
upload occurred. The replacement counts tokens locally and labels the proxy.

Codex drafted **all six Design Review sections**, including architecture, proposed
risks/owners/dates, evaluation, measured budget and team/decisions. Proposed dates
and human-review work are not claimed as completed. The contract was only renamed
to the required uppercase path; no signature was changed. Teammate review,
remote CI, merge, milestone tags and submission form remain human workflow.
