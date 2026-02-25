"""
Remove all 'code' elements from Questionnaire items at every nesting level.

Usage:
    python util/remove_item_codes.py [--dry-run]

This script processes Questionnaire-ACP-zib2020.json and removes
the 'code' property from every item (recursively through all nested items).
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
QUESTIONNAIRE_PATH = SCRIPT_DIR.parent / "input" / "resources" / "Questionnaire-ACP-zib2020.json"


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
