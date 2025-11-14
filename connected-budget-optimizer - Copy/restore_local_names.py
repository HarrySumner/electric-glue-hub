"""
Restore local CEEK references after GitHub push
Run this to restore your local version with client names
"""
import os
from pathlib import Path

# Restore mappings (reverse of anonymize)
RESTORE = {
    '[Company Name]': 'Front Left Consulting',
    '[Client]': 'CEEK',
    '[user]': 'harry',
    '/path/to/connected-budget-optimiser': r'c:\Users\harry\OneDrive\Desktop\CEEK\connected-budget-optimiser',
}

def restore_content(content):
    """Replace placeholders with original names"""
    for placeholder, original in RESTORE.items():
        content = content.replace(placeholder, original)
    return content

def process_file(filepath):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        restored = restore_content(content)

        # Only update if changes were made
        if restored != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(restored)
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False

# Files to restore (same as anonymized)
files_to_restore = [
    'README.md',
    'QUICKSTART.md',
    'CHANGES.md',
    'DECISION_LOGIC_FLOW.md',
    'RESTRUCTURE_SUMMARY.md'
]

if __name__ == '__main__':
    base_dir = Path(__file__).parent
    updated = 0

    for filename in files_to_restore:
        filepath = base_dir / filename
        if filepath.exists():
            if process_file(filepath):
                print(f"[OK] Restored: {filename}")
                updated += 1
        else:
            print(f"[WARN] Not found: {filename}")

    print(f"\n[OK] Restored {updated} files to local version")
    print("\nYour local files now have CEEK references back!")
    print("GitHub has the anonymized version.")
