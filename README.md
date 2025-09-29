# PowerCore CLI Toolkit 🚀

A collection of 8 powerful command-line utilities designed for developers, with each tool constrained to **250 executable lines** of Python for maximum clarity and maintainability.

## 🎯 Overview

PowerCore provides a unified interface to specialized developer tools ranging from semantic code analysis to generative art. Each tool follows the philosophy of doing one thing exceptionally well while remaining simple and readable.

## 📦 Installation & Usage

### Direct Tool Usage
```bash
python commit_poet.py --help
python semantic_diff.py before/ after/
python data_sanity.py --file data.csv
```

### Unified Interface (Recommended)
```bash
# Windows
powercore.cmd semantic-diff before/ after/

# Unix/Linux/macOS  
python powercore.py semantic-diff before/ after/
```

## 🛠️ Tools Overview

### 1. **Semantic Diff** - Code Structure Analyzer
**File**: `semantic_diff.py`  
**Purpose**: Understand code changes at a semantic level, not just line-by-line

**Features**:
- Detects function/class additions, removals, modifications
- Calculates code complexity metrics (branches, size, documentation)
- Identifies renamed entities with similarity scoring
- Supports Python (AST-based) and generic languages

**Usage**:
```bash
python semantic_diff.py examples/before/ examples/after/
python semantic_diff.py file1.py file2.py --format json --explain
python semantic_diff.py src/ modified_src/ --sections added,modified
```

**Example Output**:
```
[ADDED]
ADDED: after/order.py:7-11 function calculate_discount (size=5.00, branches=2.00, doc=0.00)

[MODIFIED] 
MODIFIED: after/order.py:14-26 function process_order -> process_order (size_delta=5.00, branches_delta=3.00, similarity=0.75)
```

### 2. **Commit Poet** - Lyrical Git Messages  
**File**: `commit_poet.py`  
**Purpose**: Generate poetic commit messages from diff content

**Features**:
- Creates haiku, limerick, or freeform poetry from code changes
- Extracts keywords and infers development mood
- Supports reading from files or stdin
- Deterministic output with seed option

**Usage**:
```bash
git diff | python commit_poet.py
python commit_poet.py --style limerick --path examples/order.diff
python commit_poet.py --style haiku --seed 42 --format json < changes.diff
```

**Example Output**:
```
Commit Haiku
------------
Decimal flows bright
Calculate discount magic
Order process grows

Mood: Feature forger
Keywords: decimal, calculate, discount, process, order
```

### 3. **Data Sanity** - Automated Data Quality Checker
**File**: `data_sanity.py`  
**Purpose**: Detect and fix common data quality issues in CSV/JSON/Excel files

**Features**:
- Missing value detection and suggestions
- Duplicate row identification  
- Statistical anomaly detection (Z-score and ML-based)
- Automatic data cleaning with mean/mode imputation
- Comprehensive data profiling

**Dependencies**: `pandas`, `numpy`, `scikit-learn`, `openpyxl` (for Excel support)

**Usage**:
```bash
python data_sanity.py --file dataset.csv
python data_sanity.py --file data.xlsx --output clean_data.csv --ml
python data_sanity.py --file messy.json --threshold 2.5
```

**Example Output**:
```
=== Missing Values ===
name         0
age          3
salary      12

=== Summary Statistics ===
Column: age
  mean: 32.5
  median: 30.0
  missing: 3
  unique: 45

=== Cleaning Suggestions ===
- Fill missing numeric 'age' with mean/median
- Fill missing numeric 'salary' with mean/median
```

### 4. **Focus CLI** - Productivity Time Tracker
**File**: `focuscli.py`  
**Purpose**: Track focus sessions and build productivity habits

**Features**:
- Start/stop timed focus sessions with topics and notes
- Session statistics and streak tracking  
- Data stored in `~/.focuscli.jsonl`
- Export capabilities for external analysis

**Usage**:
```bash
python focuscli.py start "Deep coding" --notes "Working on authentication"
python focuscli.py stop
python focuscli.py stats --days 30
python focuscli.py export > my_focus_data.jsonl
```

