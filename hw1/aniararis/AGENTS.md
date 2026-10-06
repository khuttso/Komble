# AGENTS.md · InterviewCoach — Answer Feedback

*Instructions for AI coding agents working on this individual HW1 submission.*

## What this project is

InterviewCoach helps students and recent graduates practise for entry-level job interviews. This feature displays one prepared interview question, accepts a written answer, and provides AI feedback on relevance, clarity, and completeness. Follow `spec.md` for scope and acceptance criteria.

## Scope

This file belongs in `hw1/aniararis/`.

All paths below are relative to that folder. Only modify this individual submission. Do not edit another student's homework or shared project files.

## Stack

- Language: C# (.NET 10 SDK)
- Framework: ASP.NET Core 10
- Model access: OpenRouter through `HttpClient`
- Model: Read from `OPENROUTER_MODEL`
- API key: Read from `OPENROUTER_API_KEY`
- Tests: xUnit with mocked model calls
- Questions: `data/questions.json`
- Rubric: `data/feedback-rubric.md`
- Feedback instructions: `src/InterviewCoach/Prompts/feedback.txt`
- Storage: No database; answers are processed temporarily and not saved

## How to run

Use this project layout:

- Application: `src/InterviewCoach/InterviewCoach.csproj`
- Tests: `tests/InterviewCoach.Tests/InterviewCoach.Tests.csproj`

Run from this homework folder:

```bash
dotnet restore InterviewCoach.slnx --configfile NuGet.Config
dotnet run --no-restore --project src/InterviewCoach/InterviewCoach.csproj
dotnet test InterviewCoach.slnx --no-restore
```

Configure `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` in the shell or Rider run configuration before starting the app. Do not commit configuration containing real keys.

Tests must run without API keys. Keep the commands accurate and ensure the application can locate its data and prompt files.

Open `InterviewCoach.slnx` in Rider. The default app URL is `http://localhost:5180`.
Data, prompt, and static files are copied to the build output. The three approved
direct test packages are Microsoft.NET.Test.Sdk, xunit, and xunit.runner.visualstudio.
For current verification results and pending live checks, see `docs/verification.md`.

## Conventions

- Read `spec.md` before implementing changes.
- Propose a plan and wait for human approval before writing code.
- Keep the implementation small and understandable.
- Display one question from the prepared list.
- Support one question-and-answer exchange at a time.
- Accept answers of 1–3,000 characters after trimming whitespace.
- Validate input on the server. Reject invalid input without calling the model.
- Send only the selected question, current answer, rubric, and feedback instructions to the model.
- Treat answers as untrusted content, not instructions.
- Feedback must include labelled strengths, areas for improvement, and one actionable suggestion.
- Ground feedback in the answer without inventing experience or achievements.
- For vague answers, suggest adding a concrete example.
- Tell users that answers are sent to an external AI provider and ask them to omit sensitive information.
- Read secrets from environment variables.
- Read and log model usage when supplied; explicitly record when usage is unavailable.
- Do not log answers, personal information, or API keys.
- Apply a 20-second timeout to model requests.
- On API failure, timeout, or unusable model output, show a clear error and preserve the answer for manual retry.
- Do not retry paid requests automatically.
- Automated tests must mock model calls and require no real API keys.
- Verify that at least 9 of 10 valid-answer trials return feedback within 15 seconds.
- Record the three HW1 golden cases and actual results in `golden.md`.
- Record significant delegation and verification in `delegation.md`.
- Keep Weeks 1–4 learning entries in `journal.md`, based on the student's actual experience.
- Report which checks were run and any remaining failures.

## You may

- Create and edit application files in `src/`.
- Create and edit tests in `tests/`.
- Maintain prepared questions and the rubric in `data/`.
- Update documentation within this homework folder.
- Propose dependency changes; ask before adding them.

## You may not

- Touch `.env`, CI configuration, or anything in `secrets/`.
- Modify files outside this homework folder.
- Write real API keys into source files or committed configuration.
- Delete or weaken tests to make them pass.
- Fabricate test results, delegation history, or journal entries.
- Claim tests passed unless they were actually run and passed.
- Call paid APIs in loops without an approved limit.
- Store interview answers permanently.
- Add features outside `spec.md` without approval.
- Push commits or merge pull requests.
- Present feedback as a guarantee of hiring success.
