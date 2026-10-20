# Job-advert extraction specification

Status: implemented; [live results](evidence/images-20261020T193252Z.json) passed
four synthetic fixtures, after an earlier failed run. Input is a screenshot/photo of an entry-level
job advert, with no personal applicant information. Purpose: help a user choose
a relevant practice pack; do not generate requirements absent from the advert.

| Field | Required | Normalization |
|---|---|---|
| role_title | yes | Trim; preserve the visible wording |
| seniority | no | Normalize only explicit level; otherwise null |
| requirements | yes | List of visibly supported skills/requirements; no inferred items |

Every field returns `{value, evidence, confidence}`; evidence is nullable, never a
guess. Unreadable values are null. Confidence is in [0,1] and is not the only
routing signal. Required missing/unsupported fields are hard failures for automatic
acceptance. See [confidence-policy.md](confidence-policy.md).

Validate file type/size and decoded dimensions; initially accept JPEG/PNG <=2 MB.
Downscale longest side to <=1024 px before sending. Send JSON schema, validate with
Pydantic, and call only through `llm.py`. Temporary image processing; no raw images
in logs. Disclose external processing before upload submission.

Fixtures in `project/tests/images/`: clean, degraded, ambiguous and
not-applicable. Record origin/synthetic status. Clean should accept or confirm;
degraded should confirm/review; contradictory required fields review; unrelated
input reject. [Fixture provenance](../project/tests/images/README.md) labels them
as synthetic rendered adverts, not real phone photographs. Real-world photo quality
and extraction accuracy remain additional evaluation work.
