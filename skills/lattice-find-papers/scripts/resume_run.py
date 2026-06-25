#!/usr/bin/env python3
import argparse
from pathlib import Path
from lattice_common import load_json, save_json, now_iso, safe_run_dir

def main():
    p = argparse.ArgumentParser(description="Inspect resume_state.json and show the next resumable phase.")
    p.add_argument("run_dir", help="runs/<run_id> directory.")
    p.add_argument("--mark-completed", action="append", default=[], help="Phase to append to completed_phases.")
    p.add_argument("--next-phase", help="Override next_resume_phase.")
    args = p.parse_args()
    run_dir = safe_run_dir(args.run_dir)
    state_path = run_dir / "resume_state.json"
    state = load_json(state_path)
    if not state:
        raise SystemExit(f"resume_state.json not found or empty: {state_path}")
    for phase in args.mark_completed:
        if phase not in state.setdefault("completed_phases", []):
            state["completed_phases"].append(phase)
    if args.next_phase:
        state["next_resume_phase"] = args.next_phase
    if args.mark_completed or args.next_phase:
        state["last_updated"] = now_iso()
        save_json(state_path, state)
    print(f"run_id: {state.get('run_id')}")
    print(f"topic: {state.get('topic')}")
    print(f"next_resume_phase: {state.get('next_resume_phase')}")
    if state.get("required_user_files"):
        print("required_user_files:")
        for item in state["required_user_files"]:
            print(f"- {item}")

if __name__ == "__main__":
    main()
