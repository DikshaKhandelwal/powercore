#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, sys, time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

STORE = Path(os.path.expanduser("~/.focuscli.jsonl"))


@dataclass
class Session:
    start: float
    end: Optional[float]
    topic: str
    notes: str = ""

    def duration(self) -> float:
        return (self.end or time.time()) - self.start


def load_sessions() -> List[Session]:
    sessions: List[Session] = []
    if STORE.exists():
        for line in STORE.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                row = json.loads(line)
                sessions.append(Session(**row))
            except Exception:
                continue
    return sessions


def save_session(s: Session) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    with STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(s)) + "\n")


def start_session(topic: str, notes: str) -> Session:
    s = Session(start=time.time(), end=None, topic=topic, notes=notes)
    save_session(s)
    return s


def stop_session() -> Optional[Session]:
    sessions = load_sessions()
    for i in range(len(sessions) - 1, -1, -1):
        if sessions[i].end is None:
            sessions[i].end = time.time()
            # rewrite file
            with STORE.open("w", encoding="utf-8") as f:
                for s in sessions:
                    f.write(json.dumps(asdict(s)) + "\n")
            return sessions[i]
    return None


def stats(days: int) -> dict:
    sessions = load_sessions()
    cutoff = time.time() - days * 86400
    total = 0.0
    by_topic: dict[str, float] = {}
    streak = 0
    last_day = None
    per_day: dict[str, float] = {}
    for s in sessions:
        if s.end is None:
            continue
        if s.end < cutoff:
            continue
        dur = s.end - s.start
        total += dur
        by_topic[s.topic] = by_topic.get(s.topic, 0.0) + dur
        day = datetime.fromtimestamp(s.end).strftime("%Y-%m-%d")
        per_day[day] = per_day.get(day, 0.0) + dur
    # compute streak of consecutive days with any focus
    for day in sorted(per_day.keys()):
        if last_day is None:
            streak = 1; last_day = day; continue
        prev = datetime.strptime(last_day, "%Y-%m-%d")
        cur = datetime.strptime(day, "%Y-%m-%d")
        if (cur - prev).days == 1:
            streak += 1
        else:
            streak = 1
        last_day = day
    top = sorted(by_topic.items(), key=lambda kv: kv[1], reverse=True)[:5]
    return {"total_hours": total / 3600.0, "top_topics": top, "streak_days": streak, "days": per_day}


def render_stats(d: dict) -> str:
    lines = ["FocusCLI Stats", "============="]
    lines.append(f"Total hours: {d['total_hours']:.2f}")
    if d.get("streak_days"):
        lines.append(f"Current streak: {d['streak_days']} days")
    if d.get("top_topics"):
        lines.append("Top topics:")
        for topic, sec in d["top_topics"]:
            lines.append(f" - {topic}: {sec/3600:.2f}h")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="focuscli", description="Distraction killer & flow tracker")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_start = sub.add_parser("start", help="Start a focus session")
    p_start.add_argument("topic")
    p_start.add_argument("--notes", default="")
    sub.add_parser("stop", help="Stop the last open session")
    p_stats = sub.add_parser("stats", help="Show stats")
    p_stats.add_argument("--days", type=int, default=7)
    p_export = sub.add_parser("export", help="Export sessions as JSONL")

    args = p.parse_args(argv)
    if args.cmd == "start":
        s = start_session(args.topic, args.notes)
        print(f"Started: {args.topic} @ {datetime.fromtimestamp(s.start).isoformat(timespec='seconds')}")
        return 0
    if args.cmd == "stop":
        s = stop_session()
        if not s:
            print("No active session found.")
            return 2
        print(f"Stopped: {s.topic} (+{(s.end-s.start)/60:.1f} min)")
        return 0
    if args.cmd == "stats":
        d = stats(args.days)
        print(render_stats(d))
        return 0
    if args.cmd == "export":
        if not STORE.exists():
            print("No sessions yet."); return 0
        print(STORE.read_text(encoding="utf-8", errors="ignore"))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
