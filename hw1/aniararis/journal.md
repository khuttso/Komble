# Pattern Journal · aniararis · InterviewCoach

Project timeline: I started the idea and team setup in **Week 3**. Specification, app setup, and testing took place in **Week 4**. The entries below distinguish that timeline from the course's weekly pattern names.

**W1 · Context as Budget.** I had not started InterviewCoach in Week 1, so I have no InterviewCoach delegation or verification to report for this week. Retrospectively, the pattern applies to the Week 4 specification: send only the selected question, answer, rubric, and instructions, and treat token estimates as assumptions until measured.

**W2 · Spec Before Code.** InterviewCoach had not started in Week 2, so there was no project implementation or agent output to verify then. I applied this pattern later in Week 4 by saving `spec.md` and `AGENTS.md` before the app was implemented and approving the agent's plan before it wrote code.

**W3 · Uncertainty-Aware UX.** I started the InterviewCoach idea and team setup this week; I have no completed app test or specific AI delegation recorded for that stage. The connection to this pattern became concrete during Week 4 testing, when the app needed to explain unavailable or unreadable feedback and preserve the user's answer rather than pretend it had succeeded.

**W4 · Grounded Generation.** I prepared the specification and agent instructions, approved the implementation plan, and delegated the app and mocked tests; the agent's latest report records 44 test passes, while I ran live browser tests and shared their failures. Feedback should refer to the submitted answer without inventing experience, but a ready-state screenshot without the full feedback and later provider errors do not establish that requirement; this version supplies context directly and has no retrieval pipeline. I ran the quota check and diagnostic, which showed 44 daily requests remaining and a Google AI Studio shared-pool rate limit, and kept those failures in `golden.md` instead of claiming a successful model-quality evaluation.

Before submission, review these entries in your own voice and add any actual Week 1–2 course exercises if applicable. No earlier coursework or personal reflection has been invented.
