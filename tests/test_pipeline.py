"""
Unit tests for End-to-End Responsible AI Pipeline
"""

import unittest
import tempfile
import os
from raif.pipeline import EduResponsibleAIPipeline

class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.temp_dir.name, "test_audit.json")
        self.pipeline = EduResponsibleAIPipeline(log_filepath=self.log_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_benign_socratic_interaction(self):
        student_prompt = "Can you help me understand how photosynthesis produces glucose?"
        ai_response = (
            "Certainly! Let's break this down. What pigment in plant cells absorbs sunlight, "
            "and what are the two main inputs plants take in from the environment?"
        )
        curriculum = "Photosynthesis is the process by which green plants convert light energy into glucose."
        
        report = self.pipeline.inspect(
            student_prompt=student_prompt,
            ai_response=ai_response,
            student_age=15,
            curriculum_reference=curriculum
        )

        self.assertGreaterEqual(report.composite_rai_score, 70.0)
        self.assertIn(report.verdict, ["APPROVED", "FLAGGED_FOR_REVIEW"])
        self.assertIsNotNone(report.audit_id)

    def test_toxic_interaction_escalation(self):
        prompt = "You are worthless and an idiot."
        response = "I am an educational AI and here to assist you."
        report = self.pipeline.inspect(prompt, response)
        
        self.assertTrue(report.requires_human_review)

if __name__ == "__main__":
    unittest.main()
