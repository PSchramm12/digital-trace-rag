import streamlit as st
from style import inject_custom_css

st.set_page_config(
    page_title="Fingerprint Demo — DigitalTrace",
    page_icon="🖐️",
    layout="centered",
)

inject_custom_css()

st.markdown("""
<div class="page-header">
    <h2>🖐️ Live Fingerprint Demo</h2>
    <p>See what your browser reveals about you — right now, in real time.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
This page runs **real fingerprinting techniques** on your browser — the same ones 
used by trackers across the web. Nothing is sent to any server; everything stays 
in your browser. Scroll down to see what websites can learn about you.
""")

FINGERPRINT_HTML = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

.fp-container {
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

.fp-hash-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 12px;
    padding: 1.8rem;
    text-align: center;
    margin-bottom: 1.5rem;
    color: white;
}

.fp-hash-banner h3 {
    margin: 0 0 0.3rem 0;
    font-size: 0.9rem;
    font-weight: 500;
    color: #a8b2d1;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.fp-hash-banner .hash-value {
    font-family: 'Courier New', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #818cf8;
    word-break: break-all;
    letter-spacing: 1px;
}

.fp-hash-banner .hash-note {
    margin-top: 0.6rem;
    font-size: 0.8rem;
    color: #64748b;
}

.fp-section {
    margin-bottom: 1.2rem;
}

.fp-section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
}

.fp-section-title h4 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
}

.fp-section-title .fp-tag {
    background: #6366f1;
    color: white;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 500;
}

.fp-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
}

.fp-item {
    background: #f8f9fc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    transition: border-color 0.2s;
}

.fp-item:hover {
    border-color: #6366f1;
}

.fp-item .fp-label {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.25rem;
    font-weight: 500;
}

.fp-item .fp-value {
    font-size: 0.9rem;
    color: #1e293b;
    font-weight: 500;
    word-break: break-word;
}

.fp-item.full-width {
    grid-column: 1 / -1;
}

.fp-canvas-wrap {
    background: #f8f9fc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-top: 0.6rem;
}

.fp-canvas-wrap canvas {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    max-width: 100%;
}

.fp-canvas-wrap .canvas-hash {
    margin-top: 0.6rem;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    color: #6366f1;
    word-break: break-all;
}

.fp-uniqueness {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%);
    border-left: 4px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.5rem;
    margin-top: 1.2rem;
}

.fp-uniqueness h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    color: #1e293b;
}

.fp-uniqueness p {
    margin: 0;
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.5;
}

.fp-meter {
    width: 100%;
    height: 8px;
    background: #e2e8f0;
    border-radius: 4px;
    margin: 0.8rem 0 0.4rem 0;
    overflow: hidden;
}

.fp-meter-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #22c55e, #f59e0b, #ef4444);
    transition: width 0.6s ease;
}
</style>

