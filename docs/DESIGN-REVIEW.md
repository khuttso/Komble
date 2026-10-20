# InterviewCoach · Team Design Review
**Anastasia Khevtsuriani · Luka Khutsidze · Nikoloz Babunashvili**

Revised 21 October 2026 against `main` commit `6553a18`. Evidence below is from the repository’s saved 20 October runs, not new live runs. Human review and submission remain unconfirmed.

## 1. Problem, users and intended outcome

Students and recent graduates need relevant entry-level interview questions, actionable feedback on truthful examples, and preparation guidance with inspectable sources. InterviewCoach connects question packs, written practice, job-advert screenshot import and sourced guidance in one local application. It is a practice aid, not a hiring predictor.

The [shared specification](spec.md) requires validated answers and recoverable errors; cautious image extraction with human confirmation; cited guidance or refusal; and privacy-conscious usage logging with free-only model access. Current evidence supports the implemented flows, but the live golden target is incomplete at **4/5**, and the proposed 9/10-under-15-seconds latency target is unverified. Accounts, persistent answer history, voice interviews and deployment are outside the current scope.

## 2. Architecture and data flow

The shared product in `project/` uses React/Vite and FastAPI/Pydantic. Individual C# and React homework remains separate. The application has three model paths:

| Path | Data flow and boundary |
|---|---|
| Written practice | Student selects a starter/personal question → server validates question and 1–3,000-character answer → `llm.py` sends the current exchange and rubric → validated feedback sections return as plain text. Errors preserve the draft. |
| Job-advert import | JPEG/PNG under 2 MB → decode and downscale to at most 1,024 px on the longest side → vision extraction → schema, field/evidence and uncertainty checks → student reviews/corrects fields before use. |
| Sourced guidance | Query → local embedding → cosine retrieval over the versioned corpus → top five passages filtered at 0.55 → generation with numbered sources → citation checks → cited answer or refusal. No accepted passage means no generation call. |

Starter packs and ten AI-assisted preparation guides are versioned. Personal packs use browser localStorage; answer drafts/feedback remain in page memory, and images are processed temporarily. External processing is disclosed. Logs contain allowlisted operation, outcome, timing and available usage metadata, excluding answers, images and keys.

Local CPU embeddings use `BAAI/bge-small-en-v1.5`; the index records model, dimension and corpus hash and rejects incompatible/stale data. Generation passes through a single gateway that checks zero-price `:free` model compatibility, caps requests at 24 per process, bounds output, applies a 20-second HTTP timeout and disables provider fallback. There is no automatic paid retry. The timeout is not a demonstrated end-to-end latency guarantee.

Citation checks require valid source numbers and a citation on every answer sentence. They do not prove semantic support; human source review remains necessary. [Implementation](../project/backend/app/grounding.py) · [Storage/stack decision](decisions/001-shared-app-stack.md).

## 3. Risks and safety threats

| Risk | Implemented mitigation | Remaining check / proposed owner |
|---|---|---|
| Invented or misplaced feedback | Fixed rubric, schema validation, no hiring guarantees; initial swapped praise/criticism retained in evidence | Human quality review / Anastasia |
| Unsupported advice or false refusal | Retrieval threshold and sentence/source citation checks | Review semantic support and failing truthful-achievements case / Anastasia |
| Incorrect screenshot fields | Nullable values/evidence, consistency and ambiguity checks, mandatory review | Real phone photos beyond synthetic fixtures / Nikoloz |
| Private data exposure | External-processing disclosure, temporary inputs, no private-content logs, ignored keys | Review disclosure and provider retention implications / Luka |
| Prompt injection | Untrusted content separated from instructions; narrow output schemas and plain-text display | Live adversarial cases; message separation alone is insufficient / Luka |
| Provider outages or spend | Zero-price catalog validation, bounded requests, no paid fallback, preserved drafts | Free capacity is not guaranteed; process restart resets call cap / Luka |
| Lost packs or weak sources | Storage limitations disclosed; versioned corpus labelled AI-assisted | Review corpus and assess export needs / Nikoloz |

Owners above follow the contract’s roles and require team confirmation. Safety failures should block release even when aggregate evaluation scores look acceptable.

## 4. Evaluation and golden-set results

The [five-case golden set](../evals/golden.yaml) runs the same guidance service used by the API. The saved baseline scored **2/5**; the selected [20 October run](../evals/results/20261020T193257001485Z.json), at 23:32 Tbilisi time, scored **4/5 (80%)**:

