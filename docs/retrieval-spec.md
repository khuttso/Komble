# Grounded preparation guidance specification

Status: implemented locally. [Tuning/results](decisions/003-retrieval-tuning.md)
record the actual 4/5 live golden outcome and remaining failure.

## Corpus and ownership

10–15 shareable documents in root `data/corpus/`, one topic per Markdown file.
Topics: behavioral-answer structure, truthful examples, limited experience,
teamwork, mistakes, learning, frontend preparation and customer-support preparation.
Owner: Anastasia as existing spec/evaluation keeper; team review before release.
Record origin, team-authored status and last-reviewed date; review monthly and
whenever guidance changes. No private employer questions or personal records.

## Retrieval contract

Exclude the document metadata header, then use <=250-word whitespace windows with
40-word overlap. IDs contain filename and word offset. Initial k=3 was increased
to **k=5** after evaluation; cosine threshold **0.55** is retained. This threshold
is model/corpus-specific. Use local CPU BAAI/bge-small-en-v1.5, as recorded in
[ADR 002](decisions/002-free-local-embeddings.md). Record model name, dimension and
corpus hash in the index; refuse incompatible loads and rebuild explicitly. A
future model-weight revision should also be pinned explicitly (remaining hardening).

Query embedding -> scored chunks -> threshold -> generation or early refusal.
No matching chunk means no generation call. A query embedding can still be a
model operation. Every operation goes through `llm.py` and logs usage/latency.

## Answer contract

Pydantic-validated `{answer, citations, grounded}`; no confidence field. Each answer
sentence cites a supplied `[n]`. Code rejects unknown citations, missing markers,
uncited sentences and grounded=false. UI maps each `[n]` to the correct retrieved
document and excerpt. Citation existence is not proof of semantic support; evaluate
support in golden checks and human review.

Refusal text: "I couldn't find enough support in our preparation guides to answer
that. Try a more specific interview-preparation question."
Log one sanitized event per answer/refusal with reason; never the private query.

## Evaluation

Five implemented cases: factual structure, factual truthful achievements, reasoning
combining limited experience and answer structure, typo/ambiguous phrasing, and
refusal for an unrelated weather/stock question. [Golden definition](../evals/golden.yaml)
and [saved runs](../evals/results/) retain failures and tuning diagnoses. The
truthful-achievements case still refuses despite source support; it is not a pass.
