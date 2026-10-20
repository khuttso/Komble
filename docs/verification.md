# Shared app verification

## Foundation: 20 October 2026

Checks below were run by Codex against the new `project/` application, not the
homework. No model calls were made; model quality, cost, latency and availability
remain unverified. No human review or remote CI success is claimed.

| Check | Observed result |
|---|---|
| Python runtime | Python 3.13.5; isolated `project/.venv` |
| Offline API tests | **4 passed**, 0 failed, 0 skipped; 0.58 s |
| Production frontend build | **Passed**; Vite 8.3.4, 16 modules transformed |
| Browser API integration | Three packs loaded from the real local backend |
| Case-insensitive search | `FrOnTeNd` returned 1 of 3 packs, frontend only |
| Preview | All four frontend questions/hints displayed; heading received focus |
| Close preview | Preview closed and the triggering control regained focus |
| Empty search and recovery | `no-such-role-xyz` returned 0 of 3; Clear search restored all three |
| Real API outage | Stopped our backend, reloaded page: readable unavailable-service message and Try again |
| Retry recovery | Restarted backend; Try again restored all three real packs |
| Visual inspection | Library inspected at the in-app browser's current desktop/tablet-width viewport |

Commands from the repository root:

```powershell
./project/.venv/Scripts/python.exe -m pytest project/tests -q
npm --prefix project/frontend run build
```

Test coverage: health does not expose an injected environment secret; pack and
question IDs are unique with nonempty required content; unknown/unimplemented
routes return 404; API responses disable caching and set `nosniff`.
The dependency emits one Starlette deprecation warning for its HTTPX-backed test
client. It does not fail the suite; no warning was hidden.

[Inspected library screenshot](evidence/foundation-library.png).

## Environment findings and limits

The sandbox's temporary directory blocked pip bootstrapping, and sandboxed local
API tests/server startup hung. Project-local dependency installation, tests and
loopback serving completed outside that execution restriction after automatic
approval. No certificate checks or OS protections were disabled. Dependency
versions are pinned in `project/backend/requirements.txt` and the frontend lockfile.

Ports 5173 and 5174 were already occupied. The shared app uses frontend **5190**
and backend **5191**, without stopping existing homework servers. Both bind to
127.0.0.1. The current browser/server setup is for local development.

Mobile-width inspection was not performed; responsive CSS exists but is not
claimed as verified on a phone. The CI workflow is written but has not run remotely.
The key was absent during the foundation. Follow-up operations are recorded below;
no paid model was used.

## Integrated prototype: 20 October 2026

- Offline safety suite: **22 passed**, 0 failed, 0 skipped (1.78 s latest run at
  this point); one visible dependency deprecation warning. Tests isolate logs and
  mock every provider call. Source: `project/tests/`.
- Built local index: ten chunks, 384 dimensions, BAAI/bge-small-en-v1.5. Public
  weights downloaded once; local CPU inference. [Manifest](evidence/index-manifest.json).
- [Golden baseline](../evals/results/20261020T193019665098Z.json): **2/5**;
  [selected run](../evals/results/20261020T193257001485Z.json): **4/5**. The
  truthful-achievements case still refuses despite a relevant source. It remains FAIL.
- [First image run](evidence/images-20261020T193142Z.json): **0/4**, truncated model
  outputs. [Rerun](evidence/images-20261020T193252Z.json): **4/4** after disabling
  optional reasoning. Fixtures are explicitly synthetic. Real-photo accuracy is unproven.
- [First feedback](evidence/live-feedback-initial.json) validated structurally but
  swapped praise/criticism labels; [retest](evidence/live-feedback.json) improved
  after schema descriptions/instructions were clarified. No 10-trial latency claim.
- Real model selected by zero-price/schema/vision capability checks:
  `dots-studio/dots-3-note-preview:free`. No paid fallback or automatic retry.
  [Usage export](../logs/verified-usage.jsonl), [budget summary](../logs/budget-summary.json).

### Additional real browser checks

Created a two-question QA Intern Practice pack, refreshed, and observed it persist.
Started its first custom question, rejected an empty answer, submitted a synthetic
answer with disclosure acknowledgment, and observed real strengths/improvements/
suggestion. Next/previous navigation retained the draft and corresponding feedback.
Ending the session returned to the library. [Feedback screenshot](evidence/practice-feedback.png).

Asked the STAR golden question through the UI and expanded its actual source
passage. Asked the unrelated weather/stock question and observed refusal. Runtime
events show query embedding and below-threshold refusal without generation for
that refusal. [Answer](evidence/grounded-answer.png), [refusal](evidence/grounded-refusal.png).

Uploaded the synthetic degraded advert through the real file picker. The result
showed **review**, with role and seniority fields empty and readable reasons.
Manually entered Frontend Developer, confirmed, and observed the matching library
pack. [Empty-field review screenshot](evidence/degraded-review.png).

### Limits and approval boundary

The user created a key file as root `project.env`; it was moved into the intended
ignored `project/.env` without printing the key. Environment variables take priority.
No secret is included in evidence. The full-corpus external comparison was rejected
by automatic approval review as broader egress than the retrieved-passage flow;
no such request ran. The replacement [comparison](evidence/context-comparison.json)
counts tokens locally using a different tokenizer from generation.

Independent teammate review, contract completion, remote CI, main merge, grading
tags and team form are not established by local checks. No historical lab review
gates or signatures have been fabricated.

## Final regression check

After request/citation fixes, the sanitized per-field extraction contract and
source formatting: **28 passed**, 0 failed, 0 skipped, 1.43 s; the same dependency
deprecation warning remains visible. Application/tool compilation also passed.
The frontend production build passed again (18 modules, 206 ms). Additional
checks cover nonzero ancillary pricing on a free-suffixed model, malformed model
JSON with no retry, safe API provider errors, index dimension mismatch, and
high-confidence mixed seniority requiring confirmation, and value/evidence/confidence
responses that do not leak unsupported guesses. No further live request
was needed for these checks.
