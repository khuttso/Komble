"""Local token-count comparison; never sends the full corpus to a provider."""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from tokenizers import Tokenizer

from project.backend.app.config import RUNTIME
from project.backend.app.grounding import retrieve
from project.backend.app.index import chunk_documents, documents
passages = chunk_documents(documents())
question = "What does STAR stand for when structuring a behavioral interview answer?"
retrieved = [hit for hit in retrieve(question, k=5) if hit["score"] >= 0.55]
tokenizer_path = next((RUNTIME / "models").rglob("tokenizer.json"))
tokenizer = Tokenizer.from_file(str(tokenizer_path))
tokenizer.no_truncation()
tokenizer.no_padding()
full_tokens = len(tokenizer.encode("\n\n".join(hit["text"] for hit in passages)).ids)
retrieved_tokens = len(tokenizer.encode("\n\n".join(hit["text"] for hit in retrieved)).ids)
result = {"question": question, "mode": "local_only", "tokenizer": "BGE local tokenizer; not the generation provider tokenizer",
          "full_corpus_passages": len(passages), "retrieved_passages": len(retrieved),
          "full_corpus_local_tokens": full_tokens, "retrieved_local_tokens": retrieved_tokens,
          "context_reduction_percent": round(100 * (1 - retrieved_tokens / full_tokens), 2),
          "limits": "Excludes instructions and query overhead. Proxy counts are not measured generation-provider tokens. No full corpus was uploaded."}
path = REPO / "docs/evidence/context-comparison.json"
path.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
