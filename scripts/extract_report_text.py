#!/usr/bin/env python3
"""Extract PDF text into page-marked Markdown for report lookup."""

from __future__ import annotations

import sys
from pathlib import Path


def extract_with_fitz(pdf_path: Path) -> list[str]:
    import fitz  # type: ignore

    doc = fitz.open(str(pdf_path))
    return [doc.load_page(i).get_text("text") or "" for i in range(doc.page_count)]


def extract_with_pypdf(pdf_path: Path) -> list[str]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return pages


def extract_pages(pdf_path: Path) -> list[str]:
    try:
        return extract_with_fitz(pdf_path)
    except Exception:
        return extract_with_pypdf(pdf_path)


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: extract_report_text.py <report.pdf> [output.md]", file=sys.stderr)
        return 2

    pdf_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else pdf_path.with_suffix(".text.md")

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    pages = extract_pages(pdf_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(f"# Extracted Text: {pdf_path.name}\n\n")
        for index, text in enumerate(pages, start=1):
            f.write(f"<!-- page: {index} -->\n\n")
            f.write(f"## Page {index}\n\n")
            f.write(text.strip())
            f.write("\n\n")

    print(f"Wrote {len(pages)} pages to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
