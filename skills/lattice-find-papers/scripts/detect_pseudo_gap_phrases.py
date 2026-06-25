#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import CSV_HEADERS, PSEUDO_GAP_PHRASES, write_csv

def detect(text):
    hits = []
    for phrase in PSEUDO_GAP_PHRASES:
        if phrase in text:
            hits.append({"gap_id": f"G{len(hits)+1:03d}", "phrase": phrase, "source_location": "text", "why_risky": "可能把工具性或空泛表述误写成研究空白。", "rewrite_action": "先检查证据、变量、流程、尺度和具体 blocker。", "severity": "medium", "notes": ""})
    return hits

def main():
    p = argparse.ArgumentParser(description="Detect pseudo research-gap phrases in Markdown/text.")
    p.add_argument("text_path")
    p.add_argument("--output-csv")
    args = p.parse_args()
    text = Path(args.text_path).read_text(encoding="utf-8")
    hits = detect(text)
    if args.output_csv:
        write_csv(Path(args.output_csv), CSV_HEADERS["pseudo_gap_hits.csv"], hits)
    for hit in hits:
        print(f"{hit['gap_id']}: {hit['phrase']}")
    raise SystemExit(1 if hits else 0)

if __name__ == "__main__":
    main()
