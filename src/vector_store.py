
import hashlib

import chromadb
from sentence_transformers import SentenceTransformer


# Create a database that saves data on your computer.
client = chromadb.PersistentClient(
    path="data/chroma_db"
)

# Create or reuse a collection for document chunks.
collection = client.get_or_create_collection(
    name="neuralmind_documents",
    metadata={"hnsw:space": "cosine"}
)

# Load the model that converts text into numerical embeddings.
model = SentenceTransformer("all-MiniLM-L6-v2")


def store_chunks(chunks, document_name="uploaded_pdf"):
    """Store text chunks and their page numbers in ChromaDB.

    Each chunk can be either:
    - A dictionary containing 'text' and 'page'
    - A plain string, for backward compatibility
    """

    if not chunks:
        raise ValueError("Cannot store an empty list of chunks.")

    documents = []
    metadatas = []

    for chunk in chunks:
        if isinstance(chunk, dict):
            text = chunk["text"]
            page = int(chunk["page"])
        else:
            text = chunk
            page = 0

        documents.append(text)
        metadatas.append({
            "document_name": document_name,
            "page": page
        })

    # Create unique IDs for this document's content.
    content_hash = hashlib.sha256(
        "\n".join(documents).encode("utf-8")
    ).hexdigest()[:12]

    ids = [
        f"{document_name}_{content_hash}_{i}"
        for i in range(len(documents))
    ]

    # Convert the text into numerical embeddings.
    embeddings = model.encode(documents).tolist()

    # Remove old chunks for this filename before storing
    # the latest version, so stale chunks are not retained.
    collection.delete(
        where={"document_name": document_name}
    )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(documents)


def search_stored_chunks(query, document_name, top_k=3):
    """Find relevant chunks and return their page numbers."""

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if not document_name:
        raise ValueError("Document name cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    # Count the chunks belonging to this document.
    matching_documents = collection.get(
        where={"document_name": document_name},
        include=[]
    )

    matching_count = len(matching_documents["ids"])

    if matching_count == 0:
        return []

    # Convert the question into an embedding.
    query_embedding = model.encode(query).tolist()

    # Retrieve only chunks from the selected document.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, matching_count),
        where={"document_name": document_name},
        include=["documents", "distances", "metadatas"]
    )

    matches = []

    retrieved_documents = results["documents"][0]
    retrieved_distances = results["distances"][0]
    retrieved_metadatas = results["metadatas"][0]

    for i, chunk in enumerate(retrieved_documents):
        metadata = retrieved_metadatas[i] or {}

        matches.append({
            "chunk": chunk,
            "page": metadata.get("page", 0),
            "score": 1 - retrieved_distances[i]
        })

    return matches