**Example Output**:
```
FocusCLI Stats
=============
Total hours: 23.50
Current streak: 5 days
Top topics:
 - Deep coding: 8.20h
 - Code review: 4.10h  
 - Documentation: 3.50h
```

### 5. **LogSage** - Intelligent Log Analyzer
**File**: `logsage.py`  
**Purpose**: Parse, analyze, and summarize log files with pattern detection

**Features**:
- Multi-format timestamp parsing (ISO, syslog, custom)
- Log level detection and classification
- Pattern normalization (UUIDs, IPs, numbers → placeholders)
- Time-window filtering with relative syntax (`-6h`, `-30m`)
- Error pattern identification

**Usage**:
```bash
python logsage.py app.log system.log
tail -f live.log | python logsage.py --since -1h
python logsage.py --format json logs/*.log --top 20
```

**Example Output**:
```
LogSage Summary
===============
Total lines: 1,247
Levels: ERROR:23, WARN:156, INFO:1068
Window: 2025-09-29T10:00:00 → 2025-09-29T18:30:00
Throughput: 15.20 lines/min

Top patterns:
 - 234× User <uuid> authenticated successfully
 - 89× Database connection timeout after <n>ms
 - 67× Rate limit exceeded for IP <ip>

Top errors:
 - 12× Failed to process payment for order <uuid>
 - 8× Connection refused to service <ip>:<n>
```

### 6. **Pattern Prophet** - Behavioral Pattern Analyzer
**File**: `pattern_prophet.py`  
**Purpose**: Reveal patterns from bash history, git logs, or custom activity traces

**Features**:
- Analyzes bash history with timestamp support
- Git repository activity mining
- Custom file format support
- Peak activity detection (hourly/daily patterns)
- Sparkline visualizations for temporal data
- Habit identification and insights

**Usage**:
```bash
python pattern_prophet.py --source bash
python pattern_prophet.py --source git --path /my/repo
python pattern_prophet.py --source file --path custom_activity.log --format json
```

**Example Output**:
```
Pattern Prophet -> bash
=======================
🔮 Signature move: `git` appears 89 times.
⚡ Peak energy: 2pm with 23 bursts.  
📅 Most active day: Tuesday (45 sessions).
🌠 Spike window: Tuesday@14 (12 hits).
🌀 Habit loop: `status` echoes 34 times.
🕰️ Longest quiet stretch: 2.3 days of silence.

Hourly sparkline:
▁▁▂▃▅▇▇▆▄▃▂▁▁▁▁▂▃▄▃▂▁▁▁▁

Top tokens:
 - git: 89
 - status: 34
 - push: 28
```

### 7. **ProcGen Art** - System-Driven Generative Art
**File**: `procgen_art.py`  
**Purpose**: Create real-time ASCII art visualizations driven by system metrics

**Features**:
- Live system monitoring (CPU, memory, disk, network via `psutil`)
- Multiple artistic styles: plasma, waves, ember
- Real-time ANSI color terminal output
- Graceful fallback to mathematical patterns if `psutil` unavailable
- JSON export mode for programmatic use
- Customizable dimensions and refresh rates

**Dependencies**: `psutil` (optional - falls back to math-based patterns)

**Usage**:
```bash
python procgen_art.py --style plasma
python procgen_art.py --style ember --width 100 --height 30 --interval 200
python procgen_art.py --once --json > system_snapshot.json
python procgen_art.py --seed 1337 --once  # Deterministic output
```

**Visual Output**: Live animated ASCII art with system metrics overlay:
```
Style plasma | Entropy 342156
CPU  45.2% | MEM  67.8% | NET   123.4 kB/s
▓▓▒▒░░  ▓▓▒▒░░  ▓▓▒▒░░  ▓▓▒▒░░  
░░▒▒▓▓  ░░▒▒▓▓  ░░▒▒▓▓  ░░▒▒▓▓  
▒▒▓▓▓▓  ▒▒▓▓▓▓  ▒▒▓▓▓▓  ▒▒▓▓▓▓  
```

