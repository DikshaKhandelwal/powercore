from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
import sys
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


class SemanticDiffError(Exception):
    pass


@dataclass
class Unit:
    path: Path
    name: str
    kind: str
    signature: str
    fingerprint: str
    span: Tuple[int, int]
    order: int
    metrics: Dict[str, float]
    source: str
    doc: Optional[str] = None


@dataclass
class DiffEntry:
    unit: Unit
    change: str
    details: Dict[str, float]
    peers: List[str]


@dataclass
class DiffReport:
    added: List[DiffEntry]
    removed: List[DiffEntry]
    modified: List[DiffEntry]
    moved: List[DiffEntry]
    renamed: List[Tuple[DiffEntry, DiffEntry]]
    meta: Dict[str, float]


LANGUAGE_MAP = {".py": "python", ".js": "js", ".ts": "js", ".jsx": "js", ".tsx": "js", ".java": "java", ".go": "go", ".rs": "rust"}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")
    except Exception as exc:
        raise SemanticDiffError(f"Failed to read {path}: {exc}") from exc


def detect_language(path: Path) -> str:
    return LANGUAGE_MAP.get(path.suffix.lower(), "generic")


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def count_branches(text: str) -> int:
    return sum(text.count(token) for token in ("if", "for", "while", "case", "elif", "try", "catch"))


def size_metric(span: Tuple[int, int]) -> int:
    return max(span[1] - span[0], 1)


def extract_python_units(path: Path, text: str) -> List[Unit]:
    try: tree = ast.parse(text)
    except SyntaxError as exc: raise SemanticDiffError(f"Python parse error in {path}: {exc}") from exc
    units: List[Unit] = []; order = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name; kind = "async_function" if isinstance(node, ast.AsyncFunctionDef) else ("class" if isinstance(node, ast.ClassDef) else "function")
            start = getattr(node, "lineno", 1); end = getattr(node, "end_lineno", start)
            args = len(node.args.args) if hasattr(node, "args") else 0; signature = f"{name}/{args}"
            doc = ast.get_docstring(node); body_text = ast.get_source_segment(text, node) or ""
            fingerprint = stable_hash(ast.dump(node, include_attributes=False)); metrics = {"size": float(size_metric((start, end))), "branches": float(count_branches(body_text)), "doc": 1.0 if doc else 0.0}
            units.append(Unit(path, name, kind, signature, fingerprint, (start, end), order, metrics, body_text, doc)); order += 1
        elif isinstance(node, ast.Assign) and getattr(node, "targets", None):
            target = node.targets[0]
            if isinstance(target, ast.Name):
                name = target.id; start = getattr(node, "lineno", 1); end = getattr(node, "end_lineno", start)
                snippet = ast.get_source_segment(text, node) or ""; fingerprint = stable_hash(ast.dump(node, include_attributes=False))
                metrics = {"size": float(size_metric((start, end))), "branches": float(count_branches(snippet)), "doc": 0.0}
                units.append(Unit(path, name, "assignment", name, fingerprint, (start, end), order, metrics, snippet, None)); order += 1
    return units


def extract_generic_units(path: Path, text: str) -> List[Unit]:
    units: List[Unit] = []; order = 0; lines = text.splitlines(); buffer: List[str] = []; head = ""; start = 1
    for idx, line in enumerate(lines, 1):
        striped = line.strip();
        if not striped:
            continue
        trigger = any(striped.startswith(token) for token in ("function", "def", "class", "struct", "impl", "fn")) or striped.endswith("{")
        if trigger and buffer:
            snippet = "\n".join(buffer); fingerprint = stable_hash(snippet); name = head or f"block_{order}"
            metrics = {"size": float(len(buffer)), "branches": float(count_branches(snippet)), "doc": 1.0 if '"""' in snippet or "///" in snippet else 0.0}
            units.append(Unit(path, name, "block", head or name, fingerprint, (start, idx - 1), order, metrics, snippet, None)); buffer = []
        if trigger:
            head = striped.split()[0] if striped else f"block_{order}"; start = idx
        buffer.append(line)
    if buffer:
        snippet = "\n".join(buffer); fingerprint = stable_hash(snippet); name = head or f"block_{order}"
        metrics = {"size": float(len(buffer)), "branches": float(count_branches(snippet)), "doc": 1.0 if '"""' in snippet or "///" in snippet else 0.0}
        units.append(Unit(path, name, "block", head or name, fingerprint, (start, len(lines)), order, metrics, snippet, None))
    return units


def load_units(path: Path) -> List[Unit]:
    text = read_text(path); lang = detect_language(path)
    return extract_python_units(path, text) if lang == "python" else extract_generic_units(path, text)


def token_bag(text: str) -> List[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9_]+", text)]


def unit_similarity(left: Unit, right: Unit) -> float:
    if left.fingerprint == right.fingerprint: return 1.0
    l_tokens, r_tokens = token_bag(left.source), token_bag(right.source)
    if not l_tokens or not r_tokens: return 0.0
    left_set, right_set = set(l_tokens), set(r_tokens); union = len(left_set | right_set)
    return len(left_set & right_set) / union if union else 0.0


