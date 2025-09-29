#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

TS_PATTERNS = [
    # 2025-09-29 12:34:56,789 or 2025-09-29T12:34:56Z
    (re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[,\.]\d+)?Z?)"), "%Y-%m-%d %H:%M:%S"),
    # 29/09/2025 12:34:56
    (re.compile(r"^(?P<ts>\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})"), "%d/%m/%Y %H:%M:%S"),
    # Sep 29 12:34:56
    (re.compile(r"^(?P<ts>[A-Z][a-z]{2} \d{1,2} \d{2}:\d{2}:\d{2})"), "%b %d %H:%M:%S"),
]
LEVEL_RE = re.compile(r"\b(DEBUG|INFO|WARN|WARNING|ERROR|ERR|CRITICAL|FATAL)\b", re.I)
NUM_RE = re.compile(r"\b\d+\b")
UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HEX_RE = re.compile(r"\b0x[0-9a-f]+\b", re.I)
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def parse_ts(text: str, today: Optional[datetime]) -> Optional[datetime]:
    for pat, _fmt in TS_PATTERNS:
        m = pat.search(text)
        if not m:
            continue
        raw = m.group("ts").replace("T", " ").rstrip("Z").replace(",", ".")
        # try several granularities
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%b %d %H:%M:%S"):
            try:
                dt = datetime.strptime(raw, fmt)
                # if format without year (e.g., syslog), assume current year
                if fmt == "%b %d %H:%M:%S" and today is not None:
                    dt = dt.replace(year=today.year)
                return dt
            except Exception:
                pass
    return None


def normalize_message(line: str) -> str:
    line = UUID_RE.sub("<uuid>", line)
    line = HEX_RE.sub("<hex>", line)
    line = IP_RE.sub("<ip>", line)
    line = NUM_RE.sub("<n>", line)
    return re.sub(r"\s+", " ", line).strip()


def detect_level(line: str) -> str:
    m = LEVEL_RE.search(line)
    if not m:
        return "INFO"  # default neutral
    level = m.group(1).upper()
    return {"ERR": "ERROR", "WARNING": "WARN"}.get(level, level)


def iter_lines(paths: List[str]) -> Iterable[Tuple[Optional[datetime], str]]:
    today = datetime.now()
    if not paths:
        for raw in sys.stdin:
            line = raw.rstrip("\n")
            yield parse_ts(line, today), line
        return
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for raw in f:
                    line = raw.rstrip("\n")
                    yield parse_ts(line, today), line
        except Exception:
            continue


def within(dt: Optional[datetime], since: Optional[datetime], until: Optional[datetime]) -> bool:
    if dt is None:
        return since is None and until is None
    if since and dt < since:
        return False
    if until and dt > until:
        return False
    return True


def summarize(paths: List[str], top: int, since: Optional[str], until: Optional[str]) -> Dict[str, object]:
    def parse_rel(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        s = s.strip()
        if s.startswith("-") and s.endswith("h"):
            return datetime.now() - timedelta(hours=float(s[1:-1]))
        if s.startswith("-") and s.endswith("m"):
            return datetime.now() - timedelta(minutes=float(s[1:-1]))
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                pass
        return None

    s_dt, u_dt = parse_rel(since), parse_rel(until)
    levels = Counter()
    patterns = Counter()
    by_level_patterns: Dict[str, Counter] = defaultdict(Counter)
    first_ts: Optional[datetime] = None
    last_ts: Optional[datetime] = None
    total = 0
    for ts, line in iter_lines(paths):
        if not within(ts, s_dt, u_dt):
            continue
        total += 1
        if ts:
            first_ts = ts if first_ts is None else min(first_ts, ts)
            last_ts = ts if last_ts is None else max(last_ts, ts)
        lvl = detect_level(line)
        levels[lvl] += 1
        norm = normalize_message(line)
        patterns[norm] += 1
        by_level_patterns[lvl][norm] += 1

    top_patterns = patterns.most_common(top)
    top_err = by_level_patterns.get("ERROR", Counter()).most_common(top)
    density = None
    if first_ts and last_ts and last_ts > first_ts:
        duration = (last_ts - first_ts).total_seconds() / 60.0
        density = total / max(duration, 1e-3)

    return {
        "total_lines": total,
        "levels": levels,
        "top_patterns": top_patterns,
        "top_errors": top_err,
        "first_ts": first_ts.isoformat() if first_ts else None,
        "last_ts": last_ts.isoformat() if last_ts else None,
        "lines_per_min": density,
    }


def render_text(summary: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("LogSage Summary")
    lines.append("===============")
    lines.append(f"Total lines: {summary['total_lines']}")
    lvl = summary["levels"]
    if isinstance(lvl, Counter):
        dist = ", ".join(f"{k}:{v}" for k, v in lvl.most_common())
        lines.append(f"Levels: {dist}")
    if summary.get("first_ts") or summary.get("last_ts"):
        lines.append(f"Window: {summary.get('first_ts')} → {summary.get('last_ts')}")
    if summary.get("lines_per_min"):
        lines.append(f"Throughput: {summary['lines_per_min']:.2f} lines/min")
    lines.append("")
    lines.append("Top patterns:")
    for pat, cnt in summary.get("top_patterns", [])[:10]:
        lines.append(f" - {cnt}× {pat}")
    if summary.get("top_errors"):
        lines.append("")
        lines.append("Top errors:")
        for pat, cnt in summary.get("top_errors", [])[:10]:
            lines.append(f" - {cnt}× {pat}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="logsage", description="Log whisperer & summarizer")
    p.add_argument("paths", nargs="*", help="Log files (defaults to STDIN)")
    p.add_argument("--top", type=int, default=10, help="Top N patterns to show")
    p.add_argument("--since", help="Start time (YYYY-MM-DD or -6h/-30m)")
    p.add_argument("--until", help="End time (YYYY-MM-DD or -6h/-30m)")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args(argv)

    summary = summarize(args.paths, args.top, args.since, args.until)
    if args.format == "json":
        def conv(o):
            if isinstance(o, Counter):
                return dict(o)
            return o
        print(json.dumps(summary, default=conv, indent=2))
    else:
        print(render_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
