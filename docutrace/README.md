# DocuTrace

**Requirement-to-Code Traceability & Change Impact Analysis System**

DocuTrace links software requirements to the code that implements them and, when code changes, reports which requirements and tests are affected. It is built in Python 3.11.

This repository contains the project's **fixed demo fixture** (`PaymentService`) that the DocuTrace engines run against, along with the requirements file and tests that go with it.

> **Do not change function signatures or call structure in `src/payment/` without updating `requirements/requirements.yaml`.** The Requirement Analyzer, AST Analyzer and Change Impact Engine all depend on the two staying in sync.

## Problem

In a growing codebase, nobody can say with confidence *which requirement does this function satisfy?* or *what breaks if I change it?* Hand-maintained traceability matrices go stale. DocuTrace builds and maintains those links automatically from the requirements file, the source code and the Git history.

## Architecture

See:

- `docs/ARCHITECTURE.md`
- `contracts/`

## Core Pipeline

```
requirements/requirements.yaml          src/payment/*.py
            ↓                                  ↓
   Requirement Analyzer                  AST Analyzer
            ↓                                  ↓
            └──────→  Traceability Graph (networkx)  ←──────┐
                                  ↓                         │
                  Git Change Detection (GitPython) ─────────┘
                                  ↓
                     Change Impact Engine
                                  ↓
              Validation + Coverage Metrics (pytest)
                                  ↓
                   Impact Reports (JSON / Markdown)
```

## Module Ownership

| Owner | Module |
|-------|--------|
| P | Architecture, Requirement Analyzer & Documentation |
| S | AST Analyzer & Traceability Graph |
| R | Change Impact Engine, Validation & CI |

## Work Breakdown

### P — Architecture, Requirement Analyzer & Documentation

- System architecture, DFDs (Level 0 / 1 / 2) and UML diagrams (use case, class, activity, sequence)
- Data contracts shared by all modules (`contracts/`): requirement, code-unit, trace-link and impact-result schemas
- **Requirement Analyzer:** loads and validates `requirements/requirements.yaml` (PyYAML) into the shared requirement schema
- Project report chapters 2–4 (Feasibility, SDLC model selection, Requirements Engineering)
- CLI entry point and end-to-end pipeline wiring

### S — AST Analyzer & Traceability Graph

- **AST Analyzer:** parses `src/payment/` with Python's `ast` module to extract functions, classes and call relationships (`process`, `validate_card`, `calculate_fee`, `save_transaction`)
- Complexity and maintainability metrics per function (`radon`)
- **Traceability Graph** (`networkx`): nodes for requirements, functions and tests, with typed edges (implements, tests, calls)
- Graph queries: requirement → code, code → requirement, orphaned code, unimplemented requirements
- Maintains the fixture and its tests (`src/payment/`, `tests/test_payment.py`)

### R — Change Impact Engine, Validation & CI

- **Change Impact Engine:** Git diffs (`GitPython`) mapped to changed functions, then traced through the graph to affected requirements and tests, with an impact score
- Validation and metrics: requirement coverage, untraced code, untested requirements, broken links
- Report generation (JSON and Markdown)
- Test suite (`pytest`) and CI pipeline (GitHub Actions)
- Optional Flask / Streamlit dashboard
- Presentation deck and presenter scripts

## Interfaces Between Modules

| From | To | Contract |
|------|----|----------|
| Requirement Analyzer (P) | Graph (S) | `Requirement` objects |
| AST Analyzer (S) | Graph (S) | `CodeUnit` objects and call edges |
| Graph (S) | Change Impact Engine (R) | Graph query API |
| Change Impact Engine (R) | Reports (R) | `ImpactResult` objects |

Agree on the schemas in `contracts/` first so P, S and R can work in parallel.

## Repository Layout

```
DocuTrace/
├── docutrace/
│   ├── requirements/
│   │   └── requirements.yaml      # requirement definitions (fixture)
│   ├── src/
│   │   └── payment/
│   │       ├── __init__.py
│   │       └── payment_service.py # PaymentService fixture
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_payment.py
│   └── README.md
```

Planned additions: `docs/`, `contracts/`, and a `src/docutrace/` package for the analyzers, graph and impact engine (kept separate from the `src/payment/` fixture).

## Tech Stack

- Python 3.11
- `networkx`, `PyYAML`, `GitPython`, `radon`, `pytest`
- GitHub Actions for CI
- Optional Flask / Streamlit dashboard
- Mermaid for diagrams

## Getting Started

```bash
git clone https://github.com/Prachi-Mehta-376/DocuTrace.git
cd DocuTrace/docutrace
python -m pip install pytest
python -m pytest tests/ -v
```

If pytest cannot import `src.payment`, add a `pytest.ini` containing `pythonpath = .`.

## Team

| Owner | Role |
|-------|------|
| P | Architecture, Requirement Analyzer & Documentation |
| S | AST Analyzer & Traceability Graph |
| R | Change Impact Engine, Validation & CI |
