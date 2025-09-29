# PowerCore — one engine, many tiny CLIs

```
 ____                        ____                
|  _ \ _____      _____ _ __ / ___|___  _ __ ___ 
| |_) / _ \ \ /\ / / _ \ '__|\___ \ _ \| '__/ _ \
|  __/ (_) \ V  V /  __/ |   ___) |  | | |  __/
|_|   \___/ \_/\_/ \___|_|  |____/   |_|  \___|
```

A powerful, user-friendly toolkit that brings together essential development utilities in one place. PowerCore acts as your central command hub, providing clean access to eight specialized micro-tools. Each tool is designed to solve real problems developers face daily, packaged as lightweight Python scripts that you can trust and understand.

**What's included:**
- **semantic-diff** — Smart code comparison that understands structure and meaning
- **pattern-prophet** — Discover hidden patterns in your bash history and git logs  
- **commit-poet** — Transform boring diffs into creative poetry (haiku, limerick, or free verse)
- **procgen-art** — Generate beautiful ASCII art powered by your system's live metrics
- **data-sanity** — Automatically detect and fix common data quality issues
- **logsage** — Intelligent log analysis and summarization
- **focuscli** — Track your focus sessions and boost productivity
- **snipvault** — Personal code snippet manager for your terminal

- Delegated tools:
  - semantic-diff — “diffs that think”
  - pattern-prophet — behavior insights from your histories
  - commit-poet — diff → poem (haiku, limerick, free)
  - procgen-art — ANSI generative art powered by live metrics
  - data-sanity — auto data crisis fixer
  - logsage — log whisperer & summarizer
  - focuscli — distraction killer & flow tracker
  - snipvault — snippet brain in your terminal

## Getting Started

PowerCore is ready to use right out of the box! Just make sure you have Python 3.9+ installed. Some tools have optional dependencies (psutil for system metrics in procgen-art, scikit-learn for advanced anomaly detection in data-sanity) but work fine without them.

```bash
# Run from the repository root
./powercore --help
```

**Make it globally available (optional):**
```bash
# Git Bash (add to ~/.bashrc for permanent)
export PATH="$PATH:/d/cli"
# Windows CMD (add to system PATH for permanent)
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

## 3) commit-poet — Turn Code Changes Into Art

Why settle for boring commit messages when you can have poetry? commit-poet transforms your git diffs into beautiful haiku, clever limericks, or flowing free verse. It analyzes the emotional tone of your changes and crafts messages that are both meaningful and memorable.

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

## 7) focuscli — Boost Your Productivity 

Stay focused and track your deep work sessions with focuscli. Start a timer when you begin focused work, stop it when you're done, and build up insights about your productivity patterns. See your longest streaks, total focus time, and which topics get your best attention.

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
