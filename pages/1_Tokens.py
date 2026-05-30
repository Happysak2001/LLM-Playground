import streamlit as st
import tiktoken

st.set_page_config(page_title="Tokens", page_icon="⚡", layout="wide")

@st.cache_resource
def load_encoder():
    return tiktoken.get_encoding("cl100k_base")

enc = load_encoder()

CHIPS = [
    ("#00f5ff", "#001a1a"), ("#a855f7", "#ffffff"), ("#f0abfc", "#2a0040"),
    ("#10b981", "#ffffff"), ("#fbbf24", "#1a1000"), ("#f87171", "#ffffff"),
    ("#60a5fa", "#ffffff"), ("#fb923c", "#ffffff"), ("#34d399", "#002a1a"),
    ("#e879f9", "#2a0040"),
]

def tokenize(text):
    ids = enc.encode(text)
    return ids, [enc.decode([t]) for t in ids]

def chips_html(text, size=15):
    ids, strs = tokenize(text)
    out = []
    for i, s in enumerate(strs):
        bg, fg = CHIPS[i % len(CHIPS)]
        d = (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
              .replace(" ", "·").replace("\n", "↵"))
        out.append(
            f'<span class="chip" style="background:{bg};color:{fg};font-size:{size}px;">{d}</span>'
        )
    return "".join(out)


# ═══════════════════════════════════════════════════════════════════
# CSS — only what is actually needed
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
  font-family: 'Space Grotesk', sans-serif !important;
}
.stApp {
  background: #070710 !important;
}
.block-container {
  max-width: 1400px !important;
  width: 95vw !important;
  padding: 0 2rem 8rem !important;
  background: transparent !important;
}

/* ── kill chrome ── */
#MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }

