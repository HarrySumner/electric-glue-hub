"""
UK Spelling Update Script
Converts US spelling to UK spelling across the entire application
"""

import os
import re
from pathlib import Path

# Spelling conversions (US -> UK)
SPELLING_UPDATES = {
    # Main terms
    'Optimizer': 'Optimiser',
    'optimizer': 'optimiser',
    'Optimization': 'Optimisation',
    'optimization': 'optimisation',
    'Optimize': 'Optimise',
    'optimize': 'optimise',
    'Optimizing': 'Optimising',
    'optimizing': 'optimising',

    'Behavior': 'Behaviour',
    'behavior': 'behaviour',
    'Behaviors': 'Behaviours',
    'behaviors': 'behaviours',
    'Behavioral': 'Behavioural',
    'behavioral': 'behavioural',

    # Common variations
    'analyze': 'analyse',
    'Analyze': 'Analyse',
    'analyzing': 'analysing',
    'Analyzing': 'Analysing',
    'analyzed': 'analysed',
    'Analyzed': 'Analysed',
}

def update_file(filepath):
    """Update a single file with UK spelling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply all spelling replacements
        for us_spelling, uk_spelling in SPELLING_UPDATES.items():
            content = content.replace(us_spelling, uk_spelling)

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, filepath
        return False, None

    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False, None

def main():
    """Update all Python, Markdown, and JSON files"""
    root_dir = Path(__file__).parent

    # File extensions to update
    extensions = ['.py', '.md', '.json', '.toml']

    updated_files = []
    skipped_files = []

    for ext in extensions:
        for filepath in root_dir.rglob(f'*{ext}'):
            # Skip this script itself and backup files
            if filepath.name == 'update_uk_spelling.py' or '_OLD' in str(filepath):
                continue

            was_updated, path = update_file(filepath)
            if was_updated:
                updated_files.append(path)
            else:
                skipped_files.append(path)

    # Print summary
    print("\n" + "="*60)
    print("UK SPELLING UPDATE COMPLETE")
    print("="*60)
    print(f"\n✅ Updated {len(updated_files)} files:")
    for f in updated_files:
        print(f"   - {f.relative_to(root_dir)}")

    print(f"\n⏭️  Skipped {len(skipped_files)} files (no changes needed)")

    print("\n" + "="*60)
    print("CHANGES APPLIED:")
    print("="*60)
    for us, uk in SPELLING_UPDATES.items():
        print(f"   {us} → {uk}")

    print("\n✅ All files updated to UK spelling!")
    print("\nPlease restart Streamlit to see changes:")
    print("   streamlit run app.py")

if __name__ == '__main__':
    main()
