import streamlit as st
from rag_core import DOCUMENTS, CHUNK_CONFIGS, get_stores
from style import inject_custom_css

st.set_page_config(page_title="Statistics — DigitalTrace", page_icon="📊", layout="centered")
inject_custom_css()

st.markdown("""
<div class="page-header">
    <h2>📊 Corpus Statistics</h2>
    <p>Structure and configuration of the DigitalTrace knowledge base.</p>
</div>
""", unsafe_allow_html=True)

stores = get_stores()
total_words = sum(len(doc["text"].split()) for doc in DOCUMENTS)
total_chars = sum(len(doc["text"]) for doc in DOCUMENTS)

# --- Key Metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📄 Documents", len(DOCUMENTS))
with col2:
    st.metric("📝 Total Words", f"{total_words:,}")
with col3:
    st.metric("📏 Avg. Words", f"{total_words // len(DOCUMENTS)}")
with col4:
    st.metric("🔤 Total Chars", f"{total_chars:,}")

st.markdown("---")

# --- Chunking Configurations ---
st.markdown("### Chunking Configurations")

CHUNK_DISPLAY = [
    ("small", "🔹 Small Chunks", "#6366f1"),
    ("medium", "🔸 Medium Chunks", "#f59e0b"),
    ("large", "🔶 Large Chunks", "#ef4444"),
]

chunk_cols = st.columns(3)
for col, (key, label, color) in zip(chunk_cols, CHUNK_DISPLAY):
    with col:
        cfg = CHUNK_CONFIGS[key]
        st.markdown(f"""
        <div class="stat-card">
            <h4>{label}</h4>
            <p style="font-size:2rem; font-weight:700; color:{color} !important; margin:0.5rem 0;">
                {stores[key]['chunk_count']}
            </p>
            <p>chunks at size={cfg['chunk_size']}, overlap={cfg['chunk_overlap']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- Embedding Model ---
st.markdown("### Embedding Model")

st.markdown("""
<div class="stat-card" style="text-align:left;">
    <h4>🤖 all-MiniLM-L6-v2</h4>
    <table style="width:100%; border-collapse:collapse;">
        <tr><td style="padding:0.3rem 0; color:#64748b;">Size</td><td style="padding:0.3rem 0;">~80 MB</td></tr>
        <tr><td style="padding:0.3rem 0; color:#64748b;">Dimensions</td><td style="padding:0.3rem 0;">384</td></tr>
        <tr><td style="padding:0.3rem 0; color:#64748b;">Language</td><td style="padding:0.3rem 0;">English</td></tr>
        <tr><td style="padding:0.3rem 0; color:#64748b;">Source</td><td style="padding:0.3rem 0;">sentence-transformers (Hugging Face)</td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Document Index ---
st.markdown("### Document Index")

for i, doc in enumerate(DOCUMENTS, 1):
    word_count = len(doc["text"].split())
    char_count = len(doc["text"])
    pct = (word_count / total_words) * 100
    st.markdown(f"""
    <div class="topic-card">
        <h4>{i}. {doc['title']}</h4>
        <p>{word_count} words · {char_count} chars · {pct:.0f}% of corpus</p>
    </div>
    """, unsafe_allow_html=True)
