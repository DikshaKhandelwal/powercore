# PowerCore — one engine, many tiny CLIs

```
 ____                              ____                      
|  _ \ ___  _____   _____ _ __    / ___|___  _ __ ___  ___  
| |_) / _ \/ _ \ \ / / _ \ '__|  | |   / _ \| '__/ _ \/ __| 
|  __/  __/  __/\ V /  __/ |     | |__| (_) | | |  __/\__ \ 
|_|   \___|\___| \_/ \___|_|      \____\___/|_|  \___||___/ 
                                                             
```

A compact, judge-friendly toolkit: one master command (PowerCore) that cleanly delegates to focused micro-CLIs. Each tool is a single Python file (≤ 250 executable lines for most) with real demos included.

- Delegated tools:
  - semantic-diff — “diffs that think”
  - pattern-prophet — behavior insights from your histories
  - commit-poet — diff → poem (haiku, limerick, free)
  - procgen-art — ANSI generative art powered by live metrics
  - data-sanity — auto data crisis fixer
  - logsage — log whisperer & summarizer
  - focuscli — distraction killer & flow tracker
  - snipvault — snippet brain in your terminal

## Install / Open

No packaging needed. Requires Python 3.9+. Optional: psutil for procgen, scikit-learn for data-sanity --ml.

```bash
# Run from repo root
./powercore --help
```

Tip (PATH):
```bash
# Git Bash (current session)
export PATH="$PATH:/d/cli"
# Windows CMD (temporary)
set PATH=%PATH%;D:\cli
```

---

## 1) semantic-diff — “Diffs that think”

```
   _____                 _             _   _  __   _  
  / ____|               | |           | | (_)/ _| | | 
 | (___  _ __ ___   __ _| |_ ___  _ __| |_ _| |_  | | 
  \___ \| '_ ` _ \ / _` | __/ _ \| '__| __| |  _| | | 
  ____) | | | | | | (_| | || (_) | |  | |_| | |   |_| 
 |_____/|_| |_| |_|\__,_|\__\___/|_|   \__|_|_|   (_) 
```

Smarter structural diffs across files/dirs. Ranks and explains high-signal changes. 250-line single file with JSON/text.

Demo inputs: `examples/before/order.py` vs `examples/after/order.py`

```bash
./powercore semantic-diff examples/before examples/after --explain --meta --sections added,modified
```

Expected (excerpt):
```
[ADDED]
ADDED: order.py:4-4 assignment MAX_DISCOUNT (...)
ADDED: order.py:7-11 function calculate_discount (...)
[MODIFIED]
MODIFIED: order.py:14-26 function process_order -> process_order (similarity=0.68, ...)
[EXPLAIN]
process_order changed structure with delta 9.0
[META]
change_score: 9.00
...
```

JSON:
```bash
./powercore semantic-diff examples/before examples/after --format json | head -n 30
```

---

## 2) pattern-prophet — behavior insights

```
 ____      _   _                 ____               _           _   
|  _ \ ___| |_(_)_ __   __ _   |  _ \ ___  ___  __| |_   _ ___| |_ 
| |_) / _ \ __| | '_ \ / _` |  | |_) / _ \/ _ \/ _` | | | / __| __|
|  __/  __/ |_| | | | | (_| |  |  __/  __/  __/ (_| | |_| \__ \ |_ 
|_|   \___|\__|_|_| |_|\__, |  |_|   \___|\___|\__,_|\__,_|___/\__|
                        |___/                                       
```

Surface “signature move”, peak hour/day, spike windows, longest quiet stretch. Works with bash/git/file.

Demo (bundled bash history):
```bash
./powercore pattern-prophet --source bash --path examples/history/bash_history_sample.txt --format text
```

---

## 3) commit-poet — diff → poem

