
from unittest.mock import patch

import pytest

from src.answer_generator import check_evidence


def test_evidence_supported():
    with patch("src.answer_generator.ollama.chat") as mock_chat:
        mock_chat.return_value = {
            "message": {"content": "YES"}
        }

        result = check_evidence(
            "What language extracts PDF text?",
            "The project uses Python to extract PDF text."
        )

    assert result is True


def test_evidence_not_supported():
    with patch("src.answer_generator.ollama.chat") as mock_chat:
        mock_chat.return_value = {
            "message": {"content": "NO"}
        }

        result = check_evidence(
            "Which database does the project use?",
            "The project uses Python to extract PDF text."
        )

    assert result is False


def test_unclear_evidence_response():
    with patch("src.answer_generator.ollama.chat") as mock_chat:
        mock_chat.return_value = {
            "message": {"content": "MAYBE"}
        }

        with pytest.raises(ValueError):
            check_evidence(
                "Which database does the project use?",
                "The project uses Python to extract PDF text."
            )
from unittest.mock import patch

from src.answer_generator import generate_answer


def test_generate_answer_when_evidence_is_supported():
    search_results = [
        {
            "chunk": "Python extracts text from PDF files.",
            "page": 1,
            "score": 0.8
        }
    ]

    with patch(
        "src.answer_generator.check_evidence",
        return_value=True
    ), patch(
        "src.answer_generator.ollama.chat"
    ) as mock_chat:

        mock_chat.return_value = {
            "message": {
                "content": "Python extracts text from PDF files. [Page 1]"
            }
        }

        answer = generate_answer(
            "What extracts text from PDF files?",
            search_results
        )

    assert "Python" in answer
    mock_chat.assert_called_once()


def test_generate_answer_when_evidence_is_missing():
    search_results = [
        {
            "chunk": "Python extracts text from PDF files.",
            "page": 1,
            "score": 0.8
        }
    ]

    with patch(
        "src.answer_generator.check_evidence",
        return_value=False
    ), patch(
        "src.answer_generator.ollama.chat"
    ) as mock_chat:

        answer = generate_answer(
            "Which database does the project use?",
            search_results
        )

    assert answer == (
        "I could not find the answer in the provided document."
    )
    mock_chat.assert_not_called()


def test_generate_answer_when_evidence_check_fails():
    search_results = [
        {
            "chunk": "Python extracts text from PDF files.",
            "page": 1,
            "score": 0.8
        }
    ]

    with patch(
        "src.answer_generator.check_evidence",
        side_effect=RuntimeError("Checker failed")
    ), patch(
        "src.answer_generator.ollama.chat"
    ) as mock_chat:

        answer = generate_answer(
            "Which database does the project use?",
            search_results
        )

    assert answer == (
        "I couldn't verify whether the document supports an answer. "
        "Please try again."
    )
    mock_chat.assert_not_called()

def test_generate_answer_when_answer_generation_fails():
    search_results = [
        {
            "chunk": "Python extracts text from PDF files.",
            "page": 1,
            "score": 0.8
        }
    ]

    with patch(
        "src.answer_generator.check_evidence",
        return_value=True
    ), patch(
        "src.answer_generator.ollama.chat",
        side_effect=RuntimeError("Ollama is unavailable")
    ):
        answer = generate_answer(
            "What extracts text from PDF files?",
            search_results
        )

    assert answer == (
        "I couldn't generate an answer right now. "
        "Please check that Ollama is running and try again."
    )
