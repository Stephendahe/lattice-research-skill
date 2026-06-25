#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import CSV_HEADERS, read_csv, write_csv

def split_items(text):
    return [x.strip() for x in (text or "").replace(";", ",").replace("；", ",").split(",") if x.strip()]

def audit(rows):
    out = []
    for row in rows:
        missing = split_items(row.get("unreported_variables")) + split_items(row.get("uncontrolled_variables"))
        for item in missing:
            idx = len(out) + 1
            severity = "conclusion_threat" if row.get("severity") == "conclusion_threat" or row.get("core_variable_match") else "medium"
            out.append({"blocker_id": f"B{idx:03d}", "paper_id": row.get("paper_id", ""), "missing_item": item, "blocker_level": "变量/流程", "why_it_blocks_comparison": "该项未报告或未控制，无法判断不同文献条件是否一致。", "is_core_variable": "true" if row.get("core_variable_match") else "unclear", "related_variable": item, "affected_observable": "", "severity": severity, "possible_resolution": "请求全文/补充材料或降级比较结论。", "note": row.get("reviewer_note", "")})
    return out

def main():
    p = argparse.ArgumentParser(description="Generate normalization blockers from experiment audit rows.")
    p.add_argument("experiment_pipeline_audit_csv")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    rows = audit(read_csv(Path(args.experiment_pipeline_audit_csv)))
    write_csv(Path(args.output), CSV_HEADERS["normalization_blockers.csv"], rows)
    print(f"blockers: {len(rows)}")

if __name__ == "__main__":
    main()
