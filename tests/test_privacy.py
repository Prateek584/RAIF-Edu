"""
Unit tests for Privacy & PII Detection Module
"""

import unittest
from raif.privacy.pii_detector import PIIDetector
from raif.privacy.ferpa_guard import FERPAConsentGuard

class TestPrivacyModule(unittest.TestCase):

    def setUp(self):
        self.detector = PIIDetector()
        self.guard = FERPAConsentGuard()

    def test_pii_detection_and_redaction(self):
        sample = "My name is John Doe, roll number RK4P25REB11, email j.doe@university.edu. Call 555-123-4567."
        findings = self.detector.detect(sample)
        self.assertTrue(len(findings) >= 2)

        sanitized, mapping = self.detector.redact(sample)
        self.assertNotIn("j.doe@university.edu", sanitized)
        self.assertNotIn("555-123-4567", sanitized)
        self.assertTrue(len(mapping) >= 2)

        # Test reversible de-anonymization
        restored = self.detector.de_anonymize(sanitized, mapping)
        self.assertEqual(restored, sample)

    def test_ferpa_coppa_compliance(self):
        # Under 13 without parental consent
        res = self.guard.evaluate_compliance("Hello bot, I am in 4th grade.", student_age=10, has_parental_consent=False)
        self.assertTrue(res["coppa_applies"])
        self.assertTrue(any("COPPA" in v for v in res["violations"]))

if __name__ == "__main__":
    unittest.main()
