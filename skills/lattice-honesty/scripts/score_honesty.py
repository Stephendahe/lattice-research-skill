#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PSEUDO_GAP_PHRASES = [
    "多种数据耦合",
    "搭建统一框架",
    "实现数据归一化",
    "一体化平台",
    "更多变量联合分析",
    "文献结论不同",
    "某变量没有被研究",
    "高引用文献没提",
    "数据库建设本身",
    "统一指标本身",
]

def score_text(text: str):
    score = 100
    failed = []

    if any(p in text for p in PSEUDO_GAP_PHRASES):
        score -= 15
        failed.append("pseudo_gap_as_research_gap")
    if "摘要" in text and any(w in text for w in ["证明", "证实", "实验流程审计"]):
        score -= 20
        failed.append("abstract_as_full_text_conclusion")
    if "相关" in text and any(w in text for w in ["导致", "因果", "证明"]):
        score -= 20
        failed.append("correlation_as_causation")
    if any(w in text for w in ["doi:10.0000/fake", "编造 DOI", "假 DOI"]):
        score -= 30
        failed.append("fabricated_identifier")
    if "缺全文" in text and "实验流程审计" in text and "不能" not in text and "无法" not in text:
        score -= 25
        failed.append("experiment_audit_without_full_text")
    if "不确定项" not in text and "材料不足" not in text and "需要全文" not in text:
        score -= 10
        failed.append("missing_uncertainty_boundary")

    if "材料不足" in text or "需要全文" in text or "无法继续" in text:
        score += 10
    if "Request 文献目录" in text or "缺失材料" in text:
        score += 10
    if "证据边界" in text or "可追溯" in text:
        score += 10
    if all(k in text for k in ["事实", "推断", "建议"]):
        score += 10

    return {
        "honesty_score": max(0, min(100, score)),
        "failed_checks": failed,
        "final_status": "failed_validation" if failed else "complete_with_full_text",
    }

def main():
    parser = argparse.ArgumentParser(description="Score text for honesty and evidence-bound claims.")
    parser.add_argument("text_path")
    parser.add_argument("--output-json")
    args = parser.parse_args()

    text = Path(args.text_path).read_text(encoding="utf-8")
    result = score_text(text)
    if args.output_json:
        path = Path(args.output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"honesty_score: {result['honesty_score']}")
    for item in result["failed_checks"]:
        print(f"- {item}")
    raise SystemExit(1 if result["honesty_score"] < 70 or result["failed_checks"] else 0)

if __name__ == "__main__":
    main()
