# Pattern Journal · Weeks 1–4 · @aniararis

**Review draft, 21 October 2026.** These entries use the timeline already recorded in this repository: the project idea/team setup began in Week 3, and specification, implementation and testing followed in Week 4. They do not invent earlier exercises. Anastasia should confirm the account and put the reflections in her own voice before submission.

## Week 1 · Context as Budget

The existing account records no InterviewCoach work in Week 1. Retrospectively, this pattern is visible in the individual feature’s narrow request: selected question, current answer, rubric and instructions, without unrelated files or history. That makes the request easier to inspect and limits unnecessary disclosure. The 800-input/300-output estimate is planning arithmetic, not measured usage. A useful next step is to compare that estimate with actual successful-request metadata while keeping answer text out of logs.

## Week 2 · Spec Before Code

The existing account also records no InterviewCoach implementation in Week 2. The pattern was applied later: a written spec and agent instructions preceded implementation. Three observable acceptance criteria constrained the work to validation, structured feedback and failure recovery. This helped distinguish “the page runs” from “the feedback is useful.” The remaining lesson is to keep the success targets visible when provider failures prevent demonstrating them, rather than quietly lowering the targets.

## Week 3 · Uncertainty-Aware UX

This was the recorded idea and team-setup period, with no completed app test claimed. Later implementation made the pattern concrete: unreadable feedback, timeouts and provider limits produce a clear error while preserving the answer. The Case 2 ready-state screenshot does not show enough content to judge the feedback. Marking that retry UNVERIFIED preserves the distinction between a visible status and evidence of quality. A next improvement to verification is to capture the complete result and elapsed time together.

## Week 4 · Grounded Generation

The existing account records spec preparation, agent delegation and student live testing in this stage. The individual C# feature supplies the current answer directly; it has no retrieval pipeline. Its grounding obligation is to discuss only stated facts and ask for missing detail instead of inventing achievements. Mocked tests check transport, validation and rendering; they cannot prove that a real model follows the rubric. Live failures and the shared-pool diagnostic therefore remain part of the submission. The next check is to obtain and inspect complete feedback for both substantive golden answers, including whether every claimed achievement appears in the input.
