def chunk_text(text: str, max_size=500):
    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) > max_size:
            chunks.append(current.strip())
            current = ""
        current += line + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks
