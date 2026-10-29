
from pathlib import Path
import sys

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.vector_store import store_chunks, search_stored_chunks


def test_vector_store():
    chunks = [
        "Artificial intelligence helps computers perform tasks.",
        "Machine learning allows computers to learn from data.",
        "The weather is sunny and warm today."
    ]

    # Store the test chunks in ChromaDB.
    stored_count = store_chunks(
        chunks,
        document_name="vector_store_test"
    )

    assert stored_count == 3

    print(f"\nStored {stored_count} chunks successfully.")

    # Search for information about learning from data.
    results = search_stored_chunks(
        "How do computers learn?",
        document_name="vector_store_test",
        top_k=2
    )

    assert len(results) == 2

    print("\nSearch results:")

    for result in results:
        print(f"Score: {result['score']:.4f}")
        print(f"Chunk: {result['chunk']}\n")

    print("Vector store test passed!")


if __name__ == "__main__":
    test_vector_store()
