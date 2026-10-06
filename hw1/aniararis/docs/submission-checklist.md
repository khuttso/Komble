# HW1 submission checklist · InterviewCoach

Student: `aniararis` · Individual submission · Due: Thursday of Week 4, 23:59 Tbilisi time. The materials do not establish the corresponding calendar date here.

## Required deliverables

| Requirement | File(s) | Current state |
|---|---|---|
| One-page specification written before code | `spec.md` | Written before implementation; current model/cost note updated |
| Agent instructions | `AGENTS.md` | Present with actual project commands |
| Working feature and runnable source | `src/`, `data/`, `InterviewCoach.slnx`, project files | Implemented and locally tested; reliable live feedback remains limited by provider failures |
| Three golden questions/cases with results | `golden.md` | Three real cases documented, including failures and evidence limits |
| Half-page delegation log | `delegation.md` | Concise account of real delegation, problems, and verification |
| Pattern Journal for Weeks 1–4 | `journal.md` | Actual timeline recorded: no project work in Weeks 1–2, idea/team setup in Week 3, app setup/testing in Week 4; student wording review remains |

## Supporting files to commit

Include `README.md`, `.gitignore`, `NuGet.Config`, `tests/`, and `docs/` alongside the required documents and source. Keep the three required feedback files and all project/data/prompt files needed for a fresh clone to run.

Do not commit API keys, private Rider settings, `.local/`, `bin/`, `obj/`, or `TestResults/`. The submission's `.gitignore` excludes generated files. Safe test-summary evidence is in `docs/verification.md`.

## Before submission

- [ ] Review the generated code and documents so you can explain them.
- [ ] Review the journal in your own voice and add any actual Week 1–2 course exercises if applicable; no InterviewCoach activity is claimed before Week 3.
- [ ] Run `dotnet test InterviewCoach.slnx --no-restore` yourself after restore, and record your actual result if you do so.
- [ ] When the provider is available, append real feedback for Cases 1 and 2 and the timing/safety checks. Preserve failures. If unresolved by the deadline, explicitly document why, as the brief allows; do not claim all criteria pass.
- [ ] Confirm instructor acceptance of C#, since the provided materials explicitly name Python and Node.js.
- [ ] Commit and push your individual homework branch.
- [ ] Open a pull request, complete required checks, and have a teammate review folder boundaries and merge according to the course workflow.
- [ ] Complete your individual submission form linked on Teams. Uploading files alone is not the final submission step.

HW2 is a separate later assignment; its tool implementation is not part of this HW1 submission.
