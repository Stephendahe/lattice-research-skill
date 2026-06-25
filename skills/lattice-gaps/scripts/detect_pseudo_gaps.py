#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

PSEUDO_GAPS = {
    "多种数据耦合": "空泛，不说明变量、尺度和证据；先检查哪些数据、尺度和缺失项。",
    "搭建统一框架": "框架是工具，不是科学问题；先检查已有框架失败在哪个边界条件。",
    "统一框架": "框架是工具，不是科学问题；先检查已有框架失败在哪个边界条件。",
    "实现数据归一化": "归一化是手段，不是 gap；先检查为什么不能归一化。",
    "数据归一化": "归一化是手段，不是 gap；先检查为什么不能归一化。",
    "一体化平台": "平台是工程愿望；先指出缺失的证据链或字段 schema。",
    "更多变量联合分析": "未说明变量优先级；先确认哪些变量必须共同控制。",
    "文献结论不同": "可能只是条件差异；先检查体系、流程、尺度和数据处理。",
    "某变量没有被研究": "变量未研究不等于重要；先证明机制路径和可测性。",
    "高引用文献没提": "高引用不等于覆盖边界；先检查后续文献是否仍缺该点。",
    "数据库建设本身": "数据库是基础设施；先说明服务于哪个科学裁决。",
    "统一指标本身": "指标不是结论；先说明指标缺失如何阻断比较。",
    "数值不同": "数值差异可能来自单位、参数定义、方法或条件；先做可比性审计。",
    "颠覆全领域": "单篇新值可能是特殊条件或方法差异；先检查证据质量和边界条件。",
}

HEADERS = ["gap_id", "phrase", "source_location", "why_risky", "rewrite_action", "severity", "notes"]


def detect(text: str):
    hits = []
    matched_spans = []
    for phrase, why in sorted(PSEUDO_GAPS.items(), key=lambda item: len(item[0]), reverse=True):
        if phrase in text:
            start = text.find(phrase)
            end = start + len(phrase)
            if any(start >= old_start and end <= old_end for old_start, old_end in matched_spans):
                continue
            matched_spans.append((start, end))
            hits.append({
                "gap_id": f"G{len(hits)+1:03d}",
                "phrase": phrase,
                "source_location": "text",
                "why_risky": why,
                "rewrite_action": "降级为具体 blocker、可验证变量缺失、参数可比性问题、边界条件失败或真实机制问题。",
                "severity": "medium",
                "notes": "",
            })
    return hits


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Detect pseudo research-gap phrases as red flags.")
    parser.add_argument("text_path")
    parser.add_argument("--output-csv")
    args = parser.parse_args()

    text = Path(args.text_path).read_text(encoding="utf-8")
    hits = detect(text)
    if args.output_csv:
        write_csv(Path(args.output_csv), hits)
    for hit in hits:
        print(f"{hit['gap_id']}: {hit['phrase']} - {hit['why_risky']}")
    raise SystemExit(1 if hits else 0)


if __name__ == "__main__":
    main()
