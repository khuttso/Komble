# HW2: run, review and submit

The shared app stays in `project/`. Root `src/` contains the small HW2 adapters
required by the course layout and imports the existing public catalogue. HW1 is unchanged.

## Run without a provider or key

From the repository root, with Python 3.12+:

```powershell
python -m venv project/.venv
./project/.venv/Scripts/python.exe -m pip install -r requirements-tools.txt
./project/.venv/Scripts/python.exe -m pytest tests -q
./project/.venv/Scripts/python.exe -m src.demo_tool
```

For existing backend tests too, install `project/backend/requirements.txt` and run
`python -m pytest project/tests tests`. CI job `test` installs both requirement
files and runs both directories, followed by the existing frontend build.

For an MCP host, use the absolute virtual-environment Python executable as the
command, arguments `-m src.mcp_server`, and the repository root as working directory.
The server uses stdio: it waits for an MCP client, not typed chat messages. The
demo and transport test show an actual client call. No GUI changes are required.

## Product and write-up workflow

1. Create a product issue for the tool. Rename the prepared product branch to
   `slice-<issue-number>-hw2-aniararis` using its actual issue number.
2. Push it and open a product PR to main. Changes include `.github/workflows/ci.yml`,
   so ask the repo keeper to review CI. Do not merge with a failing check.
3. The repo keeper must enable main protection/rules requiring the `test` check.
   It was unprotected at inspection. A YAML workflow alone does not block merging.
4. Record the successful product CI URL, then conduct the red experiment below.
5. After actual teammate review, merge the good product PR and check main CI.
6. Push `hw2-aniararis` separately. That branch contains only the three files in
   `hw2/aniararis/`. Update evidence with real PR/run URLs before its review/merge.
7. Read and confirm the retrospective journal in your own voice. Submit the form
   with the write-up folder and product PR links. No grading tag is required by HW2.

## Red experiment: never merge the weakened contract

From the good product branch, create `hw2-red-aniararis`. In `src/contracts.py`
change only `extra="forbid"` to `extra="ignore"`. Run the golden test suite: the
forged-identity case must fail. Commit/push that intentional change and open a PR
with a clear **DO NOT MERGE — contract gate experiment** title. Verify the failed
`test` check and that GitHub actually blocks merging because it is required.
Save the CI run link and merge-block evidence. Close the PR without merging and
delete the throwaway branch. Never weaken the expected golden outcome.

The local mutation check can prove that tests detect a weak contract; it cannot
prove branch protection or replace the required remote red CI link.

## What is not covered

The tool does not run an LLM, serve a public HTTP endpoint, authenticate private
users, access personal packs, or establish completion of the full Lab 5 studio.
The existing RAG false refusal is a separate issue, not hidden by this HW2 result.
