import pdfplumber
import fitz  # pymupdf
import tempfile
from .image import ocr_image

def extract_pdf(file_path: str):
    results = []

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""

            if text.strip():
                results.append((i + 1, text))
            else:
                # OCR fallback
                with fitz.open(file_path) as doc:
                    pix = doc.load_page(i).get_pixmap()
                    tmp = tempfile.NamedTemporaryFile(suffix=".png")
                    pix.save(tmp.name)
                    ocr_text = ocr_image(tmp.name)
                    results.append((i + 1, ocr_text))

    return results
