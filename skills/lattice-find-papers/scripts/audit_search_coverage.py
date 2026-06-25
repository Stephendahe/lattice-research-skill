#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import read_csv, write_csv

FIELDS = ["check_item", "result", "risk", "suggestion"]

def unique_values(rows, field):
    vals = set()
    for row in rows:
        for part in (row.get(field) or "").replace(";", ",").split(","):
            if part.strip():
                vals.add(part.strip())
    return vals

def audit(rows):
    sources = unique_values(rows, "source_name")
    journals = unique_values(rows, "covered_journals")
    publishers = unique_values(rows, "covered_publishers")
    method_types = unique_values(rows, "method_types")
    mechanism_types = unique_values(rows, "mechanism_types")
    variable_types = unique_values(rows, "variable_types")
    out = []
    out.append({"check_item": "数据库来源分布", "result": str(len(sources)), "risk": "单一数据库偏差" if len(sources) < 2 else "低", "suggestion": "增加多源检索" if len(sources) < 2 else "保持"})
    out.append({"check_item": "出版社分布", "result": str(len(publishers)), "risk": "出版社偏置" if len(publishers) < 2 else "低", "suggestion": "扩展出版社平台/机构库" if len(publishers) < 2 else "保持"})
    out.append({"check_item": "期刊分布", "result": str(len(journals)), "risk": "期刊过窄" if len(journals) < 3 else "低", "suggestion": "扩展关键词和引文链" if len(journals) < 3 else "保持"})
    out.append({"check_item": "方法类型覆盖", "result": ",".join(sorted(method_types)) or "未记录", "risk": "方法缺口" if len(method_types) < 2 else "低", "suggestion": "补实验/模拟/理论专项检索" if len(method_types) < 2 else "保持"})
    out.append({"check_item": "机制分支覆盖", "result": ",".join(sorted(mechanism_types)) or "未记录", "risk": "机制分支缺失" if len(mechanism_types) < 2 else "低", "suggestion": "增加机制关键词" if len(mechanism_types) < 2 else "保持"})
    out.append({"check_item": "变量分支覆盖", "result": ",".join(sorted(variable_types)) or "未记录", "risk": "变量分支缺失" if len(variable_types) < 2 else "低", "suggestion": "增加变量+观测量检索块" if len(variable_types) < 2 else "保持"})
    return out

def main():
    p = argparse.ArgumentParser(description="Audit search coverage risks from search_coverage_audit.csv.")
    p.add_argument("search_coverage_csv")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    rows = audit(read_csv(Path(args.search_coverage_csv)))
    write_csv(Path(args.output), FIELDS, rows)
    risky = [r for r in rows if r["risk"] != "低"]
    print(f"risks: {len(risky)}")

if __name__ == "__main__":
    main()
