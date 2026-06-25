#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def check_type(value, allowed):
    if isinstance(allowed, str):
        allowed = [allowed]
    mapping = {"string": str, "integer": int, "boolean": bool, "array": list, "object": dict}
    return any(isinstance(value, mapping[t]) and not (t == "integer" and isinstance(value, bool)) for t in allowed if t in mapping)

def validate(data, schema):
    errors = []
    for key in schema.get("required", []):
        if key not in data:
            errors.append(f"missing required field: {key}")
    for key, prop in schema.get("properties", {}).items():
        if key not in data:
            continue
        if "type" in prop and not check_type(data[key], prop["type"]):
            errors.append(f"{key}: expected {prop['type']}")
        if "enum" in prop and data[key] not in prop["enum"]:
            errors.append(f"{key}: value {data[key]!r} not in enum")
    return errors

def main():
    p = argparse.ArgumentParser(description="Lightweight JSON schema validator for required fields, types, and enums.")
    p.add_argument("json_path")
    p.add_argument("schema_path")
    args = p.parse_args()
    try:
        data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
        schema = json.loads(Path(args.schema_path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"failed to read JSON/schema: {exc}")
    errors = validate(data, schema)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("json ok")

if __name__ == "__main__":
    main()
