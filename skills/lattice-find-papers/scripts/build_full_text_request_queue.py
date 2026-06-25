#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from lattice_common import (
    CSV_HEADERS,
    append_jsonl,
    normalize_doi,
    normalize_title,
    now_iso,
    priority_for,
    read_csv,
    request_needed,
    truthy,
    write_csv,
)

RELEVANT_DECISIONS = {
    "include_core",
    "include_variable",
    "include_method",
    "include_parameter",
    "need_full_text",
}
HIGH_MEDIUM = {"high", "medium"}


def log_event(log_path: Path | None, level: str, message: str, data: dict | None = None) -> None:
    if not log_path:
        return
    append_jsonl(
        log_path,
        {
            "timestamp": now_iso(),
            "event": "full_text_local_check",
            "phase": "phase_6_full_text_availability",
            "level": level,
            "message": message,
            "data": data or {},
        },
    )


def infer_log_path(output_csv: Path) -> Path | None:
    parts = output_csv.resolve().parts
    if "request_queue" not in parts:
        return None
    request_idx = parts.index("request_queue")
    if request_idx == 0:
        return None
    output_root = Path(*parts[:request_idx])
    return output_root / "logs" / "warnings.jsonl"


def infer_request_pdf_dir(output_csv: Path) -> Path | None:
    parts = output_csv.resolve().parts
    if "request_queue" not in parts:
        return None
    request_idx = parts.index("request_queue")
    if request_idx == 0:
        return None
    output_root = Path(*parts[:request_idx])
    run_dir = output_root.parent if output_root.name == "find_papers_outputs" else output_root
    return run_dir / "request_PDF"


def online_or_local_full_text(row: dict[str, str]) -> bool:
    status = (row.get("access_status") or "").strip()
    level = (row.get("access_level") or "").strip()
    local_status = (row.get("local_full_text_status") or "").strip()
    return status in {"full_text_available", "figures_available", "supplement_available", "user_uploaded"} or level in {"L2_full_text", "L3_figures_tables", "L4_supplementary", "L5_raw_data_code"} or local_status in {"pdf_found", "html_found", "raw_data_found", "code_found"}


def relevant_for_full_text(row: dict[str, str], paper: dict[str, str] | None) -> bool:
    decision = (paper or {}).get("inclusion_decision", "").strip()
    if decision:
        return decision in RELEVANT_DECISIONS
    return request_needed(row)


def supplement_missing(row: dict[str, str]) -> bool:
    text = " ".join([row.get("missing_sections", ""), row.get("access_status", ""), row.get("notes", "")]).lower()
    return any(token in text for token in ["supplement", "si", "supporting", "补充"])


def main_text_missing(row: dict[str, str]) -> bool:
    status = (row.get("access_status") or "").strip()
    level = (row.get("access_level") or "").strip()
    local_status = (row.get("local_full_text_status") or "").strip()
    if status in {"full_text_available", "figures_available", "user_uploaded"}:
        return False
    if level in {"L2_full_text", "L3_figures_tables", "L5_raw_data_code"}:
        return False
    if local_status in {"pdf_found", "html_found"}:
        return False
    return True


def missing_after_local_resolution(row: dict[str, str]) -> str:
    if row.get("local_supplement_status") == "supplement_found" and main_text_missing(row):
        return "Full text / main PDF"
    if row.get("local_full_text_status") in {"pdf_found", "html_found"} and supplement_missing(row):
        return "Supplementary"
    return row.get("missing_sections") or "Full text / Methods / Results / Figures / Supplementary"


def update_available_sections(row: dict[str, str], value: str) -> None:
    existing = [x.strip() for x in (row.get("available_sections") or "").replace(";", ",").split(",") if x.strip()]
    if value not in existing:
        existing.append(value)
    row["available_sections"] = ";".join(existing)


