#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from lattice_common import COMMON_ENGLISH_ALLOWED

TOKEN_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9'-]{1,}\b")
PAREN_RE = re.compile(r"[（(]([^）)]+)[）)]")

def strip_code_and_urls(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    return text

def defined_terms(text: str) -> set[str]:
    terms = set(COMMON_ENGLISH_ALLOWED)
    for match in PAREN_RE.finditer(text):
        for token in TOKEN_RE.findall(match.group(1)):
            terms.add(token)
    return terms

def find_undefined_english(text: str, allow: set[str] | None = None) -> list[str]:
    cleaned = strip_code_and_urls(text)
    terms = defined_terms(cleaned) | (allow or set())
    outside = PAREN_RE.sub(" ", cleaned)
    hits = []
    for token in TOKEN_RE.findall(outside):
        if token not in terms and token.upper() not in terms and not token.isupper():
            hits.append(token)
    return sorted(set(hits))

def main():
    p = argparse.ArgumentParser(description="Check visible Chinese Markdown for undefined English terms.")
    p.add_argument("markdown_path")
    p.add_argument("--allow", action="append", default=[], help="Additional allowed English token.")
    args = p.parse_args()
    text = Path(args.markdown_path).read_text(encoding="utf-8")
    hits = find_undefined_english(text, set(args.allow))
    if hits:
        print("undefined English terms: " + ", ".join(hits))
        raise SystemExit(1)
    print("terms ok")

if __name__ == "__main__":
    main()
