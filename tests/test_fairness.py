"""
Unit tests for Fairness Metrics & Bias Auditor
"""

import unittest
from raif.fairness.metrics import FairnessMetrics
from raif.fairness.bias_auditor import BiasAuditor

class TestFairnessModule(unittest.TestCase):

    def setUp(self):
        self.auditor = BiasAuditor()

    def test_disparate_impact_metric(self):
        # 70% unpriv vs 90% priv -> ratio 0.7778 (< 0.80)
        dir_val = FairnessMetrics.calculate_disparate_impact(0.70, 0.90)
        self.assertAlmostEqual(dir_val, 0.7778, places=3)
        self.assertLess(dir_val, 0.80)

    def test_dataset_audit(self):
        mock_data = [
            {"gender": "Male", "ai_awarded_grade": 85},
            {"gender": "Male", "ai_awarded_grade": 90},
            {"gender": "Female", "ai_awarded_grade": 75},
            {"gender": "Female", "ai_awarded_grade": 60}
        ]
        result = self.auditor.audit_dataset(mock_data, protected_attr="gender", privileged_val="Male", unprivileged_val="Female")
        self.assertIn("disparate_impact_ratio", result)
        self.assertIn("demographic_parity_diff", result)
        self.assertIn("pass_rates", result)

    def test_text_feedback_bias(self):
        biased_text = "The student was quiet and sweet, but presented awkward phrasing."
        res = self.auditor.audit_text_feedback(biased_text)
        self.assertTrue(res["has_stereotyped_language"])
        self.assertGreater(len(res["flagged_terms"]), 0)

if __name__ == "__main__":
    unittest.main()
