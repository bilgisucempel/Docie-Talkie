import requests

def ask_claude_with_context(question, context, api_key):
    """
    Belirtilen context’e dayanarak Claude’dan yanıt alır.
    
    Args:
        question (str): Kullanıcının sorusu.
        context  (str): İlgili metin parçalarının birleşimi.
        api_key  (str): Geçerli Anthropic API anahtarı.
    
    Returns:
        str: Claude'ın yanıtı veya hata mesajı.
    """
    if not api_key:
        return "Claude API anahtarı bulunamadı. Lütfen geçerli bir API key girin."

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    messages = [
        {
            "role": "user",
            "content": f"""
Based **only** on the context below, answer the question.  
If the answer is not in the context, say "I could not find that information in the document."

Context:
--------------------
{context}
--------------------

Question: {question}
"""
        }
    ]

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "temperature": 0.7,
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        # Claude'dan gelen yanıtın içeriğini kontrol et
        if "content" in result and isinstance(result["content"], list):
            return "\n".join(p.get("text", "") for p in result["content"] if p.get("type") == "text").strip()

        return "Claude'dan içerik alınamadı."

    except requests.exceptions.RequestException as e:
        details = getattr(e.response, "text", str(e))
        return f"Claude bağlantı hatası: {e}\nDetay: {details}"
