# Shared InterviewCoach application

Local React/FastAPI app: starter/personal packs, written interview practice and AI
feedback, job-advert extraction with human confirmation, and cited preparation
guidance. Individual hw1 submissions are unchanged.

## Setup (PowerShell, repository root)

Requires Python 3.12+ and Node.js 22.12+. Create an isolated environment:

```powershell
python -m venv project/.venv
./project/.venv/Scripts/python.exe -m pip install -r project/backend/requirements.txt
npm --prefix project/frontend ci
```

If python is a Windows Store alias, use an installed executable for the first
command. On this machine Python 3.13.5 is available here:

```powershell
& "$env:LOCALAPPDATA/Programs/Python/Python313/python.exe" -m venv project/.venv
```

Put OPENROUTER_API_KEY=your-key in ignored **project/.env** using your editor.
Never paste the key into chat or commit it. Environment variables take precedence.
Root .env.example lists optional text/vision model IDs; leaving them blank selects
a compatible free model from the current catalog. The gateway requires a :free ID,
zero advertised pricing, schema support, and image support for vision. It rejects
non-free configuration and does not fall back or automatically retry.

Build the local index (first run downloads public model weights, no paid API):

```powershell
./project/.venv/Scripts/python.exe -m project.backend.app.index
```

CPU embeddings use BAAI/bge-small-en-v1.5 through FastEmbed. Model/index files stay
in ignored project/runtime/. Rebuild after editing the corpus or changing model.

## Run

Terminal one, from repository root:

```powershell
./project/.venv/Scripts/python.exe -m uvicorn project.backend.app.main:app --host 127.0.0.1 --port 5191
```

Terminal two, from repository root:

```powershell
npm --prefix project/frontend run dev
```

Open <http://127.0.0.1:5190>. Both servers bind to loopback. Vite proxies /api to
5191, keeping existing homework servers on other ports untouched. Use Ctrl+C in
each terminal to stop. API docs: <http://127.0.0.1:5191/docs>.

## Use

1. Browse/search a pack, preview questions, or create a personal pack.
2. Select **Practise this pack**, write an answer, acknowledge external processing,
   and request feedback. Navigate questions; drafts remain in this session.
3. **Read a job advert** accepts JPEG/PNG <=2 MB. Check the extraction; uncertain
   fields stay empty. Manually correct, then confirm to find a matching pack.
4. **Ask the preparation guides** answers from ten team-authored documents. Expand
   citations to inspect passages. Unsupported questions refuse.

Answers and uploaded images are sent externally only when submitted with the UI
disclosure. Omit private information. Personal packs persist only in this browser
and origin; clearing storage removes them. Interview drafts/feedback are page-memory
only; ending/reloading a session discards them. The server does not retain answers
or uploads in an application store; multipart parsing may use temporary OS files.
Provider processing policies still apply. This is practice guidance, not a hiring
prediction. Corpus content is AI-assisted and awaits teammate review.

## Offline verification

```powershell
./project/.venv/Scripts/python.exe -m pytest project/tests -q
npm --prefix project/frontend run build
```

Tests mock provider calls and isolate logs. CI job test runs these without keys.
The frontend build does not establish browser or live model behavior.

## Opt-in live evidence (consumes free-model quota)

```powershell
./project/.venv/Scripts/python.exe evals/run_golden.py --live --k 5 --threshold 0.55
./project/.venv/Scripts/python.exe project/tools/live_images.py
./project/.venv/Scripts/python.exe project/tools/live_smoke.py
```

The gateway limits generation to 24 outbound attempts per process, with a 20-second
model HTTP timeout and 1,000 output tokens. Separate CLI runs have separate counters;
review provider quota before deliberate reruns. No paid fallback or automatic retry.
Runtime JSONL logs contain allowlisted numeric usage/outcomes, never input bodies.
Root logs/verified-usage.jsonl is the sanitized evidence export from this build.

The saved best golden result is **4/5**, not complete success. Earlier failures are
retained. Extraction passed four synthetic fixtures; real phone-photo robustness
and the ten-trial latency target remain unverified. See [verification](../docs/verification.md)
and the [Design Review](../docs/DESIGN-REVIEW.md).
