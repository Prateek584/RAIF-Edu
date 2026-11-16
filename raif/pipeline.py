"""
Master Unified Responsible AI Pipeline for Educational Applications
Coordinates Privacy, Safety, Pedagogical Integrity, Factual Grounding, Explainability, and Governance.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

from .privacy.ferpa_guard import FERPAConsentGuard
from .safety.toxicity_filter import ToxicityFilter
from .safety.age_appropriateness import AgeAppropriatenessEvaluator
from .pedagogy.socratic_guard import SocraticPedagogyGuard
from .factual.grounding_verifier import GroundingVerifier
from .explainability.transparent_rubric import TransparentRubricScorer
from .governance.audit_logger import GovernanceAuditLogger

@dataclass
class RAIInspectionReport:
    """
    Standardized Responsible AI audit report for an educational interaction.
    """
    composite_rai_score: float
    verdict: str  # APPROVED, FLAGGED_FOR_REVIEW, BLOCKED
    requires_human_review: bool
    privacy: Dict[str, Any]
    safety: Dict[str, Any]
    pedagogy: Dict[str, Any]
    grounding: Dict[str, Any]
    explainability: Dict[str, Any]
    audit_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class EduResponsibleAIPipeline:
    """
    Central evaluation engine executing multi-pillar responsible AI audits
    on learner queries and educational AI outputs.
    """

    def __init__(self, log_filepath: Optional[str] = None):
        self.privacy_guard = FERPAConsentGuard()
        self.toxicity_filter = ToxicityFilter()
        self.age_evaluator = AgeAppropriatenessEvaluator()
        self.pedagogy_guard = SocraticPedagogyGuard()
        self.grounding_verifier = GroundingVerifier()
        self.rubric_scorer = TransparentRubricScorer()
        self.audit_logger = GovernanceAuditLogger(log_filepath)

    def inspect(
        self,
        student_prompt: str,
        ai_response: str,
        student_age: int = 16,
        target_education_tier: str = "high",
        curriculum_reference: str = "",
        auto_log: bool = True
    ) -> RAIInspectionReport:
        """
        Runs comprehensive evaluation across all Responsible AI dimensions.
        """
        # 1. Privacy & FERPA audit
        privacy_res = self.privacy_guard.evaluate_compliance(
            student_prompt + " " + ai_response,
            student_age=student_age
        )

        # 2. Safety & Toxicity check
        combined_text = f"Prompt: {student_prompt}\nResponse: {ai_response}"
        toxicity_res = self.toxicity_filter.evaluate(combined_text)
        age_res = self.age_evaluator.evaluate_target_tier(ai_response, target_education_tier)

        safety_score = max(0.0, 100.0 - (toxicity_res["toxicity_score"] * 100))
        safety_payload = {
            "safety_score": round(safety_score, 1),
            "toxicity_analysis": toxicity_res,
            "age_suitability": age_res
        }

        # 3. Pedagogical integrity & Socratic scaffolding
        pedagogy_res = self.pedagogy_guard.evaluate_interaction(student_prompt, ai_response)

        # 4. Factual grounding & Hallucination verification
        grounding_res = self.grounding_verifier.evaluate_grounding(ai_response, curriculum_reference)

        # 5. Explainability & Transparent rubric
        explainability_res = self.rubric_scorer.explain_evaluation(student_prompt)

        # 6. Composite Responsible AI Index Calculation (Weighted formulation)
        # Weights: Safety (25%), Privacy (25%), Pedagogy (25%), Grounding (15%), Explainability (10%)
        w_safety = safety_score * 0.25
        w_privacy = privacy_res["privacy_score"] * 0.25
        w_pedagogy = pedagogy_res["pedagogical_integrity_score"] * 0.25
        w_grounding = grounding_res["grounding_score"] * 0.15
        w_explain = (explainability_res["confidence"] * 100) * 0.10

        composite_score = round(w_safety + w_privacy + w_pedagogy + w_grounding + w_explain, 1)

        # Determine Verdict & Escalation triggers
        requires_review = False
        if (
            toxicity_res["requires_human_intervention"]
            or privacy_res["status"] == "CRITICAL_VIOLATION"
            or pedagogy_res["is_answer_dump"]
            or grounding_res["hallucination_risk"] >= 0.70
            or composite_score < 65.0
        ):
            requires_review = True

        if toxicity_res["severity"] == "CRITICAL" or privacy_res["privacy_score"] < 40:
            verdict = "BLOCKED"
        elif requires_review:
            verdict = "FLAGGED_FOR_REVIEW"
        else:
            verdict = "APPROVED"

        report = RAIInspectionReport(
            composite_rai_score=composite_score,
            verdict=verdict,
            requires_human_review=requires_review,
            privacy=privacy_res,
            safety=safety_payload,
            pedagogy=pedagogy_res,
            grounding=grounding_res,
            explainability=explainability_res
        )

        if auto_log:
            audit_id = self.audit_logger.log_inspection(report.to_dict())
            report.audit_id = audit_id

        return report
