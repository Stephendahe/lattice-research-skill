#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as _dt
import json
import re
from pathlib import Path

CSV_HEADERS = {
    "papers_master.csv": "paper_id,title,year,doi,source,source_url,publisher,journal,system_or_material,research_object,core_phenomenon,method_type,method_detail,main_claim,mechanism_claim,variables_changed,variables_controlled,variables_unreported,default_assumptions,key_observables,key_figures,extractable_parameters,inclusion_decision,inclusion_reason,verification_status,access_level,notes".split(","),
    "search_coverage_audit.csv": "source_name,query_block,query_string,date_searched,results_count,unique_after_dedup,covered_publishers,covered_journals,year_range,method_types,mechanism_types,variable_types,coverage_warning,notes".split(","),
    "full_text_availability.csv": "paper_id,title,doi,access_status,access_level,available_sections,missing_sections,needs_user_upload,request_priority,resume_checkpoint,notes,local_library_checked,local_library_source,local_match_method,local_match_confidence,local_full_text_status,local_supplement_status,local_resolution_notes".split(","),
    "full_text_requests.csv": "request_id,paper_id,title,year,doi,source_url,current_access_level,why_full_text_needed,needed_sections,missing_for_tasks,priority,user_action,resume_checkpoint,notes,local_library_checked,local_library_result,local_resolution_status".split(","),
    "uploaded_files_manifest.csv": "file_path,file_name,matched_paper_id,matched_doi,matched_title,match_method,notes".split(","),
    "manual_sources.csv": "source_id,title,doi,url,notes".split(","),
    "supplement_requests.csv": "request_id,paper_id,title,needed_sections,priority,user_action,resume_checkpoint,notes".split(","),
    "evidence_spans.csv": "evidence_id,paper_id,source_text,source_location,access_level,extracted_claim,claim_type,evidence_type,verification_status,confidence,notes".split(","),
    "variable_relations.csv": "relation_id,paper_id,variable_A,variable_A_role,variable_B,variable_B_role,relation_direction,relation_form,relation_type,evidence_type,access_level,control_status,controlled_variables,missing_variables,default_assumptions,mechanism_link,boundary_conditions,comparability_status,confidence,source_location,notes".split(","),
    "mechanism_comparison.csv": "mechanism_id,mechanism_name,papers,causal_chain,trigger_condition,starting_site,key_variables,supporting_evidence,access_level,alternative_explanations,applicable_conditions,limitations,confidence,notes".split(","),
    "mechanism_conflicts.csv": "conflict_id,paper_A,paper_B,shared_question,A_claim,B_claim,apparent_conflict,variable_differences,pipeline_differences,boundary_condition_differences,contradiction_type,best_interpretation,missing_evidence,access_level_sufficient,implication_for_user".split(","),
    "experiment_pipeline_audit.csv": "audit_id,paper_id,access_level,material_source,supplier_batch_purity,pretreatment,synthesis_or_processing,assembly_process,environment_condition,test_protocol,post_processing,data_processing,repeated_trials,reported_statistics,controlled_variables,uncontrolled_variables,unreported_variables,default_fixed_variables,author_explanation,core_variable_match,severity,impact_on_conclusion,reviewer_note".split(","),
    "normalization_blockers.csv": "blocker_id,paper_id,missing_item,blocker_level,why_it_blocks_comparison,is_core_variable,related_variable,affected_observable,severity,possible_resolution,note".split(","),
    "citation_audit.csv": "claim_id,claim_sentence,paper_id,citation,doi,source_location,what_the_paper_actually_supports,support_level,problem,action".split(","),
    "pseudo_gap_hits.csv": "gap_id,phrase,source_location,why_risky,rewrite_action,severity,notes".split(","),
}

