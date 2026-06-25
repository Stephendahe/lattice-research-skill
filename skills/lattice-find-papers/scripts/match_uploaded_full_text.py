#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import CSV_HEADERS, find_papers_root, load_json, normalize_doi, normalize_title, now_iso, read_csv, safe_run_dir, save_json, write_csv

def match_file(file_path: Path, rows):
    stem = normalize_title(file_path.stem)
    name = file_path.name.lower()
    for row in rows:
        doi = normalize_doi(row.get("doi", ""))
        if doi and doi != "unknown" and normalize_title(doi) in stem:
            return row, "doi"
        pid = (row.get("paper_id") or "").lower()
        if pid and pid in name:
            return row, "paper_id"
        title = normalize_title(row.get("title", ""))
        if title and (title in stem or stem in title) and min(len(title), len(stem)) > 12:
            return row, "title"
    return None, ""

def main():
    p = argparse.ArgumentParser(description="Match uploaded full texts to requests and update availability/resume state.")
    p.add_argument("run_dir")
    p.add_argument("--files", nargs="+", required=True, help="Uploaded PDF/SI/data files.")
    args = p.parse_args()
    run_dir = safe_run_dir(args.run_dir)
    output_root = find_papers_root(run_dir)
    availability_path = output_root / "tables" / "full_text_availability.csv"
    rows = read_csv(availability_path)
    manifest_rows = read_csv(output_root / "inputs" / "uploaded_files_manifest.csv")
    matched = []
    for raw in args.files:
        file_path = Path(raw)
        row, method = match_file(file_path, rows)
        entry = {"file_path": str(file_path), "file_name": file_path.name, "matched_paper_id": "", "matched_doi": "", "matched_title": "", "match_method": method or "unmatched", "notes": ""}
        if row:
            row["access_status"] = "user_uploaded"
            row["access_level"] = "L5_raw_data_code" if file_path.suffix.lower() in {".csv", ".xlsx", ".json", ".zip"} else "L2_full_text"
            row["needs_user_upload"] = "false"
            row["missing_sections"] = ""
            entry.update({"matched_paper_id": row.get("paper_id", ""), "matched_doi": row.get("doi", ""), "matched_title": row.get("title", "")})
            matched.append(row.get("paper_id", ""))
        manifest_rows.append(entry)
    write_csv(availability_path, CSV_HEADERS["full_text_availability.csv"], rows)
    write_csv(output_root / "inputs" / "uploaded_files_manifest.csv", CSV_HEADERS["uploaded_files_manifest.csv"], manifest_rows)
    state_path = run_dir / "resume_state.json"
    state = load_json(state_path, {})
    state["last_updated"] = now_iso()
    state["next_resume_phase"] = "phase_10_structure_round" if matched else state.get("next_resume_phase", "phase_7_request_queue")
    state["required_user_files"] = [x for x in state.get("required_user_files", []) if x not in matched]
    save_json(state_path, state)
    print(f"matched: {len(matched)}")

if __name__ == "__main__":
    main()
