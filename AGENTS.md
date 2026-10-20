# InterviewCoach: shared application instructions

## Scope and source of truth

Build the shared product in `project/`. Course evidence belongs in root `docs/`,
`data/`, `evals/`, and sanitized `logs/`. Leave individual `hw1/` submissions alone.
Read `docs/spec.md` and `docs/ROADMAP.md` before implementation. The user approved
the roadmap on 20 October 2026 and requested incremental execution. Routine work
inside that approved scope does not require another plan approval.

## Stack and commands

React/Vite frontend; Python 3.12+ FastAPI/Pydantic backend; pytest for offline tests.
Use a project-local virtual environment. From the repository root:

```powershell
python -m venv project/.venv
./project/.venv/Scripts/python.exe -m pip install -r project/backend/requirements.txt
./project/.venv/Scripts/python.exe -m pytest project/tests
./project/.venv/Scripts/python.exe -m uvicorn project.backend.app.main:app --host 127.0.0.1 --port 5191
npm --prefix project/frontend ci
npm --prefix project/frontend run dev
npm --prefix project/frontend run build
```

If `python` is a Windows Store alias, use an installed Python executable for the
first command. See `project/README.md`. Run commands from the repository root.

## Always

- Implement one working increment, run relevant tests, and record actual evidence.
- Validate user input on the server; render user/model text as plain text.
- Keep model access behind `llm.py`; use environment variables or ignored `project/.env`.
- Enforce the user's **$0 total / free models only** limit. Never infer that an
  arbitrary model is free. Verify compatibility before live operations.
- Log operation, outcome, latency, tokens/cost when available; missing means unknown.
- Show uncertain extraction fields empty when missing or unsupported; require review.
- Ground guidance in retrieved sources or refuse. Check citations in code.
- Keep golden questions and failed results. Distinguish mock tests from live runs.

## Ask when needed

Ask for a genuine scope change, paid access, persistent storage of answers/images,
or publication. Human teammate review/approval and the team form remain human work.

## Never

- Never commit keys, uploaded private images, interview answers, or raw prompts/logs.
- Never invent results, signatures, review approvals, journal entries, or past labs.
- Never weaken a test/golden case to hide a failure.
- Never automatically retry or fall back to a paid model.
- Never claim a planned feature or unperformed check is implemented/verified.
- Never push, merge, publish, or create/move grading tags without user authorization.

## Verification and workflow

Feature branch -> tests -> browser check for UI behavior -> truthful delegation
entry -> reviewable diff. CI job is named `test`. Changes to an implemented model
path require mocked failure cases; live evaluation is separate and opt-in.
