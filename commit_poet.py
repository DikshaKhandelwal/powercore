#!/usr/bin/env python
from __future__ import annotations
import argparse, json, random, re, sys
from collections import Counter
from typing import List, Optional, Tuple

FALLBACK = ["code", "dream", "merge", "spark", "flow", "pulse", "craft", "data", "light", "storm"]
MOOD_MAP = {"fix": "Fixer mode", "bug": "Bug hunter", "refactor": "Refactor bard", "test": "Test guardian", "feature": "Feature forger", "doc": "Documentation muse"}


def extract_keywords(text: str, limit: int = 30) -> List[str]:
    tokens = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", text)]
    counts = Counter(tokens)
    ranked = [w for w, _ in counts.most_common(limit)]
    return ranked or FALLBACK


def syllables(word: str) -> int:
    pieces = re.findall(r"[aeiouy]+", word.lower())
    return max(1, len(pieces))


def compose_line(target: int, words: List[str]) -> str:
    pool = list(dict.fromkeys(words + FALLBACK))
    random.shuffle(pool)
    chosen: List[str] = []
    score = 0
    for w in pool:
        val = syllables(w)
        if score + val <= target:
            chosen.append(w)
            score += val
        if score == target:
            break
    return " ".join(chosen) if chosen else random.choice(FALLBACK)


def infer_mood(words: List[str]) -> str:
    for key, label in MOOD_MAP.items():
        if any(key in w for w in words):
            return label
    return "Inventive wanderer"


def build_poem(style: str, words: List[str]) -> Tuple[str, List[str]]:
    if style == "haiku":
        lines = [compose_line(5, words), compose_line(7, words), compose_line(5, words)]
        title = "Commit Haiku"
    elif style == "limerick":
        pattern = [9, 9, 6, 6, 9]
        lines = [compose_line(t, words) for t in pattern]
        title = "Commit Limerick"
    else:
        pattern = [8, 8, 8]
        lines = [compose_line(t, words) for t in pattern]
        title = "Commit Freeform"
    return title, lines


def read_diff(path: Optional[str]) -> str:
    if path:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    data = sys.stdin.read()
    if data:
        return data
    raise ValueError("no diff input provided")


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="commit-poet", description="Generate lyrical commit messages from diffs")
    p.add_argument("--style", choices=["haiku", "limerick", "free"], default="haiku")
    p.add_argument("--path", help="Diff file to read; defaults to STDIN")
    p.add_argument("--seed", type=int, help="Seed for deterministic poetry")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)
    try:
        diff = read_diff(args.path)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    words = extract_keywords(diff)
    title, lines = build_poem(args.style, words)
    mood = infer_mood(words)
    payload = {"style": args.style, "title": title, "lines": lines, "keywords": words[:10], "mood": mood}

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(title)
        print("-" * len(title))
        print("\n".join(s.capitalize() for s in lines))
        print(f"\nMood: {mood}")
        print("Keywords: " + ", ".join(words[:5]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
