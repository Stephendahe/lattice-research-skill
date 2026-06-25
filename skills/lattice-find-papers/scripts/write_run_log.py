#!/usr/bin/env python3
import argparse
import json
from lattice_common import append_jsonl, find_papers_root, now_iso, safe_run_dir

def main():
    p = argparse.ArgumentParser(description="Append a structured event to logs/run.jsonl or another JSONL log.")
    p.add_argument("run_dir")
    p.add_argument("--log", default="run.jsonl", help="Log filename under logs/.")
    p.add_argument("--event", required=True)
    p.add_argument("--phase", default="")
    p.add_argument("--level", default="INFO")
    p.add_argument("--message", default="")
    p.add_argument("--data-json", default="{}", help="Optional JSON object.")
    args = p.parse_args()
    try:
        data = json.loads(args.data_json)
        if not isinstance(data, dict):
            raise ValueError
    except Exception:
        raise SystemExit("--data-json must be a JSON object")
    run_dir = safe_run_dir(args.run_dir)
    append_jsonl(find_papers_root(run_dir) / "logs" / args.log, {"timestamp": now_iso(), "event": args.event, "phase": args.phase, "level": args.level, "message": args.message, "data": data})

if __name__ == "__main__":
    main()
