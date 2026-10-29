
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from src.pdf_reader import extract_text_from_pdf
from src.text_chunker import chunk_text


# Load the model used to understand the meaning of text.
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_chunks(query, chunks, top_k=3):
    """Find the text chunks most relevant to a question."""

    # Check that the user entered a question.
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    # If there is no text to search, return an empty list.
    if not chunks:
        return []

    # Convert the document chunks and question into embeddings.
    chunk_embeddings = model.encode(
        chunks,
        convert_to_tensor=True
    )

    query_embedding = model.encode(
        query,
        convert_to_tensor=True
    )

    # Compare the meaning of the question with each chunk.
    scores = cos_sim(
        query_embedding,
        chunk_embeddings
    )[0]

    # Select the chunks with the highest similarity scores.
    ranked_indices = scores.argsort(descending=True)[:top_k]

    results = []

    for index in ranked_indices:
        index = int(index)

        results.append({
            "chunk": chunks[index],
            "score": float(scores[index])
        })

    # Return the ranked search results.
    return results


def prepare_pdf_chunks(pdf_path, chunk_size=100, overlap=20):
    """Extract text from a PDF and split it into chunks."""

    # Extract text from the PDF.
    text = extract_text_from_pdf(pdf_path)

    # Divide the extracted text into smaller pieces.
    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    return chunks
