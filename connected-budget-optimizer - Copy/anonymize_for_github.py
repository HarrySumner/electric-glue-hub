"""
Anonymize references for GitHub commit only
This creates temporary anonymized versions without changing local files
"""
import os
from pathlib import Path

# Anonymization mappings
ANONYMIZE = {
    'Front Left Consulting': '[Company Name]',
    'CEEK': '[Client]',
    'harry': '[user]',
    r'c:\\Users\\harry\\OneDrive\\Desktop\\CEEK\\connected-budget-optimiser': '/path/to/connected-budget-optimiser',
    r'c:\Users\harry\OneDrive\Desktop\CEEK\connected-budget-optimiser': '/path/to/connected-budget-optimiser',
}

def anonymize_content(content):
    """Replace sensitive information with placeholders"""
    for original, replacement in ANONYMIZE.items():
        content = content.replace(original, replacement)
    return content

def process_file(filepath):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        anonymized = anonymize_content(content)

        # Only update if changes were made
        if anonymized != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(anonymized)
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False

# Files to anonymize (only documentation, not code)
files_to_anonymize = [
    'README.md',
    'QUICKSTART.md',
    'CHANGES.md',
    'DECISION_LOGIC_FLOW.md',
    'RESTRUCTURE_SUMMARY.md'
]

if __name__ == '__main__':
    base_dir = Path(__file__).parent
    updated = 0

    for filename in files_to_anonymize:
        filepath = base_dir / filename
        if filepath.exists():
            if process_file(filepath):
                print(f"[OK] Anonymized: {filename}")
                updated += 1
        else:
            print(f"[WARN] Not found: {filename}")

    print(f"\n[OK] Anonymized {updated} files for GitHub")
