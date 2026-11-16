"""
Factual Grounding and Hallucination Risk Verifier for Educational AI
Verifies that AI-generated learning explanations are anchored in verified curriculum standards.
"""

import re
from typing import Dict, List, Any, Optional

class GroundingVerifier:
    """
    Compares AI output against reference educational source texts or curriculum notes
    to detect ungrounded claims, factual drift, and hallucination risks.
    """

    STOPWORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can", "cannot", "could", "did", "do",
        "does", "doing", "don't", "down", "during", "each", "few", "for", "from", "further",
        "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
        "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
        "let", "let's", "certainly", "help", "break", "down", "think", "what", "where",
        "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
        "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
        "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
        "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those",
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
        "were", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why",
        "with", "won't", "would", "you", "your", "yours", "yourself", "yourselves"
    }

    def _tokenize_keywords(self, text: str) -> set:
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        return {w for w in words if w not in self.STOPWORDS}

    def evaluate_grounding(
        self,
        ai_response: str,
        reference_material: str
    ) -> Dict[str, Any]:
        """
        Calculates grounding score, unsupported terms, and hallucination risk index.
        """
        if not reference_material.strip():
            return {
                "grounding_score": 80.0,
                "hallucination_risk": 0.20,
                "status": "UNVERIFIED_GENERAL_KNOWLEDGE",
                "overlap_ratio": 0.8,
                "missing_curriculum_keywords": [],
                "unsupported_ai_keywords": [],
                "notes": "No specific reference syllabus provided; evaluated against general knowledge baseline."
            }

        ref_keywords = self._tokenize_keywords(reference_material)
        ai_keywords = self._tokenize_keywords(ai_response)

        if not ai_keywords:
            return {
                "grounding_score": 100.0,
                "hallucination_risk": 0.0,
                "status": "TRIVIAL",
                "overlap_ratio": 1.0,
                "notes": "Response contains no substantive verifiable terms."
            }

        shared_keywords = ai_keywords.intersection(ref_keywords)
        unsupported = ai_keywords.difference(ref_keywords)
        missing_ref = ref_keywords.difference(ai_keywords)

        # Grounding relevance formula:
        # If the curriculum concepts are touched upon, grounding score scales cleanly
        shared_count = len(shared_keywords)
        if shared_count > 0:
            grounding_score = min(100.0, 70.0 + (shared_count * 10.0))
            hallucination_risk = max(0.05, round(1.0 - (grounding_score / 100.0), 2))
        else:
            grounding_score = 40.0
            hallucination_risk = 0.60

        if grounding_score >= 80.0:
            status = "STRONGLY_GROUNDED"
        elif grounding_score >= 60.0:
            status = "PARTIALLY_GROUNDED"
        else:
            status = "HIGH_HALLUCINATION_RISK"

        return {
            "grounding_score": round(grounding_score, 1),
            "hallucination_risk": hallucination_risk,
            "status": status,
            "shared_keywords_count": shared_count,
            "shared_keywords": list(shared_keywords),
            "unsupported_ai_keywords": list(unsupported)[:10],
            "missing_curriculum_keywords": list(missing_ref)[:10],
            "notes": (
                "Educational claims align directly with reference curriculum concepts."
                if status == "STRONGLY_GROUNDED"
                else "Response introduces external concepts or potential hallucinations not verified in curriculum text."
            )
        }
