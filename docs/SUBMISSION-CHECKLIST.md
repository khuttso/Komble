# Design Review submission checklist

Deadline supplied by the instructor: **20 October 2026, 23:59 Asia/Tbilisi**.
Local implementation/evidence does not establish successful submission.

## Prepared locally by the agent

- [x] Shared product in `project/`; individual `hw1/` unchanged.
- [x] Shared spec, multimodal spec, confidence policy, retrieval spec, instructions.
- [x] Practice, image review, and grounded guidance connected in the actual app.
- [x] Offline suite 28/28 and production frontend build pass.
- [x] Five-case live golden definition and saved results, including **4/5** selected run.
- [x] Four synthetic image fixtures, initial failures, and **4/4** selected routing run.
- [x] Sanitized measured usage, monthly arithmetic, and local context comparison.
- [x] Design Review below approximately 1,600 words, architecture, risks and owners.
- [x] Three linked decision records; all agent drafting logged.
- [x] Canonical `TEAM-CONTRACT.md`; no signature fabricated.

## Still required

- [ ] Team reads and confirms the corpus, review, proposed owners/dates and code.
- [ ] Luka completes his actual personal contract signature commit if still needed.
- [ ] Push a feature branch and open the PR; actual remote CI job `test` is green.
- [ ] Teammate reviews/approves; merge appropriate work and review to **main**.
- [ ] Create `lab3-multimodal` and `lab4-rag` only on commits containing their work.
      Do not invent historical lab approvals or move an existing tag blindly.
- [ ] Put `design-review` on the intended **main** commit and push it before deadline.
- [ ] Repo keeper submits the team form on Teams with repo/tag/member information.

No remote CI run, review approval, main merge, grading tag or form submission has
been claimed. Do not move the grading tag after the deadline.

## Known limitations to retain

Golden truthful-achievements case still refuses; ten-trial latency and live
adversarial robustness are unverified. Images are synthetic rather than real phone
photos. Embeddings are local (documented lab-example variation). Mobile inspection
and model-weight revision pinning remain. Full-corpus upload comparison was not
approved; its replacement is explicitly a local-tokenizer estimate.
