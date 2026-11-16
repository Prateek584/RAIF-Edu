"""
Educational Bias and Equity Auditor
Audits grading models, recommendation algorithms, and feedback text for systematic bias.
"""

import csv
import re
from typing import Dict, List, Any, Optional
from .metrics import FairnessMetrics

class BiasAuditor:
    """
    Analyzes student grading and evaluation datasets across protected attributes
    (e.g., gender, socio-economic status, ESL/language background).
    Also audits textual feedback for demographic stereotyping.
    """

    # Coded words that often signal stereotyping in educational reviews
    GENDER_CODED_WORDS = {
        "female_stereotyped": ["diligent", "quiet", "obedient", "sweet", "emotional", "supportive", "passive"],
        "male_stereotyped": ["natural genius", "brilliant", "assertive", "leader", "visionary", "analytical", "driven"]
    }

    ESL_PENALIZING_TERMS = [
        "awkward phrasing", "poor vocabulary", "non-native tone", "unrefined English", "broken expression"
    ]

    def __init__(self):
        self.metrics = FairnessMetrics()

    def audit_dataset(
        self,
        records: List[Dict[str, Any]],
        protected_attr: str = "gender",
        privileged_val: str = "Male",
        unprivileged_val: str = "Female",
        outcome_attr: str = "ai_awarded_grade",
        pass_threshold: float = 70.0
    ) -> Dict[str, Any]:
        """
        Audits tabular student grading data to calculate disparate impact and demographic parity.
        """
        priv_scores = []
        unpriv_scores = []
        priv_passes = 0
        unpriv_passes = 0

        for r in records:
            attr_val = str(r.get(protected_attr, "")).strip().capitalize()
            try:
                score = float(r.get(outcome_attr, 0))
            except (ValueError, TypeError):
                continue

            is_pass = 1 if score >= pass_threshold else 0

            if attr_val == privileged_val.capitalize():
                priv_scores.append(score)
                priv_passes += is_pass
            elif attr_val == unprivileged_val.capitalize():
                unpriv_scores.append(score)
                unpriv_passes += is_pass

        n_priv = len(priv_scores)
        n_unpriv = len(unpriv_scores)

        priv_rate = round(priv_passes / n_priv, 4) if n_priv > 0 else 0.0
        unpriv_rate = round(unpriv_passes / n_unpriv, 4) if n_unpriv > 0 else 0.0

        dir_ratio = self.metrics.calculate_disparate_impact(unpriv_rate, priv_rate)
        dpd = self.metrics.calculate_demographic_parity_diff(unpriv_rate, priv_rate)

        # 80% Rule (EEOC Guidelines)
        passes_four_fifths_rule = dir_ratio >= 0.80

        # Overall Fairness Health Score (0 - 100)
        fairness_score = round(max(0.0, min(100.0, (1.0 - dpd) * 100 * (dir_ratio if dir_ratio <= 1.0 else 1.0 / dir_ratio))), 1)

        findings = []
        if not passes_four_fifths_rule:
            findings.append(
                f"Disparate impact violation detected: Ratio {dir_ratio} is below the 0.80 regulatory threshold for {unprivileged_val} vs {privileged_val}."
            )
        if dpd > 0.10:
            findings.append(
                f"Significant demographic parity gap: {round(dpd * 100, 1)}% difference in favorable evaluation rates."
            )
        if not findings:
            findings.append("No statistically significant disparate impact detected across evaluated subgroups.")

        return {
            "protected_attribute": protected_attr,
            "privileged_group": privileged_val,
            "unprivileged_group": unprivileged_val,
            "sample_counts": {privileged_val: n_priv, unprivileged_val: n_unpriv},
            "pass_rates": {privileged_val: priv_rate, unprivileged_val: unpriv_rate},
            "disparate_impact_ratio": dir_ratio,
            "demographic_parity_diff": dpd,
            "four_fifths_rule_compliant": passes_four_fifths_rule,
            "fairness_score": fairness_score,
            "privileged_stats": self.metrics.summary_stats(priv_scores),
            "unprivileged_stats": self.metrics.summary_stats(unpriv_scores),
            "findings": findings
        }

    def audit_text_feedback(self, feedback_text: str) -> Dict[str, Any]:
        """
        Scans qualitative teacher or AI feedback for coded demographic stereotyping.
        """
        text_lower = feedback_text.lower()
        flagged_terms = []

        for category, terms in self.GENDER_CODED_WORDS.items():
            for t in terms:
                if re.search(r"\b" + re.escape(t) + r"\b", text_lower):
                    flagged_terms.append({"term": t, "category": category})

        for term in self.ESL_PENALIZING_TERMS:
            if term in text_lower:
                flagged_terms.append({"term": term, "category": "esl_penalty"})

        has_bias = len(flagged_terms) > 0
        sentiment_score = 100 - (len(flagged_terms) * 20)
        sentiment_score = max(0, sentiment_score)

        return {
            "has_stereotyped_language": has_bias,
            "flagged_terms": flagged_terms,
            "text_neutrality_score": sentiment_score,
            "recommendation": (
                "Ensure feedback focuses on conceptual mastery and rubric rubrics rather than subjective personal attributes."
                if has_bias else "Feedback maintains neutral, professional pedagogical focus."
            )
        }

    @classmethod
    def load_csv(cls, filepath: str) -> List[Dict[str, Any]]:
        records = []
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        return records
