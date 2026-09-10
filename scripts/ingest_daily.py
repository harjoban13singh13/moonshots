#!/usr/bin/env python3
"""
Daily ingestion: pulls current Reddit-derived stock attention data from
ApeWisdom's free, keyless public API and appends a dated snapshot to
data/daily/. No Reddit API credentials needed.

ApeWisdom docs: https://apewisdom.io/api/
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

APEWISDOM_URL = "https://apewisdom.io/api/v1.0/filter/all-stocks/page/{page}"
MAX_PAGES = 3  # ~100 tickers per page; top few hundred by mention volume is plenty
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "daily")


def fetch_page(page: int) -> dict:
    req = urllib.request.Request(
        APEWISDOM_URL.format(page=page),
        headers={"User-Agent": "moonshots-personal-tracker/0.1 (private use)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    all_results = []
    for page in range(1, MAX_PAGES + 1):
        try:
            payload = fetch_page(page)
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            print(f"Warning: failed to fetch page {page}: {exc}", file=sys.stderr)
            break
        results = payload.get("results", [])
        if not results:
            break
        all_results.extend(results)
        if page >= payload.get("pages", 1):
            break

    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "apewisdom.io (all-stocks filter)",
        "count": len(all_results),
        "results": all_results,
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = os.path.join(OUT_DIR, f"{date_str}.json")
    with open(out_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Wrote {len(all_results)} ticker rows to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
