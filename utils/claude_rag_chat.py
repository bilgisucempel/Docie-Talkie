import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLAUDE_API_KEY = os.getenv("docietalkiekey")

def ask_claude_with_context(question, context):
    if not CLAUDE_API_KEY:
        return "Claude API anahtarı bulunamadı. .env dosyasında 'docietalkiekey' tanımlı mı kontrol et."

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": CLAUDE_API_KEY,
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

        if "content" in result:
            parts = result["content"]
            return "\n".join(p.get("text", "") for p in parts if p.get("type") == "text").strip()

        return "Claude'dan içerik alınamadı."

    except requests.exceptions.RequestException as e:
        return f"Claude bağlantı hatası: {e}\nDetay: {getattr(e.response, 'text', str(e))}"