<div class="fp-container">
    <div class="fp-hash-banner">
        <h3>Your Combined Fingerprint Hash</h3>
        <div class="hash-value" id="combined-hash">Collecting...</div>
        <div class="hash-note">This single value can identify your browser among millions</div>
    </div>

    <!-- Browser Info -->
    <div class="fp-section">
        <div class="fp-section-title">
            <h4>🌐 Browser & Header Attributes</h4>
            <span class="fp-tag">Passive · Browser Fingerprinting</span>
        </div>
        <div class="fp-grid">
            <div class="fp-item full-width">
                <div class="fp-label">User-Agent</div>
                <div class="fp-value" id="fp-useragent">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Platform</div>
                <div class="fp-value" id="fp-platform">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Language</div>
                <div class="fp-value" id="fp-language">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Do Not Track</div>
                <div class="fp-value" id="fp-dnt">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Cookies Enabled</div>
                <div class="fp-value" id="fp-cookies">—</div>
            </div>
        </div>
    </div>

    <!-- Device Info -->
    <div class="fp-section">
        <div class="fp-section-title">
            <h4>📱 Device & Screen</h4>
            <span class="fp-tag">Active · Device Fingerprinting</span>
        </div>
        <div class="fp-grid">
            <div class="fp-item">
                <div class="fp-label">Screen Resolution</div>
                <div class="fp-value" id="fp-screen">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Available Screen</div>
                <div class="fp-value" id="fp-avail-screen">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Color Depth</div>
                <div class="fp-value" id="fp-color">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Device Pixel Ratio</div>
                <div class="fp-value" id="fp-dpr">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Hardware Concurrency</div>
                <div class="fp-value" id="fp-cores">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Device Memory</div>
                <div class="fp-value" id="fp-memory">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Timezone</div>
                <div class="fp-value" id="fp-timezone">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Timezone Offset</div>
                <div class="fp-value" id="fp-tz-offset">—</div>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <div class="fp-section">
        <div class="fp-section-title">
            <h4>💻 JavaScript Properties</h4>
            <span class="fp-tag">Active · JS Fingerprinting</span>
        </div>
        <div class="fp-grid">
            <div class="fp-item">
                <div class="fp-label">Plugins Count</div>
                <div class="fp-value" id="fp-plugins">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">MIME Types</div>
                <div class="fp-value" id="fp-mime">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Touch Support</div>
                <div class="fp-value" id="fp-touch">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">Max Touch Points</div>
                <div class="fp-value" id="fp-touchpoints">—</div>
            </div>
        </div>
    </div>

    <!-- WebGL -->
    <div class="fp-section">
        <div class="fp-section-title">
            <h4>🎮 WebGL & Graphics</h4>
            <span class="fp-tag">Active · Device Fingerprinting</span>
        </div>
        <div class="fp-grid">
            <div class="fp-item">
                <div class="fp-label">WebGL Renderer</div>
                <div class="fp-value" id="fp-webgl-renderer">—</div>
            </div>
            <div class="fp-item">
                <div class="fp-label">WebGL Vendor</div>
                <div class="fp-value" id="fp-webgl-vendor">—</div>
            </div>
        </div>
    </div>

    <!-- Canvas -->
    <div class="fp-section">
        <div class="fp-section-title">
            <h4>🎨 Canvas Fingerprint</h4>
            <span class="fp-tag">Active · Canvas Fingerprinting</span>
        </div>
        <div class="fp-canvas-wrap">
            <canvas id="fp-canvas" width="400" height="60"></canvas>
            <div class="canvas-hash" id="fp-canvas-hash">Computing...</div>
        </div>
    </div>

    <!-- Uniqueness -->
    <div class="fp-uniqueness">
        <h4>📊 How Unique Are You?</h4>
        <p id="fp-summary">Analyzing your fingerprint...</p>
        <div class="fp-meter">
            <div class="fp-meter-fill" id="fp-meter-fill" style="width: 0%;"></div>
        </div>
        <p id="fp-attr-count" style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.3rem;">—</p>
    </div>
</div>

