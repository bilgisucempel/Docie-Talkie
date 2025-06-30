from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384

def prepare_chunks(text: str, chunk_size: int = 500):
    """
    Belgeyi sabit uzunlukta parçalara ayırır, embedding çıkarır ve bir FAISS indeksi oluşturur.
    Global değişkenler yerine, oluşturulan parçaları ve indeksi döndürür.
    
    Args:
        text (str): İşlenecek belge metni.
        chunk_size (int): Metnin parçalara ayrılacağı boyut.
        
    Returns:
        tuple: (list of str, faiss.IndexFlatL2) - Oluşturulan parçalar ve FAISS indeksi.
               Eğer hiç geçerli parça yoksa ([], None) döndürür.
    """
    
    #metni dilimleme
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    #filtreleme
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 30]

    if not chunks:
        return [], None 

    embeddings = model.encode(chunks, show_progress_bar=False)
    
    #FAISS indeksi oluşturma
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    
    return chunks, index

def get_context_from_question(question: str, document_chunks: list, faiss_index, top_k: int = 3):
    """
    Verilen soru için FAISS indeksini kullanarak en alakalı metin parçalarını bulur.
    Global değişkenler yerine, verilen belge parçalarını ve FAISS indeksini parametre olarak alır.
    
    Args:
        question (str): Kullanıcının sorusu.
        document_chunks (list): Belgenin metin parçalarını içeren liste (app.py'daki st.session_state.document_chunks).
        faiss_index (faiss.IndexFlatL2): Belge parçalarının embeddinglerini içeren FAISS indeksi (app.py'daki st.session_state.faiss_index).
        top_k (int): En alakalı kaç parçanın döndürüleceği.
        
    Returns:
        list: En alakalı metin parçalarının listesi.
    """
    #kontrol
    if not document_chunks or faiss_index is None:
        print("Hata: Belge parçaları veya FAISS indeksi mevcut değil. Bağlam alınamıyor.")
        return []

    #sorunun embeddingini oluştur
    question_embedding = model.encode([question], show_progress_bar=False)
    
    #FAISS indeksinde arama yap
    distances, indices = faiss_index.search(np.array(question_embedding), top_k)

    #indekslere göre orijinal parçaları al
    raw_chunks = [document_chunks[i] for i in indices[0]]

    #sağlama
    filtered_chunks = [chunk for chunk in raw_chunks if len(chunk.strip()) > 30]

    #debugging
    print("Filtrelenmiş chunklar (30+ karakter):")
    for i, chunk in enumerate(filtered_chunks):
        print(f"{i+1}. Chunk: {repr(chunk)}")

    return filtered_chunks