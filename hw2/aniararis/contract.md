# Tool Contract · get_pack_questions · aniararis

**Purpose:** Read up to four questions and hints from a public InterviewCoach starter pack. Changes nothing in the catalogue.

| Property | Rule enforced in code |
|---|---|
| Effect / undo | Reads public catalogue; nothing to undo. Appends sanitized operational metadata. |
| Idempotent | Repeated calls return the same data while the catalogue is unchanged. |
| Offered to | Visitors and signed-in callers; no private-data or write capability exists. |
| Identity from | Not required for public reads. Never accepted as a tool argument. |
| Touches | Shared application's `content.PACKS`; local runtime tool audit log. |
| Must never | Read personal browser packs, answers, keys or arbitrary files; call a provider; modify the catalogue. |

| Argument | Type / constraint | Description |
|---|---|---|
| pack_id | Literal frontend, support or graduate | Which public starter pack to read |
| limit | Strict integer 1–4; default 4 | Maximum questions returned |

Unknown fields are refused with `extra="forbid"`. The same Pydantic contract supplies both schemas. The MCP handler forwards raw arguments to the common dispatcher so forged identity fields are not silently discarded.

**Result:** `pack_id`, `title` (strings), `questions` (list of id/text/hint objects), `returned`, `total` (integers). IDs identify public questions only. No model-generated facts are added. The data is the current versioned application catalogue, not a live external feed.

**Failures:** A tool outside the offered set returns “Choose a tool from the offered list.” Invalid inputs describe allowed pack names, integer bounds and removal of extra/identity fields. A missing pack requests another pack or maintainer restoration. Internal and logging failures ask for maintainer help without exposing paths or stack traces.

**Budget and logging:** One local lookup; maximum four questions; zero model calls, tokens or provider charges. No retry loop. Each call records UTC timestamp, allowlisted tool name, outcome and duration; arguments, caller identities and results are omitted.

**Verification:** [Five golden cases](https://github.com/khuttso/Komble/blob/main/evals/tools/aniararis.yaml): frontend-two, support-one, graduate-default, zero-limit, forged-identity. Additional tests cover unavailable tools, path/instruction strings, types/bounds, missing data, safe errors/logs, schema parity and actual MCP stdio transport. See [evidence](evidence.md).

**Code on main after the product merge:** [contract](https://github.com/khuttso/Komble/blob/main/src/contracts.py), [function/registry](https://github.com/khuttso/Komble/blob/main/src/tools.py), [dispatcher](https://github.com/khuttso/Komble/blob/main/src/act.py), [MCP](https://github.com/khuttso/Komble/blob/main/src/mcp_server.py). These paths are prepared locally and are not yet published on main.
