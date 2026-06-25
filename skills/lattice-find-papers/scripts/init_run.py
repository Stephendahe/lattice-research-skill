#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from lattice_common import CSV_HEADERS, PHASES, ensure_csv, find_papers_root, now_iso, save_json, simple_slug, write_csv

def create_run(base: Path, topic: str, run_id: str | None = None, user_request: str = "") -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = run_id or f"{stamp}-{simple_slug(topic)[:40]}"
    run_dir = base / run_id
    output_root = find_papers_root(run_dir)
    (run_dir / "request_PDF").mkdir(parents=True, exist_ok=True)
    for sub in ["request_queue", "logs", "tables", "outputs", "inputs", "intermediate_tables"]:
        (output_root / sub).mkdir(parents=True, exist_ok=True)
    manifest = {"run_id": run_id, "topic": topic, "created_at": now_iso(), "skill": "lattice-find-papers", "version": "1.0.0"}
    resume = {"run_id": run_id, "topic": topic, "completed_phases": [], "blocked_phases": [], "blocking_requests": [], "next_resume_phase": PHASES[0], "required_user_files": [], "tables_completed": [], "tables_partial": [], "last_updated": now_iso()}
    save_json(run_dir / "run_manifest.json", manifest)
    save_json(run_dir / "resume_state.json", resume)
    for name in ["full_text_requests.csv", "supplement_requests.csv"]:
        ensure_csv(output_root / "request_queue" / name, name)
    (output_root / "request_queue" / "unresolved_requests.md").write_text("# 未解决 Request\n\n暂无。\n", encoding="utf-8")
    (run_dir / "request_PDF" / "doi_list.md").write_text("## DOI\n\n## Web Links\n", encoding="utf-8")
    for log in ["run.jsonl", "retrieval.jsonl", "evidence_extraction.jsonl", "validation.jsonl", "warnings.jsonl"]:
        (output_root / "logs" / log).touch()
    save_json(output_root / "logs" / "self_review.json", {"honesty_score": 0, "failed_checks": [], "downgraded_claims": [], "unsupported_claims_removed": [], "requests_generated": [], "resume_required": False, "final_status": "retrieval_only"})
    for table in ["papers_master.csv", "search_coverage_audit.csv", "full_text_availability.csv", "evidence_spans.csv", "variable_relations.csv", "mechanism_comparison.csv", "mechanism_conflicts.csv", "experiment_pipeline_audit.csv", "normalization_blockers.csv", "citation_audit.csv", "pseudo_gap_hits.csv"]:
        ensure_csv(output_root / "tables" / table, table)
    (output_root / "outputs" / "final_report.md").write_text("# Lattice Find Papers 输出\n\n尚未渲染。\n", encoding="utf-8")
    (output_root / "outputs" / "final_summary.txt").write_text("尚未渲染。\n", encoding="utf-8")
    (output_root / "outputs" / "request_literature_list.md").write_text("# Request 文献目录\n\n暂无。\n", encoding="utf-8")
    (output_root / "outputs" / "mechanism_map.md").write_text("# 机制地图\n\n暂无。\n", encoding="utf-8")
    (output_root / "outputs" / "variable_network.mmd").write_text("graph TD\n", encoding="utf-8")
    (output_root / "outputs" / "glossary_zh_cn.yml").write_text("terms: []\n", encoding="utf-8")
    (output_root / "inputs" / "user_request.md").write_text(user_request or f"# 用户请求\n\n主题：{topic}\n", encoding="utf-8")
    ensure_csv(output_root / "inputs" / "uploaded_files_manifest.csv", "uploaded_files_manifest.csv")
    ensure_csv(output_root / "inputs" / "manual_sources.csv", "manual_sources.csv")
    return run_dir

def main():
    p = argparse.ArgumentParser(description="Create a resumable Lattice Find Papers run directory.")
    p.add_argument("--topic", required=True, help="Review topic.")
    p.add_argument("--runs-dir", default="runs", help="Directory that will contain run folders.")
    p.add_argument("--run-id", help="Optional deterministic run id.")
    p.add_argument("--user-request", default="", help="Raw user request text to save.")
    args = p.parse_args()
    run_dir = create_run(Path(args.runs_dir), args.topic, args.run_id, args.user_request)
    print(run_dir)

if __name__ == "__main__":
    main()
