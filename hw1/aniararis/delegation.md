# Delegation log · InterviewCoach HW1 · aniararis

**Recorded work: 6 October 2026.** This account is based on the development chat, student screenshots/terminal output, and agent-run checks.

I asked the coding agent to draft `spec.md` and `AGENTS.md` for one interview-question-and-answer feature. I saved the documents before implementation and approved the agent's plan and test dependencies. I delegated the C#/ASP.NET Core app, OpenRouter integration, validation, error handling, tests, and setup documentation. I then configured a key locally, ran the app, submitted answers, and shared errors for investigation.

The first live attempts exposed a gap between passing mocked tests and reliable model feedback. The app sometimes rejected unreadable output. The agent suspected the original 600-token cap, increased it to 1,200, and added stricter schema/reasoning settings. A later request returned HTTP 400; the exact rejected parameter was not established, so those extra settings were removed. Generic errors also hid useful information until the agent added safe provider-status diagnostics.

I reported repeated HTTP 429 failures after switching from Apodex to free Gemma. My quota check showed 6 used, 50 allowed, and 44 remaining. I ran the one-request diagnostic, which identified Google AI Studio's `upstream_provider_shared_pool` limit. This provided evidence of a provider capacity problem rather than an exhausted daily quota at that check.

The agent's latest automated run passed 44 tests; its initial browser run passed 10 checks. Those results are agent-run evidence, not a claim that I personally ran the suite. The empty-answer case passed; complete live feedback quality and the 9/10 latency target remain unverified. I retained the failed attempts in `golden.md` instead of presenting them as successful results. I still need to review the code independently and append complete live feedback when provider access allows it.
