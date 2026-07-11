import argparse
import json
import re
from pathlib import Path

REQUIRED = {"prompt.txt": 25, "commands.log": 25, "git-status.txt": 20, "redactions.txt": 15, "environment.txt": 15}
SECRET_PATTERNS = [
    re.compile(r"(gh" + "o_|s" + "k-|xox[baprs]-|A" + "KIA[0-9A-Z]{16})"),
    re.compile(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*\S+"),
]


def scan_file(path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if any(p.search(line) for p in SECRET_PATTERNS):
            hits.append({"file": str(path), "line": i, "text": "[redacted secret-like line]"})
    return hits


def check_bundle(root):
    root = Path(root)
    present = []
    missing = []
    score = 0
    for fn, pts in REQUIRED.items():
        if (root / fn).exists():
            present.append(fn)
            score += pts
        else:
            missing.append(fn)
    secret_hits = []
    for path in root.rglob("*"):
        if path.is_file() and path.stat().st_size < 500000:
            secret_hits.extend(scan_file(path))
    penalty = min(40, len(secret_hits) * 10)
    score = max(0, score - penalty)
    return {
        "score": score,
        "present": present,
        "missing": missing,
        "secret_hits": secret_hits,
        "status": "pass" if score >= 80 and not secret_hits else "review",
    }


def render_text(result):
    lines = [f"Score: {result['score']}/100, status: {result['status']}"]
    if result["present"]:
        lines.append("Present: " + ", ".join(result["present"]))
    if result["missing"]:
        lines.append("Missing: " + ", ".join(result["missing"]))
    if result["secret_hits"]:
        lines.append(f"Secret-like hits: {len(result['secret_hits'])}")
        for hit in result["secret_hits"]:
            lines.append(f"- {hit['file']}:{hit['line']} {hit['text']}")
    return "\n".join(lines)


def render_markdown(result):
    lines = [
        "# Agent session repro bundle report",
        "",
        f"- Score: {result['score']}/100",
        f"- Status: {result['status']}",
        f"- Present files: {', '.join(result['present']) or 'none'}",
        f"- Missing files: {', '.join(result['missing']) or 'none'}",
        f"- Secret-like hits: {len(result['secret_hits'])}",
    ]
    if result["secret_hits"]:
        lines.extend(["", "| File | Line | Evidence |", "| --- | ---: | --- |"])
        for hit in result["secret_hits"]:
            lines.append(f"| {hit['file']} | {hit['line']} | {hit['text']} |")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check whether an AI agent session repro bundle is complete and safe to share.")
    ap.add_argument("bundle")
    ap.add_argument("--json", action="store_true", help="Deprecated alias for --format json")
    ap.add_argument("--format", choices=["text", "json", "markdown"], default="text", help="Report output format")
    ns = ap.parse_args(argv)
    result = check_bundle(ns.bundle)

    fmt = "json" if ns.json else ns.format
    if fmt == "json":
        print(json.dumps(result, indent=2))
    elif fmt == "markdown":
        print(render_markdown(result))
    else:
        print(render_text(result))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
