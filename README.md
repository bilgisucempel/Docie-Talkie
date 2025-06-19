# Docie-Talkie

Docie-Talkie, kullanıcıların PDF ve HTML dosyaları üzerinden içerik bazlı sohbet yapabildiği, ayrıca basit diyalog kurabileceği bir yapay zeka destekli chatbot uygulamasıdır. Uygulama Streamlit ile geliştirilmiş ve Claude (Anthropic API) ile entegre edilmiştir.

---

## Özellikler

-> PDF ve HTML dosyalarını yükleyerek içerik üzerinde sohbet  
-> Serbest metin sohbeti (LLM desteğiyle)  
-> Claude (Anthropic API) üzerinden LLM entegrasyonu  
-> Streamlit tabanlı web arayüzü  
-> Kolay kurulum ve kullanım  

---

## Kurulum

### 1. Repoyu klonla

git clone bilgisucempel/Docie-Talkie
cd docie-talkie

### 2. Sanal ortam oluştur (önerilir)
python -m venv venv
source venv/bin/activate  #Windows: venv\Scripts\activate

### 3. Bağımlılıkları kur
pip install -r requirements.txt

## API anahtarı

 Projede LLM modeli ile iletişim kurmak için Anthropic API key gereklidir. Aşağıdaki yöntemlerden birini seçebilirsiniz:

Yöntem 1: Streamlit UI yoluyla
Sayfanın yanındaki çubuğa API key’ini gir

Yöntem 2: .env dosyası
Projede .env kullanmak istersen köke bir .env koy:

ANTHROPIC_API_KEY=YOUR_API_KEY_HERE

## Uygulamayı başlatın
Terminalde:
streamlit run app.py  

### Kullanılan paketler (requirements)
streamlit
python-dotenv
pdfplumber
pymupdf
beautifulsoup4
requests
anthropic

## Katkıda bulunma

Pull requestlerinizi beklerim, iyi çalışmalar!