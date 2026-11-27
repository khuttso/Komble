# HW2 evidence · aniararis

Recorded 27 November 2026. Tool: `get_pack_questions`. Agent-run local checks;
no model, API key, external generation request or private interview answer used.

## Five golden results

| Case | Input | Expected | Actual local result |
|---|---|---|---|
| frontend-two | frontend, limit 2; visitor | Two questions, total 4 | PASS through dispatcher and MCP |
| support-one | support, limit 1; synthetic caller context | One question, total 4 | PASS through dispatcher and MCP |
| graduate-default | graduate; no limit | Four questions | PASS through dispatcher and MCP |
| zero-limit | frontend, limit 0 | Refuse before execution | PASS; actionable invalid-arguments message |
| forged-identity | support, limit 1, user_id somebody-else | Refuse extra identity field | PASS; identity/extra-fields message |

The MCP server exposes public reads only and does not need caller identity. The
direct golden runner supplies synthetic trusted caller context; neither interface
accepts identity in model-controlled arguments.

## Local verification

`python -m pytest tests -q`: **30 passed** after restoring the strict contract.
This includes five golden cases, set completeness, bad-input execution guards,
current-catalogue reuse, non-mutation, logging/error redaction, both-door schema
and result comparisons, and an actual stdio subprocess/client call.

`python -m src.demo_tool` returned `frontend-web` and `frontend-accessibility`,
their existing question text/hints, `returned: 2`, and `total: 4`.

Initial local test environment: Python 3.12.3, MCP 2.3.0, Pydantic 2.14.4,
pytest 9.2.0, PyYAML 6.0.4. Repository requirements align Pydantic/pytest/YAML
with the existing backend pins; exact combined-environment verification is separate.

## Contract-weakening experiment

Codex temporarily changed only `extra="forbid"` to `extra="ignore"` locally.
Running `tests/test_tool_golden.py` produced **1 failed, 5 passed**, exit code 1.
The failed case was `aniararis:forged-identity`: the weakened contract silently
accepted the supplied identity field and returned questions. Restoring `forbid`
returned the entire tool suite to **30 passed**. No weakened code is in the good
product commit.

The experiment shows why a public read tool still needs a strict contract:
silently ignoring an identity field makes the caller's request appear accepted
and hides a contract regression. The normal calls remained valid, so they alone
would not have caught it. Running the explicit adversarial case turns that mistake
into a test failure. This local result does not prove a blocked GitHub merge.

## Remote evidence still required

| Requirement | Status |
|---|---|
| Product PR / green CI URL | Not created; Git push authentication failed in the agent environment |
| Red CI run URL | Not created; local mutation evidence above is not a substitute |
| Failed check actually blocks merge | Not verified; main was unprotected at inspection |
| Product and write-up merged to main | Pending actual review and merge |

GitHub's connector also rejected issue creation with HTTP 403, “Resource not
accessible by integration.” After repository access is available, follow
`docs/HW2-RUNBOOK.md` on the product branch to create the issue, run the throwaway
red PR, retain the real URLs and close it without merging. Update this table with
those observations before submitting. The existing main CI run predates HW2 and
is not evidence that these new tests ran remotely.
