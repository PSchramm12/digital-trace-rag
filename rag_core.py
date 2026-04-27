from pathlib import Path

import numpy as np
import streamlit as st
from dataclasses import dataclass, field
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCUMENTS = [
    {
        "text": (
            "Digital fingerprinting is a method for the automated collection of "
            "device data that generates a unique identification fingerprint for a "
            "user. A fingerprint is defined as a set of information elements that "
            "identifies a device or application instance. Fingerprinting is the "
            "process of an observer uniquely identifying a device or application "
            "based on multiple information elements communicated to them. The "
            "technique gathers information such as browser version, operating "
            "system, screen resolution, or installed fonts to produce an individual "
            "user ID. Unlike cookies, fingerprinting often occurs in the background "
            "and is barely perceptible to the user. Digital fingerprinting can be "
            "split into browser fingerprinting, which uses browser-level attributes, "
            "and device fingerprinting, which incorporates hardware characteristics."
        ),
        "title": "Digital Fingerprinting Basics",
    },
    {
        "text": (
            "Browser fingerprinting occurs when a browser divulges information "
            "about its version, the operating system, IP address, and further "
            "information necessary for HTTP communication. Passive fingerprinting "
            "happens instantly when an HTTP connection is established — the browser "
            "automatically transmits User-Agent, HTTP headers, timezone, installed "
            "plugins, fonts, screen resolution, color depth, and language settings. "
            "Active fingerprinting requires scripts or plugins to discover "
            "properties like supported MIME types, hardware information, and "
            "installed fonts. Studies show that even a few parameters are sufficient "
            "to uniquely identify a browser among millions of entries. The HTTP "
            "header includes the Do Not Track (DNT) setting, which ironically can "
            "contribute to a more unique fingerprint. Rare browsers and operating "
            "systems like Opera and Linux can be fingerprinted with even higher "
            "accuracy using the User-Agent string."
        ),
        "title": "Browser Fingerprinting",
    },
    {
        "text": (
            "Device fingerprinting extends browser data with hardware-related "
            "information. On mobile devices, sensor data, processor and GPU "
            "details, or battery level are factored in. The goal is to re-identify "
            "a device even if the browser has been changed or cookies deleted. Every "
            "hardware configuration leaves a unique trace. When device "
            "characteristics are combined with browser information, the device can "
            "be identified with high accuracy. This enables cross-browser "
            "fingerprinting — tracking users across multiple browsers because "
            "operating system and hardware attributes remain consistent. Device "
            "fingerprinting is frequently used in fraud detection to spot unusual "
            "configurations."
        ),
        "title": "Device Fingerprinting",
    },
    {
        "text": (
            "JavaScript-based fingerprinting exploits JavaScript's privileged "
            "position inside the browser. The browser resources accessible to "
            "JavaScript can disclose information about the browser, screen, "
            "operating system, time zone, supported file types, fonts, and "
            "installed plugins. In 2009, Mayer uniquely identified more than 96% "
            "of 1328 web clients using only JavaScript navigator, screen, plugins, "
            "and mimeTypes objects. Eckersley expanded the feature set in 2010 by "
            "adding fonts, timezones, and the browser-accept header. A list of "
            "installed fonts stands out as one of the most distinctive features of "
            "a system. When a third-party script includes active fingerprinting "
            "functionality, the data can be cross-validated with information from "
            "the HTTP header obtained passively. The user is typically unaware of "
            "the fingerprinting since the script may execute within the context of "
            "clicking a banner or inspecting a product."
        ),
        "title": "JavaScript-Based Fingerprinting",
    },
    {
        "text": (
            "Canvas fingerprinting exploits the HTML5 Canvas element. In the "
            "background, a webpage instructs the browser to render an invisible "
            "image or text and reads out the resulting pixel pattern. Even the "
            "smallest differences in graphics drivers or font anti-aliasing produce "
            "characteristic patterns. The rendered graphic is converted into a "
            "fingerprint via a hash algorithm such as SHA. This method was first "
            "studied by Mowery and Shacham around 2012 and is today a common "
            "component of modern fingerprinting tools. The operating system, "
            "installed fonts, graphics card, drivers, and the browser itself all "
            "affect how the image is rendered. Each browser produces a separate "
            "Base64 encrypted string whose unique hash can be used as a browser "
            "identifier. Canvas fingerprinting is both a browser and device "
            "fingerprinting technique, and the generated fingerprint remains "
            "invisible to the user."
        ),
        "title": "Canvas Fingerprinting",
    },
    {
        "text": (
            "Audio fingerprinting is a newer method that uses the processing of "
            "audio signals for tracking purposes. A webpage generates a brief "
            "sound impulse via the Web Audio API and measures how the browser and "
            "audio hardware process it. Minor differences in speaker and sound "
            "card components produce characteristic deviations that enable a "
            "fingerprint. This technique resembles canvas fingerprinting and was "
            "uncovered by researchers around 2015/16. Practical use remains rare, "
            "but it illustrates yet another avenue for tracking methods."
        ),
        "title": "Audio Fingerprinting",
    },
    {
        "text": (
            "Browser extensions like adblockers, themes, password managers, and "
            "privacy tools can be detected and used for fingerprinting. Unlike "
            "plugins, extension presence cannot be extracted with an API. Instead, "
            "extensions are detected through the DOM changes they introduce. A "
            "tracking script on an arbitrary domain can trigger extensions by "
            "dynamically creating elements like password fields, and the resulting "
            "DOM changes reveal the presence of specific extensions. On popular "
            "domains like YouTube or Twitter, extensions that add features like "
            "cinema mode or save-to-pocket create detectable DOM modifications. "
            "Research has shown that a significant proportion of popular browser "
            "extensions are fingerprintable, and they reveal aspects of users' "
            "interests and behaviors — such as income level through coupon "
            "extensions, or privacy interest through privacy tools."
        ),
        "title": "Extension-Based Fingerprinting",
    },
    {
        "text": (
            "Most fingerprinting algorithms work by combining numerous stable "
            "characteristics. This is referred to as a hash of the collected data: "
            "the list of installed fonts, browser settings, or pixel hashes of "
            "canvas images all feed into a checksum. The result is a unique value "
            "for each user. Researchers measure this uniqueness using concepts such "
            "as Shannon entropy. The EFF found as early as 2010 that most browsers "
            "could be individually identified based on such characteristics. The "
            "IP address also yields high entropy and makes the fingerprint more "
            "unique. Eckersley showed that sufficient fingerprinting information "
            "given a user's IP address will nearly always be enough to uniquely "
            "identify a browser. The IP address can even distinguish users from "
            "the same household behind the same router."
        ),
        "title": "Hashing, Entropy & IP Addresses",
    },
    {
        "text": (
            "In online marketing and the advertising industry, fingerprinting "
            "serves as an important tracking alternative to cookies. By combining "
            "multiple attributes, a user can be recognized across devices and "
            "websites, enabling targeted advertising. As major browsers now block "
            "third-party cookies, companies are increasingly turning to "
            "fingerprinting. A user with an outdated graphics card might generate "
            "a canvas fingerprint on one website, and a third-party ad script on "
            "another site could recognize their fingerprint and deliver targeted "
            "ads for new graphics cards. News websites use fingerprinting for "
            "paywall enforcement — services like Piano's Tinypass use browser "
            "fingerprinting to identify users who have already accessed free "
            "articles. Fingerprinting has become more popular than cookies for "
            "advertising and paywall enforcement."
        ),
        "title": "Marketing, Ad-Tech & Paywalls",
    },
    {
        "text": (
            "Fingerprints are used in security contexts, particularly for fraud "
            "detection. A bank can capture the device fingerprint and factor it "
            "into subsequent logins. If the fingerprint changes due to a new "
            "device, the system raises an alert. Security systems couple "
            "fingerprints with additional checks like 2FA and CAPTCHAs when an "
            "unknown fingerprint appears. Bots and fraudsters spoof features like "
            "IP address and delete cookies to avoid detection, but dependencies "
            "among fingerprint components reveal inconsistencies. If collected "
            "attributes don't match the purported device, a service provider may "
            "refuse access or halt a transaction. Commercial companies now include "
            "fingerprinting in security products to prevent online fraud. A German "
            "bank was found using canvas fingerprinting as part of their online "
            "banking security. Websites also use fingerprinting to detect web "
            "crawlers by identifying inconsistencies in URL request fingerprints."
        ),
        "title": "Security & Fraud Detection",
    },
    {
        "text": (
            "Data protection laws such as the GDPR and the ePrivacy Directive "
            "classify much fingerprinting data as personal data. Since a detailed "
            "fingerprint can infer individual browsing behavior, fingerprinting is "
            "generally subject to the same consent requirements as cookies. In the "
            "EU, collecting fingerprint information often requires explicit user "
            "consent. Data protection authorities warn that fingerprinting happens "
            "covertly, and websites can build profiles just as invasive as those "
            "from third-party cookies — but without the user's knowledge. Privacy "
            "concerns include loss of anonymity, the surreptitious nature of data "
            "collection, and the threat of data sharing with unauthorized third "
            "parties. Information gathered through fingerprinting could be linked "
            "to public records, stolen login data, or social media profiles."
        ),
        "title": "GDPR & Privacy Law",
    },
    {
        "text": (
            "Several countermeasures exist against digital fingerprinting. "
            "Blocking extensions such as NoScript, Ghostery, and Privacy Badger "
            "detect and block JavaScript-based fingerprinting scripts but are not "
            "explicitly designed to combat fingerprinting, resulting in limited "
            "effectiveness. Merzdovnik et al. noted these tools often fail to "
            "block sophisticated fingerprinting scripts and may break website "
            "functionalities. Canvas Defender is a specialized countermeasure that "
            "alters the RGB values of canvas-rendered pixels, but it remains a "
            "partial solution as it does not address other fingerprinting methods. "
            "Spoofing extensions alter HTTP header values and JavaScript properties "
            "to present a false browser identity, but can backfire — increasing "
            "uniqueness due to inconsistencies between spoofed and actual values. "
            "Privacy-focused browsers like Tor enforce a uniform configuration by "
            "spoofing language, browser version, timezone, and operating system "
            "while disabling Canvas and WebGL APIs. However, Tor users face "
            "significant usability costs: slower browsing, CAPTCHAs, blocked "
            "resources, and no saved passwords. Brave added subtle noise to "
            "fingerprinting APIs, but its strict mode was discontinued in 2024 "
            "due to low adoption and frequent web breakages."
        ),
        "title": "Countermeasures & Protection",
    },
    {
        "text": (
            "The information paradox in digital fingerprinting means that "
            "measures designed to hide your identity can actually make you stand "
            "out if few people use them. Eckersley noted that many privacy "
            "measures like spoofing or blocking features only work when many "
            "users share the same configuration — otherwise the countermeasure "
            "itself becomes a unique marker and contributes to a more distinct "
            "fingerprint. A user trying to block fingerprinting may end up with "
            "a rare combination of attributes that increases entropy instead of "
            "reducing it. A concrete example is Tor Browser's attempt to bucket "
            "screen sizes: Tor locks windows to 200x100 pixel steps and adds "
            "margins through letterboxing to force every user into a few sizes. "
            "But if a monitor size is uncommon and the user maximizes the screen, "
            "the resulting fingerprint becomes very distinct. This paradox "
            "highlights a fundamental challenge — achieving true anonymity "
            "requires a large crowd of identical configurations, which is "
            "difficult to achieve in practice."
        ),
        "title": "The Information Paradox",
    },
    {
        "text": (
            "Research shows fingerprinting is widespread on the web. In 2020, "
            "Fietkau et al. crawled the Top 10,000 Alexa websites and discovered "
            "that 19% heavily deploy obfuscated fingerprinting scripts. 28% of "
            "websites collected high amounts of device data, using 20 different "
            "features including GPU, memory, and connection information. Iqbal et "
            "al. found fingerprinting scripts present in more than 10% of the top "
            "100,000 websites, coming from vendors offering cross-site tracking or "
            "anti-fraud services. News and shopping websites most commonly deploy "
            "fingerprinting. In 2022, researchers discovered that 66.6% of the "
            "top 10,000 TRANCO websites were transmitting fingerprinting data. "
            "The overall deployment of fingerprinting has increased compared to "
            "prior research, especially canvas fingerprinting."
        ),
        "title": "Prevalence of Fingerprinting on the Web",
    },
    {
        "text": (
            "Most users are unaware of digital fingerprinting and its privacy "
            "implications. A 2021 Eurostat survey showed that while 80% of people "
            "aged 16-74 knew about cookies for online tracking, only one-third "
            "changed their browser settings, and even fewer used protection tools. "
            "In a 2020 survey, over 85% of participants were concerned about "
            "browser fingerprinting, and a majority agreed that defending against "
            "it is important but hard to achieve. Research shows that users are "
            "willing to trade off privacy for convenience — they may accept "
            "fingerprinting if protection measures are too inconvenient. "
            "Individuals influenced by short-term benefits may delay or avoid "
            "adopting privacy technologies. The drawbacks of anti-tracking tools "
            "— limited access to resources, broken websites, no saved passwords "
            "— push users toward accepting the non-tangible threat of "
            "fingerprinting over the tangible loss of browsing convenience."
        ),
        "title": "Privacy Awareness & Trade-offs",
    },
]

