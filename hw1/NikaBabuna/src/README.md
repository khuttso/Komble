# InterviewCoach Pack Hub source

This folder implements the pack browsing, search, creation, and preview feature in `../spec.md`.

## Run locally

From `hw1/NikaBabuna/`, using Node.js 20.19+ or 22.12+:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite. To verify and preview a production build:

```bash
npm run build
npm run preview
```

## Source map

| File | Responsibility |
| --- | --- |
| `main.jsx` | Mount React and load the stylesheet. |
| `App.jsx` | Own the library, search, selected pack, form, and save messages. |
| `App.css` | Responsive layout, cards, forms, dialogs, and focus styles. |
| `data/seedPacks.js` | Three starter packs, with five sample questions each. |
| `lib/packStorage.js` | Validate saved data and contain every `localStorage` read/write. |
| `lib/packUtils.js` | Shared search, question parsing, and required-field rules used by the UI and tests. |
| `components/PackSearch.jsx` | Search field and filtered result count. |
| `components/PackCard.jsx` | Clickable pack summary. |
| `components/PackForm.jsx` | Trim and validate fields, split questions by line, and request a save. |
| `components/PackPreview.jsx` | Accessible dialog with metadata and the full question list. |
| `tests/packHub.test.js` | Offline acceptance checks using Node.js's built-in test runner. |

Personal packs use the browser key `interviewcoach.personal-packs.v1`. Starter packs are never written into personal storage. Data stays in the same browser and origin; changing the host or port uses a different store. Failed saves keep the form open. Unreadable saved data is left unchanged and disables adding packs while starter packs remain available.

## Verification

Run `npm test` from the homework folder. The 13 checks cover starter data, case-insensitive search, required fields, question/tag parsing, storage round trips, malformed data, and storage errors. No extra JavaScript test package is needed.

For the course's Python entry point, install `pytest` in your Python environment if needed:

```bash
python -m pip install pytest
```

Then run from the repository root, with Node.js on `PATH`:

```bash
pytest hw1/NikaBabuna
```

`../tests/test_pack_hub.py` invokes the same JavaScript suite and reports any failure through `pytest`. Python is only a test tool; the application does not use it at runtime.

Run the three browser checks in `../golden.md` against the production preview as well. Automated storage checks use an in-memory substitute; the browser checks verify the actual form, refresh, and preview. `npm run build` checks that the app bundles; it does not prove browser behavior. Screenshots from the latest browser run are in `../tests/evidence/`.