/* ── sidebar — hide default nav, use custom ── */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] {
  background: #0d0d1a !important;
  border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
/* st.page_link anchors */
[data-testid="stSidebar"] a {
  color: #94a3b8 !important;
  text-decoration: none !important;
  display: block !important;
  padding: 7px 14px 7px 28px !important;
  border-radius: 8px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  transition: all .18s !important;
}
[data-testid="stSidebar"] a:hover { color: #f1f5f9 !important; background: rgba(255,255,255,0.06) !important; }
[data-testid="stSidebar"] a[aria-current="page"] { color: #00f5ff !important; background: rgba(0,245,255,0.08) !important; font-weight: 700 !important; }

/* ── textarea — solid background, white text ── */
.stTextArea textarea {
  background: #0d1117 !important;
  color: #f1f5f9 !important;
  border: 1.5px solid #2d3748 !important;
  border-radius: 14px !important;
  font-size: 16px !important;
  line-height: 1.65 !important;
  padding: 14px 16px !important;
  caret-color: #00f5ff !important;
  transition: border-color .25s, box-shadow .25s !important;
  font-family: 'Space Grotesk', sans-serif !important;
}
.stTextArea textarea:focus {
  border-color: rgba(0,245,255,0.45) !important;
  box-shadow: 0 0 0 3px rgba(0,245,255,0.07) !important;
  outline: none !important;
}
.stTextArea textarea::placeholder { color: #4a5568 !important; opacity: 1 !important; }
.stTextArea label { display: none !important; }

/* ── slider ── */
[data-testid="stSlider"] [role="slider"] {
  background: #00f5ff !important;
  border: none !important;
  box-shadow: 0 0 12px rgba(0,245,255,0.5) !important;
}
[data-testid="stSlider"] .st-b7 { background: rgba(0,245,255,0.14) !important; }
[data-testid="stSlider"] label, [data-testid="stSlider"] p { color: #94a3b8 !important; }

/* ── expander ── */
[data-testid="stExpander"] {
  background: rgba(255,255,255,0.018) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  margin-bottom: 8px !important;
}
.streamlit-expanderHeader {
  background: transparent !important;
  color: #94a3b8 !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  padding: 16px 20px !important;
}
.streamlit-expanderHeader:hover { color: #f1f5f9 !important; }
[data-testid="stExpanderDetails"] { padding: 0 20px 20px !important; }

/* ── token chip ── */
.chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 7px;
  margin: 3px 2px;
  font-family: 'Space Grotesk', monospace !important;
  font-weight: 700;
  transition: transform .12s ease;
  cursor: default;
}
.chip:hover { transform: translateY(-3px) scale(1.07); }

/* ── token display area ── */
.tok-area {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 14px;
  padding: 18px 16px;
  min-height: 60px;
  line-height: 2.5;
}

/* ── realization panel (appears after typing) ── */
.realization {
  background: rgba(0,245,255,0.03);
  border: 1px solid rgba(0,245,255,0.1);
  border-radius: 16px;
  padding: 24px 28px;
  margin-top: 20px;
}
.step {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 18px;
}
.step:last-child { margin-bottom: 0; }
.step-n {
  min-width: 26px; height: 26px;
  background: rgba(0,245,255,0.1);
  color: #00f5ff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800;
  flex-shrink: 0; margin-top: 2px;
}
.step-title  { font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.step-detail { font-size: 13px; color: #64748b; font-family: monospace; line-height: 1.6; }

/* ── stat strip ── */
.stats { display: flex; gap: 36px; flex-wrap: wrap; margin: 16px 0 4px; }
.stat .val {
  font-size: 34px; font-weight: 800; line-height: 1;
}
.stat .lbl {
  font-size: 10px; font-weight: 700; letter-spacing: 1.4px;
  text-transform: uppercase; color: #64748b; margin-top: 5px;
}

/* ── insight strip in dropdowns ── */
.insight {
  background: rgba(168,85,247,0.06);
  border-left: 2px solid rgba(168,85,247,0.4);
  border-radius: 0 10px 10px 0;
  padding: 12px 16px;
  font-size: 13px;
  color: #c4b5fd;
  line-height: 1.65;
  margin-top: 14px;
}

/* ── divider ── */
hr {
  border: none !important;
  border-top: 1px solid rgba(255,255,255,0.05) !important;
  margin: 48px 0 32px !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:20px 14px 12px;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:12px;">
      <div style="font-size:17px;font-weight:800;color:#f1f5f9;letter-spacing:-0.5px;">⚡ LLM Playground</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="Home")
    st.markdown("""
    <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                color:#334155;padding:14px 14px 4px;">Foundations</div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Tokens.py",    label="Tokens")
    st.page_link("pages/2_Embeddings.py", label="Embeddings")

# Subtle ambient glow — one, not three
st.markdown("""
<div style="position:fixed;top:0;right:0;width:480px;height:480px;pointer-events:none;z-index:0;
            background:radial-gradient(circle at top right,rgba(124,58,237,0.1),transparent 65%);"></div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# 1. HERO
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 72px 0 44px;">
  <div style="font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
              color:rgba(0,245,255,0.6);margin-bottom:22px;">Foundations · Tokens</div>

  <h1 style="font-size:clamp(46px,7vw,78px);font-weight:800;letter-spacing:-2px;
             line-height:1.06;color:#f1f5f9;margin:0 0 18px;">
    AI does not<br>read words.
  </h1>

  <p style="font-size:18px;color:#94a3b8;max-width:480px;line-height:1.7;margin:0 0 6px;">
    It reads chunks called <strong style="color:#e2e8f0;">tokens</strong> — pieces of text
    converted into numbers.
  </p>
  <p style="font-size:15px;color:#64748b;margin:0;">
    The model never sees your sentence. It only sees token IDs.
  </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# 2. MAIN INTERACTIVE — 2-column layout
# ═══════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    user_text = st.text_area(
        "input",
        value="Hello! I am learning about tokens.",
        height=120,
        label_visibility="collapsed",
        placeholder="Type anything: a sentence, code, emoji, another language...",
    )

    if user_text.strip():
        _, strs = tokenize(user_text)
        st.markdown(
            '<div style="font-size:10px;font-weight:700;letter-spacing:1.8px;'
            'text-transform:uppercase;color:#64748b;margin:18px 0 8px;">'
            'each block = one token</div>'
            f'<div class="tok-area">{chips_html(user_text)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="tok-area" style="display:flex;align-items:center;'
            'justify-content:center;min-height:100px;color:#1e293b;font-size:14px;">'
            'Your tokens will appear here as you type</div>',
            unsafe_allow_html=True,
        )

with col_right:
    if user_text.strip():
        ids, strs = tokenize(user_text)
        n_tok = len(ids)
        n_chr = len(user_text)
        n_wrd = len(user_text.split())
        cpp   = n_chr / n_tok

        st.markdown(f"""
        <div class="stats" style="gap:28px;margin-bottom:24px;">
          <div class="stat">
            <div class="val" style="background:linear-gradient(135deg,#00f5ff,#60a5fa);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;">{n_tok}</div>
            <div class="lbl">Tokens</div>
          </div>
          <div class="stat">
            <div class="val" style="background:linear-gradient(135deg,#a855f7,#e879f9);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;">{n_chr}</div>
            <div class="lbl">Characters</div>
          </div>
          <div class="stat">
            <div class="val" style="background:linear-gradient(135deg,#10b981,#34d399);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;">{n_wrd}</div>
            <div class="lbl">Words</div>
          </div>
          <div class="stat">
            <div class="val" style="background:linear-gradient(135deg,#fbbf24,#fb923c);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;">{cpp:.1f}</div>
            <div class="lbl">Chars / Token</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        sample_str = " > ".join(f'"{s}"' for s in strs[:4]) + ("  ..." if n_tok > 4 else "")
        sample_ids = str(list(ids[:6]))[:-1] + (", ...]" if n_tok > 6 else "]")

        st.markdown(f"""
        <div class="realization">
          <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                      color:rgba(0,245,255,0.65);margin-bottom:16px;">What just happened?</div>
          <div class="step">
            <div class="step-n">1</div>
            <div>
              <div class="step-title">Split into {n_tok} chunks</div>
              <div class="step-detail">{sample_str}</div>
            </div>
          </div>
          <div class="step">
            <div class="step-n">2</div>
            <div>
              <div class="step-title">Each chunk became a number</div>
              <div class="step-detail">{sample_ids}</div>
            </div>
          </div>
          <div class="step">
            <div class="step-n">3</div>
            <div>
              <div class="step-title">Model only sees those numbers</div>
              <div class="step-detail" style="color:#94a3b8;">
                No letters. No words. Just integers.<br>
                It predicts which number comes next.
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="padding-top:8px;color:#334155;font-size:14px;line-height:1.8;">'
            'Type something on the left.<br>Stats and explanation appear here.</div>',
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════
# 3. OPTIONAL EXPERIMENTS — each teaches ONE idea
# ═══════════════════════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="margin-bottom:24px;">
  <div style="font-size:22px;font-weight:800;color:#f1f5f9;margin-bottom:8px;">
    Dig deeper
  </div>
  <div style="font-size:15px;color:#94a3b8;line-height:1.65;max-width:560px;">
    The playground above shows the basics. These four concepts complete the picture.
    Open each one, read the one-line idea, then try the experiment yourself.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Why spaces matter ─────────────────────────────────────────────
with st.expander("📌 Concept 1 — Spaces create different tokens"):
    st.markdown("""
    <div style="background:rgba(0,245,255,0.04);border-left:3px solid rgba(0,245,255,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">A word with a leading space and the same word without are completely different token IDs.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Look at "token" vs " token" below. The IDs are different — the model treats them as unrelated.
    </div>
    """, unsafe_allow_html=True)

    for word in ["token", " token", "token!"]:
        w_ids, _ = tokenize(word)
        st.markdown(f"""
        <div style="margin:10px 0;">
          <span style="font-family:monospace;font-size:12px;color:#64748b;">
            &quot;{word}&quot; → {w_ids}
          </span>
          <div style="margin-top:5px;">{chips_html(word, 13)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight">
      This is why tiny formatting changes in prompts — an extra space, a newline,
      different punctuation — can subtly shift model outputs. The model sees different numbers.
    </div>
    """, unsafe_allow_html=True)

# ── Rare words ────────────────────────────────────────────────────
with st.expander("📌 Concept 2 — Rare words get split into smaller pieces"):
    st.markdown("""
    <div style="background:rgba(0,245,255,0.04);border-left:3px solid rgba(0,245,255,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">The tokenizer breaks unknown or rare words into smaller known pieces. More pieces = more tokens = more cost.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Compare "cat" (1 token) vs "antidisestablishmentarianism" (many tokens) below.
    </div>
    """, unsafe_allow_html=True)

    for word, label in [
        ("cat",                          "common word — 1 token"),
        ("ChatGPT",                      "proper noun (pre-2022) — split"),
        ("antidisestablishmentarianism", "rare word — many pieces"),
    ]:
        w_ids, _ = tokenize(word)
        st.markdown(f"""
        <div style="margin:12px 0;">
          <div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;
                      letter-spacing:.8px;margin-bottom:5px;">
            {label} · {len(w_ids)} token{'s' if len(w_ids) > 1 else ''}
          </div>
          <div>{chips_html(word, 13)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight">
      More pieces = more tokens = higher cost and more context window used.
      Technical jargon, brand names, and uncommon words inflate your token count.
    </div>
    """, unsafe_allow_html=True)

# ── Code vs English ───────────────────────────────────────────────
with st.expander("📌 Concept 3 — Code costs more tokens than English"):
    st.markdown("""
    <div style="background:rgba(0,245,255,0.04);border-left:3px solid rgba(0,245,255,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">Code uses more tokens per character than English, because symbols like ( : = are each their own token.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Compare the token count and chars-per-token for the English sentence vs the code snippet below.
    </div>
    """, unsafe_allow_html=True)
    prose = "The quick brown fox jumps over the lazy dog."
    code  = "for i in range(10): print(i)"

    for label, sample, color in [
        ("English prose", prose, "#10b981"),
        ("Python code",   code,  "#a855f7"),
    ]:
        s_ids, _ = tokenize(sample)
        cpp_s = len(sample) / len(s_ids)
        st.markdown(f"""
        <div style="margin:14px 0;">
          <div style="font-size:11px;font-weight:700;letter-spacing:.8px;
                      text-transform:uppercase;color:{color};margin-bottom:5px;">{label}</div>
          <div style="font-family:monospace;font-size:13px;color:#64748b;margin-bottom:5px;">{sample}</div>
          <div style="font-size:16px;font-weight:700;color:{color};">
            {len(s_ids)} tokens &nbsp;·&nbsp; {cpp_s:.1f} chars / token
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight">
      Symbols like <code style="background:rgba(255,255,255,0.07);padding:1px 5px;
      border-radius:4px;">( ) : = [ ]</code> are usually their own individual token.
      Code-heavy prompts cost 30–50% more than equivalent English.
    </div>
    """, unsafe_allow_html=True)

# ── Cost calculator ───────────────────────────────────────────────
with st.expander("📌 Concept 4 — Every token costs real money"):
    st.markdown("""
    <div style="background:rgba(0,245,255,0.04);border-left:3px solid rgba(0,245,255,0.4);
                border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:16px;">
      <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:2px;">What you'll learn</div>
      <div style="font-size:13px;color:#94a3b8;">Every API call charges per token. A longer prompt multiplied by millions of calls becomes a significant cost.</div>
    </div>
    <div style="font-size:13px;color:#64748b;margin-bottom:16px;">
      <strong style="color:#94a3b8;">Try it:</strong> Paste your own prompt below, then drag the slider to see daily and monthly costs at scale.
    </div>
    """, unsafe_allow_html=True)

    c_text = st.text_area(
        "cost_input",
        value="You are a helpful assistant. Here is the document:\n\n" + "word " * 120,
        height=100,
        label_visibility="collapsed",
    )
    st.markdown('<p style="font-size:13px;color:#64748b;margin:12px 0 4px;">API calls per day</p>',
                unsafe_allow_html=True)
    calls = st.slider("calls", 100, 200_000, 5_000, step=100, label_visibility="collapsed")

    if c_text.strip():
        n_c      = len(enc.encode(c_text))
        per_call = (n_c / 1e6 * 3.0) + (300 / 1e6 * 15.0)
        daily    = per_call * calls
        monthly  = daily * 30

        st.markdown(f"""
        <div style="display:flex;gap:32px;flex-wrap:wrap;margin-top:8px;">
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:1.2px;
                        text-transform:uppercase;color:#64748b;margin-bottom:5px;">Tokens</div>
            <div style="font-size:30px;font-weight:800;color:#a855f7;">{n_c:,}</div>
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:1.2px;
                        text-transform:uppercase;color:#64748b;margin-bottom:5px;">Per call</div>
            <div style="font-size:30px;font-weight:800;color:#10b981;">${per_call:.5f}</div>
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:1.2px;
                        text-transform:uppercase;color:#64748b;margin-bottom:5px;">Daily ({calls:,})</div>
            <div style="font-size:30px;font-weight:800;color:#fbbf24;">${daily:,.2f}</div>
          </div>
          <div>
            <div style="font-size:10px;font-weight:700;letter-spacing:1.2px;
                        text-transform:uppercase;color:#64748b;margin-bottom:5px;">Monthly</div>
            <div style="font-size:36px;font-weight:800;color:#f87171;">${monthly:,.2f}</div>
          </div>
        </div>
        <div style="font-size:12px;color:#334155;margin-top:14px;line-height:1.6;">
          Claude Sonnet 4.6 · $3 / 1M input tokens · $15 / 1M output tokens<br>
          ~300 output tokens assumed per call
        </div>
        """, unsafe_allow_html=True)

# ── Challenges ────────────────────────────────────────────────────
with st.expander("🎯 Test yourself — 3 challenges"):
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:20px;padding-top:4px;">

      <div style="border-left:2px solid rgba(0,245,255,0.3);padding-left:16px;">
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;">
          🍓 The Strawberry Problem
        </div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.65;">
          Type <code style="background:rgba(255,255,255,0.07);padding:1px 6px;
          border-radius:4px;">strawberry</code> in the playground above.
          Look at how it splits into tokens.<br>
          Now answer: why does the model struggle to count the letter R?<br>
          <span style="color:#64748b;">Hint: the letters are hidden inside token chunks.</span>
        </div>
      </div>

      <div style="border-left:2px solid rgba(168,85,247,0.3);padding-left:16px;">
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;">
          🗜️ The Compression Challenge
        </div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.65;">
          Type this into the playground and count its tokens:<br>
          <em style="color:#64748b;">"You are an extremely helpful AI assistant. Please answer in a detailed and thorough manner."</em><br>
          Now rewrite it to say the same thing in under 10 tokens.
        </div>
      </div>

      <div style="border-left:2px solid rgba(251,191,36,0.3);padding-left:16px;">
        <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:5px;">
          🌍 The Language Tax
        </div>
        <div style="font-size:13px;color:#94a3b8;line-height:1.65;">
          Type the same sentence in English, then in Hindi, Arabic, or Chinese.<br>
          Compare the token counts. The tokenizer was trained mostly on English —
          other languages often cost 2–5× more tokens per word.
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)
