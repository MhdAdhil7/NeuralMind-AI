
import pymupdf


def extract_pages_from_pdf(pdf_path):
    """Extract text from a PDF while preserving page numbers."""

    try:
        pages = []

        with pymupdf.open(pdf_path) as document:
            for page_number, page in enumerate(document, start=1):
                page_text = page.get_text().strip()

                if page_text:
                    pages.append({
                        "page": page_number,
                        "text": page_text
                    })

        return pages

    except FileNotFoundError:
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )


def extract_text_from_pdf(pdf_path):
    """Extract and combine text from every PDF page."""

    pages = extract_pages_from_pdf(pdf_path)

    return "\n\n".join(
        page["text"] for page in pages
    )
