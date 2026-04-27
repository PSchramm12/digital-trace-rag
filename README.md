# DigitalTrace — RAG Knowledge Base on Digital Fingerprinting

A Retrieval-Augmented Generation (RAG) web application that makes **digital fingerprinting** accessible and searchable. Built with Streamlit and a lightweight, memory-optimized retrieval core for stable free-tier deployment.

Developed for the AI and Deep Learning course at the University of Ljubljana, School of Economics and Business.

## What It Does

Type a natural-language question and the app retrieves the most relevant passage from a curated 15-document knowledge base on digital fingerprinting — the tracking technique that identifies users by device and browser characteristics without cookies.

## Features

- **Relevance Search** — retrieves the most relevant passages with low RAM usage
- **15 Expert-Written Documents** — covering browser, device, canvas, audio, and extension fingerprinting, plus countermeasures, legal aspects, and the information paradox
- **Corpus Statistics** — explore document structure and embedding model details
- **Custom UI** — polished design with Inter font, gradient hero sections, and interactive topic cards

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Retrieval | Lightweight TF-IDF (pure Python) |
| Text Processing | Custom chunking + tokenization |
| Runtime | Python 3.11 |

## Project Structure

```
app.py                  # Main search page
rag_core.py             # Documents, chunking, lightweight retrieval engine
style.py                # Custom CSS injection
requirements.txt        # Python dependencies
render.yaml             # Render deployment config
pages/
  1_About.py            # About page with topic coverage
  2_Statistics.py       # Corpus statistics, chunking configs, document index
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Render

The included `render.yaml` configures the app as a web service. Connect this repo to [Render](https://render.com) and it deploys automatically.
