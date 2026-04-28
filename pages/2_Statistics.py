import streamlit as st
from rag_core import DOCUMENTS, CHUNK_CONFIGS, get_chunk_count
from style import inject_custom_css

st.set_page_config(page_title="Statistics — DigitalTrace", page_icon="📊", layout="centered")
inject_custom_css()

st.markdown("""
<div class="page-header">
    <h2>📊 Corpus Statistics</h2>
    <p>Structure and configuration of the DigitalTrace knowledge base.</p>
</div>
""", unsafe_allow_html=True)

total_words = sum(len(doc["text"].split()) for doc in DOCUMENTS)
total_chars = sum(len(doc["text"]) for doc in DOCUMENTS)

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

st.markdown("### Chunking Configuration")
_m = CHUNK_CONFIGS["medium"]
st.markdown(f"""
The app uses a **medium chunking strategy** (chunk size = {_m["chunk_size"]}, overlap = {_m["chunk_overlap"]})
with **fewer, longer chunks** to keep memory use low on 512 MB hosts. The table below compares all three strategies.
""")

for key, label, color in [("small", "🔹 Small", "#6366f1"), ("medium", "🔸 Medium (active)", "#f59e0b"), ("large", "🔶 Large", "#ef4444")]:
    cfg = CHUNK_CONFIGS[key]
    chunk_count = get_chunk_count(key)
    st.markdown(f"""
    <div class="stat-card" style="margin-bottom:0.75rem;">
        <h4>{label}</h4>
        <p style="font-size:2rem; font-weight:700; color:{color} !important; margin:0.5rem 0;">{chunk_count}</p>
        <p>chunks at size={cfg['chunk_size']}, overlap={cfg['chunk_overlap']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Embedding Model")
st.markdown("""
<div class="stat-card" style="text-align:left;">
    <h4>🤖 Semantic retrieval (fastembed / ONNX)</h4>
    <table style="width:100%; border-collapse:collapse;">
        <tr><td style="padding:0.3rem 0; color:#64748b;">Model</td><td style="padding:0.3rem 0;">all-MiniLM-L6-v2 (384-d, ONNX via fastembed, bundled locally with the app)</td></tr>
        <tr><td style="padding:0.3rem 0; color:#64748b;">Distance</td><td style="padding:0.3rem 0;">Cosine distance 1 − similarity on L2-normalized vectors</td></tr>
        <tr><td style="padding:0.3rem 0; color:#64748b;">Store</td><td style="padding:0.3rem 0;">Precomputed chunk matrix + bundled ONNX model + NumPy dot-product search</td></tr>
        <tr><td style="padding:0.3rem 0; color:#64748b;">Goal</td><td style="padding:0.3rem 0;">Semantic matches with minimal footprint on free-tier hosting</td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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