PHASES = [
    "phase_0_task_intake", "phase_1_retrieval_plan", "phase_2_retrieval_or_manual_plan",
    "phase_3_dedup_master_table", "phase_4_search_coverage_audit", "phase_5_title_abstract_screening",
    "phase_6_full_text_availability", "phase_7_request_queue", "phase_8_full_text_priority",
    "phase_9_save_resume_state", "phase_10_structure_round", "phase_11_data_round",
    "phase_12_experiment_round", "phase_13_mechanism_round", "phase_14_comparability_round",
    "phase_15_contradiction_round", "phase_16_citation_expansion", "phase_17_variable_matrix",
    "phase_18_experiment_audit", "phase_19_core_variable_match", "phase_20_normalization_blockers",
    "phase_21_pseudo_gap_detection", "phase_22_citation_audit", "phase_23_chinese_terms",
    "phase_24_self_review", "phase_25_render_outputs", "phase_26_archive_logs",
]

MISSING_ACCESS_STATUSES = {"metadata_only", "abstract_only", "partial_text", "supplement_missing", "paywalled_or_unavailable", "needs_user_upload"}
FULL_ACCESS_STATUSES = {"full_text_available", "figures_available", "supplement_available", "user_uploaded"}
LOCAL_LIBRARY_SOURCES = {"none", "zotero_local_api", "zotero_export", "local_pdf_folder", "local_supplement_folder", "manual_path_list"}
LOCAL_FULL_TEXT_STATUSES = {"not_found", "metadata_only", "abstract_only", "indexed_fulltext_only", "pdf_found", "html_found", "supplement_found", "raw_data_found", "code_found", "needs_manual_confirmation"}
LOCAL_RESOLUTION_STATUSES = {"unresolved", "resolved_by_online_source", "resolved_by_zotero", "resolved_by_local_pdf_folder", "partially_resolved_missing_supplement", "tentative_match_needs_confirmation", "request_required"}
PSEUDO_GAP_PHRASES = ["多种数据耦合", "搭建统一框架", "实现数据归一化", "一体化平台", "更多变量联合分析", "文献结论不同", "某变量没有被研究", "高引用文献没提", "数据库建设本身", "统一指标本身"]
COMMON_ENGLISH_ALLOWED = {"Lattice", "Research", "Skill", "Request", "DOI", "URL", "PDF", "CSV", "JSON", "Methods", "Results", "Discussion", "Supplementary", "Figures", "Tables", "L0", "L1", "L2", "L3", "L4", "L5"}

def now_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

def ensure_csv(path: Path, key: str) -> None:
    if not path.exists():
        write_csv(path, CSV_HEADERS[key], [])

def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def append_jsonl(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def truthy(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "需要", "是"}

def normalize_title(text: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (text or "").lower())

def normalize_doi(text: str) -> str:
    text = (text or "").lower().strip()
    text = text.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return text

def safe_run_dir(run_dir: str | Path) -> Path:
    path = Path(run_dir)
    if not path.exists():
        raise SystemExit(f"run directory not found: {path}")
    return path

def find_papers_root(run_dir: str | Path) -> Path:
    return Path(run_dir) / "find_papers_outputs"

def request_needed(row: dict[str, str]) -> bool:
    status = (row.get("access_status") or "").strip()
    level = (row.get("access_level") or "").strip()
    missing = (row.get("missing_sections") or "").strip()
    return truthy(row.get("needs_user_upload")) or status in MISSING_ACCESS_STATUSES or level in {"L0_metadata_only", "L1_title_abstract", "L2_partial_text", "L2_partial_full_text", "L4_supplement_missing"} or bool(missing)

def priority_for(row: dict[str, str]) -> str:
    value = (row.get("request_priority") or "").strip().lower()
    if value in {"high", "medium", "low"}:
        return value
    notes = " ".join(str(row.get(k, "")) for k in row)
    if any(word in notes.lower() for word in ["core", "conflict", "benchmark", "关键", "冲突", "核心"]):
        return "high"
    return "medium"

def simple_slug(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text or "").strip("_").lower()
    return slug or "untitled"
