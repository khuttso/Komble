# Spec v0 · InterviewCoach

## Problem

Students and recent graduates preparing for their first job interviews often lack someone to practise with. Without specific feedback, they struggle to identify unclear, incomplete, or irrelevant answers.

## Users

Students and recent graduates preparing for entry-level job interviews who want to practise written answers independently.

## Success criteria

1. All three initial golden test cases meet their documented expected results.
2. Every successful feedback response includes strengths, areas for improvement, and one actionable suggestion tied to the answer.
3. At least 9 of 10 valid-answer trials return feedback within 15 seconds, measured from submission to display.

## Core feature (Weeks 2 to 4 scope)

A simple web page displays one general entry-level interview question from a prepared list. The user submits a written answer, and the app uses a model through OpenRouter to provide feedback on relevance, clarity, and completeness. The first version supports one question-and-answer exchange at a time and runs locally with documented setup commands.

## Context list

- **Question:** `data/questions.json`; send only the selected question to the model.
- **Answer:** Held temporarily for the current request; not saved by the app.
- **Rubric:** `data/feedback-rubric.md`; defines relevance, clarity, and completeness.
- **Instructions:** `src/InterviewCoach/Prompts/feedback.txt`; defines the feedback sections and requires treating the answer as content, not instructions.

Paths are relative to this homework submission folder.

## Acceptance criteria

1. Done when the page displays one question and accepts answers of 1–3,000 characters after trimming whitespace. Empty or overlong answers show a validation message without a model call.
2. Done when a valid answer returns labelled strengths, areas for improvement, and an actionable suggestion. A specific example receives feedback grounded in its details; a vague answer prompts a request for a concrete example without inventing experience.
3. Done when an API failure or a 20-second timeout displays a clear error message, preserves the answer for manual retry, and triggers no automatic paid retries.

## Napkin math

Current model: `google/gemma-4-26b-a4b-it:free`, configured through `OPENROUTER_MODEL`. Planning estimate: 20 requests/day, 800 input tokens and 300 output tokens per request. Published input and output prices are $0 per million tokens:

20 × (800 × $0/1,000,000 + 300 × $0/1,000,000) × 30 = **$0/month** in model-token costs.

Pricing checked on 6 October 2026 against the [OpenRouter model page](https://openrouter.ai/google/gemma-4-26b-a4b-it:free). Token counts and volume are estimates, not measured results. The implementation caps output at 1,200 tokens. Free access is rate-limited, and observed provider capacity failures mean this workload is not guaranteed. Hosting is excluded. This updates the original illustrative paid-price estimate after model selection; it does not change the success targets.

## Risks and safety

- **Misleading feedback:** Apply a consistent rubric and label feedback as practice guidance, not a hiring prediction.
- **Personal information exposure:** Ask users to omit sensitive details, disclose external AI processing, and do not persist or log answers in the app.
- **Misuse:** Users may embed instructions to manipulate feedback; separate answer content from system instructions and test an adversarial input.

## Out of scope (for now)

Accounts, databases, saved interview history, CV uploads, multi-question interviews, company-specific coaching, hiring decisions, payments, and public deployment.