CHUNK_CONFIGS = {
    "small": {"chunk_size": 200, "chunk_overlap": 50},
    "medium": {"chunk_size": 350, "chunk_overlap": 75},
    "large": {"chunk_size": 500, "chunk_overlap": 100},
}

_DATA_DIR = Path(__file__).resolve().parent / "data"
# Shipped precomputed embeddings for the active medium strategy — avoids batch-encoding
# all chunks on every cold start (major latency win on Render).
_PRECOMPUTED_MEDIUM = _DATA_DIR / "precomputed_medium.npz"


def _l2_normalize_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.maximum(norms, 1e-12)


@dataclass
class Document:
    page_content: str
    metadata: dict = field(default_factory=dict)


class NumpyVectorStore:
    """Cosine-space retrieval: distance = 1 − cosine similarity (normalized MiniLM vectors)."""

    def __init__(self, matrix: np.ndarray, texts: list[str], metadatas: list[dict]):
        self._matrix = matrix
        self._texts = texts
        self._metadatas = metadatas

    def similarity_search_with_score(self, query: str, k: int = 3):
        ef = _get_embedding_fn()
        q = np.asarray(ef([query])[0], dtype=np.float32)
        qn = np.linalg.norm(q)
        q = q / max(float(qn), 1e-12)
        sims = self._matrix @ q
        dists = 1.0 - sims
        k = min(k, len(dists))
        top_idx = np.argsort(dists)[:k]
        return [
            (
                Document(page_content=self._texts[i], metadata=self._metadatas[i]),
                float(dists[i]),
            )
            for i in top_idx
        ]