<script>
(function() {
    function simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16).padStart(8, '0');
    }

    function collectFingerprint() {
        const fp = {};

        // Browser & Header
        fp.userAgent = navigator.userAgent;
        fp.platform = navigator.platform || 'N/A';
        fp.language = navigator.language + ' (' + (navigator.languages || []).join(', ') + ')';
        fp.dnt = navigator.doNotTrack === '1' ? 'Enabled ⚠️' : 'Disabled';
        fp.cookies = navigator.cookieEnabled ? 'Yes' : 'No';

        // Device & Screen
        fp.screen = screen.width + ' × ' + screen.height;
        fp.availScreen = screen.availWidth + ' × ' + screen.availHeight;
        fp.colorDepth = screen.colorDepth + '-bit';
        fp.dpr = window.devicePixelRatio || 1;
        fp.cores = navigator.hardwareConcurrency || 'N/A';
        fp.memory = navigator.deviceMemory ? navigator.deviceMemory + ' GB' : 'N/A (Firefox/Safari)';
        fp.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        fp.tzOffset = 'UTC' + (new Date().getTimezoneOffset() > 0 ? '-' : '+') + Math.abs(new Date().getTimezoneOffset() / 60);

        // JavaScript
        fp.plugins = navigator.plugins.length + ' detected';
        fp.mimeTypes = navigator.mimeTypes.length + ' types';
        fp.touch = 'ontouchstart' in window ? 'Yes' : 'No';
        fp.touchPoints = navigator.maxTouchPoints || 0;

        // WebGL
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (gl) {
                const dbg = gl.getExtension('WEBGL_debug_renderer_info');
                fp.webglRenderer = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
                fp.webglVendor = dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR);
            } else {
                fp.webglRenderer = 'Not available';
                fp.webglVendor = 'Not available';
            }
        } catch(e) {
            fp.webglRenderer = 'Blocked';
            fp.webglVendor = 'Blocked';
        }

        // Canvas fingerprint
        try {
            const cvs = document.getElementById('fp-canvas');
            const ctx = cvs.getContext('2d');

            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, 400, 60);

            ctx.fillStyle = '#1a1a2e';
            ctx.font = '14px Arial';
            ctx.fillText('DigitalTrace Canvas Test 🔍', 10, 20);

            ctx.fillStyle = '#6366f1';
            ctx.font = 'bold 12px Courier New';
            ctx.fillText('ABCabc123!@#αβγ', 10, 45);

            ctx.beginPath();
            ctx.arc(350, 30, 20, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(99, 102, 241, 0.3)';
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(300, 10);
            ctx.lineTo(320, 50);
            ctx.lineTo(280, 50);
            ctx.closePath();
            ctx.fillStyle = 'rgba(245, 158, 11, 0.4)';
            ctx.fill();

            const dataUrl = cvs.toDataURL();
            fp.canvasHash = simpleHash(dataUrl);
        } catch(e) {
            fp.canvasHash = 'Blocked by browser';
        }

        return fp;
    }

    function render(fp) {
        document.getElementById('fp-useragent').textContent = fp.userAgent;
        document.getElementById('fp-platform').textContent = fp.platform;
        document.getElementById('fp-language').textContent = fp.language;
        document.getElementById('fp-dnt').textContent = fp.dnt;
        document.getElementById('fp-cookies').textContent = fp.cookies;
        document.getElementById('fp-screen').textContent = fp.screen;
        document.getElementById('fp-avail-screen').textContent = fp.availScreen;
        document.getElementById('fp-color').textContent = fp.colorDepth;
        document.getElementById('fp-dpr').textContent = fp.dpr;
        document.getElementById('fp-cores').textContent = fp.cores;
        document.getElementById('fp-memory').textContent = fp.memory;
        document.getElementById('fp-timezone').textContent = fp.timezone;
        document.getElementById('fp-tz-offset').textContent = fp.tzOffset;
        document.getElementById('fp-plugins').textContent = fp.plugins;
        document.getElementById('fp-mime').textContent = fp.mimeTypes;
        document.getElementById('fp-touch').textContent = fp.touch;
        document.getElementById('fp-touchpoints').textContent = fp.touchPoints;
        document.getElementById('fp-webgl-renderer').textContent = fp.webglRenderer;
        document.getElementById('fp-webgl-vendor').textContent = fp.webglVendor;
        document.getElementById('fp-canvas-hash').textContent = 'Hash: ' + fp.canvasHash;

        // Combined hash
        const combined = [
            fp.userAgent, fp.platform, fp.screen, fp.colorDepth,
            fp.timezone, fp.language, fp.cores, fp.webglRenderer,
            fp.canvasHash, fp.plugins, fp.dpr, fp.touchPoints
        ].join('|||');
        const fullHash = simpleHash(combined);
        document.getElementById('combined-hash').textContent = fullHash;

        // Uniqueness estimate
        let uniqueAttrs = 0;
        const total = 18;
        if (fp.userAgent.length > 30) uniqueAttrs += 2;
        if (fp.webglRenderer !== 'Not available' && fp.webglRenderer !== 'Blocked') uniqueAttrs += 3;
        if (fp.canvasHash !== 'Blocked by browser') uniqueAttrs += 3;
        if (fp.cores !== 'N/A') uniqueAttrs++;
        if (fp.memory !== 'N/A (Firefox/Safari)') uniqueAttrs++;
        if (fp.plugins !== '0 detected') uniqueAttrs++;
        if (fp.dnt === 'Enabled ⚠️') uniqueAttrs++;
        uniqueAttrs += 3; // screen, timezone, language always contribute
        if (fp.touch === 'Yes') uniqueAttrs++;
        uniqueAttrs += 2; // color depth, dpr

        const pct = Math.min(Math.round((uniqueAttrs / total) * 100), 100);
        document.getElementById('fp-meter-fill').style.width = pct + '%';
        document.getElementById('fp-attr-count').textContent = uniqueAttrs + ' of ' + total + ' attributes contributing to uniqueness';

        if (pct > 80) {
            document.getElementById('fp-summary').textContent = 'Your browser has a highly unique fingerprint. With ' + uniqueAttrs + ' identifying attributes, a tracker could likely distinguish you from most other visitors.';
        } else if (pct > 50) {
            document.getElementById('fp-summary').textContent = 'Your browser has a moderately unique fingerprint. Combined with a few more signals, you could be individually tracked.';
        } else {
            document.getElementById('fp-summary').textContent = 'Your browser reveals fewer identifying attributes than average — you may be using privacy protections.';
        }
    }

    const fp = collectFingerprint();
    render(fp);
})();
</script>
"""

st.components.v1.html(FINGERPRINT_HTML, height=1500, scrolling=True)

st.markdown("---")
st.markdown("### 🔗 Learn More — Click Any Topic")
st.markdown("*Each fingerprint attribute above maps to a topic in the knowledge base. Click to retrieve the relevant passage.*")

DEMO_TOPICS = [
    ("🌐", "Browser & Header Attributes", "How does browser fingerprinting through HTTP headers work?"),
    ("📱", "Device & Screen", "How does device fingerprinting use hardware information?"),
    ("💻", "JavaScript Properties", "How does JavaScript-based fingerprinting identify browsers?"),
    ("🎮", "WebGL & Graphics", "How do GPU and graphics card details contribute to device fingerprinting?"),
    ("🎨", "Canvas Fingerprint", "How does canvas fingerprinting exploit the HTML5 Canvas element?"),
    ("🔊", "Audio Fingerprint", "How does audio fingerprinting use the Web Audio API?"),
    ("🔢", "Combined Hash", "How are fingerprint characteristics combined into a unique hash?"),
    ("📊", "Uniqueness Score", "How prevalent is fingerprinting on the web?"),
    ("🔄", "Information Paradox", "Why can privacy measures make you more unique and trackable?"),
    ("🛡️", "Countermeasures", "What countermeasures exist against digital fingerprinting?"),
]

cols = st.columns(5)
for i, (icon, label, query) in enumerate(DEMO_TOPICS):
    with cols[i % 5]:
        if st.button(f"{icon} {label}", key=f"demo_{i}", use_container_width=True):
            st.session_state["demo_query"] = query

FOLLOW_UP_PROMPTS = {
    "How does browser fingerprinting through HTTP headers work?": [
        "What is the Do Not Track flag paradox?",
        "How does passive vs active fingerprinting differ?",
    ],
    "How does device fingerprinting use hardware information?": [
        "What is cross-browser fingerprinting?",
        "How do sensors contribute to mobile fingerprinting?",
    ],
    "How does JavaScript-based fingerprinting identify browsers?": [
        "What JavaScript objects are used for fingerprinting?",
        "How did Mayer identify 96% of browsers?",
    ],
    "How do GPU and graphics card details contribute to device fingerprinting?": [
        "What is WebGL fingerprinting?",
        "How does canvas fingerprinting exploit graphics hardware?",
    ],
    "How does canvas fingerprinting exploit the HTML5 Canvas element?": [
        "Who first discovered canvas fingerprinting?",
        "How is a canvas fingerprint converted to a hash?",
    ],
    "How does audio fingerprinting use the Web Audio API?": [
        "When was audio fingerprinting first researched?",
        "How does audio fingerprinting compare to canvas fingerprinting?",
    ],
    "How are fingerprint characteristics combined into a unique hash?": [
        "What is Shannon entropy in fingerprinting?",
        "How does IP address increase fingerprint uniqueness?",
    ],
    "How prevalent is fingerprinting on the web?": [
        "What percentage of top websites use fingerprinting?",
        "Which types of websites deploy fingerprinting most?",
    ],
    "Why can privacy measures make you more unique and trackable?": [
        "What is the information paradox?",
        "How does Tor Browser's letterboxing work?",
    ],
    "What countermeasures exist against digital fingerprinting?": [
        "How effective are blocking extensions against fingerprinting?",
        "Why was Brave's strict fingerprinting mode removed?",
    ],
}

if "demo_query" in st.session_state:
    query = st.session_state["demo_query"]
    from rag_core import get_store

    with st.spinner("Loading passage match… (embedding model on first use)"):
        primary_store = get_store("medium")["store"]
        results = primary_store.similarity_search_with_score(query, k=1)
    if results:
        doc, score = results[0]
        source = doc.metadata.get("source", "Unknown")
        st.markdown(f"""
        <div class="result-card">
            <span class="source-tag">📄 {source}</span>
            <p class="passage">{doc.page_content}</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Query: *{query}*  ·  Relevance: {(1 - score) * 100:.0f}%")

        follow_ups = FOLLOW_UP_PROMPTS.get(query, [])
        if follow_ups:
            st.markdown("**Dig deeper:**")
            follow_cols = st.columns(len(follow_ups))
            for j, prompt in enumerate(follow_ups):
                with follow_cols[j]:
                    if st.button(f"→ {prompt}", key=f"follow_{j}", use_container_width=True):
                        st.session_state["demo_query"] = prompt

st.markdown("---")
st.markdown("*No data from this demo is collected, stored, or transmitted. Everything runs locally in your browser.*")
