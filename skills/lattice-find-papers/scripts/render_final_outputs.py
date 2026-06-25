#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import find_papers_root, read_csv, safe_run_dir

def md_table(rows, columns, empty="暂无。"):
    if not rows:
        return empty + "\n"
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")).replace("|", "/") for c in columns) + " |")
    return "\n".join(lines) + "\n"

def main():
    p = argparse.ArgumentParser(description="Render concise final_report.md and final_summary.txt from run tables.")
    p.add_argument("run_dir")
    args = p.parse_args()
    run_dir = safe_run_dir(args.run_dir)
    output_root = find_papers_root(run_dir)
    requests = read_csv(output_root / "request_queue" / "full_text_requests.csv")
    availability = read_csv(output_root / "tables" / "full_text_availability.csv")
    relations = read_csv(output_root / "tables" / "variable_relations.csv")
    blockers = read_csv(output_root / "tables" / "normalization_blockers.csv")
    exp = read_csv(output_root / "tables" / "experiment_pipeline_audit.csv")
    local_checked = sum(1 for row in availability if str(row.get("local_library_checked", "")).lower() in {"true", "1", "yes"})
    local_resolved = sum(1 for row in availability if row.get("local_full_text_status") in {"pdf_found", "html_found", "raw_data_found", "code_found"} or row.get("local_supplement_status") == "supplement_found")
    report = ["# Lattice Find Papers 输出", "", "## 1. 结论", ""]
    if requests:
        report += ["- 本轮已完成在线全文检查，并按配置尝试 Zotero / 本地 PDF / 本地补充材料检查。", f"- 本地检查覆盖 {local_checked} 篇候选，解决或部分解决 {local_resolved} 篇全文/补充材料缺失。", f"- 仍有 {len(requests)} 篇需要用户下载、上传或人工确认。", "- 当前不能基于摘要完成被全文缺失阻断的数据轮、实验轮、机制轮或可比性轮强结论。", "- 补充 Request 文献目录中的 PDF、全文或补充材料后，可以从断点继续。"]
    else:
        report += ["- 本轮已完成在线全文检查，并按配置尝试 Zotero / 本地 PDF / 本地补充材料检查。", f"- 本地检查覆盖 {local_checked} 篇候选，解决或部分解决 {local_resolved} 篇全文/补充材料缺失。", "- 当前未生成 Request 文献目录。", "- 仍需按证据等级逐项确认事实主张。"]
    report += ["", "## 2. 证据边界", "", "| 项目 | 状态 |", "|---|---|", f"| 在线全文检查 | 已完成或按当前可用来源记录 |", f"| 本地全文检查 | 已尝试 {local_checked} 篇；本地解决或部分解决 {local_resolved} 篇 |", f"| 全文可得性 | {'存在缺全文阻断' if requests else '未发现 Request 阻断'} |", f"| 可做的数据分析 | {'仅限有 L2+ 证据的文献' if relations else '暂无可显示关系'} |", f"| 被阻断的分析 | {'数据轮、实验轮、机制轮、可比性轮的部分任务' if requests else '暂无'} |", "", "## 3. Request 文献目录", "", md_table(requests, ["request_id", "paper_id", "title", "priority", "needed_sections", "local_resolution_status", "resume_checkpoint"]), "## 4. 变量关系矩阵", "", md_table(relations, ["relation_id", "paper_id", "variable_A", "variable_B", "relation_type", "access_level", "confidence"]), "## 5. 实验流程审计", "", md_table(exp, ["audit_id", "paper_id", "unreported_variables", "severity", "impact_on_conclusion"]), "## 6. 机制对比与冲突", "", "证据不足的机制冲突不在此强行裁决。\n", "## 7. 不可归一化原因", "", md_table(blockers, ["blocker_id", "paper_id", "missing_item", "why_it_blocks_comparison", "severity"]), "## 8. 不确定项", "", "- 文中未报告、全文未获得、补充材料缺失、低置信度本地匹配或需要用户上传的项目必须保留在本节。", "", "## 9. 不应夸大的结论", "", "- 不能把“统一框架 / 数据归一化 / 多因素耦合”直接写成研究空白。", "- 不能把相关写成因果。", "", "## 10. 下一步", "", "- 优先补充 high priority 的全文或补充材料。", "- 补充后运行 resume 流程，从断点继续。", ""]
    text = "\n".join(report)
    (output_root / "outputs" / "final_report.md").write_text(text, encoding="utf-8")
    (output_root / "outputs" / "final_summary.txt").write_text("缺全文时已生成 Request；补充文件后可断点续跑。\n" if requests else "当前无 Request 阻断。\n", encoding="utf-8")
    print(output_root / "outputs" / "final_report.md")

if __name__ == "__main__":
    main()
