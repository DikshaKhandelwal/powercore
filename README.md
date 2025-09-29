# PowerCore — one engine, many tiny CLIs# PowerCore — one engine, many tiny CLIsore — one e## 1) semantic-diff — Smart Code ComparisonIs



A powerful, user-friendly toolkit that brings together essential development utilities in one place. PowerCore acts as your central command hub, providing clean access to eight specialized micro-tools. Each tool is designed to solve real problems developers face daily, packaged as lightweight Python scripts that you can trust and understand.Discover hidden patterns in your development workflow. Analyzes bash history, git commits, or any text file to reveal your most-used commands, peak productivity hours, and work rhythms.

 ____              ## 2) pattern-prophet — Development Pattern Discovery____                ## 4) procgen-art — System Metrics Visualization____      __## 5) data-sanity — Data Quality Assistant / ___|___  _ _## 6) logsage — Intelligent Log Analysis|_) / _ \ \ /\ / / _ \ '_## 8) snipvault — Personal Code Library_ \| '__/ _ \

**What's included:**|  __/ (_) \ V  V /  __/ |   ___) |  | | |  __/

- **semantic-diff** — Smart code comparison that understands structure and meaning|_|   \___/ \_/\_/ \___|_|  |____/   |_|  \___|

- **pattern-prophet** — Discover hidden patterns in your bash history and git logs  ```

- **commit-poet** — Transform boring diffs into creative poetry (haiku, limerick, or free verse)

- **procgen-art** — Generate beautiful ASCII art powered by your system's live metricsA powerful, user-friendly toolkit that brings together essential development utilities in one place. PowerCore acts as your central command hub, providing clean access to eight specialized micro-tools. Each tool is designed to solve real problems developers face daily, packaged as lightweight Python scripts that you can trust and understand.

- **data-sanity** — Automatically detect and fix common data quality issues

- **logsage** — Intelligent log analysis and summarization**What's included:**

- **focuscli** — Track your focus sessions and boost productivity- **semantic-diff** — Smart code comparison that understands structure and meaning

- **snipvault** — Personal code snippet manager for your terminal- **pattern-prophet** — Discover hidden patterns in your bash history and git logs  

- **commit-poet** — Transform boring diffs into creative poetry (haiku, limerick, or free verse)

## Getting Started- **procgen-art** — Generate beautiful ASCII art powered by your system's live metrics

- **data-sanity** — Automatically detect and fix common data quality issues

PowerCore is ready to use right out of the box! Just make sure you have Python 3.9+ installed. Some tools have dependencies (psutil for system metrics in procgen-art, scikit-learn for advanced anomaly detection in data-sanity) but work fine without them.- **logsage** — Intelligent log analysis and summarization

- **focuscli** — Track your focus sessions and boost productivity

```bash- **snipvault** — Personal code snippet manager for your terminal

# Run from the repository root

./powercore --help- Delegated tools:

```  - semantic-diff — “diffs that think”

  - pattern-prophet — behavior insights from your histories

**Make it globally available:**  - commit-poet — diff → poem (haiku, limerick, free)

```bash  - procgen-art — ANSI generative art powered by live metrics

# Git Bash (add to ~/.bashrc for permanent)  - data-sanity — auto data crisis fixer

export PATH="$PATH:/d/cli"  - logsage — log whisperer & summarizer

# Windows CMD (add to system PATH for permanent)  - focuscli — distraction killer & flow tracker

set PATH=%PATH%;D:\cli  - snipvault — snippet brain in your terminal

```

## Getting Started

---

PowerCore is ready to use right out of the box! Just make sure you have Python 3.9+ installed. Some tools have optional dependencies (psutil for system metrics in procgen-art, scikit-learn for advanced anomaly detection in data-sanity) but work fine without them.

## 1) semantic-diff — Smart Code Comparison

```bash

Go beyond traditional line-by-line diffs. semantic-diff understands code structure and identifies the most meaningful changes in your codebase. It ranks changes by importance and explains what actually happened.# Run from the repository root

./powercore --help

**Basic usage:**```

```bash

./powercore semantic-diff examples/before examples/after --explain --meta --sections added,modified**Make it globally available:**

``````bash

# Git Bash (add to ~/.bashrc for permanent)

**JSON output:**export PATH="$PATH:/d/cli"

```bash# Windows CMD (add to system PATH for permanent)

./powercore semantic-diff examples/before examples/after --format jsonset PATH=%PATH%;D:\cli

``````



**Additional options:**---

```bash

# Compare single files## 1) semantic-diff — “Diffs that think”

./powercore semantic-diff file1.py file2.py

