# HW1 specification · InterviewCoach Answer Feedback
**Anastasia Khevtsuriani · @aniararis · revised 21 October 2026**

**Problem and users.** Students and recent graduates preparing for entry-level interviews need specific feedback on written practice answers when no practice partner is available.

**Smallest useful feature.** A local ASP.NET Core page displays “Tell me about a time you solved a problem.” The student enters an answer and receives three labelled sections: strengths, areas for improvement, and one actionable suggestion. Feedback assesses relevance, clarity and completeness; it does not predict hiring success. The existing implementation is in `src/InterviewCoach/`.

**Context supplied to the model.** Only the selected question from `data/questions.json`, the current trimmed answer, `data/feedback-rubric.md`, and `src/InterviewCoach/Prompts/feedback.txt`. Instructions occupy the system message; the answer is untrusted user content. There is no conversation history or retrieval pipeline in this individual feature.

**Acceptance criteria.**

1. Display the prepared question; accept 1–3,000 characters after trimming. Reject blank/overlong answers and unknown question IDs on the server without a model call.
2. Display all three non-empty feedback sections as plain text. For a specific answer, refer only to supplied facts; for a vague answer, request a concrete example. Never invent experience or achievements.
3. On provider failure, invalid output or a 20-second timeout, show a readable error and retain the answer for manual retry. Do not retry automatically.

**Success measures.** All three cases in [golden.md](golden.md) meet their expectations, and at least 9 of 10 valid-answer trials display feedback within 15 seconds. These are targets: the recorded live attempts do not establish either target. Existing documentation reports 44 mocked test passes; a fresh restore on 21 October failed before tests could run.

**Budget.** Planning assumption: 20 requests/day × 30 days × (800 input + 300 output tokens) = 660,000 tokens/month. Output is capped at 1,200 tokens/request. With a verified zero-price model, provider token charges would be $0; free capacity is not guaranteed. This is an estimate, not measured individual-feature usage. Select the model via `OPENROUTER_MODEL`; keep `OPENROUTER_API_KEY` private. The C# client does not enforce the shared Python app’s free-model catalog check.

**Safety and exclusions.** Disclose external processing and ask users to omit sensitive information. The app does not persist answers or log answers/keys. Provider retention is outside this local guarantee. Model feedback may be wrong; message separation is tested, but live injection resistance is unverified. No accounts, database, saved history, CV upload, multi-question sessions, payments or public deployment.

**Run.** From this folder: `dotnet restore InterviewCoach.slnx --configfile NuGet.Config`, then `dotnet run --no-restore --project src/InterviewCoach/InterviewCoach.csproj`; open `http://localhost:5180`. Configure provider variables privately first. Test with `dotnet test InterviewCoach.slnx --no-restore`. See [README.md](README.md) for setup.
