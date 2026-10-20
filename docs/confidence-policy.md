# Extraction confidence policy

Status: implemented as pure `decide(extraction)` in
[extraction.py](../project/backend/app/extraction.py); no model call inside the decision.

| Signal | Route | User-facing behavior |
|---|---|---|
| Not a job advert / unusable upload | reject | Explain and request another image |
| Required field null or evidence missing | review | Field stays empty; request manual entry |
| Invalid field structure or contradictory evidence | review | Explain the conflict; require correction |
| Required fields supported, model confidence below provisional 0.85 | confirm | Ask the user to resolve uncertainty; do not prefill doubtful values |
| Required fields valid, supported, confidence >=0.85 | accept | Show supported extraction for inspection and explicit use |

Model confidence alone never permits acceptance. Rule priority is top-to-bottom;
missing evidence overrides a high model score. The 0.85 threshold is provisional,
not calibrated. Tune against fixtures and retain observed failures. Human correction
is labeled as user-entered; it does not become invented image evidence.

Offline tests cover supported clean fields; degraded missing evidence; high-confidence
missing title; unrelated image; contradictory requirements. At least three must
exercise the pure policy with handwritten extractions and no provider access.
Matching means extracted values occur in the claimed evidence string; the app
does not independently OCR-verify that string against the image. Explicit human
inspection remains necessary even for accept. Mixed junior/senior evidence confirms.
