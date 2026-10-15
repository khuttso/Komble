# Verification · khuttso HW1

## Recorded result

On **15 October 2026**, Python **3.12** with pytest **9.1.1** ran the individual submission suite:

```powershell
python -m pytest hw1/khuttso -q --junitxml=hw1/khuttso/docs/offline-tests.xml
```

Final result: **80 passed in 0.91 seconds**, no warnings. The JUnit report is `offline-tests.xml`. These timings describe the offline tests, not real model latency.

The agent used `py -3.12 -B` instead of `python`, and pytest was installed into the chat's scratch folder rather than the global interpreter. The process set `PYTHONPATH` to that installation and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` to avoid unrelated installed plugins. A fresh clone can use the normal install/run commands in `spec.md`; the scratch path is not needed by the submission.

## What was checked

- CLI success through a fake HTTP transport: normalized role/level, three validated questions, pure JSON on stdout, and disclosure/logs on stderr.
- The OpenRouter request URL, method, authorization header using a synthetic key, JSON mode, output-token cap, 20-second timeout argument, and disabled provider fallbacks.
- Input limits, all supported levels, Unicode roles, missing configuration, and invalid configuration; rejected requests make zero model calls.
- Embedded role instructions remain separate from the system prompt. This is a message-construction check, not proof of live prompt-injection resistance.
- Counts, field names/types, trimming, question marks, exact length boundaries, duplicates, malformed provider envelopes, truncated completions, and invalid JSON.
- HTTP errors, network failure, direct/wrapped timeouts, and incomplete responses. Failure paths make one transport attempt, emit one sanitized event, and produce no partial success output.
- Usage/cost accounting, explicit unavailable values, zero configured prices, invalid pricing, and logs that omit test inputs, generated text, credentials, and raw provider error bodies.
- The production HTTP adapter's size bound, response closure, redirect prevention, and default-client transport wiring, all with fake responses.
- Real CLI subprocess help, missing-argument behavior, missing-configuration behavior, and input-validation exit codes without credentials. Prompt loading works independently of the current directory.

An autouse test fixture removes model configuration and blocks socket connections in the pytest process. Provider responses are deliberately synthetic; no automated test calls a real model. CLI subprocess cases exercise only help or rejection before a request.

## Corrections during verification

The initial run passed all 80 tests but warned that pytest could not create its cache directory under this Windows sandbox. Disabling caching exposed the inaccessible temporary cache directory left by that attempt during collection. `pytest.ini` now disables the cache plugin and excludes pytest's temporary cache directories; `.gitignore` excludes the same disposable artifacts. No tests were removed or weakened. The final run passed all 80 tests without warnings.

## Golden results and remaining limits

`../golden.md` and `golden-results.json` record three actual CLI subprocess runs: **one validation pass and two generation failures due to missing model configuration**. No live model calls were made. Real question relevance/difficulty, provider compatibility, live latency, real token consumption/cost, and live prompt-injection behavior remain unverified. Timeout tests simulate exceptions and verify the timeout passed to the HTTP adapter; they do not measure a real network timeout.

## Submission audit

An export of commit `d734173` was created with `git archive HEAD hw1/khuttso`, extracted into a separate scratch directory, and tested using `py -3.12 -B -m pytest hw1/khuttso -q` with the same isolated pytest installation. Result: **80 passed**. This checks the committed source without relying on untracked application files; it is not a new live model test or a network clone/install test.

Only `hw1/khuttso/` is part of this change. The teammate's application was not modified or tested. Step 5 adds a delegation account and submission checklist. The journal remains a marked draft awaiting the student's own Weeks 1–4 notes and dates; the homework is not yet submission-ready.
