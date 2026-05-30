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

# Chapter grid
chapters = [
    ("#00f5ff", "01", "Foundations",   "How the model reads, thinks, and understands.",
     ["Tokens", "Embeddings", "Context Windows", "Chunking"]),
    ("#a855f7", "02", "Applications",  "Building things that actually work.",
     ["Semantic Search", "RAG", "Memory", "Reranking"]),
    ("#10b981", "03", "Agents",        "Systems that reason and act.",
     ["Tool Calling", "Workflows", "Reasoning Loops"]),
    ("#fbbf24", "04", "Production",    "Shipping AI that doesn't break.",
     ["Streaming", "Caching", "FastAPI", "Docker"]),
]

cols = st.columns(2)
for i, (color, num, title, desc, topics) in enumerate(chapters):
    with cols[i % 2]:
        tags = "".join(f"<span>{t}</span>" for t in topics)
        lock = "" if num == "01" else '<span style="font-size:18px;position:absolute;top:24px;right:24px;opacity:0.2;">🔒</span>'
        st.markdown(f"""
        <div class="chapter-card" style="margin-bottom:16px;">
          {lock}
          <div class="num" style="color:{color};">Chapter {num}</div>
          <h3>{title}</h3>
          <p>{desc}</p>
          <div class="topics">{tags}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:56px 0 24px;">
  <span style="font-size:14px;color:#1e293b;">
    Start with Foundations → open
  </span>
  <span style="font-size:15px;font-weight:700;
    background:linear-gradient(90deg,#00f5ff,#a855f7);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;"> Tokens </span>
  <span style="font-size:14px;color:#1e293b;">in the sidebar</span>
</div>
""", unsafe_allow_html=True)
