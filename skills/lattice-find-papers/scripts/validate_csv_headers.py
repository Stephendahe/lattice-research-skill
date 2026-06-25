#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from lattice_common import CSV_HEADERS

ALIASES = {
    "citation_audit_template.csv": "citation_audit.csv",
    "evidence_spans_template.csv": "evidence_spans.csv",
    "experiment_pipeline_audit_template.csv": "experiment_pipeline_audit.csv",
    "paper_master_template.csv": "papers_master.csv",
    "search_coverage_audit_template.csv": "search_coverage_audit.csv",
    "full_text_availability_template.csv": "full_text_availability.csv",
    "full_text_requests_template.csv": "full_text_requests.csv",
    "mechanism_comparison_template.csv": "mechanism_comparison.csv",
    "variable_relation_template.csv": "variable_relations.csv",
    "mechanism_conflict_template.csv": "mechanism_conflicts.csv",
    "normalization_blockers_template.csv": "normalization_blockers.csv",
}

def validate(path: Path, expected_name: str | None = None, expected: list[str] | None = None) -> tuple[bool, str]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        header = next(csv.reader(f), [])
    key = expected_name or path.name
    key = ALIASES.get(key, key)
    exp = expected or CSV_HEADERS.get(key)
    if not exp:
        return False, f"unknown template for {path.name}; pass --expected"
    if header != exp:
        return False, "header mismatch\nexpected: " + ",".join(exp) + "\nactual:   " + ",".join(header)
    return True, "header ok"

def main():
    p = argparse.ArgumentParser(description="Validate a CSV file header against Lattice Find Papers templates.")
    p.add_argument("csv_path")
    p.add_argument("--template", help="Template/basename to compare against.")
    p.add_argument("--expected", help="Comma-separated expected header.")
    args = p.parse_args()
    expected = args.expected.split(",") if args.expected else None
    ok, msg = validate(Path(args.csv_path), args.template, expected)
    print(msg)
    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
