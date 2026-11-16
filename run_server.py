"""
Responsible AI Framework for Educational Applications (RAIF-Edu)
Application Launcher
Candidate: Prateek Gautam (Roll No: RK4P25REB11, Reg No: 12518091)
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from web.app import app

def main():
    port = int(os.environ.get("PORT", 5000))
    print("=" * 65)
    print("  RESPONSIBLE AI FRAMEWORK FOR EDUCATIONAL APPLICATIONS (RAIF-Edu)")
    print("  Author: Prateek Gautam | Roll: RK4P25REB11 | Reg: 12518091")
    print("=" * 65)
    print(f"  Web Dashboard:  http://localhost:{port}")
    print(f"  API Docs:       http://localhost:{port}/documentation")
    print("  Press Ctrl+C to terminate.")
    print("=" * 65)
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
