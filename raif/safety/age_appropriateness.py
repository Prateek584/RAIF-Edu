"""
Age Appropriateness and Readability Evaluator for Educational Materials
Implements Flesch Reading Ease and Flesch-Kincaid Grade Level formulas.
"""

import re
from typing import Dict, Any

class AgeAppropriatenessEvaluator:
    """
    Evaluates whether generated or provided learning content is linguistically
    and conceptually suitable for the intended age bracket.
    """

    EDUCATIONAL_LEVELS = {
        "primary": {"min_grade": 1, "max_grade": 5, "name": "Primary School (Grades 1-5)"},
        "middle": {"min_grade": 6, "max_grade": 8, "name": "Middle School (Grades 6-8)"},
        "high": {"min_grade": 9, "max_grade": 12, "name": "High School (Grades 9-12)"},
        "college": {"min_grade": 13, "max_grade": 18, "name": "Higher Education / University"}
    }

    def _count_syllables(self, word: str) -> int:
        word = word.lower()
        if len(word) <= 3:
            return 1
        word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
        word = re.sub(r'^y', '', word)
        matches = re.findall(r'[aeiouy]{1,2}', word)
        return max(1, len(matches))

    def calculate_readability(self, text: str) -> Dict[str, float]:
        """
        Calculates Flesch Reading Ease and Flesch-Kincaid Grade Level.
        """
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        words = re.findall(r'\b[A-Za-z]+\b', text)

        num_sentences = max(1, len(sentences))
        num_words = max(1, len(words))
        total_syllables = sum(self._count_syllables(w) for w in words)

        # Flesch Reading Ease: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
        asl = num_words / num_sentences
        asw = total_syllables / num_words
        flesch_ease = 206.835 - (1.015 * asl) - (84.6 * asw)
        flesch_ease = max(0.0, min(100.0, flesch_ease))

        # Flesch-Kincaid Grade Level: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        fk_grade = (0.39 * asl) + (11.8 * asw) - 15.59
        fk_grade = max(1.0, round(fk_grade, 1))

        return {
            "sentence_count": num_sentences,
            "word_count": num_words,
            "flesch_reading_ease": round(flesch_ease, 1),
            "kincaid_grade_level": fk_grade
        }

    def evaluate_target_tier(self, text: str, target_tier: str = "high") -> Dict[str, Any]:
        """
        Determines if the text matches the desired educational tier.
        """
        tier_cfg = self.EDUCATIONAL_LEVELS.get(target_tier.lower(), self.EDUCATIONAL_LEVELS["high"])
        metrics = self.calculate_readability(text)
        grade = metrics["kincaid_grade_level"]

        is_appropriate = tier_cfg["min_grade"] <= grade <= tier_cfg["max_grade"] + 2
        
        status = "OPTIMAL"
        feedback = f"Content readability matches {tier_cfg['name']} (Grade {grade})."

        if grade < tier_cfg["min_grade"] - 1:
            status = "TOO_SIMPLE"
            feedback = f"Content might be overly simplistic for {tier_cfg['name']} (Grade {grade})."
        elif grade > tier_cfg["max_grade"] + 2:
            status = "TOO_COMPLEX"
            feedback = f"Cognitive complexity (Grade {grade}) exceeds target {tier_cfg['name']} limit."

        return {
            "target_tier": target_tier,
            "tier_name": tier_cfg["name"],
            "appropriate": is_appropriate,
            "alignment_status": status,
            "grade_level": grade,
            "flesch_ease": metrics["flesch_reading_ease"],
            "feedback": feedback
        }
