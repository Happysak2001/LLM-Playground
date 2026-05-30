import streamlit as st
import numpy as np

st.set_page_config(page_title="Embeddings", page_icon="🧭", layout="wide")

# ── Pre-computed GloVe 50d vectors (77KB file, no gensim needed) ─────────────
@st.cache_resource
def load_vectors():
    import json, os
    base = os.path.dirname(os.path.dirname(__file__))
    data = np.load(os.path.join(base, "data", "embeddings.npz"))
    with open(os.path.join(base, "data", "vocab.json")) as f:
        vocab = json.load(f)
    vectors = data["vectors"].astype(np.float32)
    return {w: vectors[i] for i, w in enumerate(vocab)}

wv = load_vectors()

def sentence_vec(text: str) -> np.ndarray | None:
    tokens = text.lower().split()
    vecs = [wv[w] for w in tokens if w in wv]
    if not vecs:
        return None
    v = np.mean(vecs, axis=0).astype(np.float32)
    return v / max(np.linalg.norm(v), 1e-9)

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))

def sim_color(s: float) -> str:
    if s >= 0.80: return "#10b981"
    if s >= 0.55: return "#fbbf24"
    if s >= 0.30: return "#f87171"
    return "#64748b"


# ════════════════════════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }
.stApp { background: #070710 !important; }
.block-container { max-width:1400px !important; width:95vw !important; padding:0 2rem 8rem !important; background:transparent !important; }
#MainMenu, footer, [data-testid="stDecoration"] { display:none !important; }
[data-testid="stHeader"] { background:transparent !important; height:0 !important; }

[data-testid="stSidebar"] { background:#0d0d1a !important; border-right:1px solid rgba(255,255,255,0.08) !important; }
[data-testid="stSidebar"], [data-testid="stSidebar"] p,
[data-testid="stSidebar"] span, [data-testid="stSidebar"] div { color:#e2e8f0 !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] a { color:#94a3b8 !important; text-decoration:none !important; display:block !important; padding:7px 14px 7px 28px !important; border-radius:8px !important; font-size:14px !important; font-weight:500 !important; transition:all .18s !important; }
[data-testid="stSidebar"] a:hover { color:#f1f5f9 !important; background:rgba(255,255,255,0.06) !important; }
[data-testid="stSidebar"] a[aria-current="page"] { color:#a855f7 !important; background:rgba(168,85,247,0.09) !important; font-weight:700 !important; }

.stTextArea textarea { background:#0d1117 !important; color:#f1f5f9 !important; border:1.5px solid #2d3748 !important; border-radius:14px !important; font-size:15px !important; line-height:1.65 !important; padding:14px 16px !important; caret-color:#a855f7 !important; transition:border-color .25s,box-shadow .25s !important; font-family:'Space Grotesk',sans-serif !important; }
.stTextArea textarea:focus { border-color:rgba(168,85,247,0.5) !important; box-shadow:0 0 0 3px rgba(168,85,247,0.08) !important; outline:none !important; }
.stTextArea textarea::placeholder { color:#4a5568 !important; opacity:1 !important; }
.stTextArea label { display:none !important; }

[data-testid="stSlider"] [role="slider"] { background:#a855f7 !important; border:none !important; box-shadow:0 0 12px rgba(168,85,247,0.55) !important; }
[data-testid="stSlider"] .st-b7 { background:rgba(168,85,247,0.14) !important; }

[data-testid="stExpander"] { background:rgba(255,255,255,0.018) !important; border:1px solid rgba(255,255,255,0.07) !important; border-radius:14px !important; overflow:hidden !important; margin-bottom:8px !important; }
.streamlit-expanderHeader { background:transparent !important; color:#94a3b8 !important; font-size:14px !important; font-weight:600 !important; padding:16px 20px !important; }
.streamlit-expanderHeader:hover { color:#f1f5f9 !important; }
[data-testid="stExpanderDetails"] { padding:0 20px 20px !important; }

.realization { background:rgba(168,85,247,0.03); border:1px solid rgba(168,85,247,0.1); border-radius:16px; padding:24px 28px; margin-top:20px; }
.step { display:flex; align-items:flex-start; gap:14px; margin-bottom:18px; }
.step:last-child { margin-bottom:0; }
.step-n { min-width:26px; height:26px; background:rgba(168,85,247,0.12); color:#a855f7; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:800; flex-shrink:0; margin-top:2px; }
.step-title  { font-size:14px; font-weight:700; color:#e2e8f0; margin-bottom:4px; }
.step-detail { font-size:13px; color:#64748b; line-height:1.6; }

.vec-preview { background:#0d1117; border:1px solid #2d3748; border-radius:12px; padding:14px 16px; font-family:monospace; font-size:13px; color:#a855f7; line-height:1.8; word-break:break-all; }
.insight { background:rgba(168,85,247,0.06); border-left:2px solid rgba(168,85,247,0.4); border-radius:0 10px 10px 0; padding:12px 16px; font-size:13px; color:#c4b5fd; line-height:1.65; margin-top:14px; }
.sim-bar-track { background:rgba(255,255,255,0.06); border-radius:99px; height:6px; margin:8px 0; }
.sim-bar-fill  { height:6px; border-radius:99px; }
.stats { display:flex; gap:28px; flex-wrap:wrap; margin-bottom:20px; }
.stat .val { font-size:34px; font-weight:800; line-height:1; }
.stat .lbl { font-size:10px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; color:#64748b; margin-top:5px; }
hr { border:none !important; border-top:1px solid rgba(255,255,255,0.05) !important; margin:48px 0 32px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;">
  <div style="position:absolute;top:-200px;left:-150px;width:600px;height:600px;border-radius:50%;
              background:radial-gradient(circle,rgba(168,85,247,0.1),transparent 65%);"></div>
  <div style="position:absolute;bottom:-150px;right:-150px;width:500px;height:500px;border-radius:50%;
              background:radial-gradient(circle,rgba(0,245,255,0.07),transparent 65%);"></div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:20px 14px 12px;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:12px;">
      <div style="font-size:17px;font-weight:800;color:#f1f5f9;letter-spacing:-0.5px;">⚡ Happies Playground</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="Home")
    st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#334155;padding:14px 14px 4px;">Phase 1 — How LLMs Work</div>', unsafe_allow_html=True)
    st.page_link("pages/1_Tokens.py",     label="Tokens")
    st.page_link("pages/2_Embeddings.py", label="Embeddings")
    st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1e293b;padding:14px 14px 4px;">Phase 2 — Prompting</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1e293b;padding:2px 14px 4px;">Phase 3 — Building Apps</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#1e293b;padding:2px 14px 4px;">Phase 4 — Agents</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding:72px 0 44px;position:relative;">
  <div style="position:absolute;top:-60px;right:-200px;width:500px;height:500px;border-radius:50%;
              pointer-events:none;background:radial-gradient(circle,rgba(168,85,247,0.12),transparent 65%);"></div>
  <div style="font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
              color:rgba(168,85,247,0.75);margin-bottom:22px;">Foundations · Embeddings</div>
  <h1 style="font-size:clamp(46px,7vw,78px);font-weight:800;letter-spacing:-2px;
             line-height:1.06;color:#f1f5f9;margin:0 0 18px;">
    Meaning is a<br>
    <span style="background:linear-gradient(135deg,#a855f7 0%,#00f5ff 100%);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;">location.</span>
  </h1>
  <p style="font-size:18px;color:#94a3b8;max-width:520px;line-height:1.7;margin:0 0 6px;">
    Every word can be converted into a list of numbers — an <strong style="color:#e2e8f0;">embedding</strong>.
    Words with similar meaning get similar numbers.
  </p>
  <p style="font-size:15px;color:#64748b;margin:0;">
    They end up close together in space. That's how AI understands meaning.
  </p>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# MAIN INTERACTIVE — 2-column
# ════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown('<p style="font-size:13px;font-weight:600;color:#94a3b8;margin:0 0 8px;">Sentence A</p>', unsafe_allow_html=True)
    text_a = st.text_area("A", value="The dog ran across the park.", height=80, label_visibility="collapsed")

    st.markdown('<p style="font-size:13px;font-weight:600;color:#94a3b8;margin:12px 0 8px;">Sentence B</p>', unsafe_allow_html=True)
    text_b = st.text_area("B", value="A puppy sprinted through the garden.", height=80, label_visibility="collapsed")

    va = sentence_vec(text_a) if text_a.strip() else None
    vb = sentence_vec(text_b) if text_b.strip() else None

    if va is not None and vb is not None:
        score = cosine(va, vb)
        color = sim_color(score)
        bar_w = int(max(0, score) * 100)
        label = ("Very similar" if score >= 0.80 else
                 "Related"      if score >= 0.55 else
                 "Weakly related" if score >= 0.30 else "Unrelated")

        st.markdown(f"""
        <div style="margin-top:20px;">
          <div style="font-size:10px;font-weight:700;letter-spacing:1.8px;
                      text-transform:uppercase;color:#64748b;margin-bottom:10px;">Similarity score</div>
          <div style="font-size:64px;font-weight:800;line-height:1;color:{color};margin-bottom:6px;">{score:.2f}</div>
          <div style="font-size:14px;font-weight:600;color:{color};margin-bottom:12px;">{label}</div>
          <div class="sim-bar-track">
            <div class="sim-bar-fill" style="width:{bar_w}%;background:{color};box-shadow:0 0 10px {color}88;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#334155;margin-top:4px;">
            <span>0.0 — unrelated</span><span>1.0 — identical</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:20px;">
          <div style="font-size:10px;font-weight:700;letter-spacing:1.8px;
                      text-transform:uppercase;color:#64748b;margin-bottom:8px;">
            Embedding of "A" (first 12 of 50 values)
          </div>
          <div class="vec-preview">[{", ".join(f"{x:.4f}" for x in va[:12])}, ...]</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # warn about unknown words
        if text_a.strip() and va is None:
            st.warning("No known words found in Sentence A. Try common English words.")
        elif text_b.strip() and vb is None:
            st.warning("No known words found in Sentence B. Try common English words.")

with col_right:
    if va is not None and vb is not None:
        st.markdown(f"""
        <div class="realization">
          <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                      color:rgba(168,85,247,0.75);margin-bottom:16px;">What just happened?</div>
          <div class="step">
            <div class="step-n">1</div>
            <div>
              <div class="step-title">Each word became a 50-number vector</div>
              <div class="step-detail">
                The sentence embedding = average of all word vectors.
                GloVe learned these from 6 billion words of text.
              </div>
            </div>
          </div>
          <div class="step">
            <div class="step-n">2</div>
            <div>
              <div class="step-title">Cosine similarity measures the angle</div>
              <div class="step-detail">
                1.0 = vectors point the same direction (same meaning).<br>
                0.0 = perpendicular (no relationship).
              </div>
            </div>
          </div>
          <div class="step">
            <div class="step-n">3</div>
            <div>
              <div class="step-title">Meaning determines location in space</div>
              <div class="step-detail" style="color:#94a3b8;">
                "dog" and "puppy" land near each other because they appeared
                in similar contexts across billions of sentences.
                No one told the model they are related.
              </div>
            </div>
          </div>
        </div>
        <div style="margin-top:16px;background:rgba(255,255,255,0.018);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:20px;">
          <div class="stats" style="gap:24px;">
            <div class="stat">
              <div class="val" style="background:linear-gradient(135deg,#a855f7,#e879f9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">50</div>
              <div class="lbl">Dimensions</div>
            </div>
            <div class="stat">
              <div class="val" style="background:linear-gradient(135deg,#00f5ff,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{score:.2f}</div>
              <div class="lbl">Similarity</div>
            </div>
          </div>
          <div style="font-size:12px;color:#334155;line-height:1.6;">GloVe · Wikipedia + Gigaword · 6B tokens</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding-top:8px;color:#334155;font-size:14px;line-height:1.8;">Type two sentences on the left.<br>Score and explanation appear here.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# EXPERIMENTS
# ════════════════════════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="margin-bottom:24px;">
  <div style="font-size:22px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">Dig deeper</div>
  <div style="font-size:15px;color:#94a3b8;line-height:1.65;max-width:560px;">
    The similarity score above shows you one thing. These four concepts show you the full picture.
    Open each one, read the one-line idea, then interact with the experiment.
  </div>
</div>
""", unsafe_allow_html=True)


# ── Word Map ─────────────────────────────────────────────────────
with st.expander("📌 Concept 1 — Words with similar meaning cluster together"):
    st.markdown("""
    <div style="background:rgba(168,85,247,0.05);border-left:3px solid rgba(168,85,247,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">Similar words land near each other in embedding space — without anyone telling the model which words are related.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Look at the scatter plot below. Animals cluster together, royalty clusters together, tech clusters together — purely from the geometry of meaning.
    </div>
    """, unsafe_allow_html=True)

    WORD_GROUPS = {
        "Animals":  ["cat", "dog", "fish", "bird", "horse"],
        "Royalty":  ["king", "queen", "prince", "princess", "crown"],
        "Tech":     ["computer", "software", "algorithm", "database", "code"],
        "Food":     ["pizza", "bread", "coffee", "soup", "rice"],
        "Emotions": ["happy", "sad", "angry", "calm", "fear"],
        "Sports":   ["football", "basketball", "tennis", "swimming", "running"],
    }

    all_words  = [w for grp in WORD_GROUPS.values() for w in grp]
    all_labels = [lbl for lbl, grp in WORD_GROUPS.items() for _ in grp]

    known = [(w, lbl) for w, lbl in zip(all_words, all_labels) if w in wv]
    known_words  = [w for w, _ in known]
    known_labels = [l for _, l in known]
    known_vecs   = np.array([wv[w] for w in known_words])

    from sklearn.decomposition import PCA
    coords = PCA(n_components=2, random_state=42).fit_transform(known_vecs)

    import plotly.graph_objects as go
    GROUP_COLORS = {
        "Animals": "#10b981", "Royalty": "#fbbf24", "Tech": "#00f5ff",
        "Food": "#f87171",    "Emotions": "#a855f7", "Sports": "#fb923c",
    }

    fig = go.Figure()
    for grp_name, grp_words in WORD_GROUPS.items():
        idx = [known_words.index(w) for w in grp_words if w in known_words]
        if not idx: continue
        fig.add_trace(go.Scatter(
            x=[coords[i, 0] for i in idx], y=[coords[i, 1] for i in idx],
            mode="markers+text", name=grp_name,
            text=[known_words[i] for i in idx],
            textposition="top center",
            textfont=dict(size=12, color=GROUP_COLORS[grp_name]),
            marker=dict(size=13, color=GROUP_COLORS[grp_name]),
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))

    fig.update_layout(
        paper_bgcolor="#070710", plot_bgcolor="#070710",
        font=dict(family="Space Grotesk", color="#94a3b8"),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
        margin=dict(l=20, r=20, t=20, b=20), height=420,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">The model was never told "cat and dog are both animals." It learned this from context — they appeared near similar words in billions of sentences. Clustering is an emergent property of language.</div>', unsafe_allow_html=True)


# ── Semantic arithmetic ───────────────────────────────────────────
with st.expander("📌 Concept 2 — You can do arithmetic with meaning"):
    st.markdown("""
    <div style="background:rgba(168,85,247,0.05);border-left:3px solid rgba(168,85,247,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">Embeddings encode relationships, not just words. You can subtract one concept and add another — and land near the right answer.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Use the dropdowns below. Start with "king", subtract "man", add "woman". See what comes closest.
    </div>
    """, unsafe_allow_html=True)

    VOCAB = ["king", "queen", "man", "woman", "prince", "princess",
             "boy", "girl", "father", "mother", "son", "daughter",
             "uncle", "aunt", "brother", "sister", "husband", "wife"]
    VOCAB = [w for w in VOCAB if w in wv]

    c1, c2, c3 = st.columns(3)
    word_a = c1.selectbox("Start with", VOCAB, index=VOCAB.index("king") if "king" in VOCAB else 0)
    word_b = c2.selectbox("Subtract",   VOCAB, index=VOCAB.index("man")  if "man"  in VOCAB else 2)
    word_c = c3.selectbox("Add",        VOCAB, index=VOCAB.index("woman") if "woman" in VOCAB else 3)

    va_ = wv[word_a]; vb_ = wv[word_b]; vc_ = wv[word_c]
    result = va_ - vb_ + vc_
    result_norm = result / max(np.linalg.norm(result), 1e-9)

    # find closest in full vocabulary (exclude input words)
    all_words_list = list(wv.keys())
    all_vecs = np.array(list(wv.values()), dtype=np.float32)
    scores = all_vecs @ result_norm
    top_idx = np.argsort(-scores)
    filtered = [(all_words_list[i], float(scores[i]))
                for i in top_idx
                if all_words_list[i] not in {word_a, word_b, word_c}][:5]

    st.markdown(f"""
    <div style="margin:16px 0;padding:20px;background:rgba(168,85,247,0.04);
                border:1px solid rgba(168,85,247,0.12);border-radius:14px;">
      <div style="font-size:22px;font-weight:800;color:#e2e8f0;margin-bottom:16px;letter-spacing:-0.5px;">
        {word_a} &minus; {word_b} + {word_c} &asymp; ?
      </div>
      <div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;
                  letter-spacing:1px;margin-bottom:12px;">Closest words in vector space</div>
    """, unsafe_allow_html=True)

    for rank, (word, sim) in enumerate(filtered):
        bar = int(max(0, sim) * 100)
        c = sim_color(sim)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
          <div style="font-size:13px;color:#64748b;width:20px;">#{rank+1}</div>
          <div style="font-size:16px;font-weight:700;color:#e2e8f0;width:110px;">{word}</div>
          <div style="flex:1;background:rgba(255,255,255,0.05);border-radius:4px;height:5px;">
            <div style="width:{bar}%;height:5px;border-radius:4px;background:{c};box-shadow:0 0 8px {c}66;"></div>
          </div>
          <div style="font-size:14px;font-weight:700;color:{c};width:48px;text-align:right;">{sim:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="insight">This works because embeddings encode <em>relationships</em>, not just identity. "King" and "queen" differ mainly along the gender axis — subtracting "man" and adding "woman" slides the vector into the right neighborhood. It\'s geometry, not magic.</div>', unsafe_allow_html=True)


# ── Semantic search ───────────────────────────────────────────────
with st.expander("📌 Concept 3 — Search finds meaning, not just matching words"):
    st.markdown("""
    <div style="background:rgba(168,85,247,0.05);border-left:3px solid rgba(168,85,247,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">Embedding-based search finds related content even when no keywords match — the foundation of every RAG system.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Type a query below. The system finds the most similar sentence from the list — even with zero shared words.
    </div>
    """, unsafe_allow_html=True)

    SENTENCES = [
        "The stock market fell sharply today.",
        "Scientists discovered a new species of deep-sea fish.",
        "The team won the championship in the final minute.",
        "A new programming language was released by Google.",
        "The patient recovered fully after surgery.",
        "Heavy rainfall caused flooding across the region.",
        "The latest smartphone features a foldable screen.",
        "Astronomers detected a signal from a distant galaxy.",
        "The chef opened a new restaurant downtown.",
        "Electric vehicles now outsell petrol cars in Norway.",
    ]

    query = st.text_area("search_query", value="What happened to share prices?",
                         height=70, label_visibility="collapsed")

    if query.strip():
        q_vec = sentence_vec(query)
        if q_vec is None:
            st.warning("No known words in query.")
        else:
            s_vecs  = [sentence_vec(s) for s in SENTENCES]
            results = [(SENTENCES[i], cosine(q_vec, s_vecs[i])) for i in range(len(SENTENCES)) if s_vecs[i] is not None]
            results.sort(key=lambda x: -x[1])

            st.markdown('<div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#64748b;margin:16px 0 12px;">Results ranked by similarity</div>', unsafe_allow_html=True)
            for rank, (sent, sim) in enumerate(results[:5]):
                c   = sim_color(sim)
                bar = int(max(0, sim) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;
                            padding:12px 14px;background:rgba(255,255,255,0.015);
                            border:1px solid rgba(255,255,255,0.06);border-radius:10px;">
                  <div style="font-size:20px;font-weight:800;color:#1e293b;width:28px;">{rank+1}</div>
                  <div style="flex:1;">
                    <div style="font-size:14px;color:#e2e8f0;margin-bottom:6px;">{sent}</div>
                    <div style="background:rgba(255,255,255,0.04);border-radius:4px;height:4px;">
                      <div style="width:{bar}%;height:4px;border-radius:4px;background:{c};box-shadow:0 0 8px {c}55;"></div>
                    </div>
                  </div>
                  <div style="font-size:16px;font-weight:800;color:{c};width:44px;text-align:right;">{sim:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="insight">"Share prices" matched "stock market" — zero keywords in common. The model understands they refer to the same concept. This is the foundation of every RAG retrieval system.</div>', unsafe_allow_html=True)


# ── Tokens vs Embeddings ──────────────────────────────────────────
with st.expander("📌 Concept 4 — How tokens and embeddings are different things"):
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:0;">
      <div style="padding:20px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:14px;font-weight:700;color:#00f5ff;margin-bottom:6px;">Token</div>
        <div style="font-size:14px;color:#94a3b8;line-height:1.65;">
          A chunk of text converted to an integer ID.<br>
          <span style="font-family:monospace;color:#64748b;">"hello" → 15339</span><br>
          Used for: feeding text in, billing, context limits.
        </div>
      </div>
      <div style="padding:20px 0;border-bottom:1px solid rgba(255,255,255,0.05);">
        <div style="font-size:14px;font-weight:700;color:#a855f7;margin-bottom:6px;">Token Embedding</div>
        <div style="font-size:14px;color:#94a3b8;line-height:1.65;">
          Each token ID is looked up in a learned table and mapped to a dense vector (e.g. 768 numbers).<br>
          Happens automatically inside the model. Used for internal computation.
        </div>
      </div>
      <div style="padding:20px 0;">
        <div style="font-size:14px;font-weight:700;color:#10b981;margin-bottom:6px;">Sentence Embedding</div>
        <div style="font-size:14px;color:#94a3b8;line-height:1.65;">
          The whole sentence is pooled into one vector capturing overall meaning.<br>
          <span style="font-family:monospace;color:#64748b;">"The dog ran" → [0.12, -0.34, 0.87, ...]</span><br>
          Used for: semantic search, clustering, RAG retrieval.
        </div>
      </div>
    </div>
    <div class="insight">Tokens are the input format. Embeddings are the meaning format. Tokens go in — embeddings come out. The vocabulary of integers becomes a geography of meaning.</div>
    """, unsafe_allow_html=True)


# ── Challenges ────────────────────────────────────────────────────
with st.expander("🎯 Test yourself — 3 challenges"):
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:20px;padding-top:4px;">
      <div style="border-left:2px solid rgba(168,85,247,0.35);padding-left:16px;">
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;">🎯 Challenge 1 — Find the 0.70 zone</div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.65;">Use the playground at the top. Find two sentences that score between 0.65 and 0.75 — related but clearly different ideas. What does that similarity level feel like?</div>
      </div>
      <div style="border-left:2px solid rgba(0,245,255,0.35);padding-left:16px;">
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;">🌀 Challenge 2 — Break the arithmetic</div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.65;">Try: <em>paris - france + germany</em>. Does it return "berlin"? Try other country/capital pairs. When does it work and when does it fail?</div>
      </div>
      <div style="border-left:2px solid rgba(251,191,36,0.35);padding-left:16px;">
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;">🔍 Challenge 3 — Fool the search</div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.65;">Find a query that <em>should</em> match a sentence but scores poorly. This reveals real limitations of embedding-based search — an important thing to understand before building RAG systems.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
