
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.text_chunker import chunk_text


def test_empty_text():
    assert chunk_text("   \n\n   ") == []


def test_invalid_chunk_size():
    try:
        chunk_text("hello world", chunk_size=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid chunk size should raise ValueError")


def test_invalid_overlap():
    try:
        chunk_text("hello world", chunk_size=10, overlap=10)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid overlap should raise ValueError")


def test_short_paragraphs_stay_together():
    text = "First paragraph.\n\nSecond paragraph."
    chunks = chunk_text(text, chunk_size=10, overlap=2)

    assert len(chunks) == 1
    assert "First paragraph." in chunks[0]
    assert "Second paragraph." in chunks[0]


def test_maximum_chunk_size():
    text = " ".join(f"word{i}" for i in range(25))
    chunks = chunk_text(text, chunk_size=10, overlap=2)

    assert all(len(chunk.split()) <= 10 for chunk in chunks)


def test_twelve_word_paragraph_is_balanced():
    text = " ".join(f"word{i}" for i in range(12))
    chunks = chunk_text(text, chunk_size=10, overlap=0)

    assert [len(chunk.split()) for chunk in chunks] == [6, 6]


def test_eighteen_word_paragraph():
    text = " ".join(f"word{i}" for i in range(18))
    chunks = chunk_text(text, chunk_size=10, overlap=0)

    assert [len(chunk.split()) for chunk in chunks] == [10, 8]


def test_chunk_overlap():
    text = " ".join(f"word{i}" for i in range(15))
    chunks = chunk_text(text, chunk_size=10, overlap=2)

    first_words = chunks[0].split()
    second_words = chunks[1].split()

    assert first_words[-2:] == second_words[:2]


if __name__ == "__main__":
    test_empty_text()
    test_invalid_chunk_size()
    test_invalid_overlap()
    test_short_paragraphs_stay_together()
    test_maximum_chunk_size()
    test_twelve_word_paragraph_is_balanced()
    test_eighteen_word_paragraph()
    test_chunk_overlap()

    print("All chunker tests passed!")
