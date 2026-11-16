# Responsible AI Framework for Educational Applications (RAIF-Edu)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Standards: FERPA & COPPA](https://img.shields.io/badge/Standards-FERPA%20%26%20COPPA-emerald.svg)](https://studentprivacy.ed.gov/)
[![Fairness: EEOC 80% Rule](https://img.shields.io/badge/Fairness-EEOC%204%2F5ths%20Rule-indigo.svg)](https://www.eeoc.gov/)

> **Academic Capstone Project**  
> **Author**: Prateek Gautam  
> **Roll Number**: `RK4P25REB11`  
> **Registration Number**: `12518091`  
> **Project Title**: *Responsible AI Framework for Educational Applications*  

---

## 🌟 Executive Overview

**RAIF-Edu** is an end-to-end Responsible AI (RAI) middleware framework engineered to address ethical, pedagogical, safety, and legal challenges in AI-powered educational software (intelligent tutoring systems, automated grading engines, homework helpers, and admission screeners).

Unlike generic AI guardrails that only detect profanity or toxicity, **RAIF-Edu** enforces domain-specific educational principles:
1. **Student Privacy Protection (FERPA & COPPA)**: Context-aware PII detection, reversible pseudonymization, and under-13 consent checks.
2. **Algorithmic Fairness & Equity**: Measures Disparate Impact Ratio (DIR) adhering to the US EEOC Four-Fifths (80%) Rule, Demographic Parity Differences (DPD), and scans qualitative teacher feedback for coded bias.
3. **Content Safety & Cognitive Readability**: Detects cyberbullying, harassment, and self-harm signals, and matches cognitive reading levels (Flesch-Kincaid) to target school tiers.
4. **Pedagogical Integrity & Socratic Scaffolding**: Prevents direct homework/essay dumping (academic shortcuts) and promotes active Socratic guided inquiry.
5. **Factual Grounding & Hallucination Verifier**: Verifies STEM and humanities explanations against canonical curriculum standards.
6. **Transparent XAI Rubric & Governance**: Breaks down automated scores into explainable multi-dimensional rubrics and maintains tamper-evident audit logs with Human-in-the-Loop (HITL) escalation queues.

---

## 🚀 Quickstart Guide

### 1. Requirements
* Python 3.10 or higher
* Standard packages: `Flask`, `pydantic`

```bash
pip install -r requirements.txt
```

### 2. Launching the Interactive Web Dashboard
Run the server launcher:
```bash
python run_server.py
```
Open your browser and navigate to:
👉 **`http://localhost:5000`**

Available Web Dashboard views:
* **Live Inspector (`/`)**: Real-time multi-pillar inspection playground with 5 built-in educational presets.
* **Fairness & Bias Suite (`/fairness`)**: Demographic parity and disparate impact auditor with live Chart.js visualizations.
* **FERPA Privacy Guard (`/privacy`)**: PII redaction and reversible de-anonymization tester.
* **Socratic Scaffolding (`/pedagogy`)**: Cognitive scaffolding vs answer dumping diagnostic lab.
* **Audit Logs (`/logs`)**: Institutional governance records, HITL escalation queue, and markdown report exporter.
* **Architecture Docs (`/documentation`)**: Full academic specifications and formulas.

---

## 💻 Command Line Interface (CLI)

RAIF-Edu provides a CLI for batch processing and automated auditing:

### 1. Full Interaction Inspection
```bash
python cli.py inspect \
  --prompt "Can you help me understand how photosynthesis works?" \
  --response "Certainly! What is the primary pigment in plant leaves that absorbs sunlight?" \
  --age 15 \
  --tier high
```

### 2. Tabular Grading Fairness Audit (EEOC 80% Rule)
```bash
python cli.py fairness \
  --file data/student_assessments_sample.csv \
  --attribute gender \
  --privileged Male \
  --unprivileged Female \
  --threshold 75.0
```

### 3. Student PII Redaction (FERPA Sanitizer)
```bash
python cli.py sanitize \
  --text "My name is Prateek Gautam, Roll Number RK4P25REB11, email prateek@university.edu"
```

---

## 🧪 Running Unit Tests

Execute the automated test suite with full verbose reporting:
```powershell
$env:PYTHONPATH="."
python -m unittest discover -s tests -v
```

All 12 tests will execute and verify each pillar:
```
test_dataset_audit ... ok
test_disparate_impact_metric ... ok
test_text_feedback_bias ... ok
test_direct_answer_dump_detection ... ok
test_socratic_scaffolding_approval ... ok
test_benign_socratic_interaction ... ok
test_toxic_interaction_escalation ... ok
test_ferpa_coppa_compliance ... ok
test_pii_detection_and_redaction ... ok
test_age_readability ... ok
test_cyberbullying_detection ... ok
test_safe_content ... ok
----------------------------------------------------------------------
Ran 12 tests in 0.016s

OK
```

---

## 📊 Core Architectural Formulations

| Metric | Formula | Benchmark Target |
| :--- | :--- | :--- |
| **Disparate Impact Ratio (DIR)** | $DIR = \frac{P(\hat{Y}=1 \mid A=0)}{P(\hat{Y}=1 \mid A=1)}$ | $DIR \ge 0.80$ (EEOC 80% Rule) |
| **Demographic Parity Diff (DPD)** | $DPD = \| P(\hat{Y}=1 \mid A=0) - P(\hat{Y}=1 \mid A=1) \|$ | $DPD \le 0.10$ |
| **Flesch-Kincaid Grade Level** | $0.39(words/sent) + 11.8(syllables/words) - 15.59$ | Aligned with target grade tier |
| **Composite RAI Index** | $0.25 S + 0.25 P + 0.25 E_{ped} + 0.15 G + 0.10 X$ | $\ge 75.0$ (Approved) |

---

## 📁 Repository Structure

```
responsible-ai-edu-framework/
├── raif/                              # Core Framework Package
│   ├── privacy/                       # FERPA/COPPA PII Detector & Tokenizer
│   ├── fairness/                      # Disparate Impact & Bias Auditor
│   ├── safety/                        # Toxicity, Harassment & Flesch-Kincaid
│   ├── pedagogy/                      # Socratic Scaffolding & Anti-Cheating
│   ├── factual/                       # Curriculum Grounding & Hallucination
│   ├── explainability/                # Multi-Criteria XAI Rubric Scorer
│   ├── governance/                    # Audit Trail & HITL Queue
│   └── pipeline.py                    # Master Unified Pipeline
├── web/                               # Flask Web App & REST API
│   ├── app.py                         # Application Controller
│   ├── static/                        # CSS, JS, Chart.js integrations
│   └── templates/                     # 6 Modern HTML Templates
├── data/                              # Sample Datasets & Curricula
├── tests/                             # 12 Unit Tests (100% Pass)
├── cli.py                             # CLI Auditor
├── run_server.py                      # One-click Server Launcher
├── requirements.txt                   # Dependency list
├── PROJECT_REPORT.md                  # Comprehensive Academic Project Report
├── PRESENTATION_NOTES.md              # Viva Defense Notes & Slide Script
└── README.md                          # Documentation
```

---

## 🎓 Academic Submission

* **Student Name**: Prateek Gautam
* **Roll Number**: RK4P25REB11
* **Registration Number**: 12518091
* **Project**: Responsible AI Framework for Educational Applications
