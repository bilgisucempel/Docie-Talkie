import pdfplumber
import fitz  # PyMuPDF
import tempfile
import re
from bs4 import BeautifulSoup
import os

def parse_file(file, file_type):
    """
    PDF veya HTML dosyasını düzgün şekilde okuyup metin çıkarır.

    Args:
        file: Yüklenen dosya nesnesi (Streamlit UploadedFile).
        file_type (str): Dosyanın türü ("pdf" veya "html").

    Returns:
        str: Dosyadan çıkarılan düz metin veya hata mesajı.
    """
    if file_type.lower() == "pdf":
        return parse_pdf_with_fallback(file)
    elif file_type.lower() == "html":
        return parse_html(file)
    else:
        return "Desteklenmeyen dosya türü."

def parse_pdf_with_fallback(file):
    """
    Önce pdfplumber ile PDF'ten metin çıkarmayı dener, başarısız olursa PyMuPDF kullanır.

    Args:
        file: Yüklenen PDF dosya nesnesi.

    Returns:
        str: PDF'ten çıkarılan metin.
    """
    try:
        return parse_pdfplumber(file)
    except Exception as e:
        print(f"pdfplumber başarısız oldu, PyMuPDF'e geçiliyor: {e}")
        return parse_pymupdf(file)

def parse_pdfplumber(file):
    """
    pdfplumber kullanarak PDF'ten metin çıkarır.

    Args:
        file: Yüklenen PDF dosya nesnesi.

    Returns:
        str: PDF'ten çıkarılan metin.
    """
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.strip() + "\n"
    return text.strip()

def parse_pymupdf(file):
    """
    PyMuPDF (fitz) ile PDF içeriğini okuyup düzgün formatta metne çevirir.
    Streamlit'in in-memory dosya yapısıyla uyumlu olması için geçici dosya kullanır.

    Args:
        file: Yüklenen PDF dosya nesnesi.

    Returns:
        str: PDF'ten çıkarılan metin.
    """
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    try:
        with fitz.open(tmp_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                for block in blocks:
                    block_text = block[4].strip()
                    if len(block_text.split()) > 4:
                        block_text = re.sub(r'\s+', ' ', block_text)
                        text += block_text + "\n"
    finally:
        os.remove(tmp_path)

    return text.strip()

def parse_html(file):
    """
    HTML dosyasını BeautifulSoup kullanarak düz metne çevirir.
    HTML etiketlerini, script ve style bloklarını kaldırır.

    Args:
        file: Yüklenen HTML dosya nesnesi.

    Returns:
        str: HTML'den çıkarılan düz metin.
    """
    content = file.read().decode("utf-8")
    soup = BeautifulSoup(content, 'html.parser')

    #script ve style etiketlerini kaldır
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    text = soup.get_text()

    #çoklu boşlukları tek boşluk haline getir ve baştaki/sondaki boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    return text