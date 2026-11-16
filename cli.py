"""
Responsible AI Framework for Educational Applications (RAIF-Edu)
Command Line Interface (CLI)
Candidate: Prateek Gautam (Roll No: RK4P25REB11, Reg No: 12518091)
"""

import argparse
import json
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from raif.pipeline import EduResponsibleAIPipeline
from raif.fairness.bias_auditor import BiasAuditor
from raif.privacy.pii_detector import PIIDetector

def run_inspect(args):
    pipeline = EduResponsibleAIPipeline()
    print(f"\n[RAIF-Edu] Auditing interaction...")
    report = pipeline.inspect(
        student_prompt=args.prompt,
        ai_response=args.response,
        student_age=args.age,
        target_education_tier=args.tier,
        curriculum_reference=args.curriculum or ""
    )
    print("=" * 60)
    print(f"VERDICT:                 {report.verdict}")
    print(f"COMPOSITE RAI SCORE:     {report.composite_rai_score} / 100")
    print(f"HUMAN REVIEW REQUIRED:   {report.requires_human_review}")
    print(f"PRIVACY SCORE:           {report.privacy['privacy_score']} / 100 (Status: {report.privacy['status']})")
    print(f"SAFETY SCORE:            {report.safety['safety_score']} / 100 (Toxicity: {report.safety['toxicity_analysis']['toxicity_score']})")
    print(f"PEDAGOGICAL SCORE:       {report.pedagogy['pedagogical_integrity_score']} / 100 (Mode: {report.pedagogy['pedagogical_mode']})")
    print(f"FACTUAL GROUNDING:       {report.grounding['grounding_score']} / 100 (Hallucination Risk: {report.grounding['hallucination_risk']})")
    print(f"AUDIT ID:                {report.audit_id}")
    print("=" * 60)

def run_fairness(args):
    auditor = BiasAuditor()
    filepath = args.file or os.path.join(PROJECT_ROOT, "data", "student_assessments_sample.csv")
    print(f"\n[RAIF-Edu] Auditing dataset fairness for {filepath}...")
    records = auditor.load_csv(filepath)
    res = auditor.audit_dataset(
        records=records,
        protected_attr=args.attribute,
        privileged_val=args.privileged,
        unprivileged_val=args.unprivileged,
        pass_threshold=args.threshold
    )
    print("=" * 60)
    print(f"Protected Attribute:     {res['protected_attribute']}")
    print(f"Privileged Group:        {res['privileged_group']} (Pass Rate: {res['pass_rates'][res['privileged_group']]*100:.1f}%)")
    print(f"Unprivileged Group:      {res['unprivileged_group']} (Pass Rate: {res['pass_rates'][res['unprivileged_group']]*100:.1f}%)")
    print(f"Disparate Impact Ratio:  {res['disparate_impact_ratio']} (EEOC 80% Rule: {'PASSED' if res['four_fifths_rule_compliant'] else 'FAILED'})")
    print(f"Demographic Parity Diff: {res['demographic_parity_diff']*100:.1f}%")
    print(f"Overall Fairness Score:  {res['fairness_score']} / 100")
    print("-" * 60)
    for f in res["findings"]:
        print(f" -> {f}")
    print("=" * 60)

def run_sanitize(args):
    detector = PIIDetector()
    print(f"\n[RAIF-Edu] Detecting and Redacting Student PII...")
    sanitized, mapping = detector.redact(args.text)
    print("-" * 60)
    print("ORIGINAL TEXT:\n", args.text)
    print("\nSANITIZED TEXT (Cloud-Safe):\n", sanitized)
    print("\nTOKEN MAPPING KEY:\n", json.dumps(mapping, indent=2))
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="RAIF-Edu: Responsible AI Framework for Educational Applications",
        epilog="Candidate: Prateek Gautam (Roll No: RK4P25REB11, Reg No: 12518091)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Run comprehensive multi-pillar audit on an interaction")
    p_inspect.add_argument("--prompt", required=True, help="Student prompt")
    p_inspect.add_argument("--response", required=True, help="AI generated response")
    p_inspect.add_argument("--age", type=int, default=16, help="Student age")
    p_inspect.add_argument("--tier", default="high", choices=["primary", "middle", "high", "college"])
    p_inspect.add_argument("--curriculum", default="", help="Reference curriculum text")
    p_inspect.set_defaults(func=run_inspect)

    # fairness
    p_fairness = subparsers.add_parser("fairness", help="Audit tabular grading dataset for bias")
    p_fairness.add_argument("--file", default="", help="Path to CSV dataset")
    p_fairness.add_argument("--attribute", default="gender", help="Protected attribute column")
    p_fairness.add_argument("--privileged", default="Male", help="Privileged group label")
    p_fairness.add_argument("--unprivileged", default="Female", help="Unprivileged group label")
    p_fairness.add_argument("--threshold", type=float, default=75.0, help="Pass grade threshold")
    p_fairness.set_defaults(func=run_fairness)

    # sanitize
    p_sanitize = subparsers.add_parser("sanitize", help="Redact student personal identifiers")
    p_sanitize.add_argument("--text", required=True, help="Raw student text")
    p_sanitize.set_defaults(func=run_sanitize)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
