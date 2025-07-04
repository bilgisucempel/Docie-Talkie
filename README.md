# Docie-Talkie: Akıllı Belge Asistanı
Docie-Talkie, Anthropic'in Claude 3 Haiku modeli tarafından desteklenen, PDF ve HTML belgeleriyle etkileşim kurmanızı sağlayan akıllı bir belge asistanıdır. Yüklediğiniz belgeler hakkında doğal dil kullanarak sorular sorabilir, ilgili bilgileri hızlıca bulabilir ve özetler alabilirsiniz.

Bu proje, Retrieval Augmented Generation (RAG) prensibini kullanarak, sorularınıza yalnızca sağladığınız belge bağlamında yanıt verir.

## Özellikler
* PDF ve HTML Desteği: Hem PDF hem de HTML formatındaki belgeleri yükleyebilir ve işleyebilirsiniz.

* Gelişmiş Metin Ayrıştırma (Parsing): PDF'ler için pdfplumber ve PyMuPDF (fallback ile), HTML için ise BeautifulSoup kullanarak temiz ve doğru metin çıkarma.

* Bağlama Dayalı Soru-Cevap (RAG): Yüklenen belge içeriğinden ilgili parçaları alarak Claude 3 Haiku ile doğru ve ilgili yanıtlar üretir.

* Kullanıcı Dostu Arayüz: Streamlit ile oluşturulmuş sezgisel ve etkileşimli kullanıcı arayüzü.

## Kurulum
Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

Depoyu Klonlayın:
```bash
git clone [https://github.com/bilgisucempel/docie-talkie.git](https://github.com/bilgisucempel/docie-talkie.git)
cd docie-talkie
```

Sanal Ortam Oluşturun ve Aktive Edin:
Python bağımlılıklarını izole etmek için bir sanal ortam oluşturmanız önerilir.
```bash
python -m venv venv
```
Windows için:
```bash
venv\Scripts\activate
```
macOS/Linux için:
```bash
source venv/bin/activate
```
Gerekli Paketleri Yükleyin:
```bash
pip install -r requirements.txt
```
Anthropic API Anahtarınızı Sağlayın:
Uygulamayı çalıştırmadan önce bir Anthropic API anahtarına ihtiyacınız olacak. Anahtarınızı https://console.anthropic.com/ adresinden alabilirsiniz. Uygulama başlatıldığında kenar çubuğundaki giriş alanına API anahtarınızı yapıştırmanız istenecektir.

### Kullanım
Uygulamayı Başlatın:
Sanal ortamınız aktifken projenin ana dizininde aşağıdaki komutu çalıştırın:
```bash
streamlit run app.py
```
Bu komut, uygulamanın tarayıcınızda açılmasını sağlayacaktır.

* Belge Yükleyin:
Sol taraftaki "Dosya Yükleyici ve İçerik Görüntüleme" bölümünden bir PDF veya HTML dosyası yükleyin. Dosya yüklendikten sonra, uygulama belgeyi otomatik olarak işleyecek ve metin içeriğini görüntüleyecektir.

* Belge Hakkında Soru Sorun:
Sağ taraftaki "Belgeye Dayalı Soru-Cevap (RAG)" bölümündeki metin giriş alanına belgenizle ilgili bir soru yazın ve Enter tuşuna basın. Claude 3 Haiku, belgedeki ilgili bilgilere dayanarak size bir yanıt sağlayacaktır.

#### Geliştirme Notları
Bu proje, Streamlit'in session_state özelliğini kullanarak dosya işleme ve RAG indeksleme işlemlerinin yalnızca bir kez yapılmasını sağlar, böylece performans artırılır.

Genel sohbet özelliği, projenin RAG odaklılığını artırmak amacıyla kaldırılmıştır.

Hata yönetimi, API çağrıları sırasında oluşabilecek çeşitli sorunları (ağ hataları, API hataları vb.) daha iyi ele almak için iyileştirilmiştir.

#### Katkıda Bulunma
Projeye katkıda bulunmak isterseniz, lütfen bir pull request açmaktan veya bir issue oluşturmaktan çekinmeyin.

#### Lisans
Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.