def metric_delta(left: Unit, right: Unit) -> Dict[str, float]:
    keys = left.metrics.keys() | right.metrics.keys()
    return {**{f"{key}_left": float(left.metrics.get(key, 0.0)) for key in keys}, **{f"{key}_right": float(right.metrics.get(key, 0.0)) for key in keys}, **{f"{key}_delta": float(right.metrics.get(key, 0.0) - left.metrics.get(key, 0.0)) for key in keys}}


def aggregate_metrics(units: Sequence[Unit]) -> Dict[str, Dict[str, float]]:
    summary: Dict[str, Dict[str, float]] = {}
    for unit in units:
        bucket = summary.setdefault(unit.kind, {"count": 0.0, "size": 0.0, "branches": 0.0, "doc": 0.0}); bucket["count"] += 1.0; bucket["size"] += unit.metrics.get("size", 0.0)
        bucket["branches"] += unit.metrics.get("branches", 0.0); bucket["doc"] += unit.metrics.get("doc", 0.0)
    return summary


def compare_metric_maps(left: Dict[str, Dict[str, float]], right: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    delta: Dict[str, Dict[str, float]] = {}; keys = set(left) | set(right)
    for kind in keys:
        left_bucket = left.get(kind, {"count": 0.0, "size": 0.0, "branches": 0.0, "doc": 0.0}); right_bucket = right.get(kind, {"count": 0.0, "size": 0.0, "branches": 0.0, "doc": 0.0})
        delta[kind] = {metric: float(right_bucket.get(metric, 0.0) - left_bucket.get(metric, 0.0)) for metric in {"count", "size", "branches", "doc"}}
    return delta


def build_entry(unit: Unit, change: str, details: Dict[str, float], peers: Optional[List[str]] = None) -> DiffEntry:
    return DiffEntry(unit, change, details, peers or [])


def diff_units(left_units: Sequence[Unit], right_units: Sequence[Unit], similarity_threshold: float = 0.6) -> DiffReport:
    left_map = {(u.kind, u.name): u for u in left_units}; right_map = {(u.kind, u.name): u for u in right_units}
    added: List[DiffEntry] = []; removed: List[DiffEntry] = []; modified: List[DiffEntry] = []; moved: List[DiffEntry] = []; renamed: List[Tuple[DiffEntry, DiffEntry]] = []
    seen_right: Dict[Tuple[str, str], bool] = {}
    for key, left in left_map.items():
        right = right_map.get(key)
        if right:
            seen_right[key] = True
            if left.fingerprint != right.fingerprint:
                details = metric_delta(left, right); details["similarity"] = unit_similarity(left, right)
                modified.append(build_entry(right, "modified", details, [left.name]))
            elif left.order != right.order:
                moved.append(build_entry(right, "moved", {"from": float(left.order), "to": float(right.order)}, [left.name]))
        else:
            removed.append(build_entry(left, "removed", dict(left.metrics), []))
    for key, right in right_map.items():
        if key not in seen_right:
            added.append(build_entry(right, "added", dict(right.metrics), []))
    for candidate in list(removed):
        score, match = max(((unit_similarity(candidate.unit, r.unit), r) for r in added), default=(0.0, None), key=lambda item: item[0])
        if match and score >= similarity_threshold:
            details = metric_delta(candidate.unit, match.unit); details["similarity"] = score
            renamed.append((build_entry(candidate.unit, "renamed-from", details, [match.unit.name]), build_entry(match.unit, "renamed-to", details, [candidate.unit.name])))
            removed.remove(candidate); added.remove(match)
    total_units = len(left_units) + len(right_units)
    change_score = len(added) + len(removed) + len(modified) + len(moved) + len(renamed)
    coverage = change_score / total_units if total_units else 0.0
    meta = {"left_units": float(len(left_units)), "right_units": float(len(right_units)), "change_score": float(change_score), "coverage": coverage}
    left_summary = aggregate_metrics(left_units)
    right_summary = aggregate_metrics(right_units)
    meta["kind_summary_left"], meta["kind_summary_right"], meta["kind_delta"] = left_summary, right_summary, compare_metric_maps(left_summary, right_summary)
    return DiffReport(added, removed, modified, moved, renamed, meta)


def summarize_entry(entry: DiffEntry) -> str:
    span = f"{entry.unit.span[0]}-{entry.unit.span[1]}"
    metrics = ", ".join(f"{k}={v:.2f}" for k, v in sorted(entry.details.items()) if not k.endswith("_left") and not k.endswith("_right"))
    peer_hint = f" -> {'; '.join(entry.peers)}" if entry.peers else ""; metric_part = f" ({metrics})" if metrics else ""
    return f"{entry.change.upper()}: {entry.unit.path.name}:{span} {entry.unit.kind} {entry.unit.name}{peer_hint}{metric_part}"


def generate_explanations(report: DiffReport, limit: int = 5) -> List[str]:
    pool: List[Tuple[float, str]] = []
    pool += [(abs(e.details.get("branches_delta", 0.0)) + abs(e.details.get("size_delta", 0.0)), f"{e.unit.name} changed structure with delta {abs(e.details.get('branches_delta', 0.0)) + abs(e.details.get('size_delta', 0.0)):.1f}") for e in report.modified]
    pool += [(pair[1].details.get("similarity", 0.0), f"{pair[0].unit.name} renamed to {pair[1].unit.name}, similarity {pair[1].details.get('similarity', 0.0):.2f}") for pair in report.renamed]
    pool += [(e.details.get("branches", 0.0) + e.details.get("size", 0.0), f"New {e.unit.kind} {e.unit.name} with size {e.details.get('size', 0.0):.1f}") for e in report.added]
    pool += [(e.details.get("branches", 0.0) + e.details.get("size", 0.0), f"Removed {e.unit.kind} {e.unit.name} removing size {e.details.get('size', 0.0):.1f}") for e in report.removed]
    pool.sort(key=lambda item: item[0], reverse=True)
    return [text for _, text in pool[:limit]]


def report_to_dict(report: DiffReport) -> Dict[str, object]:
    entry = lambda e: {"path": str(e.unit.path), "name": e.unit.name, "kind": e.unit.kind, "span": e.unit.span, "change": e.change, "details": e.details, "peers": e.peers}
    return {"added": [entry(e) for e in report.added], "removed": [entry(e) for e in report.removed], "modified": [entry(e) for e in report.modified], "moved": [entry(e) for e in report.moved], "renamed": [{"from": entry(a), "to": entry(b)} for a, b in report.renamed], "meta": report.meta}


def render_text(report: DiffReport, explanations: bool, sections: Sequence[str]) -> str:
    parts = [line for key, entries in (("added", report.added), ("removed", report.removed), ("modified", report.modified), ("moved", report.moved)) if key in sections and entries for line in ([f"[{key.upper()}]"] + [summarize_entry(e) for e in entries])]
    if "renamed" in sections and report.renamed:
        parts += ["[RENAMED]"] + [f"RENAMED: {left.unit.name} -> {right.unit.name} ({right.details.get('similarity', 0.0):.2f})" for left, right in report.renamed]
    if explanations:
        tips = generate_explanations(report)
        if tips:
            parts += ["[EXPLAIN]"] + tips
    return "No semantic differences detected." if not parts else "\n".join(parts)


def format_meta(meta: Dict[str, float]) -> str:
    lines: List[str] = ["[META]"]
    for key, value in sorted(meta.items()):
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for sub_key, sub_value in sorted(value.items()):
                if isinstance(sub_value, dict):
                    lines.append(f"  {sub_key}:"); lines.extend(f"    {metric}: {metric_value:.2f}" for metric, metric_value in sorted(sub_value.items()))
                else:
                    lines.append(f"  {sub_key}: {sub_value:.2f}")
        else:
            lines.append(f"{key}: {value:.2f}")
    return "\n".join(lines)


def iter_sources(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root; return
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if path.is_file():
                yield path


def gather_units(paths: Sequence[Path]) -> List[Unit]:
    units: List[Unit] = []
    for path in paths:
        for source in iter_sources(path):
            with suppress(SemanticDiffError):
                units.extend(load_units(source))
    return units


def compute_diff(left_path: Path, right_path: Path) -> DiffReport:
    if not left_path.exists(): raise SemanticDiffError(f"Left path {left_path} does not exist")
    if not right_path.exists(): raise SemanticDiffError(f"Right path {right_path} does not exist")
    return diff_units(gather_units([left_path]), gather_units([right_path]))


def count_executable_lines(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#"))


def normalize_sections(text: str) -> List[str]:
    allowed = ["added", "removed", "modified", "moved", "renamed"]; sections = [part.strip().lower() for part in text.split(",") if part.strip().lower() in allowed]; return sections or allowed


def parse_args(argv: Optional[Sequence[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="semantic-diff",
        description="Semantic-aware diff that understands code structure",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("left", help="Path to the original file or directory"); parser.add_argument("right", help="Path to the modified file or directory")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--sections", default="added,removed,modified,moved,renamed", help="Sections to include")
    parser.add_argument("--explain", action="store_true", help="Include natural language insights"); parser.add_argument("--limit", type=int, default=5, help="Max number of explanations")
    parser.add_argument("--strict", action="store_true", help="Enforce 250-line budget at runtime"); parser.add_argument("--meta", action="store_true", help="Print aggregate metric summary")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    left_path, right_path = Path(args.left), Path(args.right)
    try:
        report = compute_diff(left_path, right_path)
    except SemanticDiffError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    sections = normalize_sections(args.sections)
    if args.format == "json":
        payload = report_to_dict(report)
        if args.explain:
            payload["explanations"] = generate_explanations(report, args.limit)
        print(json.dumps(payload, indent=2))
    else:
        print((text := render_text(report, args.explain, sections)) + ("" if not args.meta else "\n" + format_meta(report.meta)))
    if args.strict:
        lines = count_executable_lines(Path(__file__))
        if lines != 250:
            print(f"warning: expected 250 executable lines, found {lines}", file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
