import streamlit as st
import os
import base64
import json

from utils.parsing import parse_file
from utils.claude_chat import ask_claude
from utils.rag import prepare_chunks, get_context_from_question
from utils.claude_rag_chat import ask_claude_with_context

st.set_page_config(page_title="Docie-Talkie", layout="wide")

api_key = st.sidebar.text_input(
    "Please enter your Anthropic API Key:", 
    type="password",
    help="API anahtarınızı https://console.anthropic.com/ adresinden alabilirsiniz."
)
if not api_key:
    st.sidebar.warning("API key is required to continue.")
    st.stop()


# sohbet yükleme kaydetme
CHAT_FILE = "chat_history.json"

def save_chat_history(history, filename=CHAT_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def load_chat_history(filename=CHAT_FILE):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_icon_base64():
    with open("utils/assets/docie_icon_final.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

icon_base64 = get_icon_base64()

if "theme" not in st.session_state:
    st.session_state.theme = "light"

clicked = st.query_params.get("theme")
if clicked == "dark":
    st.session_state.theme = "dark"
elif clicked == "light":
    st.session_state.theme = "light"

if st.session_state.theme == "light":
    bg_color = "#f1e9f9"
    text_color = "#2e2b3b"
    accent = "#9f8fff"
    bubble_user_color = "#f5f1ff"
    bubble_bot_color = "#e4f4ff"
    chat_text_color = "#2e2b3b"
else:
    bg_color = "#2a233f"
    text_color = "#ece9f5"
    accent = "#c5b8ff"
    bubble_user_color = "#4b3b72"
    bubble_bot_color = "#374f5e"
    chat_text_color = "#ffffff"

st.markdown(f"""
    <style>
    .top-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: {bg_color};
        padding: 10px 1.2rem 8px 0.2rem;
        border-bottom: 1px solid {accent};
        margin: 0;
        position: relative;
    }}
    .top-left {{
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    .top-left img {{
        height: 48px;
        margin-bottom: -4px;
    }}
    .top-left h1 {{
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        padding: 0;
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
    }}
    .theme-icons {{
        font-size: 24px;
        cursor: pointer;
        user-select: none;
        text-decoration: none !important;
    }}
    </style>
    <div class="top-navbar">
        <div class="top-left">
            <img src="data:image/png;base64,{icon_base64}" />
            <h1>Docie-Talkie</h1>
        </div>
        <div class="top-right">
            <a class="theme-icons" href="?theme=light">☀️</a>
            <a class="theme-icons" href="?theme=dark" style="margin-left:10px;">🌙</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# arka plan ve yazı stili
st.markdown(f"""
    <style>
    html, body, .main, .block-container, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    label, .stRadio > div, .stTextInput > label, .stTextArea > label, .stFileUploader > label {{
        color: {text_color} !important;
        font-weight: 500;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color};
    }}

    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 1px solid {accent};
        background-color: rgba(255,255,255,0.03);
        color: #ffffff !important;
    }}

    .stTextArea > div > textarea {{
        border-radius: 10px;
        border: 1px solid {accent};
        background-color: rgba(255,255,255,0.03);
        color: {text_color};
    }}

    .stExpander, .stChatMessage {{
        border-radius: 10px;
        border: 1px solid {accent};
        background-color: rgba(255,255,255,0.03);
        color: {text_color};
    }}

    .stTextInput, .stTextArea {{
        background-color: rgba(255,255,255,0.03);
    }}
    </style>
""", unsafe_allow_html=True)

# yazı tipi
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)

st.markdown("""
    <style>
    button[kind="secondary"] > div > p {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# açıklama
st.markdown("""
Welcome to your intelligent document assistant powered by Claude 3 Haiku.  
Upload a PDF or HTML file, and ask anything about it using natural language.
---
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("Dosya Yükleyici ve İçerik Görüntüleme", expanded=True):
        uploaded_file = st.file_uploader("PDF veya HTML dosyası yükleyin:", type=["pdf", "html"], key="uploader1")

        if uploaded_file:
            file_type = uploaded_file.type.split("/")[-1]
            with st.spinner("Dosya işleniyor..."):
                parsed_text = parse_file(uploaded_file, file_type)
                st.session_state["parsed_text"] = parsed_text
                prepare_chunks(parsed_text)
                st.session_state["document_chunks"] = True

            st.subheader("Dosyanızın İçeriği:")
            st.text_area("İçerik", st.session_state.get("parsed_text", ""), height=300)

with col2:
    with st.expander("Claude 3 Haiku ile Chatbot", expanded=True):
        chat_input = st.text_input("Claude'a bir şeyler söyle:", value=st.session_state.chat_input, key="chat_input_field")
        send_clicked = st.button("Gönder", use_container_width=True)

        if send_clicked and chat_input.strip():
            with st.spinner("Claude düşünüyor..."):
                context = get_context_from_question(chat_input) if st.session_state.get("document_chunks") else []
                response = ask_claude(chat_input, context, api_key)

            st.session_state.chat_history.append(("user", chat_input))
            st.session_state.chat_history.append(("assistant", response))
            save_chat_history(st.session_state.chat_history)
            st.session_state.chat_input = ""
            st.rerun()

        for sender, msg in st.session_state.chat_history:
            bg_color = bubble_user_color if sender == "user" else bubble_bot_color
            align = "flex-end" if sender == "user" else "flex-start"
            bubble_html = f"""
            <div style='display:flex; justify-content:{align}; margin-bottom:10px;'>
                <div style='background-color:{bg_color}; color:{chat_text_color}; padding:10px 15px; border-radius:12px; max-width:75%;'>
                    {msg}
                </div>
            </div>
            """
            st.markdown(bubble_html, unsafe_allow_html=True)

# RAG
if uploaded_file and st.session_state.get("parsed_text") and st.session_state.get("document_chunks"):
    with st.expander("Belgeye Dayalı Soru-Cevap (RAG)", expanded=True):
        question = st.text_input("Bu belge hakkında bir soru sorun:", key="rag_input")

        if question:
            relevant_chunks = get_context_from_question(question)
            context = "\n\n".join(relevant_chunks)

            st.subheader("İlgili Parçalar:")
            for i, chunk in enumerate(relevant_chunks, 1):
                st.markdown(f"**{i}. Parça:**")
                st.code(chunk, language="markdown")

            with st.spinner("Claude cevap oluşturuyor..."):
               answer = ask_claude_with_context(question, context, api_key)

            st.success("Cevabınız:")
            st.markdown(answer)

            if st.button("Cevabı Kopyala", key="copy_rag_answer"):
                st.code(answer, language='markdown')

if st.button("Sohbet Geçmişini Temizle", key="clear_history"):
    st.session_state.chat_history = []
    save_chat_history([])
    st.rerun()