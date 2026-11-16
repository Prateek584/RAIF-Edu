"""
Responsible AI Framework for Educational Applications (RAIF-Edu)
----------------------------------------------------------------
Author: Prateek Gautam
Roll Number: RK4P25REB11
Registration Number: 12518091

An end-to-end framework designed to ensure fairness, privacy, safety,
pedagogical integrity, factual grounding, and explainability in AI-assisted
educational systems.
"""

__version__ = "1.0.0"
__author__ = "Prateek Gautam"
__project__ = "Responsible AI Framework for Educational Applications"

from .pipeline import EduResponsibleAIPipeline, RAIInspectionReport

__all__ = ["EduResponsibleAIPipeline", "RAIInspectionReport", "__version__", "__author__", "__project__"]
