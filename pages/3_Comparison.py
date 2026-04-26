import streamlit as st
from rag_core import get_stores
from style import inject_custom_css

st.set_page_config(
    page_title="Chunk Comparison — DigitalTrace",
    page_icon="⚖️",
    layout="wide",
)
inject_custom_css()

st.markdown("""
<div class="page-header">
    <h2>⚖️ Chunking Strategy Comparison</h2>
    <p>See how chunk size affects retrieval quality — same query, three configurations.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Why does chunk size matter?** When documents are split into smaller chunks 
(size=200), results are more precise but may lack context. Medium chunks 
(size=350) balance precision and context. Larger chunks (size=500) provide 
more context but may include less relevant text. Compare the results below.
""")

stores = get_stores()

query = st.text_input(
    "Enter a query to compare:",
    placeholder="e.g. How does canvas fingerprinting work?",
)

CONFIGS = [
    ("small", "🔹 Small (200)", "#6366f1"),
    ("medium", "🔸 Medium (350)", "#f59e0b"),
    ("large", "🔶 Large (500)", "#ef4444"),
]

if query.strip():
    cols = st.columns(3)

    for col, (key, label, color) in zip(cols, CONFIGS):
        with col:
            st.markdown(f"### {label}")
            st.caption(f"{stores[key]['chunk_count']} chunks total")
            results = stores[key]["store"].similarity_search_with_score(query, k=3)
            for doc, score in results:
                source = doc.metadata.get("source", "Unknown")
                st.markdown(f"""
                <div class="result-card" style="border-left-color: {color};">
                    <span class="source-tag" style="background: {color};">{source}</span>
                    <p class="passage">{doc.page_content}</p>
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"Relevance: {(1 - score) * 100:.0f}%")
else:
    st.markdown("""
    <div style="text-align:center; padding:3rem;">
        <p style="font-size:1.2rem;">Type a query above to compare retrieval results across three chunk sizes.</p>
    </div>
    """, unsafe_allow_html=True)
