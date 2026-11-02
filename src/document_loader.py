import io
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from google import genai
from PIL import Image
import pymupdf
from pypdf import PdfReader


_client: Optional[genai.Client] = None


def get_genai_client() -> Optional[genai.Client]:
    """
    Lazily initialize and return the google-genai Client using GEMINI_API_KEY from src.config.
    """
    global _client
    if _client is None:
        try:
            from src.config import GEMINI_API_KEY
            if GEMINI_API_KEY:
                _client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception:
            _client = None
    return _client


def render_pdf_page_with_pymupdf(
    pdf_source: Union[str, Path, Any],
    page_index: int,
    dpi: int = 150
) -> Optional[Image.Image]:
    """
    Render a specific PDF page (0-based page_index) into a high-resolution PIL Image using PyMuPDF.
    Uses ~150 DPI for balanced image quality and size.
    """
    doc = None
    try:
        if isinstance(pdf_source, (str, Path)):
            doc = pymupdf.open(str(pdf_source))
        elif hasattr(pdf_source, "getvalue"):
            doc = pymupdf.open(stream=pdf_source.getvalue(), filetype="pdf")
        elif hasattr(pdf_source, "read"):
            if hasattr(pdf_source, "seek"):
                pdf_source.seek(0)
            data = pdf_source.read()
            if hasattr(pdf_source, "seek"):
                pdf_source.seek(0)
            doc = pymupdf.open(stream=data, filetype="pdf")
        else:
            doc = pymupdf.open(pdf_source)

        if doc is None or page_index < 0 or page_index >= len(doc):
            return None

        page = doc[page_index]
        pix = page.get_pixmap(dpi=dpi)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        return img
    except Exception:
        return None
    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass


def transcribe_page_image(image: Optional[Image.Image], model: str = "gemini-2.5-flash") -> str:
    """
    Send a rendered PDF page image to Gemini Vision for OCR transcription.
    Accurately handles printed and handwritten text while avoiding hallucinations.
    """
    if image is None:
        return ""

    client = get_genai_client()
    if client is None:
        return ""

    prompt = (
        "You are an expert OCR engine. Accurately transcribe all readable printed and handwritten text from this page image.\n"
        "Rules:\n"
        "- Accurately transcribe readable text, preserving meaningful structure and line breaks where possible.\n"
        "- Handle both printed and handwritten text.\n"
        "- Return ONLY the transcribed text content.\n"
        "- Avoid inventing, hallucinating, or guessing unreadable content.\n"
        "- If nothing readable exists or the page is blank, return an empty string."
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=[image, prompt],
        )
        return (response.text or "").strip()
    except Exception:
        return ""


def load_pdf(
    pdf_source: Union[str, Path, Any],
    ocr_threshold: int = 50,
    dpi: int = 150,
    **kwargs: Any
) -> List[Dict[str, Any]]:
    """
    Process every page of a PDF separately using pypdf for text extraction,
    with PyMuPDF page rendering and Gemini Vision OCR fallback for scanned/low-text pages.

    Returns page-level document records:
        - source: PDF filename
        - page: 1-based page number
        - text: extracted page text (or OCR transcribed text)
        - needs_ocr: True if page required OCR, else False
        - extraction_method: "text" or "vision_ocr"
    """
    threshold = kwargs.get("min_text_length", ocr_threshold)

    if isinstance(pdf_source, (str, Path)):
        source_path = Path(pdf_source)
        source_name = source_path.name
        reader = PdfReader(str(source_path))
    else:
        source_name = Path(getattr(pdf_source, "name", "document.pdf")).name
        reader = PdfReader(pdf_source)

    documents = []

    for page_num, page in enumerate(reader.pages, start=1):
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""

        needs_ocr = len(page_text.strip()) < threshold

        if needs_ocr:
            ocr_text = ""
            try:
                page_img = render_pdf_page_with_pymupdf(
                    pdf_source=pdf_source,
                    page_index=page_num - 1,
                    dpi=dpi
                )
                if page_img is not None:
                    ocr_text = transcribe_page_image(page_img)
            except Exception:
                ocr_text = ""

            documents.append({
                "source": source_name,
                "page": page_num,
                "text": ocr_text,
                "needs_ocr": True,
                "extraction_method": "vision_ocr",
            })
        else:
            documents.append({
                "source": source_name,
                "page": page_num,
                "text": page_text,
                "needs_ocr": False,
                "extraction_method": "text",
            })

    return documents


load_document = load_pdf


def load_documents(
    folder_path: Union[str, Path] = "data/documents",
    ocr_threshold: int = 50,
    dpi: int = 150,
    **kwargs: Any
) -> List[Dict[str, Any]]:
    """
    Load PDF documents from a folder (or a single PDF file) and return page-level records.
    """
    path = Path(folder_path)
    documents = []

    if not path.exists():
        return documents

    if path.is_file():
        if path.suffix.lower() == ".pdf":
            return load_pdf(path, ocr_threshold=ocr_threshold, dpi=dpi, **kwargs)
        return documents

    for pdf_file in sorted(path.glob("*.pdf")):
        documents.extend(load_pdf(pdf_file, ocr_threshold=ocr_threshold, dpi=dpi, **kwargs))

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks with specified overlap.
    """
    if not text:
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += step

    return chunks