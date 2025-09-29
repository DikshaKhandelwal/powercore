#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, re, subprocess, sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SPARKS = "▁▂▃▄▅▆▇█"


def sparkline(samples: List[int]) -> str:
    if not samples:
        return ""
    high = max(samples)
    if not high:
        return ""
    scale = len(SPARKS) - 1
    return "".join(SPARKS[int((v / high) * scale)] for v in samples)


def load_history(source: str, path: Optional[str]) -> List[Tuple[str, Optional[int], str]]:
    records: List[Tuple[str, Optional[int], str]] = []
    try:
        if source == "bash":
            hist_path = Path(path or os.path.expanduser("~/.bash_history"))
            if not hist_path.exists():
                return []
            text = hist_path.read_text(encoding="utf-8", errors="ignore")
            last_ts: Optional[int] = None
            for raw in text.splitlines():
                line = raw.strip()
                if not line:
                    continue
                if line.startswith("#") and line[1:].strip().isdigit():
                    last_ts = int(line[1:].strip())
                    continue
                records.append((line, last_ts, "you"))
        elif source == "git":
            cwd = Path(path) if path else Path.cwd()
            result = subprocess.run(["git", "-C", str(cwd), "log", "--pretty=format:%ct|%an|%s", "-n", "200"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if result.returncode != 0:
                return []
            for row in result.stdout.splitlines():
                parts = row.split("|", 2)
                if len(parts) == 3 and parts[0].isdigit():
                    ts, author, msg = parts
                    records.append((msg, int(ts), author))
        else:
            if not path:
                return []
            file_path = Path(path)
            if not file_path.exists():
                return []
            data = file_path.read_text(encoding="utf-8", errors="ignore")
            for line in data.splitlines():
                line = line.strip()
                if line:
                    records.append((line, None, file_path.name))
    except Exception:
        return []
    return records


def summarize_patterns(records: List[Tuple[str, Optional[int], str]], limit: int) -> Dict[str, object]:
    tokens: Counter[str] = Counter()
    combos: Counter[str] = Counter()
    hourly: Counter[int] = Counter()
    weekday: Counter[str] = Counter()
    actors: Counter[str] = Counter()
    spikes: Counter[str] = Counter()
    for text, ts, actor in records:
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_\-]+", text) if len(w) > 2]
        if words:
            tokens[words[0]] += 1
            for word in words[:5]:
                combos[word] += 1
        if ts:
            dt = datetime.fromtimestamp(ts)
            hourly[dt.hour] += 1
            weekday[dt.strftime("%A")] += 1
            spikes[f"{dt.strftime('%A')}@{dt.hour:02d}"] += 1
        if actor:
            actors[actor] += 1
    timeline = sorted(ts for _, ts, _ in records if ts)
    longest_gap = max((b - a for a, b in zip(timeline, timeline[1:])), default=0)
    return {
        "top_commands": tokens.most_common(limit),
        "top_tokens": combos.most_common(limit),
        "peak_hour": hourly.most_common(1)[0] if hourly else None,
        "peak_day": weekday.most_common(1)[0] if weekday else None,
        "top_actor": actors.most_common(1)[0] if actors else None,
        "spikes": spikes.most_common(limit),
        "hourly_series": [hourly.get(i, 0) for i in range(24)],
        "longest_gap": longest_gap,
    }


def describe_gap(seconds: int) -> str:
    if not seconds:
        return ""
    hours = seconds / 3600
    if hours < 1:
        return f"{int(seconds // 60)} minutes"
    if hours < 24:
        return f"{hours:.1f} hours"
    return f"{hours / 24:.1f} days"


def render_prophet_text(source: str, summary: Dict[str, object]) -> List[str]:
    insights: List[str] = []
    if summary["top_commands"]:
        cmd, count = summary["top_commands"][0]
        insights.append(f"🔮 Signature move: `{cmd}` appears {count} times.")
    if summary["peak_hour"]:
        hour, count = summary["peak_hour"]
        if hour >= 12:
            label = "pm"; hr = hour - 12 if hour > 12 else 12
        else:
            label = "am"; hr = hour if hour else 12
        insights.append(f"⚡ Peak energy: {hr}{label} with {count} bursts.")
    if summary["peak_day"]:
        day, count = summary["peak_day"]
        insights.append(f"📅 Most active day: {day} ({count} sessions).")
    if summary["spikes"]:
        slot, score = summary["spikes"][0]
        insights.append(f"🌠 Spike window: {slot} ({score} hits).")
    if source == "git" and summary["top_actor"]:
        actor, count = summary["top_actor"]
        insights.append(f"👥 Loudest voice: {actor} ({count} commits).")
    if source == "bash" and summary["top_tokens"]:
        token, count = summary["top_tokens"][0]
        insights.append(f"🌀 Habit loop: `{token}` echoes {count} times.")
    if gap := describe_gap(summary.get("longest_gap", 0)):
        insights.append(f"🕰️ Longest quiet stretch: {gap} of silence.")
    if not insights:
        insights.append("No standout patterns detected—time to create some sparkle.")
    return insights


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="pattern-prophet", description="Reveal behavioral patterns from activity traces")
    p.add_argument("--source", choices=["bash", "git", "file"], default="bash")
    p.add_argument("--path", help="Optional path override (history file, repo path, or generic file)")
    p.add_argument("--limit", type=int, default=5, help="Max items in report")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    def out(text: str) -> None:
        enc = (getattr(sys.stdout, "encoding", None) or "utf-8")
        try:
            sys.stdout.buffer.write((text + "\n").encode(enc, errors="replace"))
        except Exception:
            print(text)
        sys.stdout.flush()

    records = load_history(args.source, args.path)
    if not records:
        out("error: no activity found")
        return 2
    summary = summarize_patterns(records, args.limit)
    insights = render_prophet_text(args.source, summary)
    payload = {"source": args.source, "insights": insights, "stats": summary, "samples": min(len(records), args.limit)}
    if args.format == "json":
        out(json.dumps(payload, indent=2))
    else:
        title = f"Pattern Prophet -> {args.source}"
        out(title)
        out("=" * len(title))
        out("\n".join(insights))
        series = summary.get("hourly_series", [])
        if series:
            out("\nHourly sparkline:\n" + sparkline(series))
        out("\nTop tokens:\n" + "\n".join(f" - {t}: {c}" for t, c in summary["top_tokens"]))
        out(f"\nSamples analyzed: {len(records)} events.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
