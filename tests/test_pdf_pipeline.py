
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pdf_reader import extract_text_from_pdf
from src.text_chunker import chunk_text


def test_pdf_to_chunks():
    # Locate our sample PDF.
    project_root = Path(__file__).resolve().parents[1]
    pdf_path = project_root / "data" / "sample.pdf"

    # Step 1: Extract text from the PDF.
    text = extract_text_from_pdf(str(pdf_path))

    assert text.strip(), "PDF extraction returned no text"

    # Step 2: Split the extracted text into chunks.
    chunks = chunk_text(text, chunk_size=20, overlap=5)

    assert chunks, "Chunking returned no chunks"
    assert all(chunk.strip() for chunk in chunks), "An empty chunk was created"

    print(f"Extracted characters: {len(text)}")
    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {index}: {chunk}")
        print(f"Word count: {len(chunk.split())}")


if __name__ == "__main__":
    test_pdf_to_chunks()
    print("\nPDF pipeline test passed!")
