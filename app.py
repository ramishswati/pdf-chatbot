import streamlit as st
from utils.pdf_processor import process_pdfs
from utils.rag_pipeline import get_answer

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #050508;
    --surface: #0e0e16;
    --card:    #14141e;
    --card2:   #1a1a26;
    --border:  rgba(255,255,255,0.07);
    --border2: rgba(255,255,255,0.12);
    --cyan:    #00e5ff;
    --violet:  #9d4edd;
    --pink:    #ff4d9d;
    --green:   #06d6a0;
    --gold:    #ffd166;
    --grad1:   linear-gradient(135deg,#00e5ff,#9d4edd);
    --grad2:   linear-gradient(135deg,#ff4d9d,#9d4edd);
    --grad3:   linear-gradient(135deg,#06d6a0,#00e5ff);
    --text:    #f0eeff;
    --muted:   #6e6d8a;
    --mono:    'JetBrains Mono',monospace;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

html,body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"]{
    background:var(--bg)!important;
    color:var(--text)!important;
    font-family:'Outfit',sans-serif!important;
}

[data-testid="stAppViewContainer"]::before{
    content:'';position:fixed;inset:0;
    background-image:
        linear-gradient(rgba(0,229,255,0.025) 1px,transparent 1px),
        linear-gradient(90deg,rgba(0,229,255,0.025) 1px,transparent 1px);
    background-size:48px 48px;
    pointer-events:none;z-index:0;
}

[data-testid="stSidebar"]{
    background:var(--surface)!important;
    border-right:1px solid var(--border2)!important;
    position:relative;
}
[data-testid="stSidebar"]::before{
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:var(--grad1);
}

.logo-wrap{padding:32px 0 20px;text-align:center}
.logo-ring{
    width:70px;height:70px;margin:0 auto 14px;border-radius:22px;
    background:var(--grad1);
    display:flex;align-items:center;justify-content:center;font-size:32px;
    box-shadow:0 0 35px rgba(0,229,255,0.35),0 0 70px rgba(157,78,221,0.2);
    animation:glow 3s ease-in-out infinite;
}
@keyframes glow{
    0%,100%{box-shadow:0 0 35px rgba(0,229,255,0.35),0 0 70px rgba(157,78,221,0.2)}
    50%{box-shadow:0 0 50px rgba(0,229,255,0.55),0 0 100px rgba(157,78,221,0.35)}
}
.logo-name{
    font-size:22px;font-weight:800;letter-spacing:-0.3px;
    background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.logo-tag{font-family:var(--mono);font-size:9px;color:var(--muted);letter-spacing:2.5px;text-transform:uppercase;margin-top:5px}

.hr{height:1px;background:linear-gradient(90deg,transparent,var(--border2),transparent);margin:16px 0}

.slabel{
    font-family:var(--mono);font-size:9px;color:var(--muted);
    letter-spacing:2.5px;text-transform:uppercase;
    display:flex;align-items:center;gap:8px;margin-bottom:10px;
}
.slabel::after{content:'';flex:1;height:1px;background:var(--border)}

[data-testid="stFileUploader"]{
    background:var(--card)!important;
    border:1.5px dashed rgba(0,229,255,0.2)!important;
    border-radius:14px!important;
    transition:all 0.3s!important;
}
[data-testid="stFileUploader"]:hover{
    border-color:rgba(0,229,255,0.5)!important;
    background:rgba(0,229,255,0.03)!important;
}

.stButton>button{
    font-family:'Outfit',sans-serif!important;font-weight:600!important;
    font-size:13px!important;border:none!important;border-radius:12px!important;
    padding:12px 20px!important;width:100%!important;
    transition:all 0.25s!important;cursor:pointer!important;
}

.stat-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0}
.stat-box{
    background:var(--card);border:1px solid var(--border2);border-radius:12px;
    padding:14px;text-align:center;position:relative;overflow:hidden;
}
.stat-box::after{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.stat-box.c1::after{background:var(--grad3)}
.stat-box.c2::after{background:var(--grad2)}
.stat-n{
    font-size:30px;font-weight:800;line-height:1;
    background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.stat-l{font-size:10px;color:var(--muted);margin-top:4px;font-family:var(--mono)}

.ftag{
    display:flex;align-items:center;gap:8px;
    background:rgba(0,229,255,0.05);border:1px solid rgba(0,229,255,0.18);
    border-radius:8px;padding:8px 12px;
    font-size:11px;color:var(--cyan);font-family:var(--mono);margin-top:6px;
}

.mhdr{
    padding:36px 0 22px;
    border-bottom:1px solid var(--border);
    margin-bottom:28px;
    display:flex;align-items:center;gap:18px;
}
.micon{
    width:56px;height:56px;border-radius:18px;
    background:var(--grad1);
    display:flex;align-items:center;justify-content:center;font-size:28px;
    box-shadow:0 0 28px rgba(0,229,255,0.3);flex-shrink:0;
}
.mtitle{
    font-size:30px;font-weight:800;letter-spacing:-0.5px;
    background:var(--grad1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.msub{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:4px}

.empty{text-align:center;padding:70px 20px}
.orb{
    width:110px;height:110px;margin:0 auto 24px;border-radius:50%;
    background:radial-gradient(circle at 35% 35%,rgba(0,229,255,0.12),rgba(157,78,221,0.06));
    border:1px solid rgba(0,229,255,0.15);
    display:flex;align-items:center;justify-content:center;font-size:46px;
    box-shadow:0 0 50px rgba(0,229,255,0.08);
    animation:float 4s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.etitle{font-size:22px;font-weight:700;margin-bottom:10px}
.edesc{font-size:14px;color:var(--muted);line-height:1.7}
.steps{display:flex;justify-content:center;gap:28px;margin-top:28px}
.step{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:12px;color:var(--muted)}
.snum{
    width:34px;height:34px;border-radius:50%;
    border:1px solid rgba(0,229,255,0.3);
    display:flex;align-items:center;justify-content:center;
    font-family:var(--mono);font-size:13px;color:var(--cyan);
    background:rgba(0,229,255,0.05);
}

.cwrap{display:flex;flex-direction:column;gap:22px;padding-bottom:130px}
.msg{display:flex;gap:14px;animation:slideUp 0.35s ease}
.msg.user{flex-direction:row-reverse}
@keyframes slideUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

.av{width:40px;height:40px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.av.bot{background:var(--grad1);box-shadow:0 0 16px rgba(0,229,255,0.3)}
.av.usr{background:var(--grad2);box-shadow:0 0 16px rgba(255,77,157,0.3)}

.bbl{max-width:70%;padding:16px 20px;border-radius:18px;font-size:14px;line-height:1.75;border:1px solid var(--border2)}
.bbl.bot{
    background:var(--card);border-radius:4px 18px 18px 18px;
    border-color:rgba(0,229,255,0.1);
    box-shadow:0 4px 24px rgba(0,0,0,0.35),inset 0 1px 0 rgba(255,255,255,0.03);
}
.bbl.usr{
    background:linear-gradient(135deg,rgba(255,77,157,0.1),rgba(157,78,221,0.1));
    border-radius:18px 4px 18px 18px;border-color:rgba(157,78,221,0.2);text-align:right;
}

.srcs{margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}
.srclbl{font-family:var(--mono);font-size:9px;color:var(--muted);letter-spacing:2px;margin-bottom:6px}
.srcb{
    display:inline-flex;align-items:center;gap:5px;
    background:rgba(6,214,160,0.07);border:1px solid rgba(6,214,160,0.22);
    color:var(--green);font-family:var(--mono);font-size:10px;
    padding:4px 10px;border-radius:6px;margin:2px 3px 0 0;
}

.stTextInput>div>div>input{
    background:var(--card2)!important;border:1.5px solid var(--border2)!important;
    border-radius:14px!important;color:var(--text)!important;
    font-family:'Outfit',sans-serif!important;font-size:14px!important;
    padding:15px 20px!important;transition:all 0.3s!important;
}
.stTextInput>div>div>input:focus{
    border-color:var(--cyan)!important;
    box-shadow:0 0 0 3px rgba(0,229,255,0.08),0 0 24px rgba(0,229,255,0.12)!important;
}
.stTextInput>div>div>input::placeholder{color:var(--muted)!important}

[data-testid="stFormSubmitButton"]>button{
    background:var(--grad1)!important;color:#000!important;
    font-weight:700!important;border-radius:12px!important;border:none!important;
    padding:15px 26px!important;
    box-shadow:0 4px 20px rgba(0,229,255,0.25)!important;
    transition:all 0.25s!important;
}
[data-testid="stFormSubmitButton"]>button:hover{
    transform:translateY(-2px)!important;
    box-shadow:0 8px 32px rgba(0,229,255,0.4)!important;
}

::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(0,229,255,0.18);border-radius:2px}

#MainMenu,footer,header{visibility:hidden}
[data-testid="stDecoration"]{display:none}
</style>
""", unsafe_allow_html=True)

if "messages"     not in st.session_state: st.session_state.messages     = []
if "vector_store" not in st.session_state: st.session_state.vector_store = None
if "doc_count"    not in st.session_state: st.session_state.doc_count    = 0
if "pdf_names"    not in st.session_state: st.session_state.pdf_names    = []

with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-ring">🧠</div>
        <div class="logo-name">DocuMind AI</div>
        <div class="logo-tag">RAG · PDF · Intelligence</div>
    </div>
    <div class="hr"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="slabel">📂 Upload Documents</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "PDFs", type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if uploaded_files:
        if st.button("⚡  Process & Index"):
            with st.spinner("Indexing your documents..."):
                vs, chunks = process_pdfs(uploaded_files)
                st.session_state.vector_store = vs
                st.session_state.doc_count    = chunks
                st.session_state.pdf_names    = [f.name for f in uploaded_files]
            st.success(f"✅ {len(uploaded_files)} file(s) ready!")

    if st.session_state.vector_store:
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-box c1">
                <div class="stat-n">{len(st.session_state.pdf_names)}</div>
                <div class="stat-l">PDFs</div>
            </div>
            <div class="stat-box c2">
                <div class="stat-n">{st.session_state.doc_count}</div>
                <div class="stat-l">Chunks</div>
            </div>
        </div>
        <div class="hr"></div>
        <div class="slabel">📄 Loaded Files</div>
        """, unsafe_allow_html=True)
        for name in st.session_state.pdf_names:
            st.markdown(f'<div class="ftag">📄 {name}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Chat"):
        st.session_state.messages = []
        st.rerun()

_, col, _ = st.columns([1, 7, 1])
with col:
    st.markdown("""
    <div class="mhdr">
        <div class="micon">🧠</div>
        <div>
            <div class="mtitle">DocuMind AI</div>
            <div class="msub">// Ask anything about your documents</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div class="empty">
            <div class="orb">📄</div>
            <div class="etitle">Ready to explore your documents</div>
            <div class="edesc">Upload any PDF and ask questions in plain English.<br>DocuMind finds the answers using AI.</div>
            <div class="steps">
                <div class="step"><div class="snum">1</div><span>Upload PDF</span></div>
                <div class="step"><div class="snum">2</div><span>Process it</span></div>
                <div class="step"><div class="snum">3</div><span>Ask away</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="cwrap">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg user">
                    <div class="av usr">👤</div>
                    <div class="bbl usr">{msg["content"]}</div>
                </div>""", unsafe_allow_html=True)
            else:
                srcs = ""
                if msg.get("sources"):
                    badges = "".join([f'<span class="srcb">📄 {s}</span>' for s in msg["sources"]])
                    srcs = f'<div class="srcs"><div class="srclbl">SOURCES</div>{badges}</div>'
                st.markdown(f"""
                <div class="msg bot">
                    <div class="av bot">🧠</div>
                    <div class="bbl bot">{msg["content"]}{srcs}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            user_input = st.text_input(
                "q", placeholder="Ask anything about your documents...",
                label_visibility="collapsed"
            )
        with c2:
            submitted = st.form_submit_button("Send →")

    if submitted and user_input:
        if not st.session_state.vector_store:
            st.warning("⚠️ Pehle sidebar se PDF upload aur process karo!")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("🧠 Thinking..."):
                answer, sources = get_answer(user_input, st.session_state.vector_store)
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            st.rerun()