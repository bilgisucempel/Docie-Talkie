import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLAUDE_API_KEY = os.getenv("docietalkiekey")

def ask_claude(question, chunks):
    if not CLAUDE_API_KEY:
        return "Claude API anahtarı bulunamadı. Lütfen .env dosyasına CLAUDE_API_KEY ekleyin."

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

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
            return full_answer if full_answer else "Claude'dan metin içeren bir yanıt alınamadı."

        return f"Claude beklenmeyen formatta cevap verdi:\n{result}"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Hatası: {http_err}\nDetay: {response.text}"

    except Exception as e:
        return f"Claude bağlantı hatası: {e}"