| Case | Expected | Recorded result |
|---|---|---|
| STAR definition | Situation, Task, Action, Result; cite structure guide | PASS; 4,419 ms |
| Inventing a percentage | Explain not to invent metrics; cite truthful-achievements guide | FAIL; application refused (`invalid_citations_or_ungrounded`); 3,465 ms |
| Coursework without employment | Combine limited-experience and STAR guidance | PASS; 3,798 ms |
| “temwork” typo | Explain personal contribution; cite teamwork guide | PASS; 2,260 ms |
| Weather and stock request | Refuse outside-corpus request | PASS; below threshold, no generation; 16 ms |

These are mechanical pass/fail checks, not independent human quality ratings. [ADR 003](decisions/003-retrieval-tuning.md) records increasing retrieval k from three to five because a needed second source ranked fourth. Reasoning settings and citation-punctuation handling also changed, so improvement cannot be attributed solely to retrieval k.

Existing [verification](verification.md) reports 28 offline checks, a successful frontend build and browser flow checks. The selected [synthetic image run](evidence/images-20261020T193252Z.json) passed 4/4 routes; earlier failures are retained. These results were not rerun for this documentation revision. Anastasia’s individual C# HW1 has different live results and must not inherit these passes.

Next evaluation: fix and retest the answerable refusal, obtain human support judgments, add real photos and adversarial inputs, and measure ten deliberate end-to-end timing trials. Proposed Week 11 set: ten cases (3 factual, 2 reasoning, 2 edge, 2 refusal, 1 format). Proposed gate: at least 8/10 overall, both refusals correct, and no known invalid-citation displays or automatic paid calls.

## 5. Token budget from recorded logs

The [sanitized usage log](../logs/verified-usage.jsonl) and [computed summary](../logs/budget-summary.json) record:

| Operation | Sample size | Mean input / output tokens | Mean model latency | Reported mean cost |
|---|---:|---:|---:|---:|
| Latest browser feedback | 1 | 234 / 153 | 5.094 s | $0 |
| Latest golden generations | 4 | 821.75 / 82 | 3.162 s | $0 |
| Completed extraction | 5 | 1,042.4 / 87.2 | 2.106 s | $0 |

Generation model recorded in the summary: `dots-studio/dots-3-note-preview:free`. The four golden generation rows include one model response subsequently refused by application checks. Across all 25 real generation rows, seven failures remain recorded; selected successful-operation samples are not an overall reliability rate. Missing usage means unknown. Local embeddings use no provider tokens.

Planning workload: 20 users/month × (10 feedback + 10 guidance + 1 import) = **420 requests/month**. Applying observed means gives approximately **232,998 input and 48,744 output tokens/month**, assuming every guidance request generates. At the recorded zero provider prices, estimated token charges are **$0/month**, excluding hosting/hardware and without a capacity guarantee.

The [local context comparison](evidence/context-comparison.json) counts 677 retrieved-context versus 1,311 full-corpus BGE tokens: **48.36% less passage text**. These are local-tokenizer proxies, not measured generation-provider savings or a live long-context comparison. RAG is chosen for bounded context and pre-generation refusal, accepting index complexity.

## 6. Team, decisions and delivery status

Per [TEAM-CONTRACT.md](../TEAM-CONTRACT.md), Anastasia owns specification/evaluation and answer feedback; Luka owns repository/integration and interview questions; Nikoloz owns shared application engineering and Pack Hub. Backup responsibilities support integration, review and QA. Luka’s signature is listed as pending; no approval or signature is supplied on his behalf.

Key decisions are the [shared Python/React stack](decisions/001-shared-app-stack.md), [free local embeddings](decisions/002-free-local-embeddings.md), and [retrieval tuning](decisions/003-retrieval-tuning.md). Existing implementation and evidence are already on inspected `main` through merge `6553a18`; this revised review is a local draft. Codex drafted this revision from repository evidence. Team code/corpus review and agreement on follow-up work are still needed.

The supplied deadline was **20 October 2026, 23:59 Tbilisi**, which has passed at revision time. No `design-review` tag was advertised by the inspected remote clone. Revised-document merge, tag publication and Teams form submission are not claimed. The repo keeper must confirm the permitted submission process; do not backdate evidence or claim an on-time submission without evidence.
