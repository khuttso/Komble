# Verification record · 2026-10-06

Checks below were performed by the coding agent. They are not claims that the student has independently reviewed or run them.

**Current status:** the latest code regression run passed **44/44 mocked tests**. The student ran live app tests and a diagnostic; the diagnostic returned Google AI Studio HTTP 429 with `limit_source=upstream_provider_shared_pool`. The previous quota query showed 6/50 used and 44 remaining. That identifies the latest diagnostic's provider limit, not the cause of every earlier failure. `golden.md` records two student-tested answers and the agent-tested empty-answer case. Reliable live feedback and the latency target remain unverified.

## Completed

- Application build: **passed, 0 warnings and 0 errors**, using .NET SDK 10.0.103.
- xUnit suite: **32 passed, 0 failed, 0 skipped**, approximately 21 seconds. Includes HTTP routes, validation boundaries, unknown question IDs, request/message composition, usage redaction, malformed/truncated output, missing credentials, provider/network failures, and a real 20-second cancellation check.
- Browser checks in headless Microsoft Edge: **10 passed**. Checked page/question/assets, empty-answer rejection without a feedback request, 3,001-character rejection, real backend configuration error, mocked feedback display and timing label, stale feedback removal, mocked timeout with answer preservation, plain-text rendering of model HTML, a 390px mobile layout without horizontal overflow, and no JavaScript errors.
- Desktop and mobile screenshots were visually inspected by the agent.
- **Real model calls: 0.** Automated tests replace the outbound HTTP transport. Browser success, timeout, and HTML-output cases use intercepted mock responses.

## Test environment note

The restricted automation environment could not read the default NuGet configuration as required by the SDK, and its .NET HTTPS client then reported a Windows TLS authentication error when restoring packages. Verification used process-local configuration/cache folders under ignored `.local/`, with the exact pinned NuGet packages and their transitive dependencies downloaded from `api.nuget.org` using Node's HTTPS support. Restore then used that local package feed, without disabling TLS certificate checks. NuGet vulnerability auditing was disabled for that offline restore only; this run is not a vulnerability audit.

The repository's `NuGet.Config` still uses the ordinary official NuGet source. The standard user commands are in `README.md`; `.local/`, build output, and `TestResults/` are ignored by Git.

The verified commands, after isolated restore, were:

```text
dotnet build src/InterviewCoach/InterviewCoach.csproj --no-restore
dotnet test InterviewCoach.slnx --no-restore --logger "trx;LogFileName=automated-tests.trx" --results-directory TestResults
```

## Not yet verified

- Model access and compatibility for the student's selected OpenRouter model.
- Real feedback relevance, clarity, completeness, and resistance to the adversarial prompt.
- The success target of 9/10 real requests displayed within 15 seconds.
- Actual token usage for successful feedback (the current free model's published $0 token price is recorded in `spec.md`).
- Independent student code/test review and final review of the written journal. Its project timeline is now confirmed: idea/team setup in Week 3, app setup/testing in Week 4.

Passing mocked tests proves application behavior under the tested responses; it does not prove real model quality or performance. Complete the pending cases in `golden.md` before treating the assignment as finished.

## Follow-up: live Case 1 failure and response-handling revision

The student supplied a screenshot showing Case 1 rejected as incomplete/unreadable feedback. That attempt is recorded as FAIL in `golden.md`; it is not overwritten by later tests. The selected model is `apodex/apodex-1.1-mini:free`.

The initial 600-token budget may have been exhausted by reasoning, but the exact failure mechanism is unconfirmed because the old log did not record the finish reason. OpenRouter's public model metadata lists optional reasoning and structured-output support. The revision disables optional reasoning for this specific model family, requests a strict three-field JSON schema, raises the bounded output cap to 1,200, and logs only safe diagnostic metadata. It continues to reject incomplete feedback and makes no automatic retries.

Regression run: **34 passed, 0 failed, 0 skipped**, approximately 20 seconds. This includes all prior tests and new checks for the selected model's request settings and reasoning-only truncation without leaking reasoning content. The report is `TestResults/response-fix-tests.trx`.

Tests used a separate ignored build-output folder (`.local/response-fix-artifacts`) so the student's running app was not stopped or overwritten. Restart the app with a rebuilding `dotnet run --no-restore --project src/InterviewCoach/InterviewCoach.csproj` command before retesting. No new live model call was made by the agent. The live result of this revision remains pending.

## Follow-up: provider rejection diagnostics

The student reported a generic provider rejection and supplied an old-format log with no upstream status, no token usage, and `elapsed_ms=795`. The log cannot distinguish invalid credentials, request incompatibility, account limits, or provider failures. The Case 1 retest remains FAIL.

The diagnostic revision now displays safe, status-specific explanations and logs numeric upstream HTTP/error codes. It also correctly handles HTML error pages and errors embedded in successful HTTP responses, without exposing raw provider text or adding retries.

Regression run: **44 passed, 0 failed, 0 skipped**, approximately 21 seconds. Added coverage checks eight status-specific errors with non-JSON bodies, and numeric/string error codes in HTTP 200 responses. Report: `TestResults/provider-error-tests.trx`. The separate test output directory again avoided changing the running application. No live calls were made by the agent; a restart and a single live retest are needed to identify the student's upstream rejection.

## Follow-up: HTTP 400 compatibility correction

The student subsequently reported OpenRouter code 400. The new strict-schema and optional-reasoning request controls have been removed, returning to JSON-object mode that previously succeeded in a student live trial. The 1,200-token cap and local validation of all three non-empty fields remain. No provider-specific reasoning override is sent. This is a compatibility correction based on observed behavior; the exact rejected field is still unknown.

Regression run: **44 passed, 0 failed, 0 skipped**, approximately 21 seconds; report `TestResults/json-compatibility-tests.trx`. The updated compatibility fixture rejects schema/reasoning overrides and verifies that the selected model receives the simpler request. Existing malformed-feedback, error, privacy, validation, and timeout tests still pass. A fresh live Case 1 result remains pending; no model call was made by the agent.
