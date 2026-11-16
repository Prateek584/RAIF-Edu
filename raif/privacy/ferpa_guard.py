"""
FERPA and COPPA Compliance Assessment for Educational Systems
"""

from typing import Dict, Any, List
from .pii_detector import PIIDetector

class FERPAConsentGuard:
    """
    Evaluates whether an educational prompt or context complies with
    Family Educational Rights and Privacy Act (FERPA) and
    Children's Online Privacy Protection Act (COPPA).
    """

    def __init__(self):
        self.detector = PIIDetector()

    def evaluate_compliance(
        self,
        text: str,
        student_age: int = 16,
        has_parental_consent: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates compliance status, risk score, and policy flags.
        """
        pii_entities = self.detector.detect(text)
        sanitized_text, mapping = self.detector.redact(text)

        violations = []
        recommendations = []

        # COPPA check: Children under 13
        coppa_risk = False
        if student_age < 13 and not has_parental_consent:
            coppa_risk = True
            violations.append("COPPA Breach Risk: Learner is under 13 without verified parental consent.")
            recommendations.append("Obtain verified guardian consent before processing persistent learner data.")

        # FERPA check: Unredacted PII in transmission
        if pii_entities:
            violations.append(f"FERPA Warning: Detected {len(pii_entities)} unprotected student identifiers in raw input.")
            recommendations.append("Mask personal identifiers before routing prompts to external cloud models.")

        # Compute Privacy Score (100 = completely compliant, 0 = severe breach risk)
        deduction = (len(pii_entities) * 15) + (35 if coppa_risk else 0)
        privacy_score = max(0, 100 - deduction)

        status = "COMPLIANT"
        if privacy_score < 50:
            status = "CRITICAL_VIOLATION"
        elif privacy_score < 80:
            status = "NEEDS_REMEDIATION"

        return {
            "status": status,
            "privacy_score": privacy_score,
            "detected_pii_count": len(pii_entities),
            "pii_entities": pii_entities,
            "sanitized_text": sanitized_text,
            "redaction_map": mapping,
            "violations": violations,
            "recommendations": recommendations,
            "coppa_applies": student_age < 13
        }
