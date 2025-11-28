"""
Startup script for TV Campaign Impact Analyzer
"""

import subprocess
import sys
from pathlib import Path

# Generate sample data if it doesn't exist
sample_data_path = Path('sample_data/nielsen_tv_sample.csv')
if not sample_data_path.exists():
    print("📊 Generating sample data...")
    from agents.data_agent import create_sample_data

    sample_data_path.parent.mkdir(exist_ok=True)
    sample_df = create_sample_data()
    sample_df.to_csv(sample_data_path, index=False)
    print(f"✅ Sample data created: {sample_data_path}")

# Run Streamlit app
print("\n🚀 Starting TV Campaign Impact Analyzer...")
print("🌐 Opening browser at http://localhost:8501\n")

subprocess.run([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "streamlit_app/app.py",
    "--server.port=8501",
    "--server.headless=false"
])
