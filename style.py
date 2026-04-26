import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ══════════════════════════════════════
       LAYER 1: Backgrounds
       ══════════════════════════════════════ */

    .stApp,
    .stApp > header,
    .main,
    .main .block-container,
    section[data-testid="stMain"],
    div[data-testid="stAppViewContainer"],
    div[data-testid="stAppViewBlockContainer"],
    .stMainBlockContainer,
    div[class*="stAppViewContainer"],
    div[class*="main"] {
        background: linear-gradient(160deg, #dbeafe 0%, #ede9fe 35%, #e0e7ff 65%, #dbeafe 100%) !important;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div > div,
    section[data-testid="stSidebar"] > div > div > div,
    div[data-testid="stSidebarContent"],
    [data-testid="stSidebar"] * {
        background: #e0e7ff !important;
        background-color: #e0e7ff !important;
    }

    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="column"],
    .element-container,
    .stMarkdown,
    div[data-testid="stExpander"],
    div[data-testid="stForm"],
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent !important;
    }

    .main .block-container { max-width: 900px; padding-top: 2rem; }

    /* ══════════════════════════════════════
       LAYER 2: Global black text
       ══════════════════════════════════════ */

    h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif; color: #000 !important; }
    h1 { font-weight: 700; letter-spacing: -0.5px; }
    h2, h3 { font-weight: 600; }

    .main p, .main li, .main span, .main label, .main div,
    .main strong, .main em, .main a, .main code,
    .stMarkdown, .stMarkdown *, .stText,
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] *,
    .element-container, .element-container *,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] a {
        color: #000 !important;
    }

    /* ══════════════════════════════════════
       LAYER 3: Components (cards, inputs, etc.)
       ══════════════════════════════════════ */

    .topic-card {
        background: white; border: 1px solid #c7d2fe; border-radius: 14px;
        padding: 1.2rem 1.4rem; margin-bottom: 0.75rem;
        transition: all 0.25s ease; box-shadow: 0 2px 8px rgba(99,102,241,0.06);
    }
    .topic-card:hover { border-color: #818cf8; box-shadow: 0 6px 24px rgba(99,102,241,0.15); transform: translateY(-2px); }
    .topic-card h4 { margin: 0 0 0.3rem 0; color: #1e293b !important; font-size: 1rem; font-weight: 600; }
    .topic-card p { margin: 0; color: #64748b !important; font-size: 0.88rem; line-height: 1.5; }
    .topic-icon { font-size: 1.4rem; margin-right: 0.5rem; }

    .result-card {
        background: white; border-left: 5px solid #6366f1; border-radius: 0 14px 14px 0;
        padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 16px rgba(99,102,241,0.1);
    }
    .result-card .passage { color: #334155 !important; font-size: 1rem; line-height: 1.7; }

    .stat-card {
        background: white; border: 1px solid #c7d2fe; border-radius: 14px;
        padding: 1.5rem; text-align: center; box-shadow: 0 2px 8px rgba(99,102,241,0.06);
        transition: all 0.2s ease;
    }
    .stat-card:hover { box-shadow: 0 6px 20px rgba(99,102,241,0.12); transform: translateY(-1px); }

    div[data-testid="stTextInput"] input {
        border-radius: 12px; border: 2px solid #c7d2fe; padding: 0.75rem 1rem;
        font-size: 1rem; background: white !important; transition: all 0.2s ease;
        caret-color: #000000 !important;
        color: #000000 !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #94a3b8 !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1; box-shadow: 0 0 0 4px rgba(99,102,241,0.15);
    }

    div[data-testid="stMetric"] {
        background: white !important; border: 1px solid #c7d2fe; border-radius: 14px;
        padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(99,102,241,0.06);
    }

    hr {
        border: none; height: 2px;
        background: linear-gradient(90deg, transparent 0%, #a5b4fc 30%, #818cf8 50%, #a5b4fc 70%, transparent 100%);
        margin: 2rem 0;
    }

    .stButton > button {
        border: 1px solid #c7d2fe !important; border-radius: 10px !important;
        background: white !important; color: #4338ca !important; font-weight: 500;
        transition: all 0.2s ease; font-size: 0.82rem;
    }
    .stButton > button:hover {
        background: #eef2ff !important; border-color: #818cf8 !important;
        color: #312e81 !important; box-shadow: 0 4px 12px rgba(99,102,241,0.15);
    }

    .stTabs [data-baseweb="tab-list"] { background: #e0e7ff !important; border-radius: 10px; padding: 4px; gap: 4px; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; color: #4338ca !important; border-radius: 8px; font-weight: 500; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: white !important; color: #312e81 !important; font-weight: 600; box-shadow: 0 2px 8px rgba(99,102,241,0.15); }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

    table { border-radius: 12px; overflow: hidden; }
    th { background: #eef2ff !important; color: #312e81 !important; }
    td { background: white !important; color: #000 !important; }

    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] * { color: #333 !important; }

    .stAlert { background: white !important; border: 1px solid #c7d2fe; border-radius: 12px; }

    /* ══════════════════════════════════════
       LAYER 4 (LAST): White text on dark boxes
       These MUST come last to win specificity
       ══════════════════════════════════════ */

    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #3730a3 70%, #4338ca 100%) !important;
        border-radius: 20px; padding: 3rem 2.5rem; margin-bottom: 2rem;
        text-align: center; box-shadow: 0 10px 40px rgba(67,56,202,0.3);
    }
    .hero-container h1,
    .hero-container h2,
    .hero-container h3,
    .hero-container h4,
    .hero-container p,
    .hero-container span,
    .hero-container div,
    .hero-container strong,
    .hero-container em,
    .hero-container a,
    .hero-container li,
    .hero-container label { color: #ffffff !important; }
    .hero-container h1 { font-size: 2.8rem; margin-bottom: 0.5rem; }
    .hero-subtitle,
    .hero-subtitle * { color: #c7d2fe !important; }

    .page-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #3730a3 70%, #4338ca 100%) !important;
        border-radius: 16px; padding: 1.8rem 2rem; margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(67,56,202,0.25);
    }
    .page-header h1,
    .page-header h2,
    .page-header h3,
    .page-header h4,
    .page-header p,
    .page-header span,
    .page-header div,
    .page-header strong,
    .page-header em,
    .page-header a,
    .page-header li,
    .page-header label { color: #ffffff !important; }
    .page-header h2 { margin: 0; }
    .page-header p { color: #c7d2fe !important; margin: 0.3rem 0 0 0; }

    .result-card .source-tag {
        background: linear-gradient(135deg, #6366f1, #818cf8) !important;
        color: #ffffff !important; padding: 0.25rem 0.85rem; border-radius: 20px;
        font-size: 0.8rem; font-weight: 500; display: inline-block; margin-bottom: 0.75rem;
    }
    </style>
    """, unsafe_allow_html=True)
