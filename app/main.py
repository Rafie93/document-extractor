from fastapi import FastAPI, Header, HTTPException
import tempfile, requests
from app.config import API_KEY, MAX_CHUNK_SIZE
from app.extractor.pdf import extract_pdf
from app.extractor.excel import extract_excel
from app.chunker.basic import chunk_text
from app.ollama_client import chat_with_ollama, chat_with_gemini

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/extract")
def extract(payload: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(403)

    file_url = payload["file_url"]
    doc_id = payload["document_id"]
    file_type = payload["file_type"]

    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(requests.get(file_url).content)

    raw_pages = []
    if file_type == "pdf":
        raw_pages = extract_pdf(tmp.name)
    elif file_type == "excel":
        raw_pages = extract_excel(tmp.name)

    chunks = []
    for page, text in raw_pages:
        for c in chunk_text(text, MAX_CHUNK_SIZE):
            chunks.append({
                "page": page,
                "content": c
            })

    return {
        "document_id": doc_id,
        "chunks": chunks
    }

@app.post("/chat-gemini")
def chat_gemini(payload: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(403)

    question = payload.get("question")
    chunks_raw = payload.get("chunks")  # list of text
    chunks = []
    if chunks_raw:
        for c in chunks_raw:
            if isinstance(c, dict) and "content" in c:
                chunks.append(c["content"])
    answer = chat_with_gemini(question, chunks)

    return {
        "answer": answer
    }

@app.post("/chat")
def chat(payload: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(403)

    question = payload.get("question")
    chunks = payload.get("chunks")  # list of text

    if not question or not chunks:
        raise HTTPException(400, "Invalid payload")

    context = "\n\n".join(chunks[:5])  # LIMIT konteks (WAJIB)

    answer = chat_with_ollama(question, context)

    return {
        "answer": answer
    }