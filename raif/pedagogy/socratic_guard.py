"""
Socratic Scaffolding and Academic Integrity Guard
Distinguishes between academic shortcutting (homework dumping) and healthy Socratic tutoring.
"""

import re
from typing import Dict, List, Any

class SocraticPedagogyGuard:
    """
    Evaluates student-AI interactions to safeguard academic integrity and encourage
    active cognitive engagement through Socratic dialogue rather than answer-dumping.
    """

    HOMEWORK_SHORTCUT_PROMPT_PATTERNS = [
        r"\b(write (my|an) essay for me|write this entire assignment|do my homework)\b",
        r"\b(give me the direct answer|just tell me the answer|solve all these questions for me)\b",
        r"\b(write the code for my test|cheat on my quiz)\b"
    ]

    SOCRATIC_INDICATORS = [
        r"\b(what do you think|how would you start|what is the first step)\b",
        r"\b(let's break this down|consider the following|hint:)\b",
        r"\b(why do you believe|can you identify|recall the formula)\b",
        r"\b(give it a try and share your steps)\b"
    ]

    DIRECT_ANSWER_PATTERNS = [
        r"^The answer is\s+[:\-]?\s*([A-D]|\d+|[a-zA-Z\s]+)$",
        r"^Here is the complete solution:\s*",
        r"^Here is your finished essay:\s*"
    ]

    def __init__(self):
        self.shortcut_regexes = [re.compile(p, re.IGNORECASE) for p in self.HOMEWORK_SHORTCUT_PROMPT_PATTERNS]
        self.socratic_regexes = [re.compile(p, re.IGNORECASE) for p in self.SOCRATIC_INDICATORS]
        self.direct_regexes = [re.compile(p, re.IGNORECASE) for p in self.DIRECT_ANSWER_PATTERNS]

    def evaluate_interaction(self, student_prompt: str, ai_response: str) -> Dict[str, Any]:
        """
        Assesses the student prompt for bypass attempts and tests the AI response
        for pedagogical scaffolding quality.
        """
        # 1. Analyze prompt intent
        is_bypass_attempt = any(r.search(student_prompt) for r in self.shortcut_regexes)

        # 2. Analyze AI response
        socratic_hits = sum(1 for r in self.socratic_regexes if r.search(ai_response))
        question_count = ai_response.count("?")
        direct_dump_detected = any(r.search(ai_response.strip()) for r in self.direct_regexes)

        # Response length check: if student asked for essay and response is a ready-to-submit 400+ word essay
        words = ai_response.split()
        word_count = len(words)
        is_essay_dump = is_bypass_attempt and word_count > 150 and socratic_hits == 0 and question_count == 0

        # Calculate Pedagogical Integrity Score (0 - 100)
        # Higher score means better educational scaffolding
        if is_essay_dump or (is_bypass_attempt and direct_dump_detected):
            pedagogical_score = 25.0
            mode = "UNCRITICAL_ANSWER_DUMP"
            critique = "AI directly completed the student's task without pedagogical scaffolding."
        elif socratic_hits >= 2 or (question_count >= 1 and socratic_hits >= 1):
            pedagogical_score = 95.0
            mode = "EXEMPLARY_SOCRATIC_SCAFFOLDING"
            critique = "AI effectively guides the student with reflective questions and hints."
        elif question_count >= 1:
            pedagogical_score = 80.0
            mode = "MODERATE_GUIDANCE"
            critique = "AI includes prompts to involve the student, though could offer more structured scaffolding."
        else:
            pedagogical_score = 60.0
            mode = "INFORMATIVE_EXPLANATION"
            critique = "Response explains concepts but provides direct solution without actively testing understanding."

        return {
            "pedagogical_integrity_score": pedagogical_score,
            "pedagogical_mode": mode,
            "student_bypass_attempt": is_bypass_attempt,
            "is_answer_dump": is_essay_dump or direct_dump_detected,
            "socratic_indicators_found": socratic_hits,
            "guiding_questions_count": question_count,
            "critique": critique,
            "recommendation": (
                "Adopt Socratic questioning: ask the student to explain their current thinking before revealing final answers."
                if pedagogical_score < 75 else "Excellent educational engagement maintained."
            )
        }

    def generate_socratic_scaffold_suggestion(self, topic: str, difficulty: str = "intermediate") -> str:
        """
        Generates a recommended Socratic pedagogical template for a given topic.
        """
        return (
            f"Instead of providing the final answer directly for '{topic}', ask:\n"
            f"1. 'What do you already understand about {topic}?'\n"
            f"2. 'Can you identify the core principle or formula needed here?'\n"
            f"3. 'Try working through the very first step, and tell me where you feel stuck!'"
        )