```

# Show only specific sections   _____                 _             _   _  __   _  

./powercore semantic-diff dir1 dir2 --sections added,removed,modified  / ____|               | |           | | (_)/ _| | | 

 | (___  _ __ ___   __ _| |_ ___  _ __| |_ _| |_  | | 

# Include detailed explanations  \___ \| '_ ` _ \ / _` | __/ _ \| '__| __| |  _| | | 

./powercore semantic-diff dir1 dir2 --explain --meta  ____) | | | | | | (_| | || (_) | |  | |_| | |   |_| 

``` |_____/|_| |_| |_|\__,_|\__\___/|_|   \__|_|_|   (_) 

```

---

Go beyond traditional line-by-line diffs. semantic-diff understands code structure and identifies the most meaningful changes in your codebase. It ranks changes by importance and explains what actually happened.

## 2) pattern-prophet — Development Pattern Discovery

```bash

Discover hidden patterns in your development workflow. Analyzes bash history, git commits, or any text file to reveal your most-used commands, peak productivity hours, and work rhythms../powercore semantic-diff examples/before examples/after --explain --meta --sections added,modified

```

**Analyze bash history:**

```bashExpected (excerpt):

./powercore pattern-prophet --source bash --path examples/history/bash_history_sample.txt```

```[ADDED]

ADDED: order.py:4-4 assignment MAX_DISCOUNT (...)

**Analyze git history:**ADDED: order.py:7-11 function calculate_discount (...)

```bash[MODIFIED]

./powercore pattern-prophet --source git --path examples/history/git_log_sample.txtMODIFIED: order.py:14-26 function process_order -> process_order (similarity=0.68, ...)

```[EXPLAIN]

process_order changed structure with delta 9.0

**Analyze any file:**[META]

```bashchange_score: 9.00

./powercore pattern-prophet --source file --path /path/to/file.txt...

``````



**JSON output:**JSON:

```bash```bash

./powercore pattern-prophet --source bash --path ~/.bash_history --format json./powercore semantic-diff examples/before examples/after --format json | head -n 30

``````



------



## 3) commit-poet — Turn Code Changes Into Art## 2) pattern-prophet — behavior insights



Transform boring diffs into beautiful haiku, clever limericks, or flowing free verse. Analyzes the emotional tone of your changes and crafts messages that are both meaningful and memorable.```

 ____      _   _                 ____               _           _   

**Generate haiku:**|  _ \ ___| |_(_)_ __   __ _   |  _ \ ___  ___  __| |_   _ ___| |_ 

```bash| |_) / _ \ __| | '_ \ / _` |  | |_) / _ \/ _ \/ _` | | | / __| __|

./powercore commit-poet --style haiku --path examples/order.diff --seed 21|  __/  __/ |_| | | | | (_| |  |  __/  __/  __/ (_| | |_| \__ \ |_ 

```|_|   \___|\__|_|_| |_|\__, |  |_|   \___|\___|\__,_|\__,_|___/\__|

                        |___/                                       

**Generate limerick:**```

```bash

./powercore commit-poet --style limerick --path examples/order.diffSurface “signature move”, peak hour/day, spike windows, longest quiet stretch. Works with bash/git/file.

```

Demo (bundled bash history):

**Free verse poetry:**```bash

```bash./powercore pattern-prophet --source bash --path examples/history/bash_history_sample.txt --format text

./powercore commit-poet --style free --path examples/order.diff```

```

---

**Use with git diffs:**

```bash## 3) commit-poet — Turn Code Changes Into Art

git diff > current.diff

./powercore commit-poet --style haiku --path current.diffWhy settle for boring commit messages when you can have poetry? commit-poet transforms your git diffs into beautiful haiku, clever limericks, or flowing free verse. It analyzes the emotional tone of your changes and crafts messages that are both meaningful and memorable.

```

Demo (bundled diff):

---```bash

./powercore commit-poet --style haiku --path examples/order.diff --seed 21

## 4) procgen-art — System Metrics Visualization```



Generate beautiful ASCII art from your system's real-time metrics like CPU usage, memory, and disk activity. Perfect for live displays or creative terminal backgrounds.---



**Single frame:**## 4) procgen-art — ANSI generative art

```bash

./powercore procgen-art --once --width 60 --height 18```

