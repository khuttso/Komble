# Three golden cases · @aniararis

**Question for all cases:** Tell me about a time you solved a problem.

These are the existing repository’s recorded 6 October results, reviewed on 21 October 2026. They have not been rerun live in this revision. Mocked application tests and live model quality are reported separately.

## 1. Specific example

**Answer:** “Our team’s task list was confusing, so I created a shared board, assigned owners, and held short check-ins. We finished two days before the deadline.”

**Expected:** Three labelled feedback sections, referring to the board, ownership, check-ins and stated result without invented achievements.

**Recorded result:** The first attempt displayed “The service returned incomplete or unreadable feedback. Your answer is still here; you can try again manually.” The answer was preserved. Later documented attempts encountered provider errors, including HTTP 400 and 429; no complete feedback or successful display time was captured.

**Outcome: FAIL.** Error handling worked, but the expected feedback was not obtained. [Saved screenshot](docs/evidence/case-1-error.png).

## 2. Short answer

**Answer:** “I helped someone with math and they got full marks.”

**Expected:** Recognise the stated result, ask what difficulty the person had and what the candidate personally did, and supply one actionable suggestion. Do not invent a teaching method.

**Recorded result:** An initial attempt produced the same unreadable-feedback error. A later screenshot showed the ready status, but not the feedback sections or elapsed time.

**Outcome: initial FAIL; retry quality UNVERIFIED.** A ready status is insufficient evidence of useful feedback. [Initial error](docs/evidence/case-2-error.png) · [Ready status](docs/evidence/case-2-ready-status.png).

## 3. Empty answer

**Answer:** Empty string or whitespace only.

**Expected:** Validation message and zero model calls.

**Recorded result:** The previous agent browser check displayed “Enter an answer between 1 and 3,000 characters after trimming spaces.” No feedback HTTP request was sent. Documented integration tests submitted null, empty and whitespace answers and received HTTP 400 with zero mocked transport calls.

**Outcome: PASS in the recorded agent checks.** The relevant test is `EmptyAnswerIsRejectedBeforeAnyModelCall` in [FeedbackTests.cs](tests/InterviewCoach.Tests/FeedbackTests.cs).

## Interpretation and next check

The prior [verification record](docs/verification.md) reports **44 mocked tests passed** and ten initial browser checks. Those establish tested application behavior, not live coaching quality. The existing diagnostic records HTTP 429 with `limit_source=upstream_provider_shared_pool`, despite an earlier quota check showing 44 requests remaining. It does not explain every earlier failure.

On 21 October, .NET SDK 10.0.103 was available, but a fresh solution restore exited unsuccessfully before tests ran; no new passing test run is claimed. No provider calls were made for this revision. The shared Python app’s successful feedback is a different implementation and does not replace these results.

Rerun Cases 1 and 2 with a confirmed compatible free model, recording the exact displayed sections and elapsed times. Then record ten deliberate timing trials, counting failures as failures. The 9/10-under-15-seconds target and live prompt-injection resistance remain unverified.
