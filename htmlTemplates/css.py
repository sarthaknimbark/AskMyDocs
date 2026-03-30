css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ─────────────────────────────────────────────── */
body, .stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    color: #e0e0e0;
}

/* ── Header ─────────────────────────────────────────────── */
.header {
    text-align: center;
    padding: 2rem 1.5rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.10) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 1rem;
    margin-bottom: 1.5rem;
    animation: fadeSlideDown 0.6s ease-out;
}
.header h2 {
    font-weight: 700;
    font-size: 1.8rem;
    color: #fff;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
}
.header h2 img {
    height: 52px;
    width: 52px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(139,92,246,0.35);
}
.header p {
    color: rgba(255,255,255,0.6);
    font-weight: 400;
    margin-top: 0.4rem;
    font-size: 1rem;
}

/* ── Footer ─────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 1.2rem;
    font-size: 0.85rem;
    font-weight: 300;
    margin-top: 3rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.05) 100%);
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    color: rgba(255,255,255,0.45);
}
.footer a, .footer-link {
    color: rgba(139,92,246,0.8);
    text-decoration: none;
    transition: color 0.2s ease;
}
.footer a:hover, .footer-link:hover {
    color: #a78bfa;
}

/* ── Chat Messages ──────────────────────────────────────── */
.chat-message {
    padding: 1.1rem 1.3rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    width: 95%;
    animation: fadeSlideUp 0.35s ease-out;
    border: 1px solid rgba(255,255,255,0.06);
}

.chat-message.user {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(59,130,246,0.08) 100%);
    border-left: 4px solid #6366f1;
    margin-left: auto;
}

.chat-message.bot {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
    border-left: 4px solid #8b5cf6;
}

.chat-message .message {
    padding: 0.4rem 0;
    color: #e0e0e0;
    font-size: 0.95rem;
    line-height: 1.65;
}

.chat-message.bot .message::before {
    content: '🤖 AskMyDocs';
    font-weight: 600;
    display: block;
    color: #a78bfa;
    font-size: 0.8rem;
    margin-bottom: 0.35rem;
    letter-spacing: 0.02em;
}

.chat-message.user .message::before {
    content: '🧑 You';
    font-weight: 600;
    display: block;
    color: #818cf8;
    font-size: 0.8rem;
    margin-bottom: 0.35rem;
    letter-spacing: 0.02em;
}

/* ── Animations ─────────────────────────────────────────── */
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Streamlit Overrides (dark theme polish) ────────────── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e0e0e0 !important;
    border-radius: 0.75rem !important;
    padding: 0.7rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 0.75rem !important;
    padding: 0.55rem 1.5rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.02em !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
.stFileUploader {
    border: 1px dashed rgba(139,92,246,0.3) !important;
    border-radius: 1rem !important;
    background: rgba(139,92,246,0.04) !important;
}

/* ── Markdown in bot responses ──────────────────────────── */
.stMarkdown h2, .stMarkdown h3 {
    color: #c4b5fd !important;
    border-bottom: 1px solid rgba(139,92,246,0.15);
    padding-bottom: 0.3rem;
    margin-top: 0.8rem;
}
.stMarkdown strong {
    color: #e0e7ff !important;
}
.stMarkdown blockquote {
    border-left: 3px solid #8b5cf6;
    padding-left: 1rem;
    color: rgba(255,255,255,0.7);
    font-style: italic;
}
.stMarkdown code {
    background: rgba(139,92,246,0.1);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-size: 0.9em;
}
.stMarkdown table {
    border-collapse: collapse;
    width: 100%;
}
.stMarkdown th, .stMarkdown td {
    border: 1px solid rgba(255,255,255,0.1);
    padding: 0.5rem 0.8rem;
    text-align: left;
}
.stMarkdown th {
    background: rgba(99,102,241,0.12);
    color: #c4b5fd;
    font-weight: 600;
}

</style>
"""
