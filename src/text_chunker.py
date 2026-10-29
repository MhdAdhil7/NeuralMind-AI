
def chunk_text(text, chunk_size=100, overlap=20):
    """Split text into chunks while avoiding tiny leftover chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    paragraphs = [
        paragraph.split()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current = []

    for words in paragraphs:
        # Keep short paragraphs together when possible.
        if len(words) <= chunk_size:
            if current and len(current) + len(words) > chunk_size:
                chunks.append(" ".join(current))
                current = []

            current.extend(words)
            continue

        if current:
            chunks.append(" ".join(current))
            current = []

        # Calculate how far each new chunk advances.
        step = chunk_size - overlap
        count = (len(words) + step - 1) // step

        if overlap == 0:
            remainder = len(words) % chunk_size

            # Rebalance when the final chunk would be very small.
            if count > 1 and 0 < remainder < chunk_size // 2:
                base, extra = divmod(len(words), count)
                sizes = [
                    base + (1 if i < extra else 0)
                    for i in range(count)
                ]
            else:
                sizes = [chunk_size] * (count - 1)
                sizes.append(remainder or chunk_size)
        else:
            # Balance chunks so overlap doesn't exceed the limit.
            base, extra = divmod(len(words), count)
            sizes = [
                base + (1 if i < extra else 0)
                for i in range(count)
            ]

        start = 0

        for size in sizes:
            end = start + size
            chunk_start = max(0, start - overlap)

            chunks.append(" ".join(words[chunk_start:end]))
            start = end

    if current:
        chunks.append(" ".join(current))

    return chunks


def chunk_pages(pages, chunk_size=100, overlap=20):
    """Split PDF pages into chunks while preserving page numbers."""

    page_chunks = []

    for page in pages:
        chunks = chunk_text(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk in chunks:
            page_chunks.append({
                "page": page["page"],
                "text": chunk
            })

    return page_chunks
