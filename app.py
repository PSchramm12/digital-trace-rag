import streamlit as st
from style import inject_custom_css

st.set_page_config(
    page_title="DigitalTrace",
    page_icon="🔍",
    layout="centered",
)

# Precomputed chunk matrix only (fast). The ONNX query model loads on first search.
from rag_core import get_store

primary_store = get_store("medium")["store"]

inject_custom_css()

# --- Hero Section ---
st.markdown("""
<div class="hero-container">
    <h1>🔍 DigitalTrace</h1>
    <p class="hero-subtitle">
        Understand how websites identify and track you — without cookies.<br>
        A searchable knowledge base on <strong>digital fingerprinting</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

query = st.text_input(
    "🔎 Search the Knowledge Base",
    placeholder="e.g. How does canvas fingerprinting work?",
)
st.caption(
    "First search on a cold server can take ~30–90s while the small embedding model downloads; "
    "later searches are quick."
)

# Cosine distance = 1 − similarity (lower is better). Tuned so typos still match
# (~0.7) while clearly off-topic queries stay above ~0.85–0.95.
RELEVANCE_THRESHOLD = 0.84

if query.strip():
    with st.spinner("Searching… (loading embedding model on first use)"):
        results = primary_store.similarity_search_with_score(query, k=3)
    if results:
        best_score = results[0][1]
        is_off_topic = best_score > RELEVANCE_THRESHOLD
        if is_off_topic:
            st.warning(
                "No relevant match found for this query. "
                "This app only contains digital fingerprinting content. "
                "Try asking something like *\"How does canvas fingerprinting work?\"* "
                "or *\"What countermeasures exist against tracking?\"*"
            )
        else:
            shown = 0
            seen_sources = set()
            for doc, score in results:
                source = doc.metadata.get("source", "Unknown")
                if source in seen_sources:
                    continue
                seen_sources.add(source)
                relevance_pct = max(0, (1 - score) * 100)
                if shown == 0 or (score < RELEVANCE_THRESHOLD and shown < 2):
                    st.markdown(f"""
                    <div class="result-card">
                        <span class="source-tag">📄 {source}</span>
                        <p class="passage">{doc.page_content}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption(f"Relevance: {relevance_pct:.0f}%")
                    shown += 1

# --- What is Digital Fingerprinting? ---
st.markdown("---")
st.markdown("## 🧬 What is Digital Fingerprinting?")
st.markdown("""
Every time you visit a website, your browser shares details about itself — your 
screen size, installed fonts, operating system, timezone, and more. **Digital 
fingerprinting** combines these details into a unique identifier that can track 
you across the web — even if you clear your cookies or use private browsing.

Unlike cookies, fingerprinting happens silently in the background. Most people 
don't know it exists, and the resources that explain it are often too technical.
**DigitalTrace** makes this topic accessible.
""")

# --- Topic Cards ---
st.markdown("## 📚 Explore Topics")
st.markdown("*Click on the sidebar pages to learn more, or search above for specific questions.*")

TOPIC_DATA = [
    ("🌐", "Browser Fingerprinting", "User-Agent strings, HTTP headers, plugins, fonts — passive and active techniques that uniquely identify your browser."),
    ("📱", "Device Fingerprinting", "Hardware sensors, GPU details, battery level — cross-browser tracking via device characteristics."),
    ("💻", "JavaScript Fingerprinting", "How scripts use navigator, screen, and plugin objects to identify 96%+ of browsers."),
    ("🧩", "Extension Fingerprinting", "How adblockers, password managers, and privacy tools change the DOM and reveal your identity."),
    ("🎨", "Canvas Fingerprinting", "Invisible images rendered via HTML5 Canvas produce unique pixel patterns per device."),
    ("🔊", "Audio Fingerprinting", "Sound signals processed through the Web Audio API reveal hardware-specific deviations."),
    ("🔢", "Hashing & Entropy", "How characteristics combine into a unique hash — Shannon entropy and IP address entropy."),
    ("📢", "Marketing & Paywalls", "Fingerprinting as the cookie alternative for targeted ads and paywall enforcement."),
    ("🛡️", "Security & Fraud Detection", "Banks, 2FA systems, and bot detection using device fingerprints."),
    ("⚖️", "GDPR & Privacy Law", "How data protection laws classify fingerprint data and require consent."),
    ("🔒", "Countermeasures", "Tor, Brave, Privacy Badger, NoScript — what works, what breaks, and the usability cost."),
    ("📊", "Prevalence on the Web", "19% of top sites use fingerprinting scripts — and the number is growing."),
    ("🧠", "Privacy vs. Convenience", "Why most users accept tracking rather than deal with broken countermeasures."),
    ("🔄", "The Information Paradox", "Why hiding your identity can actually make you more unique and trackable."),
]

col1, col2 = st.columns(2)
for i, (icon, title, desc) in enumerate(TOPIC_DATA):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div class="topic-card">
            <h4><span class="topic-icon">{icon}</span>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# --- How it works ---
st.markdown("---")
st.markdown("## ⚙️ How It Works")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 1. Ask")
    st.markdown("Type a natural-language question about digital fingerprinting.")

with col_b:
    st.markdown("### 2. Search")
    st.markdown("Semantic search finds the most relevant passage by meaning, not keywords.")

with col_c:
    st.markdown("### 3. Learn")
    st.markdown("Read the matched passage from our curated 15-document knowledge base.")
