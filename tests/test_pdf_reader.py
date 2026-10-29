from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pdf_reader import extract_text_from_pdf

pdf_path = Path(__file__).resolve().parents[1] / "data" / "sample.pdf"

try:
    text = extract_text_from_pdf(str(pdf_path))
    print(text)
except FileNotFoundError as e:
    print(e)