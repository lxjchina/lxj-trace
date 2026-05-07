#!/usr/bin/env python3
"""Search report-text.md and print page-numbered snippets."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DEFAULT_REPORT_TEXT = Path(__file__).resolve().parents[1] / "references" / "report-text.md"


def page_for_offset(text: str, offset: int) -> str:
    markers = list(re.finditer(r"<!-- page: (\d+) -->", text[:offset]))
    return markers[-1].group(1) if markers else "unknown"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: search_report.py <query> [report-text.md] [--limit N]", file=sys.stderr)
        return 2

    query = sys.argv[1]
    limit = 20
    args = sys.argv[2:]
    if "--limit" in args:
        index = args.index("--limit")
        try:
            limit = int(args[index + 1])
        except (IndexError, ValueError):
            print("--limit requires an integer", file=sys.stderr)
            return 2
        del args[index : index + 2]

    report_text = Path(args[0]) if args else DEFAULT_REPORT_TEXT
    if not report_text.exists():
        print(f"Report text not found: {report_text}", file=sys.stderr)
        print("Run scripts/extract_report_text.py references/report.pdf references/report-text.md first.", file=sys.stderr)
        return 1

    text = report_text.read_text(encoding="utf-8")
    flags = re.IGNORECASE if query.isascii() else 0
    matches = list(re.finditer(re.escape(query), text, flags))
    if not matches:
        print(f"No matches for: {query}")
        return 0

    for match in matches[:limit]:
        start = max(0, match.start() - 180)
        end = min(len(text), match.end() + 280)
        snippet = " ".join(text[start:end].split())
        print(f"[page {page_for_offset(text, match.start())}] {snippet}")

    if len(matches) > limit:
        print(f"... {len(matches) - limit} more matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
