"""
Fairness and Algorithmic Equity Metrics for Educational Models
Includes Demographic Parity, Disparate Impact (80% Rule), and Equal Opportunity.
"""

from typing import Dict, List, Any
import math

class FairnessMetrics:
    """
    Standard quantitative fairness metrics formulated for educational prediction,
    automated grading, and admissions decisions.
    """

    @staticmethod
    def calculate_disparate_impact(
        unprivileged_pass_rate: float,
        privileged_pass_rate: float
    ) -> float:
        """
        Disparate Impact Ratio (DIR).
        A DIR < 0.8 violates the US EEOC Four-Fifths (80%) Rule.
        """
        if privileged_pass_rate <= 0:
            return 1.0 if unprivileged_pass_rate <= 0 else 2.0
        return round(unprivileged_pass_rate / privileged_pass_rate, 4)

    @staticmethod
    def calculate_demographic_parity_diff(
        unprivileged_pass_rate: float,
        privileged_pass_rate: float
    ) -> float:
        """
        Demographic Parity Difference (DPD) = |P(Y=1|unprivileged) - P(Y=1|privileged)|
        Ideal value: 0.0 (Acceptable threshold typically < 0.10).
        """
        return round(abs(unprivileged_pass_rate - privileged_pass_rate), 4)

    @staticmethod
    def calculate_equal_opportunity_diff(tpr_unprivileged: float, tpr_privileged: float) -> float:
        """
        Equal Opportunity Difference = |TPR_unprivileged - TPR_privileged|
        Compares true positive rates across groups.
        """
        return round(abs(tpr_unprivileged - tpr_privileged), 4)

    @staticmethod
    def calculate_average_odds_diff(
        tpr_unprivileged: float,
        tpr_privileged: float,
        fpr_unprivileged: float,
        fpr_privileged: float
    ) -> float:
        """
        Average Odds Difference = 0.5 * (|FPR_unpriv - FPR_priv| + |TPR_unpriv - TPR_priv|)
        """
        fpr_diff = abs(fpr_unprivileged - fpr_privileged)
        tpr_diff = abs(tpr_unprivileged - tpr_privileged)
        return round(0.5 * (fpr_diff + tpr_diff), 4)

    @staticmethod
    def summary_stats(values: List[float]) -> Dict[str, float]:
        if not values:
            return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
        n = len(values)
        mean_val = sum(values) / n
        variance = sum((x - mean_val) ** 2 for x in values) / max(1, n - 1)
        std_val = math.sqrt(variance)
        return {
            "mean": round(mean_val, 2),
            "std": round(std_val, 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2)
        }
