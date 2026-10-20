# Shared InterviewCoach specification v1

Approved direction: 20 October 2026. Product source: `project/`. Implementation
status is tracked in [ROADMAP.md](ROADMAP.md) and [verification.md](verification.md).

## Problem and users

Students and recent graduates preparing for entry-level interviews need a way to
choose relevant questions, practise truthful answers, and understand how to improve
without inventing experience or relying on unsupported coaching claims.

## Product and data

Three connected journeys: browse a role pack and practise; import role/requirements
from a job-advert screenshot with human confirmation; ask preparation questions
answered from the team's versioned guidance corpus. Starter packs ship with the
app; personal packs persist in the same browser. Answers/feedback remain in page
memory. Images are processed temporarily. The corpus is versioned; its index is
rebuildable. No accounts, database, CVs, voice, hiring predictions, or deployment.

## Four measurable release criteria

1. **Practice:** starting with any starter or personal pack, select a question,
   submit a 1–3,000-character trimmed answer, receive three validated feedback
   sections, and advance. Invalid input makes zero model calls. Timeout/provider
   errors preserve the answer and trigger no automatic retry. Browser and mocked
   API tests must demonstrate the flow; live quality is evaluated separately.
2. **Extraction:** schema-validated fields include nullable value/evidence and
   confidence; image longest side <=1024 px before sending. Missing/unsupported
   required fields cannot auto-accept or be prefilled with guesses. Clean and
   degraded live fixtures plus >=3 offline routing tests provide evidence.
3. **Grounding:** a five-case live golden run is saved with honest outcomes. No
   retrieved chunk above threshold means no generation call. Unknown/missing
   citations and uncited answer sentences cause refusal. Offline tests prove each
   rule. Retrieval tuning retains baseline and changed-setting results.
4. **Operations:** every model operation and guidance refusal records outcome,
   timing, reason and available usage, excluding answers/images/keys. User budget
   is **$0 total / free models only**. Requests have a 20-second model timeout,
   bounded output and no paid fallback. Report actual latency/cost and unknowns;
   the proposed guidance target is <=15 s for 9/10 deliberate trials, unverified
   until measured. Failed calls count as failed trials.

## First slice: foundation (at most three criteria)

1. A local FastAPI health endpoint and validated starter-pack endpoint run without
   provider credentials. Library contains >=3 packs with unique question IDs.
2. React loads that API, filters by title/role/tag, and previews all questions in
   a selected pack, including an explicit empty-search state.
3. An unavailable API shows an actionable retry state; offline API tests and the
   frontend build run with documented commands. This slice makes no model calls.

## Context boundaries

Feedback receives only current question/answer, trusted rubric and instructions.
Extraction receives a downscaled image and extraction schema. Grounded guidance
receives query and retrieved chunks, never arbitrary files or interview history.
External processing is disclosed before submissions once model paths exist.
