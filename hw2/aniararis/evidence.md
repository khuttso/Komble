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
with the existing backend pins. After installing both committed requirements files,
`python -m pytest project/tests tests -q` passed **58 tests in 7.32 seconds**:
28 existing backend checks plus 30 tool checks. This final run used Pydantic 2.14.1,
pytest 9.1.1 and PyYAML 6.0.3 with MCP 2.3.0. It verifies the new adapter alongside
the existing application under the pinned dependencies. No frontend files changed;
the frontend build remains in CI and was not rerun locally for this backend change.

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

## Remote evidence · updated 28 November 2026

| Requirement | Status |
|---|---|
| Product branch green CI | [Passing run](https://github.com/khuttso/Komble/actions/runs/46029627824); product PR still pending |
| Red CI | [Failed branch run](https://github.com/khuttso/Komble/actions/runs/46029627291), [PR run](https://github.com/khuttso/Komble/actions/runs/46072627282), [red PR #4](https://github.com/khuttso/Komble/pull/4) |
| Failed check actually blocks merge | Not demonstrated. The screenshot shows a missing-review block; the test check was not required. The user chose to skip this enforcement step. |
| Product and write-up merged to main | Pending actual review and merge |

The user pushed all three branches and opened red PR #4. Its screenshot shows
failed checks and merging blocked because one approving review is missing.
This establishes failed CI, but not the required test-based merge block; that
assignment requirement remains incomplete. Close the red PR without merging.
The connector returned HTTP 403 when attempting both PR creation and closure,
so neither action is claimed. Product/write-up review and merge remain pending.
