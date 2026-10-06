# InterviewCoach · Answer Feedback

Individual HW1 submission for `aniararis`. A local web app shows one prepared interview question, accepts an answer, and returns strengths, areas for improvement, and one actionable suggestion through OpenRouter.

## Requirements

- .NET 10 SDK (implementation verified with 10.0.103).
- Rider or a terminal.
- An OpenRouter API key and a model that supports JSON-object output (`response_format: json_object`).
- Internet access for initial NuGet restore and live feedback requests.

The course materials explicitly list Python and Node.js; confirm that your instructor accepts this C# implementation.

## Open in Rider

Open `InterviewCoach.slnx` in this folder. It contains the application and xUnit test projects. Keep this individual submission under `hw1/aniararis/` in the team repository.

## Restore and run

Run all commands from this homework folder:

```powershell
dotnet restore InterviewCoach.slnx --configfile NuGet.Config
```

Set `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` in your shell or in a private Rider run configuration. Do not save a real key in source code, `appsettings.json`, a committed run configuration, or homework documents. The app does not load `.env` files.

To enter the key in PowerShell without typing its value into command history:

```powershell
$interviewKey = Read-Host 'OpenRouter API key' -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new('', $interviewKey).Password
$env:OPENROUTER_MODEL = Read-Host 'Exact OpenRouter model ID'
dotnet run --no-restore --project src/InterviewCoach/InterviewCoach.csproj
```

Open **http://localhost:5180**. The question and form work without a key; submitting a valid answer then shows a configuration error, not fabricated feedback. Restart the app after changing its environment variables. Stop it with Ctrl+C.

If port 5180 is in use:

```powershell
dotnet run --no-restore --project src/InterviewCoach/InterviewCoach.csproj -- --urls http://localhost:5181
```

