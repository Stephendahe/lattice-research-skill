#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from lattice_common import read_csv

def node_id(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_]+", "_", text or "unknown").strip("_")
    return slug or "unknown"

def build(rows):
    lines = ["graph TD"]
    for row in rows:
        a = row.get("variable_A") or "unknown_A"
        b = row.get("variable_B") or "unknown_B"
        label = row.get("relation_type") or row.get("relation_form") or "relation"
        lines.append(f'  {node_id(a)}["{a}"] -->|"{label}"| {node_id(b)}["{b}"]')
    return "\n".join(lines) + "\n"

def main():
    p = argparse.ArgumentParser(description="Build Mermaid variable network from variable_relations.csv.")
    p.add_argument("variable_relations_csv")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    Path(args.output).write_text(build(read_csv(Path(args.variable_relations_csv))), encoding="utf-8")

if __name__ == "__main__":
    main()
