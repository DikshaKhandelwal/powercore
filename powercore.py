from __future__ import annotations
import argparse, sys
from pathlib import Path
from typing import Optional, Sequence
import semantic_diff
import procgen_art as procgen_mod
import pattern_prophet as prophet_mod
import commit_poet as poet_mod
import data_sanity as datasanity_mod
import logsage as logsage_mod
import focuscli as focus_mod
import snipvault as snip_mod


def count_exec(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#"))


def ensure_strict(flag: bool) -> Optional[int]:
    if not flag:
        return None
    lines = count_exec(Path(__file__))
    if lines > 250:
        print(f"warning: exceeded 250 executable lines, found {lines}", file=sys.stderr)
        return 3
    return None


def delegate_pattern_prophet(argv: Sequence[str]) -> int:
    return prophet_mod.main(list(argv))


def delegate_commit_poet(argv: Sequence[str]) -> int:
    return poet_mod.main(list(argv))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="powercore", description="PowerMinimalCodeCore toolkit")
    parser.add_argument("--strict", action="store_true", help="Enforce 250-line budget")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("semantic-diff", help="Semantic-aware diff (delegates to semantic_diff)")
    sub.add_parser("pattern-prophet", help="Reveal behavioral patterns (delegates)")
    sub.add_parser("commit-poet", help="Generate lyrical commit messages (delegates)")
    sub.add_parser("procgen-art", help="Generative ASCII art (delegates)")
    sub.add_parser("data-sanity", help="Data sanity checker/cleaner (delegates)")
    sub.add_parser("logsage", help="Log whisperer & summarizer (delegates)")
    sub.add_parser("focuscli", help="Distraction killer & flow tracker (delegates)")
    sub.add_parser("snipvault", help="Snippet brain in your terminal (delegates)")
    args, remainder = parser.parse_known_args(argv)
    status = ensure_strict(args.strict)
    if status is not None:
        return status
    if args.command == "semantic-diff":
        return semantic_diff.main(remainder)
    if args.command == "pattern-prophet":
        return delegate_pattern_prophet(remainder)
    if args.command == "commit-poet":
        return delegate_commit_poet(remainder)
    if args.command == "procgen-art":
        return procgen_mod.main(list(remainder))
    if args.command == "data-sanity":
        return datasanity_mod.main(list(remainder))
    if args.command == "logsage":
        return logsage_mod.main(list(remainder))
    if args.command == "focuscli":
        return focus_mod.main(list(remainder))
    if args.command == "snipvault":
        return snip_mod.main(list(remainder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
