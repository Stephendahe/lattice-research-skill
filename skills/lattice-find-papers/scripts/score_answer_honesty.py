#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import PSEUDO_GAP_PHRASES, save_json

def score_text(text):
    score = 100
    failed = []
    if any(p in text for p in PSEUDO_GAP_PHRASES):
        score -= 15
        failed.append("pseudo_gap_as_gap")
    if "摘要" in text and any(w in text for w in ["证明", "证实"]):
        score -= 20
        failed.append("abstract_as_full_text")
    if "相关" in text and any(w in text for w in ["导致", "因果"]):
        score -= 20
        failed.append("correlation_as_causation")
    if any(w in text for w in ["编造 DOI", "doi:10.0000/fake"]):
        score -= 30
        failed.append("fabricated_identifier")
    if "材料不足" in text or "需要全文" in text or "无法继续" in text:
        score += 10
    if "Request 文献目录" in text:
        score += 10
    if "证据边界" in text:
        score += 10
    return {"honesty_score": max(0, min(100, score)), "failed_checks": failed}

def main():
    p = argparse.ArgumentParser(description="Score final_report.md for honesty and evidence-bound output.")
    p.add_argument("final_report_md")
    p.add_argument("--output-json")
    args = p.parse_args()
    result = score_text(Path(args.final_report_md).read_text(encoding="utf-8"))
    if args.output_json:
        save_json(Path(args.output_json), result)
    print(f"honesty_score: {result['honesty_score']}")
    raise SystemExit(1 if result["honesty_score"] < 70 else 0)

if __name__ == "__main__":
    main()
