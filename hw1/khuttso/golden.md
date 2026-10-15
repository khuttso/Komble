# Golden cases · InterviewCoach question generator · khuttso

Recorded **15 October 2026, 19:03:34 Tbilisi time**. Raw subprocess outputs, arguments, and exit codes are in `docs/golden-results.json`.

These are actual CLI runs with `OPENROUTER_API_KEY` and `OPENROUTER_MODEL` unset. Neither variable was configured in the agent's shell; the recording process explicitly omitted both to guarantee zero live calls. No model was selected and no model request/spend limit had been agreed. No network request was made and no generated questions are claimed as live evidence. Mocked success is tested separately in the 80-test offline suite; it does not establish real question quality.

## Case 1 · Junior backend developer

**Input:** role `backend developer`, level `junior`.

**Expected:** exit code 0; JSON preserving the role and level, with exactly three distinct question/explanation pairs. Each question ends in `?` and meets the length rules. Manual review should find junior-level backend topics (for example, APIs, databases, or testing), with explanations matching the questions and no claim that they are actual employer questions.

**Command, from the repository root:**

```powershell
py -3.12 -B hw1/khuttso/src/main.py --role "backend developer" --level junior
```

**Actual:** exit code **1**, stdout empty, stderr:

```text
Error: Set OPENROUTER_API_KEY and OPENROUTER_MODEL before generating questions.
```

**Result: FAIL — generation unavailable because model configuration is missing.** The configuration guard behaved correctly, but no questions were produced. Relevance and difficulty are unverified.

## Case 2 · Intern marketing assistant

**Input:** role `marketing assistant`, level `intern`.

**Expected:** exit code 0; JSON preserving the role and level, with three distinct question/explanation pairs meeting the schema. Manual review should find beginner marketing topics suitable for an intern, such as understanding an audience, basic campaign measurement, or a coursework example; it should not require senior strategy or leadership experience.

**Command, from the repository root:**

```powershell
py -3.12 -B hw1/khuttso/src/main.py --role "marketing assistant" --level intern
```

**Actual:** exit code **1**, stdout empty, stderr:

```text
Error: Set OPENROUTER_API_KEY and OPENROUTER_MODEL before generating questions.
```

**Result: FAIL — generation unavailable because model configuration is missing.** No live content or difficulty assessment is available.

## Case 3 · Whitespace-only role

**Input:** role containing three spaces, level `junior`.

**Expected:** nonzero exit code, no success JSON, a role-validation error, and no model call, even with credentials absent.

**Command, from the repository root:**

```powershell
py -3.12 -B hw1/khuttso/src/main.py --role "   " --level junior
```

**Actual:** exit code **1**, stdout empty, stderr:

```text
Error: Enter a job role between 1 and 100 characters after trimming.
```

**Result: PASS.** The CLI rejected the input before checking model configuration. The matching offline test also records zero fake-transport invocations.

## Follow-up

After the user selects a model and agrees to a request/spend limit, configure the two environment variables privately and rerun Cases 1 and 2. Append their exact JSON output, model ID, measured times, and content assessments while retaining these original failures. Do not mark a mock response as a successful live generation or retry provider calls automatically.
