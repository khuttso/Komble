# InterviewCoach tool contracts

## get_pack_questions

Read up to four questions and hints from the current public starter-pack catalogue.
This tool reads only; it does not generate questions or change application data.

| Property | Contract |
|---|---|
| Effect / undo | Read; nothing to undo |
| Idempotent | Yes, for unchanged catalogue data; each call appends operational metadata |
| Offered to | All callers, including visitors; only this public read capability exists |
| Identity | Not needed for public data; never accepted from model arguments |
| Touches | `project/backend/app/content.py::PACKS`; sanitized runtime audit log |
| Must never | Access private browser packs, answers, credentials, arbitrary paths or external APIs |
| Inputs | `pack_id`: frontend/support/graduate; `limit`: strict integer 1–4, default 4; extra fields forbidden |
| Result | pack_id/title strings; questions containing id/text/hint; returned/total integers |
| Failures | Bad arguments, tool not offered, catalogue entry unavailable, internal failure, audit log unavailable; readable corrective messages |
| Logging | UTC timestamp, allowlisted tool name, outcome and duration only; no inputs, caller identity or returned text |
| Budget | One bounded local lookup, at most four questions; zero model calls/tokens; no autonomous retry loop |

Source: [contract](../src/contracts.py), [implementation](../src/tools.py),
[dispatcher](../src/act.py), [MCP server](../src/mcp_server.py).
Both interfaces use the exact same Pydantic schema and dispatcher. The low-level
MCP handler preserves extra fields so they are refused rather than silently dropped.
The tool is a lookup of the running application's versioned catalogue, not a live
external data service. It cannot read personal packs stored in browser localStorage.

## Ownership

| Owner | HW2 tool | Status |
|---|---|---|
| aniararis | get_pack_questions | Selected by the user; implemented in this product branch |

No existing Lab 5 studio tool or owners table was present on the inspected main
commit `2f4e91f`. This addition supplies the minimal registry and MCP foundation;
it does not claim that earlier studio work was completed. Other students' choices
and the remaining Lab 5 coursework are not fabricated here.
