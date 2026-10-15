# Submission preparation · khuttso HW1

**Status: preparation only; the journal is incomplete.** Nothing has been pushed and no pull request or Teams form has been submitted by the agent.

The assignment is individual HW1 / Milestone 1, worth 5 points. Deadline: **Tuesday 20 October 2026, 23:59 Tbilisi time**. The separate team Design Review is not included in this individual submission.

## Deliverable audit

| Requirement | Current evidence/status |
| --- | --- |
| One-page specification and setup commands | `../spec.md` |
| Working feature and at least one offline test | `../src/`, `../tests/`; 80 tests pass |
| Three golden inputs, expectations, actuals, commands, and verdicts | `../golden.md`; one pass and two documented configuration failures |
| Delegation log with an actual correction and verification | `../delegation.md`; student should review before submitting |
| Four dated, personal journal entries | **Incomplete**: `../journal.md` is a clearly marked draft awaiting student notes |
| No modifications to teammate/shared files | Commits through step 4 change only `hw1/khuttso/`; recheck the final PR diff |
| Tests from committed source rather than local-only files | Export of commit `d734173` passed all 80 tests |
| Live model behavior | Unverified; model/key absent and no live request limit agreed |
| PR, teammate boundary review/merge, Teams submission | Pending; no push authorized |

## Finish before submission

1. Supply real Weeks 1–4 notes and entry dates; replace the journal draft, review the delegation account, and commit the completed documentation.
2. Read and understand the implementation and tests. Inspect the diff and make sure every changed path starts with `hw1/khuttso/`.
3. If live verification is available, privately configure a selected OpenRouter model and key, agree on a request/spend limit, and rerun the two valid golden cases. Append exact results without deleting earlier failures. The course permits honestly documented failed goldens; do not invent successes.
4. Rerun `python -m pytest hw1/khuttso` after any implementation changes. Setup commands are in `../spec.md`.
5. Once the user authorizes pushing, push `hw1-khuttso` and open a PR into `main` titled **HW1 · khuttso**. A draft description is in `pr-description.md`.
6. A teammate checks only folder boundaries, then approves and merges; they must not edit or improve this individual work. The agent has not performed these actions.
7. Submit the form pinned on Teams with the merged-folder URL: `https://github.com/khuttso/Komble/tree/main/hw1/khuttso`. This is the intended destination, not a claim that the folder is already on remote `main`. Both the merged folder and form are required.

If the teammate has not merged the PR 24 hours before the deadline, the official brief provides an instructor-email exception using the open PR link. Consult the brief for the exact procedure; the agent will not send a message without explicit user authorization.

Source: [official Milestone 1 brief](https://github.com/ZA-KIU-Classroom/AIPSD-F26/blob/main/Lab-3/MILESTONE-1.md).
