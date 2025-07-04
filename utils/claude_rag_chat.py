import requests
import json

def ask_claude_with_context(question: str, context: str, api_key: str) -> str:
    """
    Belirtilen context’e dayanarak Claude’dan yanıt alır.

    Args:
        question (str): Kullanıcının sorusu.
        context (str): İlgili metin parçalarının birleşimi.
        api_key (str): Geçerli Anthropic API anahtarı.

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
    #kullanıcı sorusunu ve bağlamı içeren mesaj yapısı
    messages = [
        {
            "role": "user",
            "content": f"""
Soru metninin dilini tespit edin ve **yalnızca** size verilen bağlama dayanarak yanıt verin. Yanıtınızı, tespit ettiğiniz soru diliyle aynı dilde verin ve cevabı çevirmeyin. Eğer cevap bağlamda bulunmuyorsa, tespit ettiğiniz dilde "Bu bilgiyi belgede bulamadım." şeklinde yanıtlayın.

Bağlam:
------------------
{context}
------------------

Soru: {question}
"""
        }
    ]
    #claude ve parametreler
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

        if "content" in result and isinstance(result["content"], list):
            texts = [c.get("text", "") for c in result["content"] if c.get("type") == "text"]
            full_answer = "\n".join(texts).strip()
            return full_answer if full_answer else "Claude'dan metin içeren bir yanıt alınamadı."
        
        return f"Claude'dan içerik alınamadı veya beklenmeyen format: {result}"

    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP Hatası: {http_err}"
        if http_err.response is not None:
            try:
                error_details = http_err.response.json()
                api_error_detail = error_details.get('error', {}).get('message', 'Detay yok.')
                error_message += f"\nAPI Detayları: {api_error_detail}"
            except json.JSONDecodeError:
                error_message += f"\nYanıt Metni: {http_err.response.text}"
        return error_message
    except requests.exceptions.ConnectionError as conn_err:
        return f"Bağlantı Hatası: Claude API'ye bağlanılamadı. İnternet bağlantınızı veya API endpoint'ini kontrol edin. Detay: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Zaman Aşımı Hatası: Claude API yanıt vermesi çok uzun sürdü. ({timeout_err})."
    except json.JSONDecodeError as json_err:
        return f"JSON Ayrıştırma Hatası: Claude API'den gelen yanıt JSON formatında değil. Detay: {json_err}"
    except requests.exceptions.RequestException as e:
        return f"Genel İstek Hatası: {e}"
    except Exception as e:
        return f"Beklenmedik Hata Oluştu: {e}"