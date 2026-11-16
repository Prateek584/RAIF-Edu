"""
Responsible AI Framework for Educational Applications (RAIF-Edu)
Web Server and REST API
Author: Prateek Gautam (Roll No: RK4P25REB11, Reg No: 12518091)
"""

import os
import sys
import json
from flask import Flask, render_template, request, jsonify, Response

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from raif.pipeline import EduResponsibleAIPipeline
from raif.fairness.bias_auditor import BiasAuditor
from raif.privacy.ferpa_guard import FERPAConsentGuard
from raif.pedagogy.socratic_guard import SocraticPedagogyGuard
from raif.factual.grounding_verifier import GroundingVerifier
from raif.explainability.transparent_rubric import TransparentRubricScorer

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "web", "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "web", "static")
)

# Instantiate core components
pipeline = EduResponsibleAIPipeline()
bias_auditor = BiasAuditor()
ferpa_guard = FERPAConsentGuard()
pedagogy_guard = SocraticPedagogyGuard()
grounding_verifier = GroundingVerifier()
rubric_scorer = TransparentRubricScorer()

# Pre-load curriculum reference data
CURRICULUM_FILE = os.path.join(PROJECT_ROOT, "data", "reference_curriculum.json")
CURRICULUM_DATA = {}
if os.path.exists(CURRICULUM_FILE):
    try:
        with open(CURRICULUM_FILE, "r", encoding="utf-8") as f:
            CURRICULUM_DATA = json.load(f)
    except Exception:
        pass

# Web UI Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fairness")
def fairness_page():
    return render_template("fairness.html")

@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")

@app.route("/pedagogy")
def pedagogy_page():
    return render_template("pedagogy.html")

@app.route("/logs")
def logs_page():
    return render_template("logs.html")

@app.route("/documentation")
def docs_page():
    return render_template("documentation.html")

# REST API Endpoints
@app.route("/api/v1/inspect", methods=["POST"])
def api_inspect():
    data = request.get_json() or {}
    student_prompt = data.get("student_prompt", "")
    ai_response = data.get("ai_response", "")
    student_age = int(data.get("student_age", 16))
    target_tier = data.get("target_education_tier", "high")
    curriculum_ref = data.get("curriculum_reference", "")

    # If curriculum reference not directly given, check if topic keyword is supplied
    topic_key = data.get("curriculum_topic", "")
    if not curriculum_ref and topic_key in CURRICULUM_DATA.get("topics", {}):
        curriculum_ref = CURRICULUM_DATA["topics"][topic_key]["canonical_facts"]

    report = pipeline.inspect(
        student_prompt=student_prompt,
        ai_response=ai_response,
        student_age=student_age,
        target_education_tier=target_tier,
        curriculum_reference=curriculum_ref,
        auto_log=True
    )

    return jsonify(report.to_dict())

@app.route("/api/v1/fairness/audit", methods=["POST"])
def api_fairness_audit():
    data = request.get_json() or {}
    dataset_file = data.get("dataset_path") or os.path.join(PROJECT_ROOT, "data", "student_assessments_sample.csv")
    protected_attr = data.get("protected_attribute", "gender")
    privileged_val = data.get("privileged_group", "Male")
    unprivileged_val = data.get("unprivileged_group", "Female")
    outcome_attr = data.get("outcome_attribute", "ai_awarded_grade")
    pass_threshold = float(data.get("pass_threshold", 75.0))

    if not os.path.exists(dataset_file):
        return jsonify({"error": f"Dataset file not found: {dataset_file}"}), 404

    records = bias_auditor.load_csv(dataset_file)
    audit_results = bias_auditor.audit_dataset(
        records=records,
        protected_attr=protected_attr,
        privileged_val=privileged_val,
        unprivileged_val=unprivileged_val,
        outcome_attr=outcome_attr,
        pass_threshold=pass_threshold
    )

    # Also audit qualitative feedback for coded bias if feedback column exists
    qualitative_findings = []
    for r in records[:10]:
        feedback = r.get("feedback_notes", "")
        if feedback:
            txt_res = bias_auditor.audit_text_feedback(feedback)
            if txt_res["has_stereotyped_language"]:
                qualitative_findings.append({
                    "student_id": r.get("student_id"),
                    "gender": r.get("gender"),
                    "feedback": feedback,
                    "analysis": txt_res
                })

    audit_results["qualitative_stereotypes_found"] = qualitative_findings
    audit_results["sample_records_preview"] = records[:8]

    return jsonify(audit_results)

