"""Rebuild data/precomputed_medium.npz after changing DOCUMENTS, chunking, or EMBED_MODEL_NAME."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag_core import CHUNK_CONFIGS, DOCUMENTS, EMBED_MODEL_NAME, embed_passages  # noqa: E402


def main() -> None:
    cfg = CHUNK_CONFIGS["medium"]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["chunk_size"],
        chunk_overlap=cfg["chunk_overlap"],
    )
    texts: list[str] = []
    metadatas: list[dict] = []
    for doc in DOCUMENTS:
        for chunk in splitter.split_text(doc["text"]):
            texts.append(chunk)
            metadatas.append({"source": doc["title"]})

    matrix = embed_passages(texts)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    matrix = matrix / np.maximum(norms, 1e-12)

    out = ROOT / "data" / "precomputed_medium.npz"
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out,
        matrix=matrix,
        texts=np.array(texts, dtype=object),
        metadatas=np.array(metadatas, dtype=object),
        embed_model=np.array(EMBED_MODEL_NAME),
    )
    print(f"Wrote {out} ({matrix.shape[0]} chunks, dim {matrix.shape[1]}, model={EMBED_MODEL_NAME})")


if __name__ == "__main__":
    main()
