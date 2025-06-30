# Docie-Talkie

Docie-Talkie, Anthropic'in Claude 3 Haiku modeli tarafından desteklenen, PDF ve HTML belgeleriyle etkileşim kurmanızı sağlayan akıllı bir belge asistanıdır. Yüklediğiniz belgeler hakkında doğal dil kullanarak sorular sorabilir, ilgili bilgileri hızlıca bulabilir ve özetler alabilirsiniz.

Bu proje, Retrieval Augmented Generation (RAG) prensibini kullanarak, sorularınıza yalnızca sağladığınız belge bağlamında yanıt verir.

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
PyMuPDF
python-dotenv
streamlit
requests
anthropic
pymupdf
pdfplumber
beautifulsoup4
sentence-transformers
faiss-cpu

## Katkıda bulunma

Pull requestlerinizi beklerim, iyi çalışmalar!

## Notlar:
Genel sohbet özelliği, projenin RAG odaklılığını artırmak amacıyla kaldırılmıştır.

Bu proje, Streamlit'in session_state özelliğini kullanarak dosya işleme ve RAG indeksleme işlemlerinin yalnızca bir kez yapılmasını sağlar, böylece performans artırılır.

Hata yönetimi, API çağrıları sırasında oluşabilecek çeşitli sorunları (ağ hataları, API hataları vb.) daha iyi ele almak için iyileştirilmiştir.