"""Rebuild data/precomputed_medium.npz after changing DOCUMENTS / chunk settings in rag_core."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag_core import CHUNK_CONFIGS, DOCUMENTS  # noqa: E402


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

    from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2

    ef = ONNXMiniLM_L6_V2()
    raw = ef(texts)
    matrix = np.stack([np.asarray(e, dtype=np.float32) for e in raw], axis=0)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    matrix = matrix / np.maximum(norms, 1e-12)

    out = ROOT / "data" / "precomputed_medium.npz"
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out,
        matrix=matrix,
        texts=np.array(texts, dtype=object),
        metadatas=np.array(metadatas, dtype=object),
    )
    print(f"Wrote {out} ({matrix.shape[0]} chunks, dim {matrix.shape[1]})")


if __name__ == "__main__":
    main()
