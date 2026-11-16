"""
Institutional Governance and Audit Trail Module
Logs student-AI interactions, manages Human-In-The-Loop (HITL) escalations,
and generates compliance audit reports.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class GovernanceAuditLogger:
    """
    Maintains immutable interaction logs and manages educator review queues
    to satisfy institutional accountability standards.
    """

    def __init__(self, log_filepath: Optional[str] = None):
        if not log_filepath:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.log_filepath = os.path.join(base_dir, "data", "rai_audit_log.json")
        else:
            self.log_filepath = log_filepath

        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.log_filepath):
            os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)
            with open(self.log_filepath, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def log_inspection(self, report_dict: Dict[str, Any]) -> str:
        """
        Appends an inspection report to the audit repository with timestamp and unique audit ID.
        """
        records = self.get_all_logs()

        audit_id = f"AUDIT-EDU-{int(time.time())}-{len(records) + 1:04d}"
        entry = {
            "audit_id": audit_id,
            "timestamp": datetime.now().isoformat(),
            "framework_version": "1.0.0",
            "report": report_dict,
            "escalated_for_human_review": report_dict.get("requires_human_review", False),
            "review_status": "PENDING" if report_dict.get("requires_human_review", False) else "RESOLVED_AUTO"
        }

        records.append(entry)
        with open(self.log_filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        return audit_id

    def get_all_logs(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.log_filepath):
            return []
        try:
            with open(self.log_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_hitl_escalations(self) -> List[Dict[str, Any]]:
        """
        Retrieves interactions requiring manual teacher/counselor review.
        """
        logs = self.get_all_logs()
        return [entry for entry in logs if entry.get("escalated_for_human_review", False)]

    def generate_compliance_report(self) -> Dict[str, Any]:
        """
        Summarizes institutional compliance metrics across all audited sessions.
        """
        logs = self.get_all_logs()
        total = len(logs)
        if total == 0:
            return {
                "total_audits": 0,
                "compliance_rate_percent": 100.0,
                "hitl_escalations_count": 0,
                "average_safety_index": 100.0,
                "average_privacy_index": 100.0,
                "average_pedagogy_index": 100.0
            }

        hitl_count = sum(1 for e in logs if e.get("escalated_for_human_review"))
        safety_scores = [e["report"].get("safety", {}).get("safety_score", 100) for e in logs]
        privacy_scores = [e["report"].get("privacy", {}).get("privacy_score", 100) for e in logs]
        pedagogy_scores = [e["report"].get("pedagogy", {}).get("pedagogical_integrity_score", 80) for e in logs]

        avg_safety = round(sum(safety_scores) / total, 1)
        avg_privacy = round(sum(privacy_scores) / total, 1)
        avg_pedagogy = round(sum(pedagogy_scores) / total, 1)

        compliant_count = total - hitl_count
        compliance_rate = round((compliant_count / total) * 100, 1)

        return {
            "total_audits": total,
            "compliance_rate_percent": compliance_rate,
            "hitl_escalations_count": hitl_count,
            "average_safety_index": avg_safety,
            "average_privacy_index": avg_privacy,
            "average_pedagogy_index": avg_pedagogy,
            "generated_at": datetime.now().isoformat()
        }
