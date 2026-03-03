"""
questionnaire_item_code_remover.py

Removes all ``code`` elements from Questionnaire items at every nesting
level.  This is a one-off cleanup utility for cases where item codes were
added during authoring but are not desired in the published Questionnaire.

Workflow:
  1. Loads the target Questionnaire JSON resource.
  2. Recursively walks every ``item`` and deletes the ``code`` property
     when present.
  3. Writes the modified resource back (unless ``--dry-run`` is given).

Usage:
  python util/questionnaire_item_code_remover.py [--dry-run]

Examples:
  # Preview changes
  python util/questionnaire_item_code_remover.py --dry-run

  # Apply changes
  python util/questionnaire_item_code_remover.py
"""

import json
import sys
from pathlib import Path

# =============================================================================
# Configuration — edit these values to match your project
# =============================================================================

# Path to the Questionnaire resource to process (relative to project root).
QUESTIONNAIRE_RELATIVE_PATH = "input/resources/Questionnaire-ACP-zib2020.json"

# Resolved absolute path (derived from the script location).
SCRIPT_DIR = Path(__file__).resolve().parent
QUESTIONNAIRE_PATH = SCRIPT_DIR.parent / QUESTIONNAIRE_RELATIVE_PATH


def remove_codes_from_items(items: list, path: str = "item") -> int:
    """Recursively remove 'code' from all items. Returns count of removed elements."""
    count = 0
    for i, item in enumerate(items):
        item_path = f"{path}[{i}] (linkId={item.get('linkId', '?')})"
        if "code" in item:
            print(f"  Removing 'code' from {item_path}")
            del item["code"]
            count += 1
        if "item" in item:
            count += remove_codes_from_items(item["item"], path=f"{item_path}.item")
    return count


def main():
    dry_run = "--dry-run" in sys.argv

    if not QUESTIONNAIRE_PATH.exists():
        print(f"ERROR: File not found: {QUESTIONNAIRE_PATH}")
        sys.exit(1)

    print(f"Processing: {QUESTIONNAIRE_PATH}")
    if dry_run:
        print("(dry-run mode — no changes will be written)\n")

    with open(QUESTIONNAIRE_PATH, "r", encoding="utf-8") as f:
        questionnaire = json.load(f)

    items = questionnaire.get("item", [])
    removed = remove_codes_from_items(items)

    print(f"\nTotal 'code' elements removed: {removed}")

    if not dry_run and removed > 0:
        with open(QUESTIONNAIRE_PATH, "w", encoding="utf-8") as f:
            json.dump(questionnaire, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("File saved.")
    elif dry_run:
        print("No changes written (dry-run).")
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
