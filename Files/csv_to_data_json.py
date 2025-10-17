#!/usr/bin/env python3
import csv
import json
import sys


def main(inp: str):
    with open(inp, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        item = {
            "name": r.get("name_provisional") or r.get("name") or "",
            "street": r.get("street") or "",
            "city": r.get("city") or "",
            "rating": float(r.get("rating") or 0) if r.get("rating") else 0,
            "url": r.get("url") or "#",
            "latitude": float(r["latitude"]) if r.get("latitude") else None,
            "longitude": float(r["longitude"]) if r.get("longitude") else None,
            "feature_shade": (r.get("feature_schatten", "false").lower() == "true"),
            "feature_water": (r.get("feature_wasser_flach", "false").lower() == "true"),
            "feature_benches": (r.get("feature_wiese", "false").lower() == "true"),
            "feature_parking": (r.get("feature_parking", "false").lower() == "true"),
            "feature_toilets": (r.get("feature_toilets", "false").lower() == "true"),
            "feature_fkk": (r.get("feature_fkk", "false").lower() == "true"),
            "feature_grillen": (r.get("feature_grillen", "false").lower() == "true"),
            "feature_steg": (r.get("feature_steg", "false").lower() == "true"),
        }
        out.append(item)
    print("const DATA = " + json.dumps(out, ensure_ascii=False, indent=2) + ";")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python csv_to_data_json.py spot_capture_sheet.csv",
            file=sys.stderr,
        )
        sys.exit(1)
    main(sys.argv[1])