@app.route("/api/v1/privacy/sanitize", methods=["POST"])
def api_privacy_sanitize():
    data = request.get_json() or {}
    raw_text = data.get("text", "")
    student_age = int(data.get("student_age", 16))
    has_consent = bool(data.get("has_parental_consent", False))

    res = ferpa_guard.evaluate_compliance(
        raw_text,
        student_age=student_age,
        has_parental_consent=has_consent
    )
    return jsonify(res)

@app.route("/api/v1/privacy/de-anonymize", methods=["POST"])
def api_privacy_deanonymize():
    data = request.get_json() or {}
    sanitized_text = data.get("sanitized_text", "")
    mapping = data.get("mapping", {})
    restored = ferpa_guard.detector.de_anonymize(sanitized_text, mapping)
    return jsonify({"restored_text": restored})

@app.route("/api/v1/pedagogy/evaluate", methods=["POST"])
def api_pedagogy_evaluate():
    data = request.get_json() or {}
    prompt = data.get("student_prompt", "")
    response = data.get("ai_response", "")
    res = pedagogy_guard.evaluate_interaction(prompt, response)
    
    # Generate Socratic scaffold suggestion if bypass was detected
    if res["is_answer_dump"] or res["student_bypass_attempt"]:
        topic = data.get("topic", "the student's assignment topic")
        res["suggested_socratic_response"] = pedagogy_guard.generate_socratic_scaffold_suggestion(topic)
        
    return jsonify(res)

@app.route("/api/v1/explainability/rubric", methods=["POST"])
def api_explainability_rubric():
    data = request.get_json() or {}
    submission = data.get("student_submission", "")
    score = float(data.get("assigned_score", 85.0))
    res = rubric_scorer.explain_evaluation(submission, score)
    return jsonify(res)

@app.route("/api/v1/logs", methods=["GET"])
def api_get_logs():
    all_logs = pipeline.audit_logger.get_all_logs()
    return jsonify({"total": len(all_logs), "logs": list(reversed(all_logs))})

@app.route("/api/v1/governance/compliance-report", methods=["GET"])
def api_compliance_report():
    report = pipeline.audit_logger.generate_compliance_report()
    return jsonify(report)

@app.route("/api/v1/export/markdown", methods=["GET"])
def api_export_markdown():
    report = pipeline.audit_logger.generate_compliance_report()
    logs = pipeline.audit_logger.get_all_logs()

    md = f"""# Institutional Responsible AI Compliance Audit Report
**Project**: Responsible AI Framework for Educational Applications (RAIF-Edu)  
**Author**: Prateek Gautam (Roll No: RK4P25REB11 | Reg No: 12518091)  
**Generated At**: {report.get('generated_at')}  

## Executive Summary
- **Total Audited Sessions**: {report.get('total_audits')}
- **Institutional Compliance Rate**: {report.get('compliance_rate_percent')}%
- **Human-in-the-Loop Escalations**: {report.get('hitl_escalations_count')}
- **Average Safety Index**: {report.get('average_safety_index')} / 100
- **Average Privacy (FERPA) Index**: {report.get('average_privacy_index')} / 100
- **Average Pedagogical Integrity Index**: {report.get('average_pedagogy_index')} / 100

## Recent Audit Trail (Last 10 Records)
| Audit ID | Timestamp | Composite Score | Verdict | Review Status |
| :--- | :--- | :--- | :--- | :--- |
"""
    for item in list(reversed(logs))[:10]:
        rep = item.get("report", {})
        md += f"| {item.get('audit_id')} | {item.get('timestamp')} | {rep.get('composite_rai_score')} | {rep.get('verdict')} | {item.get('review_status')} |\n"

    return Response(md, mimetype="text/markdown", headers={"Content-disposition": "attachment; filename=rai_compliance_report.md"})

if __name__ == "__main__":
    print(f"Starting Responsible AI Edu Framework on http://127.0.0.1:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=False)