def apply_match(row: dict[str, str], match: dict[str, str], source: str) -> bool:
    confidence = match.get("confidence", "")
    status = match.get("local_full_text_status", "not_found")
    method = match.get("method", "")
    row["local_library_checked"] = "true"
    row["local_library_source"] = source
    row["local_match_method"] = method
    row["local_match_confidence"] = confidence

    if confidence not in HIGH_MEDIUM:
        row["local_full_text_status"] = "needs_manual_confirmation"
        row["local_resolution_notes"] = "本地低置信度匹配，需要人工确认；未自动更新全文状态。"
        return False

    if status in {"supplement_found"}:
        row["local_supplement_status"] = "supplement_found"
        update_available_sections(row, "Supplementary")
        row["access_status"] = "supplement_available"
        row["access_level"] = "L4_supplementary"
        row["local_resolution_notes"] = "本地找到补充材料。"
        return True

    row["local_full_text_status"] = status
    if status == "pdf_found":
        update_available_sections(row, "PDF")
        if supplement_missing(row):
            row["access_status"] = "supplement_missing"
            row["access_level"] = "L2_full_text"
            row["missing_sections"] = "Supplementary"
            row["needs_user_upload"] = "true"
            row["local_supplement_status"] = row.get("local_supplement_status") or "not_found"
            row["local_resolution_notes"] = "本地找到主文 PDF，但仍缺补充材料。"
        else:
            row["access_status"] = "full_text_available"
            row["access_level"] = "L2_full_text"
            row["missing_sections"] = ""
            row["needs_user_upload"] = "false"
            row["local_resolution_notes"] = "本地找到主文 PDF。"
        return True
    if status == "html_found":
        update_available_sections(row, "HTML full text")
        row["access_status"] = "full_text_available"
        row["access_level"] = "L2_full_text"
        row["missing_sections"] = "" if not supplement_missing(row) else "Supplementary"
        row["needs_user_upload"] = "true" if supplement_missing(row) else "false"
        row["local_resolution_notes"] = "本地找到 HTML 全文。"
        return True
    if status == "indexed_fulltext_only":
        row["access_status"] = "partial_text"
        row["access_level"] = "L2_partial_text"
        row["needs_user_upload"] = "true"
        row["local_resolution_notes"] = "仅找到 indexed full-text，未找到 PDF；不得进入图表/数据深度分析。"
        return True
    if status in {"raw_data_found", "code_found"}:
        update_available_sections(row, "Raw data/code")
        row["access_status"] = "full_text_available"
        row["access_level"] = "L5_raw_data_code"
        row["needs_user_upload"] = "false"
        row["missing_sections"] = ""
        row["local_resolution_notes"] = "本地找到原始数据或代码。"
        return True
    if status in {"metadata_only", "abstract_only"}:
        row["local_resolution_notes"] = "只找到本地条目或摘要，仍需全文。"
    return False


def file_status(path: Path, supplement: bool = False) -> str:
    suffix = path.suffix.lower()
    if supplement:
        return "supplement_found"
    if suffix == ".pdf":
        return "pdf_found"
    if suffix in {".html", ".htm"}:
        return "html_found"
    if suffix in {".csv", ".tsv", ".xlsx", ".json", ".zip"}:
        return "raw_data_found"
    if suffix in {".py", ".r", ".m", ".ipynb"}:
        return "code_found"
    return "needs_manual_confirmation"


def match_by_metadata(row: dict[str, str], paper: dict[str, str], item: dict[str, str]) -> dict[str, str] | None:
    row_doi = normalize_doi(row.get("doi") or paper.get("doi", ""))
    item_doi = normalize_doi(item.get("doi", ""))
    if row_doi and item_doi and row_doi == item_doi:
        return {"method": "doi_exact", "confidence": "high"}

    paper_key = (paper.get("citation_key") or row.get("citation_key") or "").strip().lower()
    item_key = (item.get("citation_key") or item.get("citekey") or "").strip().lower()
    if paper_key and item_key and paper_key == item_key:
        return {"method": "citation_key", "confidence": "high"}

    row_title = normalize_title(row.get("title") or paper.get("title", ""))
    item_title = normalize_title(item.get("title", ""))
    if row_title and item_title and row_title == item_title:
        return {"method": "title_exact", "confidence": "medium"}

    if (
        (paper.get("year") or row.get("year")) == item.get("year")
        and (paper.get("journal") or "").strip().lower() == (item.get("journal") or "").strip().lower()
        and (paper.get("first_author") or "").strip().lower()
        and (paper.get("first_author") or "").strip().lower() == (item.get("first_author") or item.get("author") or "").strip().lower()
    ):
        return {"method": "author_year_journal", "confidence": "medium"}

    if row_title and item_title and (row_title in item_title or item_title in row_title) and min(len(row_title), len(item_title)) >= 16:
        return {"method": "title_fuzzy", "confidence": "low"}
    return None


def match_file(row: dict[str, str], paper: dict[str, str], path: Path, supplement: bool = False) -> dict[str, str] | None:
    item = {"title": path.stem}
    match = match_by_metadata(row, paper, item)
    if not match:
        pid = (row.get("paper_id") or "").strip().lower()
        if pid and pid in path.name.lower():
            match = {"method": "paper_id_filename", "confidence": "medium"}
    if not match:
        return None
    match["local_full_text_status"] = file_status(path, supplement=supplement)
    match["path_name"] = path.name
    return match