@st.cache_resource
def _get_embedding_fn():
    from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2

    return ONNXMiniLM_L6_V2()


@st.cache_resource
def build_vectorstore(chunk_size: int, chunk_overlap: int):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    texts = []
    metadatas = []
    for doc in DOCUMENTS:
        for chunk in splitter.split_text(doc["text"]):
            texts.append(chunk)
            metadatas.append({"source": doc["title"]})

    if (
        chunk_size == CHUNK_CONFIGS["medium"]["chunk_size"]
        and chunk_overlap == CHUNK_CONFIGS["medium"]["chunk_overlap"]
        and _PRECOMPUTED_MEDIUM.is_file()
    ):
        loaded = np.load(_PRECOMPUTED_MEDIUM, allow_pickle=True)
        matrix = _l2_normalize_rows(loaded["matrix"].astype(np.float32))
        file_texts = loaded["texts"].tolist()
        file_metas = [dict(m) for m in loaded["metadatas"].tolist()]
        if len(file_texts) == len(texts) and file_texts == texts:
            return NumpyVectorStore(matrix, file_texts, file_metas), len(file_texts)

    ef = _get_embedding_fn()
    raw = ef(texts)
    matrix = _l2_normalize_rows(
        np.stack([np.asarray(e, dtype=np.float32) for e in raw], axis=0)
    )
    return NumpyVectorStore(matrix, texts, metadatas), len(texts)


def get_store(key="medium"):
    cfg = CHUNK_CONFIGS[key]
    store, count = build_vectorstore(cfg["chunk_size"], cfg["chunk_overlap"])
    # With precomputed chunks, only the query encoder must load (still the main cost).
    _get_embedding_fn()
    return {"store": store, "chunk_count": count}


def get_chunk_count(key: str) -> int:
    cfg = CHUNK_CONFIGS[key]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["chunk_size"],
        chunk_overlap=cfg["chunk_overlap"],
    )
    return sum(len(splitter.split_text(doc["text"])) for doc in DOCUMENTS)


def display_results(results):
    for i, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "Unknown")
        st.markdown(f"**Result {i + 1}** — *{source}*")
        st.info(doc.page_content)
        st.caption(f"Similarity score: {score:.4f}")
        st.divider()
