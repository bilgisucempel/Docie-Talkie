import streamlit as st
import os
import base64
import json

from utils.parsing import parse_file
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

def get_icon_base64():
    #dizin bazlı path ayarı
    icon_path = os.path.join(os.path.dirname(__file__), "utils", "assets", "docie_icon_final.png")
    with open(icon_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

icon_base64 = get_icon_base64()


st.markdown(f"""
    <style>
    .top-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 1.2rem 8px 0.2rem;
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
    </style>
    <div class="top-navbar">
        <div class="top-left">
            <img src="data:image/png;base64,{icon_base64}" />
            <h1>Docie-Talkie</h1>
        </div>
    </div>
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

#açıklama
st.markdown("""
Akıllı belge asistanınız Docie-Talkie'ye hoş geldiniz! Claude 3 Haiku tarafından desteklenmektedir.
Bir PDF veya HTML dosyası yükleyin ve belge hakkında kullanarak herhangi bir şey sorun.
---
""")

#session state başlatılması
if "parsed_text" not in st.session_state:
    st.session_state.parsed_text = ""
if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = None
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
if "uploaded_file_id" not in st.session_state:
    st.session_state.uploaded_file_id = None

#Dosya Yükleyici ve İçerik Görüntüleme bölümü
with st.expander("Dosya Yükleyici ve İçerik Görüntüleme", expanded=True):
    uploaded_file = st.file_uploader("PDF veya HTML dosyası yükleyin:", type=["pdf", "html"], key="uploader1")

    if uploaded_file:
        if st.session_state.uploaded_file_id != uploaded_file.file_id:
            st.session_state.uploaded_file_id = uploaded_file.file_id
            file_type = uploaded_file.type.split("/")[-1]
            with st.spinner("Dosya işleniyor..."):
                parsed_text = parse_file(uploaded_file, file_type)
                st.session_state.parsed_text = parsed_text
                
                chunks, faiss_index = prepare_chunks(parsed_text)
                st.session_state.document_chunks = chunks
                st.session_state.faiss_index = faiss_index
                st.success("Dosya başarıyla işlendi!")
            st.rerun()
        
        st.subheader("Dosyanızın İçeriği:")
        st.text_area("İçerik", st.session_state.parsed_text, height=300)
    else:
        if st.session_state.uploaded_file_id is not None:
            st.session_state.uploaded_file_id = None
            st.session_state.parsed_text = ""
            st.session_state.document_chunks = None
            st.session_state.faiss_index = None
            st.rerun()

#RAG
if st.session_state.document_chunks is not None and st.session_state.faiss_index is not None:
    with st.expander("Belgeye Dayalı Soru-Cevap (RAG)", expanded=True):
        question = st.text_input("Bu belge hakkında bir soru sorun:", key="rag_input")

        if question:
            with st.spinner("İlgili parçalar aranıyor..."):
                relevant_chunks = get_context_from_question(question, st.session_state.document_chunks, st.session_state.faiss_index)
            
            context = "\n\n".join(relevant_chunks)

            if relevant_chunks:
                st.subheader("İlgili Parçalar:")
                for i, chunk in enumerate(relevant_chunks, 1):
                    st.markdown(f"**{i}. Parça:**")
                    st.code(chunk, language="markdown")
            else:
                st.info("Bu soruyla ilgili belge içinde yeterli bağlam bulunamadı.")

            with st.spinner("Claude cevap oluşturuyor..."):
                answer = ask_claude_with_context(question, context, api_key)

            st.success("Cevabınız:")
            st.markdown(answer)

            if st.button("Cevabı Kopyala", key="copy_rag_answer"):
                st.code(answer, language='markdown')
else:
    st.info("Lütfen yukarıdan bir belge yükleyin ve işlenmesini bekleyin.")
