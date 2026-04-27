import streamlit as st
from style import inject_custom_css

st.set_page_config(page_title="About — DigitalTrace", page_icon="ℹ️", layout="centered")
inject_custom_css()

st.markdown("""
<div class="page-header">
    <h2>ℹ️ About DigitalTrace</h2>
    <p>What this project is, how it works, and why it exists.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### What is this?

**DigitalTrace** is a searchable knowledge base that explains **digital
fingerprinting** — the tracking method that identifies users by their device and
browser characteristics, without relying on cookies.

Most resources on this topic are jargon-heavy, fragmented, and assume prior
knowledge. DigitalTrace makes digital fingerprinting accessible to anyone curious
about how online tracking works.

### How does it work?

Type a natural-language question on the main page. The app uses **semantic
search** (powered by sentence-transformers and ChromaDB) to find the most
relevant passage from the curated document corpus. Results are ranked by meaning,
not keywords.

---

### Topic Coverage

The knowledge base covers **15 distinct subtopics**:
""")

topics = [
    ("🌐", "Digital Fingerprinting Basics", "Definition, passive vs active fingerprinting, how it differs from cookies"),
    ("🖥️", "Browser Fingerprinting", "User-Agent, HTTP headers, plugins, fonts, DNT flag paradox"),
    ("📱", "Device Fingerprinting", "Hardware sensors, GPU, battery, cross-browser tracking"),
    ("💻", "JavaScript-Based Fingerprinting", "Navigator, screen, mimeTypes objects — identifying 96%+ of browsers"),
    ("🎨", "Canvas Fingerprinting", "HTML5 Canvas pixel patterns, Base64 hashing, GPU-driven uniqueness"),
    ("🔊", "Audio Fingerprinting", "Web Audio API, hardware deviations, 2015/16 research"),
    ("🧩", "Extension-Based Fingerprinting", "DOM changes from adblockers, password managers, privacy tools"),
    ("🔢", "Hashing, Entropy & IP Addresses", "Shannon entropy, EFF 2010 study, IP as high-entropy identifier"),
    ("📢", "Marketing, Ad-Tech & Paywalls", "Cross-device tracking, targeted ads, paywall enforcement"),
    ("🛡️", "Security & Fraud Detection", "Bank logins, bot prevention, augmented authentication, 2FA coupling"),
    ("⚖️", "GDPR & Privacy Law", "Personal data classification, consent requirements, surreptitious collection"),
    ("🔒", "Countermeasures & Protection", "Tor, Brave, NoScript, Canvas Defender, spoofing — and their limitations"),
    ("📊", "Prevalence on the Web", "19% of top 10K sites, 66.6% of TRANCO top 10K transmitting FP data"),
    ("🧠", "Privacy Awareness & Trade-offs", "Why users accept tracking over broken countermeasures"),
    ("🔄", "The Information Paradox", "Why hiding your identity can make you more unique and trackable"),
]

for i, (icon, title, desc) in enumerate(topics, 1):
    st.markdown(f"""
    <div class="topic-card">
        <h4><span class="topic-icon">{icon}</span>{i}. {title}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
### Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Embeddings | all-MiniLM-L6-v2 (sentence-transformers) |
| Vector Store | ChromaDB |
| Text Processing | LangChain |
| Runtime | Python 3.11 |

---

### About this project

This is an academic project for a university AI & Deep Learning course,
demonstrating Retrieval-Augmented Generation (RAG) technology. The documents are
author-written based on genuine research expertise in digital fingerprinting.

This is a **retrieval-only tool** — it returns relevant source passages, not
AI-generated answers.
""")