def iter_files(directory: str | None, suffixes: set[str]) -> list[Path]:
    if not directory:
        return []
    root = Path(directory)
    if not root.exists() or not root.is_dir():
        return []
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in suffixes]


def parse_bib_like(text: str) -> list[dict[str, str]]:
    entries = []
    for chunk in re.split(r"\n\s*@", text):
        doi = re.search(r"\bdoi\s*=\s*[{\"]([^}\"]+)", chunk, re.I)
        title = re.search(r"\btitle\s*=\s*[{\"]([^}\"]+)", chunk, re.I)
        year = re.search(r"\byear\s*=\s*[{\"]?(\d{4})", chunk, re.I)
        key = re.match(r"[^,{]+[,{]([^,\s]+)", chunk.strip())
        if doi or title:
            entries.append(
                {
                    "doi": doi.group(1).strip() if doi else "",
                    "title": title.group(1).strip() if title else "",
                    "year": year.group(1) if year else "",
                    "citation_key": key.group(1).strip() if key else "",
                    "local_full_text_status": "metadata_only",
                    "local_library_source": "zotero_export",
                }
            )
    return entries


def parse_ris(text: str) -> list[dict[str, str]]:
    entries = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("ER  -"):
            if current:
                current.setdefault("local_full_text_status", "metadata_only")
                current.setdefault("local_library_source", "zotero_export")
                entries.append(current)
            current = {}
            continue
        if len(line) < 6 or "  - " not in line:
            continue
        tag, value = line[:2], line[6:].strip()
        if tag == "DO":
            current["doi"] = value
        elif tag in {"TI", "T1"}:
            current["title"] = value
        elif tag == "PY":
            current["year"] = value[:4]
        elif tag in {"JO", "JF", "JA"}:
            current["journal"] = value
        elif tag == "AU" and "first_author" not in current:
            current["first_author"] = value.split(",")[0].strip()
    if current:
        current.setdefault("local_full_text_status", "metadata_only")
        current.setdefault("local_library_source", "zotero_export")
        entries.append(current)
    return entries


