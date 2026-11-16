"""
Educational Safety and Toxicity Filter
Detects cyberbullying, toxic harassment, self-harm signals, and inappropriate content.
"""

import re
from typing import Dict, List, Any

class ToxicityFilter:
    """
    Analyzes student-AI dialogues for harmful content, harassment, and unsafe language.
    Specifically calibrated for educational environments.
    """

    CATEGORIES = {
        "CYBERBULLYING": [
            r"\byou('re| are)? (an idiot|stupid|dumb|worthless|loser|pathetic|ugly|retarded)\b",
            r"\bkill yourself\b",
            r"\bnobody likes you\b",
            r"\bgo away and die\b"
        ],
        "SELF_HARM": [
            r"\b(want to die|commit suicide|end my life|hurt myself|cut myself)\b",
            r"\bbetter off dead\b"
        ],
        "PROFANITY_INAPPROPRIATE": [
            r"\b(fuck|shit|bitch|bastard|asshole|cunt|dick|pussy)\b",
            r"\b(porn|nsfw|sexually explicit|nude pics)\b"
        ],
        "HATE_SPEECH": [
            r"\b(slur|nigger|faggot|chink|spic|kike)\b",
            r"\b(hate all (muslims|jews|christians|blacks|whites|asians|gays))\b"
        ],
        "ACADEMIC_DISHONESTY": [
            r"\b(cheat on my test|hack the exam|bypass proctor|steal the answers)\b"
        ]
    }

    def __init__(self):
        self.compiled = {
            cat: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for cat, patterns in self.CATEGORIES.items()
        }

    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Scans text and returns safety evaluation, flagged items, and severity score.
        """
        if not text:
            return {
                "safe": True,
                "toxicity_score": 0.0,
                "severity": "SAFE",
                "flagged_categories": [],
                "flagged_matches": []
            }

        flagged_categories = set()
        flagged_matches = []

        for category, regex_list in self.compiled.items():
            for regex in regex_list:
                for match in regex.finditer(text):
                    flagged_categories.add(category)
                    flagged_matches.append({
                        "category": category,
                        "matched_term": match.group(0),
                        "position": (match.start(), match.end())
                    })

        # Calculate toxicity score between 0.0 and 1.0
        # High impact categories like SELF_HARM and HATE_SPEECH trigger immediate high score
        score = 0.0
        if "SELF_HARM" in flagged_categories:
            score = max(score, 0.95)
        if "HATE_SPEECH" in flagged_categories:
            score = max(score, 0.90)
        if "CYBERBULLYING" in flagged_categories:
            score = max(score, 0.75)
        if "PROFANITY_INAPPROPRIATE" in flagged_categories:
            score = max(score, 0.60)
        if "ACADEMIC_DISHONESTY" in flagged_categories:
            score = max(score, 0.50)

        # Increment for multiple occurrences
        score = min(1.0, score + (len(flagged_matches) * 0.05))

        if score >= 0.8:
            severity = "CRITICAL"
        elif score >= 0.5:
            severity = "HIGH"
        elif score >= 0.2:
            severity = "MODERATE"
        else:
            severity = "SAFE"

        return {
            "safe": score < 0.3,
            "toxicity_score": round(score, 2),
            "severity": severity,
            "flagged_categories": list(flagged_categories),
            "flagged_matches": flagged_matches,
            "requires_human_intervention": score >= 0.6 or "SELF_HARM" in flagged_categories
        }
