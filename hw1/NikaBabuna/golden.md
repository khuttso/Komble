# Golden questions

Run these checks in a browser after the feature is built. Record what actually happened; do not change an expected result just to turn a failure into a pass.

## Check setup · 20 October 2026

Run `npm install`, `npm run build`, then `npm run preview` from this homework folder. Open the local URL printed by Vite (normally `http://127.0.0.1:4173/`) using the same browser and origin throughout. The initial library has the three starter packs below, with five questions each. Personal packs already saved in that browser may also appear.

The production build passed and the local server returned HTTP 200. The earlier browser-access problem was resolved by starting the preview outside the restricted execution sandbox. The checks below were observed in the in-app browser at `http://127.0.0.1:4173/` on 20 October 2026. This browser initially contained only the three starter packs.

Automated verification also passed: `npm test` ran 14 checks; `pytest hw1/NikaBabuna` ran one Python entry-point test that invokes those same checks. The verification environment used Node.js 22.16.0, bundled Python 3.12.14, and pytest 9.1.1 installed in the ignored `.test-deps/` directory. That directory was added to the verification process's `PYTHONPATH` and its `bin/` directory to `PATH`; pytest's cache was directed inside this homework folder. This setup is local to verification, not an application dependency.

## Question 1 — Search finds the matching seeded pack

- **Input:** Open the hub and search for `frontend`.
- **Expected behavior:** `Junior Frontend Developer` remains visible. The Customer Support and Graduate Trainee packs do not appear in the filtered list.
- **How run:** Entered `frontend` in the visible Search interview packs field in the production preview.
- **Actual result:** The result count changed from three packs to `1 of 3 packs`. Only `Junior Frontend Developer` remained; the Customer Support and Graduate Trainee cards disappeared.
- **Status:** Pass.

## Question 2 — A valid personal pack persists and can be previewed

- **Input:** Add a pack named `QA Intern Practice`, with target role `QA Intern`, tags `testing, junior`, and these questions:
  1. How would you test a login form?
  2. What would you include in a bug report?
  Refresh the browser, then open the added pack.
- **Expected behavior:** The pack appears after saving and remains visible after refresh. Its preview shows the target role, both tags, a count of two questions, and both question texts.
- **How run:** Cleared search, clicked Create a pack, filled the form exactly as above, clicked Save pack, refreshed the page, and opened Preview QA Intern Practice.
- **Actual result:** Saving displayed a success message and increased the library to four packs. After refresh the QA pack was still present. Its preview showed QA Intern, `testing` and `junior`, two questions, and both exact question texts.
- **Evidence:** [Pack preview after refresh](tests/evidence/qa-pack-preview.png).
- **Status:** Pass.

## Question 3 — Invalid pack input is rejected without external work

- **Input:** Attempt to add a pack with a blank title, a valid target role, and one question.
- **Expected behavior:** The app shows a validation message and does not add a pack. The local-only application contains no external API, AI, database, or remote-asset request code.
- **How run:** Opened a fresh create-pack form, left the title blank, entered QA Intern and one question, and clicked Save pack. Cancelled the rejected form and checked the library count. Ran the external-request guard in `npm test`, which scans application source files for request APIs, model/API clients, and remote URLs, and checks `index.html` for remotely loaded assets.
- **Actual result:** The form stayed open, displayed `Enter a pack title.`, and moved focus to the title field. The library still contained four packs after cancellation. The external-request guard passed: no request API, AI/API client, remote URL, or remotely loaded asset was found in the application code.
- **Evidence:** [Blank-title validation](tests/evidence/blank-title-validation.png).
- **Status:** Pass.
