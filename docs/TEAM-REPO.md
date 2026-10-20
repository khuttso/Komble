# Team repository guide

## 1. Members and roles

Transcribed from existing [TEAM-CONTRACT.md](../TEAM-CONTRACT.md); no new signatures are asserted.

| Member | GitHub | Primary | Backup |
|---|---|---|---|
| Anastasia Khevtsuriani | aniararis | Specification/evaluation; answer feedback | Integration |
| Luka Khutsidze | khuttso | Repository/integration; interview questions | Spec/evaluation |
| Nikoloz Babunashvili | NikaBabuna | Shared app; pack hub | QA/release |

The existing contract was renamed to the course-required `TEAM-CONTRACT.md` path.
It lists Luka's personal signature commit as pending. That remains human work;
the agent will not impersonate members or invent approval.

## 2. Locations and commands

`project/` is the shared product; `hw1/` contains individual work. Root `docs/`,
`data/corpus/`, `evals/`, and sanitized `logs/` contain team evidence.
Use [project/README.md](../project/README.md) for exact setup/test/run commands.

## 3. Workflow and gates

Spec/issue -> proposed slice -> feature branch -> implementation -> human reads
tests and diff -> real tests -> PR -> CI job `test` -> teammate review -> squash
merge. Keep actual delegation and corrections in `delegation-log.md`.
Main protection/access and teammate approval need real GitHub configuration;
local files alone do not establish them.

## 4. Milestones

Only tag completed, merged work. Lab 3 evidence includes extraction, confidence
policy, fixtures and real clean/degraded runs. Lab 4 includes retrieval, citation
checks, golden results and tuning. `design-review` must identify the main commit
with `docs/DESIGN-REVIEW.md` and linked evidence. The repo keeper submits the team
form. Deadline from the supplied brief: 20 October 2026, 23:59 Asia/Tbilisi.
