import requests

def ask_claude(question, chunks, api_key):
    """
    Claude ile soru-cevap yapar.
    
    Args:
        question (str): Kullanıcının sorusu.
        chunks (list): Belgeden alınmış metin parçaları.
        api_key (str): Geçerli Anthropic API anahtarı.
    
    Returns:
        str: Claude'dan gelen yanıt veya hata mesajı.
    """
    if not api_key:
        return "Claude API anahtarı bulunamadı. Lütfen geçerli bir API key girin."

    if chunks is None:
        chunks = []
        
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    # İlk 3 parçayı bağlayarak bağlam oluştur
    context_text = "\n\n".join(chunks[:3])
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion:\n{question}"
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "content" in result and isinstance(result["content"], list):
            texts = [c.get("text", "") for c in result["content"] if c.get("type") == "text"]
            full_answer = "\n".join(texts).strip()
            return full_answer or "Claude'dan metin içeren bir yanıt alınamadı."

        return f"Claude beklenmeyen formatta cevap verdi:\n{result}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Hatası: {http_err}\nDetay: {response.text}"
    except Exception as e:
        return f"Claude bağlantı hatası: {e}"

