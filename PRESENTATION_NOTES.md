# Viva & Project Defense Presentation Guide

## Project Title: Responsible AI Framework for Educational Applications (RAIF-Edu)
**Candidate**: Prateek Gautam  
**Roll Number**: RK4P25REB11  
**Registration Number**: 12518091  

---

## 1. The 60-Second Elevator Pitch
> *"Good morning, esteemed examiners. My project is the **Responsible AI Framework for Educational Applications (RAIF-Edu)**.*  
> *While generative AI offers massive potential in classrooms, standard commercial models pose severe risks: they leak student personal data in violation of FERPA and COPPA, they exhibit demographic grading bias under the EEOC 80% rule, and worst of all, they act as 'homework dumpers' that bypass active student learning.*  
> *To solve this, I designed and built RAIF-Edu—a modular, 6-pillar framework that redacts student PII, audits algorithmic fairness, enforces Socratic scaffolding, validates curriculum grounding, demystifies grades via explainable rubrics, and maintains an institutional audit log. I have implemented this as both an interactive web dashboard and a high-performance REST API."*

---

## 2. Slide-by-Slide Defense Script

### Slide 1: Title & Author Introduction
* **Speaker**: *"I am Prateek Gautam (Roll No: RK4P25REB11, Reg No: 12518091). My project addresses ethical and responsible AI governance specifically tailored for educational systems."*

### Slide 2: The Core Problem
* **Talking Points**:
  1. Privacy: Students unknowingly paste personal names and roll numbers into cloud LLMs.
  2. Inequity: Automated grading algorithms disadvantage ESL and minority student cohorts.
  3. Metacognitive Bypass: AI writes full essays for students instead of teaching them how to write.
  4. Hallucinations: Confident errors in STEM and history.

### Slide 3: Framework Architecture (The 6 Pillars)
* **Talking Points**:
  * **Pillar 1 - Privacy**: FERPA/COPPA PII detector and reversible tokenization.
  * **Pillar 2 - Fairness**: Disparate Impact Ratio ($DIR$) & Demographic Parity Difference ($DPD$) with the 80% rule.
  * **Pillar 3 - Safety & Readability**: Toxicity detection and Flesch-Kincaid educational grade leveling.
  * **Pillar 4 - Socratic Pedagogy**: Intercepts homework cheating; rewards guiding hints and questions.
  * **Pillar 5 - Factual Grounding**: Cross-references against curriculum standards to detect hallucinations.
  * **Pillar 6 - Governance & XAI**: Explainable criteria rubrics + Human-in-the-Loop escalation.

### Slide 4: Key Mathematical Formulations
* **Formulas to highlight**:
  * Disparate Impact Ratio: $DIR = \frac{P(\hat{Y}=1 | A=0)}{P(\hat{Y}=1 | A=1)}$ (EEOC 80% benchmark)
  * Demographic Parity Difference: $DPD = |P(\hat{Y}=1|A=0) - P(\hat{Y}=1|A=1)|$
  * Flesch-Kincaid Grade Level: $FKGL = 0.39(words/sent) + 11.8(syllables/words) - 15.59$
  * Composite Responsible AI Score: Linear weighted sum ($w_s=0.25, w_p=0.25, w_{ped}=0.25, w_g=0.15, w_x=0.10$).

### Slide 5: Live Demonstration
* Demonstrate the 5 scenarios on the web interface:
  1. *Exemplary Socratic Tutoring* $\rightarrow$ Approved, score 92%.
  2. *Homework Dump & Cheating* $\rightarrow$ Flagged for Review, score drops to 35%.
  3. *Student PII Leakage* $\rightarrow$ Cleanly sanitized into `[STUDENT_NAME_1]`, `[STUDENT_ID_1]`.
  4. *Fairness Tab* $\rightarrow$ Show Chart.js charts and EEOC 80% rule audit on sample dataset.

### Slide 6: Conclusion & Impact
* Demonstrates an autonomous, reproducible middleware for schools, universities, and LMS platforms (Canvas/Moodle).

---

## 3. High-Probability Examiner Questions & Answers

### Q1: *"Why do we need a specialized educational framework instead of using generic guardrails like Llama Guard or NeMo Guardrails?"*
> **Answer**:  
> *"Generic guardrails only look for vulgarity, violence, or hate speech. They are blind to educational ethics! A generic guardrail sees nothing wrong when an AI writes a student's history essay or solves all 10 algebra problems for them. But in education, that is an academic integrity failure. Furthermore, generic guardrails do not measure disparate impact under the EEOC 80% rule, nor do they calculate Flesch-Kincaid grade levels or FERPA compliance."*

### Q2: *"How does your framework prevent cheating without completely refusing to help the student?"*
> **Answer**:  
> *"That is the core function of Pillar 4—the Socratic Pedagogy Guard. Instead of just blocking the prompt, RAIF-Edu detects if the student is asking for a direct answer dump versus conceptual guidance. When a bypass is detected, it generates a Socratic Scaffolding template: it asks guiding questions, provides conceptual hints, and prompts the student to share their first step."*

### Q3: *"What is the 80% rule in algorithmic fairness, and how do you calculate it?"*
> **Answer**:  
> *"The Four-Fifths or 80% rule originates from the US EEOC Uniform Guidelines. It states that the selection or pass rate for any unprivileged group must be at least 80% (or 0.80) of the rate for the privileged group. In RAIF-Edu, my `BiasAuditor` calculates $DIR = \frac{PassRate_{unpriv}}{PassRate_{priv}}$. If $DIR < 0.80$, the system automatically flags a disparate impact violation."*

### Q4: *"How is student data protected under FERPA and COPPA?"*
> **Answer**:  
> *"Under FERPA (34 CFR Part 99), student education records cannot be disclosed to third parties without consent. RAIF-Edu intercepts the prompt before it leaves the institutional perimeter, detects names, roll numbers (like RK4P25REB11), emails, and student IDs, and substitutes them with pseudonymous tokens like `[STUDENT_NAME_1]`. The token map stays within the institution. For COPPA, if the student is under 13, it enforces verified parental consent checks."*