def load_source_list(path: str | None) -> list[dict[str, str]]:
    if not path:
        return []
    source_path = Path(path)
    if not source_path.exists():
        return []
    suffix = source_path.suffix.lower()
    if suffix == ".csv":
        with source_path.open(newline="", encoding="utf-8-sig") as f:
            return [dict(row) for row in csv.DictReader(f)]
    if suffix == ".json":
        data = json.loads(source_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("items") or data.get("references") or []
        return [dict(item) for item in data if isinstance(item, dict)]
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    if suffix in {".bib", ".bibtex"}:
        return parse_bib_like(text)
    if suffix == ".ris":
        return parse_ris(text)
    return []


def check_zotero_api(url: str, log_path: Path | None) -> bool:
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/", timeout=2) as response:
            ok = 200 <= response.status < 500
    except (OSError, urllib.error.URLError) as exc:
        log_event(log_path, "WARNING", "Zotero Local API 不可访问；不中断流程。", {"reason": exc.__class__.__name__})
        return False
    if ok:
        log_event(log_path, "INFO", "Zotero Local API 可访问；当前脚本保留接口，不读取 zotero.sqlite。")
    return ok


def update_availability_with_local_checks(
    availability: list[dict[str, str]],
    papers: list[dict[str, str]],
    *,
    check_zotero: bool = False,
    zotero_url: str = "http://localhost:23119/api/",
    local_pdf_dir: str | None = None,
    local_supplement_dir: str | None = None,
    local_source_list: str | None = None,
    skip_local_check: bool = False,
    log_path: Path | None = None,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    paper_map = {r.get("paper_id"): r for r in papers}
    stats = {"checked": 0, "resolved": 0, "manual_confirmation": 0, "skipped": 0}
    source_items = load_source_list(local_source_list)
    pdf_files = iter_files(local_pdf_dir, {".pdf", ".html", ".htm", ".csv", ".tsv", ".xlsx", ".json", ".zip", ".py", ".r", ".m", ".ipynb"})
    supplement_files = iter_files(local_supplement_dir, {".pdf", ".docx", ".xlsx", ".csv", ".zip", ".json"})

    if skip_local_check:
        return availability, stats
    if check_zotero:
        check_zotero_api(zotero_url, log_path)

    for row in availability:
        paper = paper_map.get(row.get("paper_id"), {})
        if not relevant_for_full_text(row, paper) or online_or_local_full_text(row) and not supplement_missing(row):
            stats["skipped"] += 1
            row.setdefault("local_library_checked", "false")
            row.setdefault("local_library_source", "none")
            continue

        stats["checked"] += 1
        row["local_library_checked"] = "true"
        row.setdefault("local_library_source", "none")
        row.setdefault("local_full_text_status", "not_found")
        row.setdefault("local_supplement_status", "not_found")

        resolved = False
        for item in source_items:
            match = match_by_metadata(row, paper, item)
            if not match:
                continue
            match["local_full_text_status"] = item.get("local_full_text_status") or item.get("full_text_status") or ("pdf_found" if item.get("file_path", "").lower().endswith(".pdf") else "metadata_only")
            source = item.get("local_library_source") or ("zotero_export" if local_source_list else "manual_path_list")
            resolved = apply_match(row, match, source)
            if row.get("local_full_text_status") == "needs_manual_confirmation":
                stats["manual_confirmation"] += 1
            break

        if not resolved:
            for path in pdf_files:
                match = match_file(row, paper, path)
                if match:
                    resolved = apply_match(row, match, "local_pdf_folder")
                    if row.get("local_full_text_status") == "needs_manual_confirmation":
                        stats["manual_confirmation"] += 1
                    break

        if supplement_missing(row) or not resolved:
            for path in supplement_files:
                match = match_file(row, paper, path, supplement=True)
                if match:
                    apply_match(row, match, "local_supplement_folder")
                    resolved = resolved or match.get("confidence") in HIGH_MEDIUM
                    break

        if resolved:
            stats["resolved"] += 1
        elif row.get("local_full_text_status") != "needs_manual_confirmation":
            row["local_full_text_status"] = row.get("local_full_text_status") or "not_found"
            row["local_supplement_status"] = row.get("local_supplement_status") or "not_found"
            row["local_resolution_notes"] = "在线和本地检查后仍缺全文。"

    log_event(log_path, "INFO", "本地全文可得性检查完成。", stats)
    return availability, stats


def local_resolution_status(row: dict[str, str]) -> str:
    if row.get("local_full_text_status") == "needs_manual_confirmation":
        return "tentative_match_needs_confirmation"
    if row.get("local_full_text_status") in {"pdf_found", "html_found", "raw_data_found", "code_found"} and supplement_missing(row):
        return "partially_resolved_missing_supplement"
    if row.get("local_library_source") in {"zotero_local_api", "zotero_export"} and row.get("local_full_text_status") in {"pdf_found", "html_found"}:
        return "resolved_by_zotero"
    if row.get("local_library_source") == "local_pdf_folder" and row.get("local_full_text_status") in {"pdf_found", "html_found", "raw_data_found", "code_found"}:
        return "resolved_by_local_pdf_folder"
    if row.get("local_full_text_status") == "indexed_fulltext_only":
        return "request_required"
    return "request_required"


def build_requests(availability, papers):
    paper_map = {r.get("paper_id"): r for r in papers}
    requests = []
    for row in availability:
        paper = paper_map.get(row.get("paper_id"), {})
        if not relevant_for_full_text(row, paper):
            continue
        if not request_needed(row):
            continue
        missing = missing_after_local_resolution(row)
        idx = len(requests) + 1
        resolution = local_resolution_status(row)
        user_action = "请上传 PDF、全文链接或补充材料。"
        if resolution == "partially_resolved_missing_supplement":
            user_action = "本地已有主文 PDF；请补充 Supplementary。"
        elif resolution == "tentative_match_needs_confirmation":
            user_action = "请人工确认本地低置信度匹配，或上传 PDF/补充材料。"
        elif row.get("local_supplement_status") == "supplement_found" and main_text_missing(row):
            user_action = "本地已有补充材料；请上传主文 PDF 或全文链接。"
        requests.append({
            "request_id": f"R{idx:03d}",
            "paper_id": row.get("paper_id", ""),
            "title": row.get("title") or paper.get("title", ""),
            "authors": paper.get("authors") or paper.get("author") or paper.get("first_author") or row.get("authors") or row.get("author") or row.get("first_author") or "unknown",
            "year": paper.get("year", ""),
            "doi": row.get("doi") or paper.get("doi") or "unknown",
            "source_url": paper.get("source_url") or "unknown",
            "current_access_level": row.get("access_level") or "L1_title_abstract",
            "why_full_text_needed": f"缺少 {missing}，不能进行数据、实验流程或机制深度分析。",
            "needed_sections": missing,
            "missing_for_tasks": "数据轮;实验轮;机制轮;可比性轮",
            "priority": priority_for(row),
            "user_action": user_action,
            "resume_checkpoint": row.get("resume_checkpoint") or "phase_10_structure_round",
            "notes": row.get("notes", ""),
            "local_library_checked": row.get("local_library_checked", "false"),
            "local_library_result": row.get("local_resolution_notes", ""),
            "local_resolution_status": resolution,
        })
    return requests


def compact_text(value: object, default: str = "unknown") -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text or default


def doi_url(doi: str) -> str:
    normalized = normalize_doi(doi)
    if not normalized or normalized == "unknown":
        return ""
    return f"https://doi.org/{normalized}"


def best_web_link(request: dict[str, str]) -> str:
    source_url = compact_text(request.get("source_url"), "")
    if source_url and source_url.lower() != "unknown":
        return source_url
    return doi_url(request.get("doi", "")) or "unknown"


def render_doi_list_md(requests):
    seen: set[str] = set()
    dois: list[str] = []
    for request in requests:
        doi = normalize_doi(request.get("doi", ""))
        if doi and doi != "unknown" and doi not in seen:
            seen.add(doi)
            dois.append(doi)

    lines = ["## DOI", ""]
    lines.extend(f"- {doi}" for doi in dois)
    lines.extend(["", "## Web Links", ""])
    for request in requests:
        lines.append(f"- Title: {compact_text(request.get('title'))}")
        lines.append(f"  Authors: {compact_text(request.get('authors'))}")
        lines.append(f"  Year: {compact_text(request.get('year'))}")
        lines.append(f"  Link: {best_web_link(request)}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_md(requests):
    lines = ["# Request 文献目录", "", "以下文献因缺少全文、图表或补充材料，当前无法进行真实的数据、实验流程或机制深度分析。", "", "| request_id | paper_id | title | year | doi | current_access_level | why_full_text_needed | needed_sections | missing_for_tasks | priority | user_action | resume_checkpoint |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in requests:
        lines.append("| " + " | ".join(str(r.get(k, "")).replace("|", "/") for k in ["request_id", "paper_id", "title", "year", "doi", "current_access_level", "why_full_text_needed", "needed_sections", "missing_for_tasks", "priority", "user_action", "resume_checkpoint"]) + " |")
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description="Build full_text_requests.csv after online and optional local full-text availability checks.")
    p.add_argument("full_text_availability_csv")
    p.add_argument("--papers-master", default="")
    p.add_argument("--output-csv", required=True)
    p.add_argument("--output-md", required=True)
    p.add_argument("--check-zotero", action="store_true", help="Probe Zotero Local API before local file checks; warning only if unavailable.")
    p.add_argument("--zotero-url", default="http://localhost:23119/api/", help="Zotero Local API URL.")
    p.add_argument("--local-pdf-dir", help="Directory containing candidate local PDFs or HTML/full-text files.")
    p.add_argument("--local-supplement-dir", help="Directory containing candidate supplementary files.")
    p.add_argument("--local-source-list", help="CSV/JSON/BibTeX/RIS source list exported from Zotero or prepared manually.")
    p.add_argument("--skip-local-check", action="store_true", help="Do not run local checks; generate Request from current availability table.")
    args = p.parse_args()

    availability_path = Path(args.full_text_availability_csv)
    availability = read_csv(availability_path)
    papers = read_csv(Path(args.papers_master)) if args.papers_master else []
    output_csv = Path(args.output_csv)
    log_path = infer_log_path(output_csv)

    availability, stats = update_availability_with_local_checks(
        availability,
        papers,
        check_zotero=args.check_zotero,
        zotero_url=args.zotero_url,
        local_pdf_dir=args.local_pdf_dir,
        local_supplement_dir=args.local_supplement_dir,
        local_source_list=args.local_source_list,
        skip_local_check=args.skip_local_check,
        log_path=log_path,
    )
    write_csv(availability_path, CSV_HEADERS["full_text_availability.csv"], availability)

    requests = build_requests(availability, papers)
    write_csv(output_csv, CSV_HEADERS["full_text_requests.csv"], requests)
    Path(args.output_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_md).write_text(render_md(requests), encoding="utf-8")
    request_pdf_dir = infer_request_pdf_dir(output_csv)
    if request_pdf_dir:
        request_pdf_dir.mkdir(parents=True, exist_ok=True)
        (request_pdf_dir / "doi_list.md").write_text(render_doi_list_md(requests), encoding="utf-8")
    print(f"local_checked: {stats['checked']}")
    print(f"local_resolved: {stats['resolved']}")
    print(f"requests: {len(requests)}")


if __name__ == "__main__":
    main()