### 8. **SnipVault** - Terminal-Based Snippet Manager
**File**: `snipvault.py`  
**Purpose**: Store, search, and manage code snippets from the command line

**Features**:
- Add snippets with tags and language metadata
- Multi-criteria search (text content, tags, language)
- UUID-based snippet identification
- JSONL storage in `~/.snipvault.jsonl`
- Tag-based organization system

**Usage**:
```bash
python snipvault.py add "print('Hello World')" --tag python --tag demo --lang python
python snipvault.py find --q "hello" --tag python
python snipvault.py ls --limit 5
python snipvault.py rm a1b2c3d4  # Remove by ID prefix
```

**Example Output**:
```
SnipVault
=========
- a1b2c3d4 [python] (demo, tutorial): print('Hello World')
- f5e6d7c8 [bash] (git, workflow): git commit -am "feat: add new feature"  
- 9a8b7c6d [sql] (query, users): SELECT * FROM users WHERE active = true
```

## 🎨 Design Constraints

### **250-Line Limit**
Each tool is constrained to **exactly 250 executable lines** (excluding comments and blank lines) to ensure:
- **Clarity**: Code remains readable and understandable
- **Maintainability**: Small, focused tools are easier to debug and extend  
- **Learning**: Great examples of concise, effective Python programming
- **Performance**: Minimal overhead and fast startup times

### **Code Quality Standards**
- Type hints with `from __future__ import annotations`
- Comprehensive error handling
- Clean argument parsing with `argparse`
- Modular design with clear separation of concerns
- Cross-platform compatibility (Windows batch file + Python)

## 📁 Project Structure

```
cli/
├── README.md              # This comprehensive guide
├── powercore.py           # Unified CLI interface  
├── powercore.cmd          # Windows batch wrapper
├── commit_poet.py         # Poetic commit messages
├── data_sanity.py         # Data quality checker  
├── focuscli.py           # Productivity tracker
├── logsage.py            # Log analysis tool
├── pattern_prophet.py     # Behavioral pattern mining
├── procgen_art.py        # Generative ASCII art
├── semantic_diff.py      # Semantic code analyzer
├── snipvault.py          # Snippet management
└── examples/             # Sample files for testing
    ├── order.diff        # Sample diff for commit_poet
    ├── before/order.py   # Original code
    ├── after/order.py    # Modified code  
    └── history/          # Sample activity logs
        ├── bash_history_sample.txt
        └── git_log_sample.txt
```

## 🚦 Quick Start Examples

### Analyze Code Changes
```bash
# Compare two versions of code
python semantic_diff.py examples/before/ examples/after/ --explain

# Generate a poetic commit message
python commit_poet.py --path examples/order.diff --style haiku
```

### System Monitoring & Productivity  
```bash
# Start a focus session
python focuscli.py start "Code review session"

# Create live system art
python procgen_art.py --style waves

# Analyze your bash habits
python pattern_prophet.py --source bash
```

### Data Analysis & Management
```bash  
# Check data quality
python data_sanity.py --file tmp.csv --output clean.csv

# Analyze logs
python logsage.py sample.log --since -24h

# Save a useful snippet
python snipvault.py add "git log --oneline -10" --tag git --lang bash
```

## 🎯 Use Cases

- **Code Review**: Use `semantic_diff.py` to understand structural changes
- **Git Workflows**: Generate creative commit messages with `commit_poet.py`
- **Data Science**: Quality check datasets with `data_sanity.py`
- **DevOps**: Monitor system patterns with `procgen_art.py` and `logsage.py`
- **Productivity**: Track focus time and analyze work patterns
- **Learning**: Study concise, well-structured Python CLI tools

## 🤝 Contributing

Each tool is designed to be self-contained and easily extensible. When contributing:

1. Maintain the 250-line executable constraint
2. Include comprehensive argument parsing
3. Add proper error handling and user feedback
4. Test cross-platform compatibility
5. Update this README with new features

## 📄 License

Open source tools designed for developer productivity and learning.

---

*PowerCore: Where constraint breeds creativity, and simplicity meets power.*