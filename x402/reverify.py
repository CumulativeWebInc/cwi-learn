#!/usr/bin/env python3
"""Re-verifier for the CWI Verified x402 Directory (stdlib only).

Checks every listing in x402/directory.json:
  - required fields present
  - manifest_url reachable, valid JSON, IETF-draft-shaped (x402Version present)
  - evidence.first_spin_verdict_url reachable, valid JSON
  - evidence.needle_drop_ref reachable, valid JSON
  - last_reverified within --max-age-days (default 7); older = STALE = failure
  - public endpoints: still answer HTTP 402 (the x402 "alive" signal);
    private pilots are skipped by design, never failed for being private

Exit 0: all listings green. Exit 1: prints each failing listing by name.

Pre-merge use (branches not yet on GitHub Pages):
  python3 x402/reverify.py x402/directory.json \\
      --url-base https://raw.githubusercontent.com/CumulativeWebInc/cwi-learn/needs/receipts-directory
"""

import datetime
import json
import sys
import urllib.error
import urllib.request

CANONICAL_PREFIX = "https://cumulativewebinc.github.io/cwi-learn/"

REQUIRED_LISTING_FIELDS = [
    "service", "provider", "endpoint_url", "x402_price",
    "evidence", "manifest_url", "last_reverified", "status",
]
REQUIRED_EVIDENCE_FIELDS = ["first_spin_verdict_url", "needle_drop_ref"]


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "cwi-x402-reverify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            # file:// handlers report status None on success — normalize.
            status = resp.status if resp.status is not None else 200
            return status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # network/DNS/TLS failures are failures, loudly
        return None, str(e).encode()


def fetch_json_ok(url, what, failures, service):
    status, body = fetch(url)
    if status != 200:
        failures.append(f"{service}: {what} unreachable (HTTP {status}): {url}")
        return None
    try:
        return json.loads(body.decode("utf-8"))
    except Exception as e:
        failures.append(f"{service}: {what} not valid JSON: {url} ({e})")
        return None


def parse_date(s):
    s = s.strip()
    try:
        return datetime.date.fromisoformat(s[:10])
    except ValueError:
        return None


def check_listing(lst, url_base, max_age_days, today):
    service = lst.get("service", "<unnamed>")
    failures = []

    for f in REQUIRED_LISTING_FIELDS:
        if f not in lst:
            failures.append(f"{service}: missing required field '{f}'")
    ev = lst.get("evidence", {})
    for f in REQUIRED_EVIDENCE_FIELDS:
        if f not in ev:
            failures.append(f"{service}: evidence missing '{f}'")

    def canon(u):
        if url_base and u.startswith(CANONICAL_PREFIX):
            return url_base.rstrip("/") + "/" + u[len(CANONICAL_PREFIX):]
        return u

    manifest = fetch_json_ok(canon(lst["manifest_url"]), "manifest", failures, service)
    if manifest is not None and "x402Version" not in manifest:
        failures.append(f"{service}: manifest missing x402Version (not IETF-draft-shaped): {lst['manifest_url']}")

    if "first_spin_verdict_url" in ev:
        fetch_json_ok(canon(ev["first_spin_verdict_url"]), "first_spin_verdict", failures, service)
    if "needle_drop_ref" in ev:
        fetch_json_ok(canon(ev["needle_drop_ref"]), "needle_drop attestation", failures, service)

    seen = parse_date(str(lst.get("last_reverified", "")))
    if seen is None:
        failures.append(f"{service}: last_reverified not a parseable date: {lst.get('last_reverified')!r}")
    else:
        age = (today - seen).days
        due = str(lst.get("reverify_due", ""))
        if age > max_age_days:
            failures.append(
                f"{service}: STALE — last_reverified {seen} is {age} days ago "
                f"(max {max_age_days}; reverify_due {due or 'unset'})"
            )

    reach = lst.get("endpoint_reachability", "public")
    if reach == "public":
        status, _ = fetch(lst["endpoint_url"])
        # An x402 endpoint proves liveness by answering 402 to an unpaid call.
        if status != 402:
            failures.append(
                f"{service}: public endpoint did not answer HTTP 402 "
                f"(got {status}): {lst['endpoint_url']}"
            )
    else:
        print(f"  note: {service}: endpoint_reachability={reach!r} — live endpoint check skipped by policy")

    return failures


def main(argv):
    directory_src = argv[1] if len(argv) > 1 else "x402/directory.json"
    url_base = None
    max_age_days = 7
    i = 2
    while i < len(argv):
        if argv[i] == "--url-base" and i + 1 < len(argv):
            url_base = argv[i + 1]
            i += 2
        elif argv[i] == "--max-age-days" and i + 1 < len(argv):
            max_age_days = int(argv[i + 1])
            i += 2
        else:
            print(f"unknown arg: {argv[i]}", file=sys.stderr)
            return 2

    if directory_src.startswith("http"):
        status, body = fetch(directory_src)
        if status != 200:
            print(f"FAIL: cannot fetch directory: {directory_src} (HTTP {status})")
            return 1
        directory = json.loads(body.decode("utf-8"))
    else:
        with open(directory_src, encoding="utf-8") as f:
            directory = json.load(f)

    print(f"CWI Verified x402 Directory v{directory.get('version', '?')} — "
          f"{len(directory.get('listings', []))} listing(s), max_age {max_age_days}d"
          + (f", url-base {url_base}" if url_base else ""))

    today = datetime.date.today()
    all_failures = []
    for lst in directory.get("listings", []):
        service = lst.get("service", "<unnamed>")
        failures = check_listing(lst, url_base, max_age_days, today)
        if failures:
            print(f"FAIL {service}")
            all_failures.extend(failures)
        else:
            print(f"OK   {service} (status={lst.get('status')}, "
                  f"last_reverified={lst.get('last_reverified')})")

    if all_failures:
        print(f"\n{len(all_failures)} failure(s):")
        for f in all_failures:
            print(f"  - {f}")
        return 1
    print("\nAll listings verified green.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