```
   ____                _ _ _   
  / ___|___  _ __  __| (_) |_ 
 | |   / _ \| '_ \/ _` | | __|
 | |__| (_) | | | | (_| | | |_ 
  \____\___/|_| |_|\__,_|_|\__|
```

Takes a diff and crafts a haiku/limerick/freeform with mood inference.

Demo (bundled diff):
```bash
./powercore commit-poet --style haiku --path examples/order.diff --seed 21
```

---

## 4) procgen-art — ANSI generative art

```
 ____                      _             _       _   
|  _ \ ___  ___ ___  _ __ | |_ _ __ ___ (_)_ __ | |_ 
| |_) / _ \/ __/ _ \| '_ \| __| '__/ _ \| | '_ \| __|
|  __/  __/ (_| (_) | | | | |_| | | (_) | | | | | |_ 
|_|   \___|\___\___/|_| |_|\__|_|  \___/|_|_| |_|\__|
```

Live ASCII visuals seeded by system metrics (psutil if present, otherwise synthetic). Once, JSON snapshot, or live.

```bash
# Single frame
./powercore procgen-art --once --width 60 --height 18
# JSON snapshot
./powercore procgen-art --json --once --width 20 --height 6 | head -n 30
```

---

## 5) data-sanity — auto data crisis fixer

```
 ____        _        ____             _ _      
|  _ \  __ _| |_ __ _/ ___|  ___  __ _| | | ___ 
| | | |/ _` | __/ _` \___ \ / _ \/ _` | | |/ _ \
| |_| | (_| | || (_| |___) |  __/ (_| | | |  __/
|____/ \__,_|\__\__,_|____/ \___|\__,_|_|_|\___|
```

Loads CSV/JSON/Excel, shows missing/duplicates/stats, z-score anomalies (+ optional ML), suggests cleaning, can save cleaned output.

```bash
# Quick run on a sample
./powercore data-sanity --file tmp.csv --threshold 3.0
# With ML anomalies (requires scikit-learn)
./powercore data-sanity --file tmp.csv --ml
# Save cleaned data
./powercore data-sanity --file tmp.csv --output tmp_clean.csv
```

---

## 6) logsage — log whisperer & summarizer

```
 _               ____                     
| |    ___  __ _/ ___|  __ _  __ _  ___ _ __ 
| |   / _ \/ _` \___ \ / _` |/ _` |/ _ \ '__|
| |__|  __/ (_| |___) | (_| | (_| |  __/ |   
|_____\___|\__,_|____/ \__,_|\__, |\___|_|   
                            |___/            
```

Parses timestamps, levels, normalizes noisy tokens, shows top patterns/errors, time window, throughput. Reads files or STDIN.

```bash
printf "alpha=1\nalpha=1\nbeta=2\n" > sample.log
./powercore logsage sample.log --format text
# JSON
./powercore logsage sample.log --format json | jq . | head -n 40
```

---

## 7) focuscli — distraction killer & flow tracker

```
 _____           _            ____ _     
|  ___|__  _ __| | ___  ___ / ___| |__  
| |_ / _ \| '__| |/ _ \/ __| |   | '_ \ 
|  _| (_) | |  | |  __/\__ \ |___| | | |
|_|  \___/|_|  |_|\___||___/\____|_| |_|
```

Track focus sessions locally (~/.focuscli.jsonl). Start/stop, stats (total hours, streak, top topics), export.

```bash
./powercore focuscli start "Deep work" --notes "Refactor pricing"
./powercore focuscli stop
./powercore focuscli stats --days 7
./powercore focuscli export
```

---

## 8) snipvault — snippet brain in your terminal

```
 ____       _            _           _ _   
/ ___|  ___| | ___  _ __(_) ___  ___| | |  
\___ \ / _ \ |/ _ \| '__| |/ _ \/ __| | |  
 ___) |  __/ | (_) | |  | |  __/ (__| | |  
|____/ \___|_|\___/|_|  |_|\___|\___|_|_|  
```

Save/find/list/rm code snippets with tags/language filters. Stored as JSONL in ~/.snipvault.jsonl.

```bash
./powercore snipvault add "git log --oneline" --tag git --tag tips --lang bash
./powercore snipvault find --q "oneline" --tag git
./powercore snipvault ls --limit 5
./powercore snipvault rm <id>
```

---

## Screenshots / GIFs (optional)

- Add terminal GIFs of semantic-diff and procgen-art runs.
- Add JSON snapshots (truncated) for judges.

---

## Constraints & guardrails

- Most tools adhere to a 250 executable-line cap; some enforce at runtime with `--strict`.
- Single-file tools; zero/minimal deps.
- Deterministic runs where possible (e.g., commit-poet `--seed`).

## Troubleshooting

- PATH not picking up `powercore`:
  - Run via relative path `./powercore ...` or add repo folder to PATH (see “Install / Open”).
- Windows console Unicode:
  - Pattern-prophet and others print safely; if you see garbled symbols, try `chcp 65001` or rely on JSON output.
- DataSanity ML:
  - Install scikit-learn or run without `--ml`.

## Judge cheatsheet

```bash
# semantic-diff
./powercore semantic-diff examples/before examples/after --explain --meta --sections added,modified

# pattern-prophet
./powercore pattern-prophet --source bash --path examples/history/bash_history_sample.txt

# commit-poet
./powercore commit-poet --style haiku --path examples/order.diff --seed 21

# procgen (single frame)
./powercore procgen-art --once --width 40 --height 10

# data-sanity
./powercore data-sanity --file tmp.csv --threshold 3.0

# logsage
./powercore logsage sample.log --format text

# focuscli
./powercore focuscli start "Deep work" && sleep 2 && ./powercore focuscli stop && ./powercore focuscli stats --days 1

# snipvault
./powercore snipvault add "git log --oneline" --tag git --lang bash && ./powercore snipvault ls --limit 3
```
