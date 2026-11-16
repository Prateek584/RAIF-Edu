"""
Unit tests for Socratic Scaffolding and Pedagogy Guard
"""

import unittest
from raif.pedagogy.socratic_guard import SocraticPedagogyGuard

class TestPedagogyModule(unittest.TestCase):

    def setUp(self):
        self.guard = SocraticPedagogyGuard()

    def test_direct_answer_dump_detection(self):
        prompt = "Write an essay for me on Macbeth."
        dump_response = (
            "Here is your finished essay: Macbeth is a tragedy by William Shakespeare that illustrates the damaging physical "
            "and psychological effects of political ambition on those who seek power for its own sake. " * 10
        )
        res = self.guard.evaluate_interaction(prompt, dump_response)
        self.assertTrue(res["student_bypass_attempt"])
        self.assertTrue(res["is_answer_dump"])
        self.assertLessEqual(res["pedagogical_integrity_score"], 40.0)

    def test_socratic_scaffolding_approval(self):
        prompt = "How do I solve for x in 2x + 4 = 12?"
        socratic_response = (
            "Great question! What is the first step you would take to isolate the term with x? "
            "Hint: Think about what operation undoes addition."
        )
        res = self.guard.evaluate_interaction(prompt, socratic_response)
        self.assertFalse(res["is_answer_dump"])
        self.assertGreaterEqual(res["pedagogical_integrity_score"], 80.0)
        self.assertEqual(res["pedagogical_mode"], "EXEMPLARY_SOCRATIC_SCAFFOLDING")

if __name__ == "__main__":
    unittest.main()
