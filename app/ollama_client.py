import requests
from app.config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_API_KEY

def chat_with_gemini(question: str, contexts: list[str]) -> str:
    # safety: pastikan contexts list of str
    contexts = [str(c) for c in contexts if c]

    prompt = f"""
Kamu adalah asisten analisis dokumen akreditasi.
Gunakan konteks berikut untuk menjawab pertanyaan secara faktual.
Jika informasi tidak ada di konteks, jawab: "Data tidak ditemukan di dokumen".

KONTEKS:
{chr(10).join(contexts)}

PERTANYAAN:
{question}
"""
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}"
        },
    )

    return res.json()["response"]
    
def chat_with_ollama(question: str, context: str) -> str:
    prompt = f"""
Gunakan konteks berikut untuk menjawab pertanyaan.
Jika jawaban tidak ada di konteks, jawab: "Tidak ditemukan dalam dokumen".

KONTEKS:
{context}

PERTANYAAN:
{question}

JAWABAN:
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]
