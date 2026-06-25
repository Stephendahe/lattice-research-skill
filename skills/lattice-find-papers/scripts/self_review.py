#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import PSEUDO_GAP_PHRASES, save_json

def review(text: str, has_requests: bool = False):
    failed = []
    downgraded = []
    removed = []
    if any(p in text for p in PSEUDO_GAP_PHRASES):
        failed.append("pseudo_gap_phrase")
        downgraded.append("将空泛 gap 降级为待验证 blocker。")
    if "摘要" in text and any(w in text for w in ["证明", "证实", "实验流程"]):
        failed.append("abstract_overclaim")
    if "缺少全文" in text and "实验流程审计" in text and "无法" not in text:
        failed.append("experiment_audit_without_full_text")
    if "不确定项" not in text and "材料不足" not in text:
        failed.append("missing_uncertainty_section")
    score = max(0, 100 - 15 * len(failed))
    if has_requests:
        score = min(100, score + 10)
    final_status = "partial_due_to_missing_full_text" if has_requests else ("failed_validation" if failed else "complete_with_full_text")
    return {"honesty_score": score, "failed_checks": failed, "downgraded_claims": downgraded, "unsupported_claims_removed": removed, "requests_generated": ["request_literature_list.md"] if has_requests else [], "resume_required": has_requests, "final_status": final_status}

def main():
    p = argparse.ArgumentParser(description="Self-review a final report for Lattice Find Papers rules.")
    p.add_argument("final_report_md")
    p.add_argument("--request-md", default="")
    p.add_argument("--output-json", required=True)
    args = p.parse_args()
    text = Path(args.final_report_md).read_text(encoding="utf-8")
    has_requests = bool(args.request_md and Path(args.request_md).exists() and "| R" in Path(args.request_md).read_text(encoding="utf-8"))
    result = review(text, has_requests)
    save_json(Path(args.output_json), result)
    print(f"honesty_score: {result['honesty_score']}")
    raise SystemExit(1 if result["failed_checks"] else 0)

if __name__ == "__main__":
    main()
