"""
Startup script for Electric Glue Hub
Runs on port 8505 (different from Budget Optimizer)
"""

import subprocess
import sys

print("\n" + "=" * 80)
print("ELECTRIC GLUE HUB - AGENTIC MARKETING PLATFORM")
print("=" * 80)
print("\nStarting on http://localhost:8505")
print("\nAvailable Products:")
print("  [OK] Product 1: TV Campaign Impact Analyzer (standalone on :8501)")
print("  [OK] Product 2: Marketing Intelligence Assistant (integrated)")
print("  [SOON] Product 3: Report QA Layer (coming soon)")
print("\n" + "=" * 80 + "\n")

subprocess.run([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "app.py",
    "--server.port=8505",
    "--server.headless=false"
])