Choose a model with JSON-object output support from the [OpenRouter model catalog](https://openrouter.ai/models). The student's current selected model is `google/gemma-4-26b-a4b-it:free`; the earlier model was `apodex/apodex-1.1-mini:free`. The free model's published price is recorded in `spec.md`. The latest student diagnostic returned HTTP 429 from Google AI Studio with `limit_source=upstream_provider_shared_pool`, despite 44 daily requests remaining at the earlier quota check. Live feedback quality is not yet verified reliably.

## Test

```powershell
dotnet test InterviewCoach.slnx --no-restore
```

Tests run the real local HTTP endpoints and replace the outbound model transport with a fake handler. They do not require a key or call OpenRouter. One test intentionally waits approximately 20 seconds to verify the real timeout.

For a machine-readable report:

```powershell
dotnet test InterviewCoach.slnx --no-restore --logger "trx;LogFileName=automated-tests.trx" --results-directory TestResults
```

## Structure

```text
InterviewCoach.slnx
AGENTS.md / spec.md                 Instructions and specification
golden.md                          Three HW1 evaluation cases and results
delegation.md / journal.md          Evidence and individual reflections
data/questions.json                Prepared question list
data/feedback-rubric.md             Relevance, clarity, completeness rubric
src/InterviewCoach/
  Program.cs                       Startup, question and feedback endpoints
  OpenRouterFeedbackClient.cs      Single outbound request, parsing, usage, timeout
  InterviewContent.cs              Loads prepared context
  OpenRouterOptions.cs             Environment configuration
  Models.cs                        Request/response types
  Prompts/feedback.txt              Coaching instructions
  wwwroot/                         HTML, CSS, browser JavaScript
tests/InterviewCoach.Tests/         Mocked HTTP integration tests
docs/verification.md                Checks actually completed and remaining work
```

Data, prompts, and browser assets are copied beside the application assembly when built. You do not need to change the working directory in Rider to make those files load.

## Request flow

1. The browser loads the prepared question from `GET /api/question`.
2. `POST /api/feedback` accepts a question ID and answer. The server trims and validates the answer (1–3,000 characters) and looks up the trusted question.
3. One non-streaming request goes to OpenRouter in JSON-object mode. The prompt requires three feedback fields, which the app validates before display. The rubric and instructions are a system message; the question and answer are JSON in a separate user message.
4. The app validates three non-empty feedback fields and displays them as plain text. Incomplete or truncated output is rejected.
5. Errors preserve the answer in the current page for manual retry. There are no automatic retries or provider fallbacks.

The request has a 20-second server deadline and a 1,200-token output cap. The app does not override model reasoning settings or send a strict JSON schema: that combination produced HTTP 400 during live testing, so the request now uses the simpler JSON-object format that previously succeeded. Reasoning can still consume the output budget; a truncated response is reported as a failure rather than displayed as complete feedback. The page also has a 25-second network deadline so it cannot wait indefinitely if the local server stops responding. Every click that reaches the model may incur usage. Repeat trials manually and deliberately.

If a response hits its output limit, the app now reports that specific error. Terminal diagnostics include an allowlisted finish reason, parsing stage, and numeric reasoning-token count when available. This helps distinguish truncation from malformed JSON without exposing the answer, key, or model reasoning text.

Provider failures also show an OpenRouter code and a safe explanation. Terminal logs include numeric `provider_status` and `provider_error_code`; no raw error bodies are displayed or logged.

| Code | Check |
|---|---|
| 400 / 422 | Failed request details in Activity; model support for JSON output and the output limit |
| 401 | API key validity; set it in the terminal that starts the app and restart |
| 402 | Account credits and the API key's spending limit |
| 403 | Account/model access or moderation restrictions in OpenRouter Activity |
| 404 | Model ID, endpoint availability, and provider/privacy restrictions |
| 429 | Rate limit or free-model quota; check Activity and wait before retrying |
| 5xx | OpenRouter/provider availability; retry manually later |

After a source-code update, stop the existing process with Ctrl+C and use `dotnet run --no-restore --project src/InterviewCoach/InterviewCoach.csproj` in the same configured terminal. Do not add `--no-build`, since it would run the old executable.

For a persistent 429 with daily quota remaining, run this once in the configured PowerShell terminal:

```powershell
.\src\diagnose-openrouter.ps1
```

The helper sends exactly one tiny synthetic request (32-token cap, 20-second timeout, no retries), refuses model IDs without `:free`, and prints the selected model, HTTP status, available reset headers, and selected error details. It does not send your interview answer, print your key, save a response, or dump raw provider metadata. A successful diagnostic is not a successful golden test. Its syntax and key-redaction function were checked locally without making a live request.

## Privacy and limitations

There are no accounts, database, saved answers, analytics, or browser storage. Reloading the page clears the current answer. Answers are sent externally through OpenRouter; the provider's own processing/retention policies still apply. Avoid sensitive information.

Application logs record numeric token usage, cost when supplied, elapsed time, and outcome. They do not record answers, prompts, keys, or provider response bodies. Missing usage is explicitly logged. Prompt separation reduces injection risk but does not prove the model will always resist it.

This is a local homework prototype. Feedback is practice guidance, not a hiring prediction. Public deployment and multi-user operation are outside the specification.

## Complete before submission

- Rerun the two student-tested inputs in golden cases 1 and 2 when the provider is available, and append exact feedback while retaining the failures.
- Run the additional adversarial check and 10 timing trials described there; keep honest failure results.
- Recheck the model and cost assumptions in `spec.md` if you change models.
- Review and understand the generated implementation. Add your own verification notes to `delegation.md`.
- Review the journal's confirmed timeline: project idea/team setup in Week 3; specification, app setup, and testing in Week 4. Add any actual Week 1–2 course work if applicable.
- Commit and submit through the team repository workflow, then complete the form on Teams.

The deliverable-by-deliverable status is in `docs/submission-checklist.md`. The HW1 brief allows documented failures; this submission records them without claiming that all success criteria pass.

## Implementation references

- [OpenRouter chat-completion API](https://openrouter.ai/docs/api/api-reference/chat/create-a-chat-completion)
- [OpenRouter structured-output capabilities](https://openrouter.ai/docs/guides/features/structured-outputs)
- [OpenRouter reasoning tokens and output budgets](https://openrouter.ai/docs/guides/best-practices/reasoning-tokens)

