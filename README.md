# InterviewCoach

A local app for students and recent graduates preparing for entry-level interviews.
The shared product lives in [`project/`](project/README.md); individual homework
remains in `hw1/`.

- Browse, search and create personal question packs.
- Practise written answers with strengths, improvements and an actionable next step.
- Read a job-advert screenshot and confirm uncertain fields before selecting a pack.
- Ask preparation questions with inspectable citations or an honest refusal.

[Setup and run](project/README.md) · [Specification](docs/spec.md) ·
[Design Review](docs/DESIGN-REVIEW.md) · [Verification](docs/verification.md) ·
[Team workflow](docs/TEAM-REPO.md)

Current local evidence: 28 offline checks; successful frontend build; **4/5 live
golden cases**; **4/4 synthetic image routing cases**; actual provider usage logs.
Earlier failures are retained. Human corpus/code review, a missing contract signature,
remote CI, merge/tag/form submission and mobile inspection remain outstanding.

Free models only: user-authorized provider budget $0. Private configuration belongs
in ignored `project/.env`; no key or personal interview answer belongs in Git.
