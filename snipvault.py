#!/usr/bin/env python
from __future__ import annotations
import argparse, json, os, re, sys, uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

VAULT = Path(os.path.expanduser("~/.snipvault.jsonl"))


@dataclass
class Snip:
    id: str
    tags: List[str]
    lang: str
    text: str


def load_all() -> List[Snip]:
    out: List[Snip] = []
    if VAULT.exists():
        for line in VAULT.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                row = json.loads(line)
                out.append(Snip(**row))
            except Exception:
                continue
    return out


def save_append(s: Snip) -> None:
    VAULT.parent.mkdir(parents=True, exist_ok=True)
    with VAULT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(s)) + "\n")


def add_snip(text: str, tags: List[str], lang: str) -> Snip:
    s = Snip(id=str(uuid.uuid4()), tags=tags, lang=lang, text=text)
    save_append(s)
    return s


def search_snips(q: str, tags: List[str], lang: Optional[str]) -> List[Snip]:
    items = load_all()
    def match(s: Snip) -> bool:
        if q and not (q.lower() in s.text.lower() or q.lower() in " ".join(s.tags).lower()):
            return False
        if tags and not set(t.lower() for t in tags).issubset(set(t.lower() for t in s.tags)):
            return False
        if lang and s.lang.lower() != lang.lower():
            return False
        return True
    return [s for s in items if match(s)]


def delete_snip(sid: str) -> bool:
    items = load_all()
    new = [s for s in items if s.id != sid]
    if len(new) == len(items):
        return False
    with VAULT.open("w", encoding="utf-8") as f:
        for s in new:
            f.write(json.dumps(asdict(s)) + "\n")
    return True


def list_snips(limit: int) -> List[Snip]:
    return load_all()[-limit:]


def render_list(items: List[Snip]) -> str:
    lines = ["SnipVault", "========="]
    for s in items:
        tags = ", ".join(s.tags)
        preview = re.sub(r"\s+", " ", s.text.strip())[:80]
        lines.append(f"- {s.id[:8]} [{s.lang}] ({tags}): {preview}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="snipvault", description="Snippet brain in your terminal")
    sub = p.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add", help="Add a new snippet")
    p_add.add_argument("text")
    p_add.add_argument("--tag", action="append", default=[])
    p_add.add_argument("--lang", default="text")

    p_find = sub.add_parser("find", help="Search snippets")
    p_find.add_argument("--q", default="")
    p_find.add_argument("--tag", action="append", default=[])
    p_find.add_argument("--lang")

    p_del = sub.add_parser("rm", help="Delete a snippet by id")
    p_del.add_argument("sid")

    p_ls = sub.add_parser("ls", help="List recent snippets")
    p_ls.add_argument("--limit", type=int, default=10)

    args = p.parse_args(argv)

    if args.cmd == "add":
        s = add_snip(args.text, args.tag, args.lang)
        print(f"Saved {s.id}")
        return 0
    if args.cmd == "find":
        items = search_snips(args.q, args.tag, args.lang)
        print(render_list(items))
        return 0
    if args.cmd == "rm":
        ok = delete_snip(args.sid)
        print("Removed" if ok else "Not found")
        return 0
    if args.cmd == "ls":
        print(render_list(list_snips(args.limit)))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
