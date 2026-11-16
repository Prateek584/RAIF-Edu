"""
Unit tests for Safety, Toxicity and Age Appropriateness
"""

import unittest
from raif.safety.toxicity_filter import ToxicityFilter
from raif.safety.age_appropriateness import AgeAppropriatenessEvaluator

class TestSafetyModule(unittest.TestCase):

    def setUp(self):
        self.tox_filter = ToxicityFilter()
        self.age_eval = AgeAppropriatenessEvaluator()

    def test_safe_content(self):
        safe_text = "Let's explore how linear equations are solved using substitution."
        res = self.tox_filter.evaluate(safe_text)
        self.assertTrue(res["safe"])
        self.assertEqual(res["severity"], "SAFE")

    def test_cyberbullying_detection(self):
        toxic_text = "You are an idiot and nobody likes you."
        res = self.tox_filter.evaluate(toxic_text)
        self.assertFalse(res["safe"])
        self.assertIn("CYBERBULLYING", res["flagged_categories"])
        self.assertGreaterEqual(res["toxicity_score"], 0.7)

    def test_age_readability(self):
        primary_text = "The cat sat on the mat. The sun was hot and bright."
        res = self.age_eval.evaluate_target_tier(primary_text, target_tier="primary")
        self.assertTrue(res["appropriate"])

if __name__ == "__main__":
    unittest.main()
