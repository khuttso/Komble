# ADR 002: local embeddings within the $0 budget

Date: 20 October 2026. Status: selected for implementation; live index/evaluation
verification must be recorded separately.

The user explicitly limited all provider spend to $0. Use FastEmbed CPU inference
with `BAAI/bge-small-en-v1.5` for document/query vectors. Download public weights
once into ignored `project/runtime/models/`; queries and documents stay local for
embedding. All embedding operations still pass through the same `llm.py` gateway
and log elapsed time, count, zero provider cost and unavailable provider tokens.

This deliberately differs from Lab 4's hosted embedding API example. We do not
claim to have made hosted embedding requests. Generation/vision use compatible
OpenRouter models with a `:free` ID and verified zero pricing, without fallbacks.

Index metadata records model name, dimensions and corpus fingerprint; incompatible
loads refuse. A change to the embedding model requires rebuilding the index.
Consequences: a model download and CPU memory/latency; no hosted embedding bill.
Hardware/electricity costs are excluded, not claimed to be literally zero.

Reference: [FastEmbed official documentation](https://qdrant.github.io/fastembed/).
