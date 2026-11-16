"""
Explainable AI (XAI) Rubric and Feedback Transparency Module
Demystifies automated educational scoring by generating multi-dimensional criteria rubrics.
"""

from typing import Dict, List, Any
import re

class TransparentRubricScorer:
    """
    Deconstructs automated grading and evaluation into transparent, traceable rubrics
    with evidence extraction and confidence calibration.
    """

    CRITERIA = [
        {
            "name": "Conceptual Understanding",
            "weight": 0.35,
            "description": "Mastery of foundational theory, definitions, and domain principles.",
            "keywords": ["define", "concept", "principle", "theory", "formula", "meaning", "law"]
        },
        {
            "name": "Methodological & Problem Solving Rigor",
            "weight": 0.30,
            "description": "Step-by-step logic, problem breakdown, calculation, and structural cohesion.",
            "keywords": ["step", "calculate", "solve", "method", "logic", "because", "therefore", "derive"]
        },
        {
            "name": "Clarity of Expression",
            "weight": 0.20,
            "description": "Grammatical precision, terminology usage, and clear communicative structure.",
            "keywords": ["clear", "structure", "organized", "cohesive", "summarize", "express"]
        },
        {
            "name": "Critical Reflection & Originality",
            "weight": 0.15,
            "description": "Ability to draw connections, synthesize novel examples, and evaluate limitations.",
            "keywords": ["example", "analyze", "evaluate", "compare", "contrast", "limitation", "insight"]
        }
    ]

    def explain_evaluation(
        self,
        student_submission: str,
        assigned_score: float = 85.0
    ) -> Dict[str, Any]:
        """
        Synthesizes a transparent rubric breakdown for a student submission.
        """
        text_lower = student_submission.lower()
        words = text_lower.split()
        word_count = len(words)

        rubric_breakdown = []
        overall_evidence = []

        total_weighted_score = 0.0

        for criterion in self.CRITERIA:
            # Check presence of indicator keywords
            hits = [kw for kw in criterion["keywords"] if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)]
            
            # Base criterion score adjusted by keyword evidence and length
            base_ratio = min(1.0, (len(hits) * 0.25) + (min(word_count, 150) / 200.0))
            criterion_score = round(base_ratio * 100, 1)
            weighted_contrib = round(criterion_score * criterion["weight"], 1)
            total_weighted_score += weighted_contrib

            rubric_breakdown.append({
                "criterion": criterion["name"],
                "weight_percent": int(criterion["weight"] * 100),
                "score": criterion_score,
                "weighted_contribution": weighted_contrib,
                "description": criterion["description"],
                "evidence_found": hits if hits else ["General textual context"]
            })

        # Confidence score based on length and substantive indicators
        confidence = 0.94 if word_count > 60 else (0.80 if word_count > 25 else 0.65)

        return {
            "assigned_score": assigned_score,
            "rubric_derived_score": round(total_weighted_score, 1),
            "confidence": confidence,
            "explainability_rating": "HIGH_TRANSPARENCY",
            "criteria_breakdown": rubric_breakdown,
            "transparency_rationale": (
                f"Evaluation is distributed across 4 pedagogical pillars. "
                f"Confidence is rated at {int(confidence*100)}% based on textual signal density."
            )
        }
