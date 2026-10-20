# AGENTS.md · InterviewCoach Pack Hub

Instructions for AI coding agents working only in `hw1/NikaBabuna/`.

## What this project is

InterviewCoach Pack Hub is a small React web application for students and recent graduates preparing for interviews. It lets a user browse locally seeded interview-question packs, search them by title, role, or tag, add a personal pack, and preview its questions.

This is a local mock. It does not use a database, external API, AI model, login, or cloud storage.

## Source of truth

Read these files before making a change:

1. `spec.md` — approved feature scope and acceptance criteria
2. This file — operating constraints
3. `golden.md` — current verification evidence
4. `delegation.md` — record meaningful agent work and corrections

If a requested change conflicts with `spec.md`, or expands its scope, stop and ask.

## Stack

- Runtime: Node.js 20.19+ or 22.12+ (tested with Node.js 22.16.0)
- UI: React, scaffolded with Vite
- Styling: plain CSS; no UI component library
- Data: locally seeded JavaScript data and browser `localStorage`
- Network/model access: none
- Testing: Node.js built-in test runner; Python and `pytest` only for the course test entry point

## Commands

Run from `hw1/NikaBabuna/`:

```bash
npm install
npm run dev
npm test
npm run build
npm run preview
```

The course test command, run from the repository root with Python, `pytest`, and Node.js available, is:

```bash
pytest hw1/NikaBabuna
```

`tests/test_pack_hub.py` runs the same JavaScript checks as `npm test`. These exercise the real search, form-validation, and storage helpers; the storage tests use an in-memory substitute. They do not replace the three browser checks in `golden.md`. A successful build alone does not prove browser behavior. Source entry points and setup instructions are documented in `src/README.md`.

## Working order

1. Read the spec before changing code.
2. For any non-trivial change, state the exact files to be changed and wait for approval.
3. Implement the smallest change that satisfies the approved acceptance criteria.
4. Run `npm test`, the course `pytest` entry point when available, and `npm run build` for code changes; run the relevant browser check for UI behavior.
5. Update `golden.md` with actual results only.
6. Record meaningful delegation, mistakes, corrections, and checks in `delegation.md`.

## Conventions

- Keep components small and named for one UI responsibility.
- Keep seeded packs separate from UI code.
- Read and write personal packs through one `localStorage` helper.
- Treat pack titles, roles, tags, and questions as plain text; do not render them as HTML.
- Validate before saving: title, target role, and at least one non-empty question are required.
- Keep all user-facing text clear and concise.
- Prefer no new dependency. Ask before adding any package beyond the approved React/Vite setup.

## You may

- Create and edit files within this HW1 folder.
- Create the React application under `src/`.
- Edit `spec.md`, `golden.md`, and `delegation.md` when the change truthfully reflects approved work.
- Add a small test or helper that directly verifies an acceptance criterion.

## You may not

- Edit files outside `hw1/NikaBabuna/`.
- Change `docs/protocol/`, teammate homework folders, shared application files, CI configuration, or secrets.
- Add a database, authentication, cloud storage, real AI/API calls, file import/export, or interview-feedback logic.
- Delete or weaken a golden question to make work appear successful.
- Invent passing results, delegation events, or journal reflections.
- Commit `node_modules/`, API keys, or `.env` files.

## Definition of done

The feature is complete only when:

- all six acceptance criteria in `spec.md` hold;
- the automated checks pass through both `npm test` and the course `pytest` command;
- the production build succeeds;
- all three golden questions have real results;
- failures are fixed or honestly documented;
- `delegation.md` reflects the actual collaboration; and
- no out-of-scope feature was added.
