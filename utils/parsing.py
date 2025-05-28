import pdfplumber
import fitz  #PyMuPDF
import tempfile
import re

def parse_file(file, file_type):
    #PDF veya HTML dosyasını düzgün şekilde okuyup metin çıkarır.
    if file_type.lower() == "pdf":
        return parse_pdf_with_fallback(file)
    elif file_type.lower() == "html":
        return parse_html(file)
    else:
        return "Desteklenmeyen dosya türü."

def parse_pdf_with_fallback(file):
    #önce pdfplumber ile dener, başarısız olursa PyMuPDF kullanır.
    try:
        return parse_pdfplumber(file)
    except Exception as e:
        print("pdfplumber başarısız oldu, PyMuPDF'e geçiliyor:", e)
        return parse_pymupdf(file)

def parse_pdfplumber(file):
    #pdfplumber kullanarak PDF'ten metin çıkarır.
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.strip() + "\n"
    return text.strip()

def parse_pymupdf(file):
    #PyMuPDF (fitz) ile PDF içeriğini okuyup düzgün formatta metne çevirir.
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    with fitz.open(tmp_path) as doc:
        for page in doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                block_text = block[4].strip()
                if len(block_text.split()) > 4:
                    block_text = re.sub(r'\s+', ' ', block_text)
                    text += block_text + "\n"

    return text.strip()

def parse_html(file):
    #HTML dosyasını düz metne çevirir.
    return file.read().decode("utf-8")
