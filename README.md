# DigitalTrace — RAG Knowledge Base on Digital Fingerprinting

A Retrieval-Augmented Generation (RAG) web application that makes **digital fingerprinting** accessible and searchable. Built with Streamlit, **MiniLM-L6-v2 sentence embeddings (ONNX)**, and a **NumPy** retrieval layer for semantic search without a full vector DB — tuned for modest RAM on free-tier hosting.

Developed for the AI and Deep Learning course at the University of Ljubljana, School of Economics and Business.

## What It Does

Type a natural-language question and the app retrieves the most relevant passage from a curated 15-document knowledge base on digital fingerprinting — the tracking technique that identifies users by device and browser characteristics without cookies.

## Features

- **Semantic search** — dense embeddings so similar *meaning* matches (including light typos), not just shared keywords
- **15 Expert-Written Documents** — covering browser, device, canvas, audio, and extension fingerprinting, plus countermeasures, legal aspects, and the information paradox
- **Live Fingerprint Demo** — interactive browser fingerprint visualization with linked topic prompts
- **Corpus Statistics** — explore document structure and embedding model details
- **Custom UI** — polished design with Inter font, gradient hero sections, and interactive topic cards

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Retrieval | MiniLM-L6-v2 (ONNX) + NumPy cosine similarity |
| Text Processing | LangChain `RecursiveCharacterTextSplitter` |
| Runtime | Python 3.11 |

## Project Structure

```
app.py                  # Main search page
rag_core.py             # Documents, chunking, embeddings, NumPy vector store
style.py                # Custom CSS injection
requirements.txt        # Python dependencies
render.yaml             # Render deployment config
pages/
  1_About.py            # About page with topic coverage
  2_Statistics.py       # Corpus statistics, chunking configs, document index
  3_Fingerprint_Demo.py # Interactive fingerprint demo page
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Render

The included `render.yaml` configures the app as a web service. Connect this repo to [Render](https://render.com) and it deploys automatically.
