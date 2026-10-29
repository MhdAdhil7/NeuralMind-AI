
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.semantic_search import search_chunks

from src.semantic_search import prepare_pdf_chunks


def test_search_finds_relevant_chunk():
    chunks = [
        "Artificial intelligence helps computers understand information.",
        "The weather is sunny and warm today.",
        "Machine learning allows computers to learn patterns from data."
    ]

    results = search_chunks(
        "How do computers learn?",
        chunks,
        top_k=2
    )

    assert len(results) == 2

    retrieved_text = " ".join(
        result["chunk"] for result in results
    )

    assert (
        "learn patterns" in retrieved_text
        or "understand information" in retrieved_text
    )

    print("\nSearch results:")

    for result in results:
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk: {result['chunk']}\n")


def test_prepare_pdf_chunks():
    project_root = Path(__file__).resolve().parents[1]
    pdf_path = project_root / "data" / "sample.pdf"

    chunks = prepare_pdf_chunks(str(pdf_path))

    assert chunks, "No chunks were created from the PDF"
    assert all(chunk.strip() for chunk in chunks)

    print("\nPDF chunks:")
    for chunk in chunks:
        print(chunk)

    print("\nPDF processing test passed!")
if __name__ == "__main__":
    test_search_finds_relevant_chunk()
    test_prepare_pdf_chunks()
    print("All semantic search tests passed!")