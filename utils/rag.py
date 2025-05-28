from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384

index = faiss.IndexFlatL2(dimension)

document_chunks = []

def prepare_chunks(text, chunk_size=500):
    #belgeyi sabit uzunlukta parçalara ayırır, embedding çıkarır ve FAISS'e ekler.
    global document_chunks, index
    document_chunks = []
    index.reset()

    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = model.encode(chunks, show_progress_bar=False)
    index.add(np.array(embeddings))
    document_chunks.extend(chunks)

def get_context_from_question(question, top_k=3):
    question_embedding = model.encode([question], show_progress_bar=False)
    distances, indices = index.search(np.array(question_embedding), top_k)

    raw_chunks = [document_chunks[i] for i in indices[0]]

    filtered_chunks = [chunk for chunk in raw_chunks if len(chunk.strip()) > 30]

    print("Filtrelenmiş chunklar (30+ karakter):")
    for i, chunk in enumerate(filtered_chunks):
        print(f"{i+1}. Chunk: {repr(chunk)}")

    return filtered_chunks
