# Execution roadmap

User approved this direction on 20 October 2026, changing the application folder
to `project/`. Work incrementally and verify each slice. Status is evidence-based.

| Increment | Scope | Done when | Status |
|---|---|---|---|
| 1. Foundation | Initial specs, runtime, API, searchable starter library | API checks, build, browser load/search/preview/error | Complete locally; [evidence](verification.md) |
| 2. Practice | Personal packs, question navigation, current-answer feedback | Real UI journey; offline input/output/failure tests; separate live evidence | Implemented; browser/live checked |
| 3. Multimodal | Advert extraction, downscale, schema, human confirmation | Four fixtures, >=3 routing tests, clean/degraded live runs | Implemented; 4/4 synthetic routes; degraded browser review checked |
| 4. Grounding | Corpus, model-tagged index, scored retrieval, cite/refuse | Citation/threshold tests and answer/refusal in UI | Implemented; browser cited answer/refusal checked |
| 5. Evaluation | Five golden questions; baseline and one setting change | Real result, diagnosis and tuning decision | Saved 2/5 to 4/5; failing case retained |
| 6. Review | Usage arithmetic, risks/owners, diagram, <=1,600-word review | Every factual claim links to existing evidence | Draft written, about 1,050 words excluding diagram; teammate review pending |
| 7. Submission | PR review, merge, lab/review tags, team form | Human review + correct tagged main commit + form | Pending human workflow |

## Constraints and dependencies

- Budget: $0 total; free model access only. No paid fallback. Compatibility and
  rate limits must be checked; no live success is assumed from old homework.
- Embeddings use the [documented local CPU model](decisions/002-free-local-embeddings.md).
  The index refuses different model metadata or a changed corpus fingerprint.
- Initial docs are prospective. Results, completed mitigations and grading claims
  are added only after implementation and verification.
- Existing `hw1/` stays unchanged. No generated history, signatures or approvals.
- Repository course paths stay at root. Application and its tests stay in `project/`.

## After the first usable release

Consider saved local session history (only with explicit consent and deletion),
SQLite, larger corpus, generated role questions, and eventual authenticated hosting.
These are future proposals, not promises or features of the first release.