``` ____                      _             _       _   

|  _ \ ___  ___ ___  _ __ | |_ _ __ ___ (_)_ __ | |_ 

**JSON snapshot:**| |_) / _ \/ __/ _ \| '_ \| __| '__/ _ \| | '_ \| __|

```bash|  __/  __/ (_| (_) | | | | |_| | | (_) | | | | | |_ 

./powercore procgen-art --json --once --width 20 --height 6|_|   \___|\___\___/|_| |_|\__|_|  \___/|_|_| |_|\__|

``````



**Live mode (continuous):**Generate beautiful ASCII art from your system's real-time metrics like CPU usage, memory, and disk activity. Perfect for live displays or creative terminal backgrounds.

```bash

./powercore procgen-art --width 50 --height 15```bash

```# Single frame

./powercore procgen-art --once --width 60 --height 18

**Custom seed:**# JSON snapshot

```bash./powercore procgen-art --json --once --width 20 --height 6 | head -n 30

./powercore procgen-art --once --seed 42 --width 40 --height 10```

```

---

---

## 5) data-sanity — auto data crisis fixer

## 5) data-sanity — Data Quality Assistant

```

Automatically detect and fix data quality issues in CSV, JSON, and Excel files. Identifies missing values, duplicates, outliers, and provides smart cleaning suggestions with export capabilities. ____        _        ____             _ _      

|  _ \  __ _| |_ __ _/ ___|  ___  __ _| | | ___ 

**Basic analysis:**| | | |/ _` | __/ _` \___ \ / _ \/ _` | | |/ _ \

```bash| |_| | (_| | || (_| |___) |  __/ (_| | | |  __/

./powercore data-sanity --file tmp.csv --threshold 3.0|____/ \__,_|\__\__,_|____/ \___|\__,_|_|_|\___|

``````



**With ML anomaly detection:**Automatically detect and fix data quality issues in CSV, JSON, and Excel files. Identifies missing values, duplicates, outliers, and provides smart cleaning suggestions with export capabilities.

```bash

./powercore data-sanity --file data.csv --ml```bash

```# Quick run on a sample

./powercore data-sanity --file tmp.csv --threshold 3.0

**Save cleaned data:**# With ML anomalies (requires scikit-learn)

```bash./powercore data-sanity --file tmp.csv --ml

./powercore data-sanity --file data.csv --output cleaned_data.csv# Save cleaned data

```./powercore data-sanity --file tmp.csv --output tmp_clean.csv

```

**JSON output:**

```bash---

./powercore data-sanity --file data.csv --format json

```## 6) logsage — log whisperer & summarizer



**Analyze Excel files:**```

```bash _               ____                     

./powercore data-sanity --file spreadsheet.xlsx| |    ___  __ _/ ___|  __ _  __ _  ___ _ __ 

```| |   / _ \/ _` \___ \ / _` |/ _` |/ _ \ '__|

| |__|  __/ (_| |___) | (_| | (_| |  __/ |   

---|_____\___|\__,_|____/ \__,_|\__, |\___|_|   

                            |___/            

## 6) logsage — Intelligent Log Analysis```



Intelligent log analysis that cuts through noise to show what matters. Parses timestamps, extracts log levels, normalizes patterns, and identifies the most important events and errors.Intelligent log analysis that cuts through noise to show what matters. Parses timestamps, extracts log levels, normalizes patterns, and identifies the most important events and errors.



**Analyze log file:**```bash

```bashprintf "alpha=1\nalpha=1\nbeta=2\n" > sample.log

./powercore logsage sample.log --format text./powercore logsage sample.log --format text

```# JSON

./powercore logsage sample.log --format json | jq . | head -n 40

**JSON output:**```

```bash

./powercore logsage sample.log --format json---

```

## 7) focuscli — Boost Your Productivity 

**Analyze from stdin:**

```bashStay focused and track your deep work sessions with focuscli. Start a timer when you begin focused work, stop it when you're done, and build up insights about your productivity patterns. See your longest streaks, total focus time, and which topics get your best attention.

tail -f /var/log/app.log | ./powercore logsage

``````bash

./powercore focuscli start "Deep work" --notes "Refactor pricing"

**Time window analysis:**./powercore focuscli stop

```bash./powercore focuscli stats --days 7

./powercore logsage app.log --since "2023-09-29 10:00:00" --until "2023-09-29 12:00:00"./powercore focuscli export

``````



**Filter by log level:**---

```bash

./powercore logsage app.log --level ERROR,WARN## 8) snipvault — snippet brain in your terminal

```

```

--- ____       _            _           _ _   

/ ___|  ___| | ___  _ __(_) ___  ___| | |  

## 7) focuscli — Focus Session Tracking\___ \ / _ \ |/ _ \| '__| |/ _ \/ __| | |  

 ___) |  __/ | (_) | |  | |  __/ (__| | |  

Stay focused and track your deep work sessions. Start a timer when you begin focused work, stop it when you're done, and build up insights about your productivity patterns.|____/ \___|_|\___/|_|  |_|\___|\___|_|_|  

```

**Start a focus session:**

```bashNever lose useful code snippets again. Terminal-based snippet manager with smart search, tagging, and language filtering. All data stored locally.

./powercore focuscli start "Deep work" --notes "Refactor pricing module"

``````bash

./powercore snipvault add "git log --oneline" --tag git --tag tips --lang bash

**Stop current session:**./powercore snipvault find --q "oneline" --tag git

```bash./powercore snipvault ls --limit 5

./powercore focuscli stop./powercore snipvault rm <id>

``````



**View productivity stats:**

```bash

./powercore focuscli stats --days 7---

```

## Constraints & guardrails

**Export session data:**

```bash- Most tools adhere to a 250 executable-line cap; some enforce at runtime with `--strict`.

./powercore focuscli export- Single-file tools; zero/minimal deps.

```- Deterministic runs where possible (e.g., commit-poet `--seed`).



**List recent sessions:**## Troubleshooting

```bash

./powercore focuscli list --limit 10- PATH not picking up `powercore`:

```  - Run via relative path `./powercore ...` or add repo folder to PATH (see “Install / Open”).

- Windows console Unicode:

---  - Pattern-prophet and others print safely; if you see garbled symbols, try `chcp 65001` or rely on JSON output.

- DataSanity ML:

## 8) snipvault — Personal Code Library  - Install scikit-learn or run without `--ml`.



Never lose useful code snippets again. Terminal-based snippet manager with smart search, tagging, and language filtering. All data stored locally.## Judge cheatsheet



**Add a snippet:**```bash

```bash# semantic-diff

./powercore snipvault add "git log --oneline --graph" --tag git --tag visualization --lang bash./powercore semantic-diff examples/before examples/after --explain --meta --sections added,modified

```

# pattern-prophet

**Find snippets:**./powercore pattern-prophet --source bash --path examples/history/bash_history_sample.txt

```bash

./powercore snipvault find --q "git log" --tag git# commit-poet

```./powercore commit-poet --style haiku --path examples/order.diff --seed 21



**List all snippets:**# procgen (single frame)

```bash./powercore procgen-art --once --width 40 --height 10

./powercore snipvault ls --limit 5

```# data-sanity

./powercore data-sanity --file tmp.csv --threshold 3.0

**Remove a snippet:**

```bash# logsage

./powercore snipvault rm <snippet_id>./powercore logsage sample.log --format text

```

# focuscli

**Search by language:**./powercore focuscli start "Deep work" && sleep 2 && ./powercore focuscli stop && ./powercore focuscli stats --days 1

```bash

./powercore snipvault find --lang python# snipvault

```./powercore snipvault add "git log --oneline" --tag git --lang bash && ./powercore snipvault ls --limit 3

```

**Search by tags:**
```bash
./powercore snipvault find --tag docker --tag deployment
```

---

## Design Philosophy

- **Lightweight**: Most tools stay under 250 executable lines to remain readable and maintainable
- **Single-file**: Each tool is self-contained with minimal dependencies
- **Deterministic**: Consistent results with seed options where applicable
- **User-friendly**: Clear output, helpful error messages, and intuitive commands

## Troubleshooting

**PowerCore command not found:**
- Run using the relative path: `./powercore ...`
- Or add the repository folder to your PATH (see "Getting Started" section)

**Unicode display issues on Windows:**
- Tools handle encoding safely, but if you see garbled symbols, try `chcp 65001`
- Alternatively, use JSON output mode for clean data

**Missing ML features in data-sanity:**
- Install scikit-learn: `pip install scikit-learn`
- Or run without the `--ml` flag for basic analysis

**Missing system metrics in procgen-art:**
- Install psutil: `pip install psutil`
- Tool works with synthetic metrics if psutil is not available

## Quick Demo Commands

Test all tools quickly with these commands:

```bash
# Smart code diff
./powercore semantic-diff examples/before examples/after --explain --meta

# Development patterns
./powercore pattern-prophet --source bash --path examples/history/bash_history_sample.txt

# Code poetry
./powercore commit-poet --style haiku --path examples/order.diff --seed 21

# ASCII art
./powercore procgen-art --once --width 40 --height 10

# Data analysis
./powercore data-sanity --file tmp.csv --threshold 3.0

# Log analysis
printf "2023-09-29 10:15:32 INFO Processing order\n2023-09-29 10:16:45 ERROR Payment failed\n" > test.log
./powercore logsage test.log

# Focus tracking
./powercore focuscli start "Demo session" && sleep 3 && ./powercore focuscli stop

# Snippet management
./powercore snipvault add "ls -la" --tag basics --lang bash
./powercore snipvault ls --limit 1
```

---

*PowerCore: Making development tools powerful, accessible, and fun to use.*