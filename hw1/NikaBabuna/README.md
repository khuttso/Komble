# InterviewCoach Pack Hub

This folder is my individual HW1 submission: a small, working slice of the InterviewCoach capstone. It is intentionally self-contained so it can be reviewed, run, and verified without changing the shared team application.

## My interpretation of the assignment

I understood HW1 as asking each student to take one focused slice of the larger application from specification to a visible, working mock: write the spec first, delegate deliberately, verify the result, and record the process honestly. On that reading, this slice did not need its own model call or AI integration. Its purpose was to practise agentic engineering through a real but bounded feature, while leaving the team's AI-powered interview features to the shared project.

This is my good-faith interpretation of the classroom repository and the homework brief. The implementation, verification evidence, delegation log, and journal are all kept here so that interpretation is easy to inspect.

## Why this uses a lightweight version of my protocol

I originally considered applying my full agentic-engineering methodology from the [`docs/` folder of MapMakingTool](https://github.com/NikaBabuna/MapMakingTool/tree/main/docs). That methodology grew from lessons learned while working on a startup and from your course emphasis on defining scope, checking agent work, and keeping evidence for claims.

For this small mock feature, the complete protocol would have added more process than the task needed. I used a lightweight version instead:

1. Define scope and acceptance criteria before implementation.
2. Keep the agent inside this folder and out of the shared project.
3. Turn core rules into automated tests and run browser golden checks.
4. Record corrections and incomplete evidence rather than hiding them.

I am mentioning the larger protocol here because it shaped the decisions in this submission, even though the full methodology was unnecessary for a feature of this scale.

## The feature

InterviewCoach is intended to help students and recent graduates prepare for interviews. The Pack Hub gives them a simple starting point before a separate practice or feedback flow:

- browse three locally seeded interview-question packs;
- search packs by title, target role, or tag;
- create a personal pack by entering a title, role, optional tags, and questions;
- keep personal packs in browser `localStorage`; and
- preview every question in a selected pack.

The project is a React/Vite mock. It intentionally uses no account system, database, cloud storage, external API, AI model, or file upload. Those boundaries are part of the approved feature scope in [spec.md](spec.md).

## Run and verify

From this folder:

```bash
npm install
npm test
npm run build
npm run preview
```

`npm test` runs the offline JavaScript acceptance checks. To run the course-required Python entry point from the repository root, ensure `pytest` is installed and run:

```bash
pytest hw1/NikaBabuna
```

The real browser checks and their results are in [golden.md](golden.md). The implementation record is in [delegation.md](delegation.md), and the Week 1–4 reflections are in [journal.md](journal.md).

## Folder map

| Path | Purpose |
| --- | --- |
| [spec.md](spec.md) | Problem, users, acceptance criteria, context, and boundaries. |
| [golden.md](golden.md) | Three browser-oriented golden questions and results. |
| [delegation.md](delegation.md) | Delegation, corrections, and verification record. |
| [journal.md](journal.md) | Pattern Journal for Weeks 1–4. |
| [AGENTS.md](AGENTS.md) | Operating constraints for agents working in this folder. |
| [src/](src/) | React application and JavaScript tests. |
| [tests/](tests/) | Required `pytest` entry point and browser evidence screenshots. |
