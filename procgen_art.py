from __future__ import annotations
import argparse
import json
import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psutil  # type: ignore
except ImportError:  # pragma: no cover
    psutil = None

LINE_LIMIT = 250
STYLE_PRESETS = {
    "plasma": {"colors": [57, 93, 129, 165, 201], "ramp": " .:-=+*#%@"},
    "waves": {"colors": [18, 19, 20, 32, 33], "ramp": " .~*oOX"},
    "ember": {"colors": [52, 88, 124, 166, 202, 214], "ramp": " `^,:;Il!i><~+_/\\"},
}


def count_exec(text: str) -> int:
    count = 0
    for raw in text.splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            count += 1
    return count


def ensure_strict(flag: bool) -> None:
    if flag and count_exec(Path(__file__).read_text(encoding="utf-8")) != LINE_LIMIT:
        print(f"warning: expected {LINE_LIMIT} executable lines", file=sys.stderr)
        sys.exit(3)


def gather_metrics(previous: Optional[Dict[str, float]]) -> Dict[str, float]:
    now = time.time()
    if psutil:
        cpu = psutil.cpu_percent(interval=None) / 100.0
        vm = psutil.virtual_memory()
        mem = vm.percent / 100.0
        disk = psutil.disk_usage(os.getcwd())
        disk_fill = 1.0 - (disk.free / disk.total if disk.total else 0.0)
        net = psutil.net_io_counters()
        rx, tx = float(net.bytes_recv), float(net.bytes_sent)
    else:
        cpu = (math.sin(now) + 1.0) * 0.5
        mem = (math.cos(now * 0.5) + 1.0) * 0.5
        disk_fill = 0.3 + 0.2 * math.sin(now * 0.2)
        rx = tx = 1e6 + math.sin(now) * 2e5
    if previous:
        dt = max(now - previous["stamp"], 1e-3)
        net_rate = ((rx - previous["rx"]) + (tx - previous["tx"])) / dt
    else:
        net_rate = 0.0
    entropy = (cpu + mem + disk_fill) * 1e6 + rx + tx + now
    return {
        "cpu": max(0.0, min(cpu, 1.0)),
        "mem": max(0.0, min(mem, 1.0)),
        "disk": max(0.0, min(disk_fill, 1.0)),
        "rx": rx,
        "tx": tx,
        "net_rate": max(0.0, net_rate),
        "entropy": entropy,
        "stamp": now,
    }


def render_frame(metrics: Dict[str, float], rng: random.Random, width: int, height: int, style: str, tick: float) -> List[str]:
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS["plasma"])
    colors = preset["colors"]
    ramp = preset["ramp"]
    rows: List[str] = []
    cpu = metrics["cpu"]
    mem = metrics["mem"]
    disk = metrics["disk"]
    net = math.log1p(metrics["net_rate"]/1024.0)
    for y in range(height):
        pieces: List[str] = []
        for x in range(width):
            nx = x / max(width - 1, 1)
            ny = y / max(height - 1, 1)
            wave = math.sin((nx + tick) * math.pi * (1.5 + cpu * 4.0))
            wave += math.cos((ny + tick) * math.pi * (1.0 + mem * 3.0))
            wave += rng.random() * (0.2 + net * 0.1)
            wave += math.sin((nx - ny) * 6.0 + disk * 3.0)
            intensity = (wave + 4.0) / 8.0
            intensity = max(0.0, min(intensity, 1.0))
            index = min(int(intensity * (len(ramp) - 1)), len(ramp) - 1)
            color = colors[min(int(intensity * len(colors)), len(colors) - 1)]
            pieces.append(f"\x1b[38;5;{color}m{ramp[index]}")
        rows.append("".join(pieces) + "\x1b[0m")
    overlay = f"CPU {cpu*100:5.1f}% | MEM {mem*100:5.1f}% | NET {metrics['net_rate']/1024:7.1f} kB/s"
    if rows:
        header = f"Style {style} | Entropy {int(metrics['entropy'] % 1_000_000):06d}"
        rows[0] = f"\x1b[48;5;{colors[0]}m{header[:width].ljust(width)}\x1b[0m"
        rows[height // 2 % len(rows)] = overlay[:width].center(width)
    return rows


def snapshot_payload(metrics: Dict[str, float], frame: List[str], width: int, height: int, style: str) -> Dict[str, object]:
    return {
        "metrics": {
            "cpu": metrics["cpu"],
            "mem": metrics["mem"],
            "disk": metrics["disk"],
            "net_rate": metrics["net_rate"],
        },
        "frame": frame,
        "width": width,
        "height": height,
        "style": style,
    }


def clear_screen() -> None:
    sys.stdout.write("\x1b[?25l\x1b[H\x1b[2J")
    sys.stdout.flush()


def restore_screen() -> None:
    sys.stdout.write("\x1b[0m\x1b[?25h")
    sys.stdout.flush()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generative ASCII art powered by live system metrics")
    parser.add_argument("--interval", type=int, default=400, help="Frame interval in milliseconds")
    parser.add_argument("--style", choices=sorted(STYLE_PRESETS), default="plasma")
    parser.add_argument("--width", type=int, default=80)
    parser.add_argument("--height", type=int, default=24)
    parser.add_argument("--seed", type=int, help="Seed for deterministic art")
    parser.add_argument("--once", action="store_true", help="Render a single frame")
    parser.add_argument("--json", action="store_true", help="Emit JSON snapshot instead of ANSI art")
    parser.add_argument("--strict", action="store_true", help="Enforce 250 executable lines")
    args = parser.parse_args(argv)
    ensure_strict(args.strict)
    rng = random.Random(args.seed or time.time_ns())
    prev: Optional[Dict[str, float]] = None
    did_hide = False
    try:
        if args.json or args.once:
            metrics = gather_metrics(prev)
            frame = render_frame(metrics, rng, args.width, args.height, args.style, 0.0)
            if args.json:
                print(json.dumps(snapshot_payload(metrics, frame, args.width, args.height, args.style), indent=2))
            else:
                sys.stdout.write("\n".join(frame) + "\n")
                sys.stdout.flush()
            return 0
        clear_screen()
        did_hide = True
        tick = 0.0
        while True:
            metrics = gather_metrics(prev)
            frame = render_frame(metrics, rng, args.width, args.height, args.style, tick)
            sys.stdout.write("\x1b[H" + "\n".join(frame) + "\n")
            sys.stdout.flush()
            prev = metrics
            tick += 0.05 + metrics["cpu"] * 0.1
            time.sleep(max(args.interval, 16) / 1000.0)
    except KeyboardInterrupt:
        return 0
    finally:
        if did_hide:
            restore_screen()


if __name__ == "__main__":
    sys.exit(main())
