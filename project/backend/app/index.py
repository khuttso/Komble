"""Versioned local index; refuse different models, dimensions or changed corpus."""

import hashlib
import json
from pathlib import Path

from .config import EMBEDDING_MODEL, REPO, RUNTIME
from .llm import ModelError, gateway

CORPUS = REPO / "data" / "corpus"
INDEX_PATH = RUNTIME / "index.json"


def documents():
    return [(path.relative_to(CORPUS).as_posix(), path.read_text(encoding="utf-8"))
            for path in sorted(CORPUS.glob("*.md"))]


def corpus_hash(docs):
    return hashlib.sha256(json.dumps(docs, ensure_ascii=False).encode()).hexdigest()


def chunk_documents(docs):
    chunks = []
    for name, text in docs:
        # Metadata is retained in the document but excluded from retrieval text.
        body = text.split("\n---\n", 1)[-1].strip()
        words = body.split()
        for offset in range(0, len(words), 210):
            chunk = " ".join(words[offset:offset + 250])
            if chunk:
                chunks.append({"id": f"{name}:{offset}", "document": name, "text": chunk})
            if offset + 250 >= len(words):
                break
    return chunks


def build(client=gateway):
    docs = documents()
    if not docs:
        raise ModelError("No preparation documents are available.")
    chunks = chunk_documents(docs)
    vectors = client.embed([chunk["text"] for chunk in chunks])
    dimension = len(vectors[0])
    data = {"model": EMBEDDING_MODEL, "dimension": dimension, "corpus_hash": corpus_hash(docs),
            "chunks": [dict(chunk, vector=vector) for chunk, vector in zip(chunks, vectors, strict=True)]}
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = INDEX_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, allow_nan=False), encoding="utf-8")
    temporary.replace(INDEX_PATH)
    return data


def load():
    try:
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        if data["model"] != EMBEDDING_MODEL or data["corpus_hash"] != corpus_hash(documents()):
            raise ValueError("Incompatible index")
        if not data["chunks"] or any(len(chunk["vector"]) != data["dimension"] for chunk in data["chunks"]):
            raise ValueError("Invalid dimensions")
        return data
    except (OSError, ValueError, KeyError, TypeError):
        raise ModelError("The preparation index is missing or out of date. Run the documented index-build command.") from None


if __name__ == "__main__":
    index = build()
    print(f"Built {len(index['chunks'])} chunks; model={index['model']}; dimension={index['dimension']}")
