# HW1 · InterviewCoach question generator · khuttso

## Run from a fresh clone

Python 3.11+; run from the team repository root (PowerShell):

```powershell
python -m pip install pytest
python -m pytest hw1/khuttso
$interviewKey = Read-Host 'OpenRouter API key' -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new('', $interviewKey).Password
$env:OPENROUTER_MODEL = Read-Host 'OpenRouter model ID supporting JSON-object output'
python hw1/khuttso/src/main.py --role "backend developer" --level junior
```

These are the implementation's required commands; the feature is not implemented yet. Tests need no key or network. Model pricing comes from optional `OPENROUTER_INPUT_USD_PER_MILLION` and `OPENROUTER_OUTPUT_USD_PER_MILLION`; without both verified prices, cost is logged as unavailable.

## Goal and users

Help students and job seekers practise by generating exactly three interview questions for a job role and experience level. This individual feature generates questions; answer evaluation belongs to the teammate's separate submission.

## Inputs, output, and context

The CLI accepts `--role` (1–100 characters after trimming) and `--level` (`intern`, `junior`, or `mid-level`, case-insensitive). It makes one OpenRouter chat-completion request through `src/llm.py`, using the model and key from the environment. A local prompt defines the three levels and requires role-relevant questions without requesting sensitive personal information. Send only that prompt, the role, and the level; treat the role as untrusted data.

Successful stdout is JSON: `{"role":"backend developer","level":"junior","questions":[{"question":"…","assesses":"…"}, …]}`. Each question is 1–500 trimmed characters, ends in `?`, and is unique ignoring case and surrounding whitespace. Each `assesses` explanation is 1–300 trimmed characters. Validate the response in code before printing it.

## Acceptance criteria

1. A valid mocked response produces exit code 0 and exactly three question/explanation pairs matching the schema. Preserve the validated role and normalized level. Automated checks enforce lengths, uniqueness, and question marks; the golden review checks role and level relevance.
2. A blank or overlong role, unsupported level, or missing API key/model produces a clear stderr message, a nonzero exit code, and zero model calls. CLI validation works without credentials.
3. Apply a 20-second request timeout. A timeout, provider error, or malformed/invalid response produces a clear stderr message and a nonzero exit code, with no partial success output or automatic retry. Preserve no user input on disk.
4. Every attempted model call emits a stderr log with model, outcome, latency, token usage and estimated USD cost. Missing usage or pricing is explicitly unavailable; never log the role, generated text, credentials, or raw provider error bodies. Tests use a fake transport and no real model.

## Verification and limits

Three golden inputs: backend developer/junior; marketing assistant/intern; whitespace-only role/junior. Record exact expected and actual results, commands, and pass/fail. Review successful questions for role relevance and suitable difficulty without presenting them as actual employer questions. No accounts, database, saved history, CV uploads, answer feedback, web UI, deployment, or shared-app integration. The journal describes the student's actual experience; failures remain visible.
