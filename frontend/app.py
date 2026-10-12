"""
Hostel Management System - Streamlit Entry Point
Delegates execution to frontend.hostel.main()
"""
import sys
from pathlib import Path

# Add current directory to path
frontend_dir = Path(__file__).resolve().parent
if str(frontend_dir) not in sys.path:
    sys.path.insert(0, str(frontend_dir))

from hostel import main

if __name__ == "__main__":
    main()
