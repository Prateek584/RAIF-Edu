"""
PII Detection and Tokenization Module for Educational Applications
Complies with FERPA (Family Educational Rights and Privacy Act) and COPPA.
"""

import re
from typing import Dict, List, Tuple, Any

class PIIDetector:
    """
    Detects and redacts Personally Identifiable Information (PII)
    commonly present in student prompts, assignments, and school records.
    """

    PATTERNS = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b",
        "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "STUDENT_ID": r"\b(?:Roll(?:\s*Number)?|Reg(?:\s*Number)?|Student\s*ID|ID)[:\s#]*([A-Za-z0-9]{6,12})\b|\b[A-Z]{2,4}\d{2,4}[A-Z0-9]{3,6}\b|\b\d{8,10}\b",
        "SSN_OR_GOV_ID": r"\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s\d{4}\s\d{4}\b",
        "DATE_OF_BIRTH": r"\b(?:DOB[:\s]*|born on[:\s]*)(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
        "NAME_PREFIX": r"\b(?:My name is|I am|Student:|Learner:)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b"
    }

    def __init__(self):
        self.compiled_patterns = {
            k: re.compile(v, re.IGNORECASE if k != "NAME_PREFIX" else 0)
            for k, v in self.PATTERNS.items()
        }

    def detect(self, text: str) -> List[Dict[str, Any]]:
        """
        Scans text and returns a list of non-overlapping detected PII entities.
        """
        raw_findings = []
        if not text:
            return raw_findings

        # Name prefix regex match
        name_match = re.search(self.PATTERNS["NAME_PREFIX"], text)
        if name_match:
            raw_findings.append({
                "type": "STUDENT_NAME",
                "value": name_match.group(1),
                "start": name_match.start(1),
                "end": name_match.end(1),
                "confidence": 0.95,
                "ferpa_flag": True
            })

        # Match other patterns
        for p_type, regex in self.compiled_patterns.items():
            if p_type == "NAME_PREFIX":
                continue
            for match in regex.finditer(text):
                val = match.group(0).strip()
                # If regex has capturing group, use that
                if match.groups() and match.group(1):
                    val = match.group(1).strip()
                    start = match.start(1)
                    end = match.end(1)
                else:
                    start = match.start()
                    end = match.end()

                # Filter false positives
                if p_type == "STUDENT_ID" and (len(val) < 6 or val.isalpha()):
                    continue

                raw_findings.append({
                    "type": p_type,
                    "value": val,
                    "start": start,
                    "end": end,
                    "confidence": 0.90,
                    "ferpa_flag": True
                })

        # Resolve overlapping spans: prioritize by length/priority
        # Sort by start ascending, then length descending
        raw_findings.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))

        non_overlapping: List[Dict[str, Any]] = []
        last_end = -1

        for item in raw_findings:
            if item["start"] >= last_end:
                non_overlapping.append(item)
                last_end = item["end"]

        return non_overlapping

    def redact(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Redacts detected PII by replacing occurrences with pseudonymous tokens
        (e.g., [STUDENT_NAME_1], [EMAIL_1]). Returns sanitized text and token mapping.
        """
        findings = self.detect(text)
        if not findings:
            return text, {}

        mapping: Dict[str, str] = {}
        type_counters: Dict[str, int] = {}

        # Reverse sort by start index to maintain offsets during replacement
        findings.sort(key=lambda x: x["start"], reverse=True)

        sanitized_chars = list(text)
        for item in findings:
            itype = item["type"]
            type_counters[itype] = type_counters.get(itype, 0) + 1
            token = f"[{itype}_{type_counters[itype]}]"
            mapping[token] = item["value"]

            # Replace span
            s, e = item["start"], item["end"]
            sanitized_chars[s:e] = list(token)

        sanitized_text = "".join(sanitized_chars)
        return sanitized_text, mapping

    def de_anonymize(self, sanitized_text: str, mapping: Dict[str, str]) -> str:
        """
        Restores sanitized tokens back to original values in authorized contexts.
        """
        result = sanitized_text
        for token, original in mapping.items():
            result = result.replace(token, original)
        return result
