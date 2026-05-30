import streamlit as st

st.set_page_config(
    page_title="Happies Playground",
    page_icon="⚡",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {
  font-family:'Space Grotesk','Inter',-apple-system,sans-serif !important;
}
.stApp { background:#06060f !important; }
.block-container { max-width:1400px !important; width:95vw !important; padding:0 2rem 6rem !important; background:transparent !important; }
#MainMenu, footer, [data-testid="stDecoration"] { display:none !important; }
[data-testid="stHeader"] { background:transparent !important; height:0 !important; }
[data-testid="stSidebar"] {
  background:#0a0a14 !important;
  border-right:1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebarNav"] a {
  border-radius:10px !important;
  color:#cbd5e1 !important;
  font-size:14px !important;
  font-weight:600 !important;
  transition:all .2s !important;
  padding:10px 14px !important;
  display:block !important;
}
[data-testid="stSidebarNav"] a:hover {
  color:#ffffff !important;
  background:rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
  color:#00f5ff !important;
  background:rgba(0,245,255,0.09) !important;
  font-weight:700 !important;
}

@keyframes orb1 { 0%,100%{transform:translate(0,0) scale(1)} 33%{transform:translate(40px,-50px) scale(1.05)} 66%{transform:translate(-25px,25px) scale(0.96)} }
@keyframes orb2 { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(-50px,-35px) scale(1.08)} }

.neon {
  background:linear-gradient(135deg,#00f5ff 0%,#a855f7 55%,#f0abfc 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.chapter-card {
  background:rgba(255,255,255,0.018);
  border:1px solid rgba(255,255,255,0.06);
  border-radius:20px; padding:28px 26px;
  position:relative; overflow:hidden;
  transition:border-color .3s, transform .3s;
}
.chapter-card::before {
  content:''; position:absolute; top:0;left:0;right:0; height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.08),transparent);
}
.chapter-card .num {
  font-size:11px;font-weight:700;letter-spacing:2px;
  text-transform:uppercase;margin-bottom:12px;
}
.chapter-card h3 { font-size:20px;font-weight:800;color:#f1f5f9;margin:0 0 8px; }
.chapter-card p  { font-size:13px;color:#475569;margin:0 0 16px;line-height:1.6; }
.chapter-card .topics span {
  display:inline-block; font-size:12px; font-weight:600;
  color:#334155; background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:8px; padding:3px 10px; margin:3px 2px;
}
</style>

<div style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;">
  <div style="position:absolute;top:-250px;right:-180px;width:750px;height:750px;border-radius:50%;
              background:radial-gradient(circle,rgba(124,58,237,0.13),transparent 65%);animation:orb1 14s ease-in-out infinite;"></div>
  <div style="position:absolute;bottom:-300px;left:-200px;width:650px;height:650px;border-radius:50%;
              background:radial-gradient(circle,rgba(0,245,255,0.08),transparent 65%);animation:orb2 17s ease-in-out infinite;"></div>
</div>

<div style="padding:100px 0 72px;position:relative;">
  <div style="font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
              color:rgba(0,245,255,0.65);margin-bottom:20px;">
    ⚡&nbsp;&nbsp;Interactive AI Learning Platform
  </div>
  <h1 style="font-size:clamp(52px,8vw,90px);font-weight:800;letter-spacing:-2.5px;
             color:#f1f5f9;margin:0 0 22px;line-height:1.03;">
    Happies<br><span class="neon">Playground</span>
  </h1>
  <p style="font-size:19px;color:#475569;max-width:520px;line-height:1.7;margin:0 0 20px;">
    Most people use AI like a black box.<br>
    <span style="color:#334155;">This is the black box, opened.</span>
  </p>
</div>
""", unsafe_allow_html=True)

# ── Progress tracker ─────────────────────────────────────────────────────────
PHASES = [
    {
        "num": "01", "color": "#00f5ff",
        "title": "How LLMs Actually Work",
        "desc":  "Understand what is happening inside the model before you build anything.",
        "topics": [
            ("Tokens",              True,  "How text becomes numbers"),
            ("Embeddings",          True,  "How meaning becomes location"),
            ("Context Windows",     False, "How much the model can remember"),
            ("Temperature",         False, "How randomness affects output"),
        ],
    },
    {
        "num": "02", "color": "#a855f7",
        "title": "Talking to Models Well",
        "desc":  "Get reliable, useful output. This is where most engineers spend most of their time.",
        "topics": [
            ("Prompt Engineering",  False, "Zero-shot, few-shot, chain-of-thought"),
            ("System Prompts",      False, "Shaping model behavior and persona"),
            ("Structured Output",   False, "Getting back clean JSON every time"),
            ("Hallucinations",      False, "Why models confabulate and how to reduce it"),
        ],
    },
    {
        "num": "03", "color": "#10b981",
        "title": "Building Real Apps",
        "desc":  "The most important phase. RAG alone unlocks 80% of real AI products.",
        "topics": [
            ("Calling the API",     False, "Claude / OpenAI SDK basics"),
            ("Chunking",            False, "Splitting documents for retrieval"),
            ("Vector Search",       False, "Finding meaning, not keywords"),
            ("RAG",                 False, "Grounding models in real knowledge"),
            ("Memory",              False, "Making conversations stateful"),
        ],
    },
    {
        "num": "04", "color": "#fbbf24",
        "title": "Agents + Production",
        "desc":  "Build systems that reason across multiple steps and run reliably at scale.",
        "topics": [
            ("Tool Calling",        False, "Giving the model hands"),
            ("Reasoning Loops",     False, "ReAct pattern and self-correction"),
            ("Streaming",           False, "Showing output token by token"),
            ("Evaluation",          False, "Measuring if your app actually works"),
        ],
    },
]

cols = st.columns(2)
for i, phase in enumerate(PHASES):
    with cols[i % 2]:
        done_count = sum(1 for _, done, _ in phase["topics"] if done)
        total      = len(phase["topics"])
        pct        = int(done_count / total * 100)
        color      = phase["color"]
        is_active  = done_count > 0

        topic_html = ""
        for name, done, subtitle in phase["topics"]:
            if done:
                icon  = f'<span style="color:{color};font-weight:700;">✓</span>'
                tcolor = "#e2e8f0"
            else:
                icon  = '<span style="color:#2d3748;">○</span>'
                tcolor = "#475569"
            topic_html += f"""
            <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:8px;">
              <div style="width:16px;flex-shrink:0;font-size:13px;">{icon}</div>
              <div>
                <div style="font-size:14px;font-weight:600;color:{tcolor};">{name}</div>
                <div style="font-size:12px;color:#334155;">{subtitle}</div>
              </div>
            </div>"""

        lock_icon = "" if is_active else '<div style="font-size:20px;position:absolute;top:22px;right:22px;opacity:0.15;">🔒</div>'

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
                    border-radius:20px;padding:28px;margin-bottom:16px;position:relative;">
          {lock_icon}
          <div style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                      color:{color};margin-bottom:8px;">Phase {phase['num']}</div>
          <div style="font-size:19px;font-weight:800;color:#f1f5f9;margin-bottom:6px;
                      letter-spacing:-0.5px;">{phase['title']}</div>
          <div style="font-size:13px;color:#64748b;margin-bottom:20px;line-height:1.55;">
            {phase['desc']}
          </div>
          {topic_html}
          <div style="margin-top:18px;">
            <div style="display:flex;justify-content:space-between;font-size:11px;
                        color:#334155;margin-bottom:6px;">
              <span style="font-weight:600;letter-spacing:.5px;">PROGRESS</span>
              <span style="color:{color};">{done_count} / {total}</span>
            </div>
            <div style="background:rgba(255,255,255,0.05);border-radius:99px;height:3px;">
              <div style="width:{pct}%;height:3px;border-radius:99px;background:{color};
                          box-shadow:0 0 8px {color}66;"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:48px 0 16px;">
  <span style="font-size:14px;color:#334155;">Continue where you left off → </span>
  <span style="font-size:15px;font-weight:700;
    background:linear-gradient(90deg,#a855f7,#00f5ff);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;">Embeddings</span>
  <span style="font-size:14px;color:#334155;"> in the sidebar</span>
</div>
""", unsafe_allow_html=True)
