"""
Questionnaire Item Prefix Populator

This script is used to populate the prefix of questionnaire items based on the prefix in item.text examples. 
It is intended to be run as a post-processing step after generating the FHIR Questionnaire.

The script will:
1. Loop through the input/resources files and find the questionnaire resources
2. Transform/move the item.text values that start with a prefix like "a)", "b)", "1.", "2." etc 
3. Populate the item.prefix field with that value and remove it from the item.text field

Examples of text that will be processed:
- "text": "c) Relatie tot patiënt (2)" -> prefix: "c)", text: "Relatie tot patiënt (2)"
- "text": "d) Is de wettelijk vertegenwoordiger ook de eerste contactpersoon?" -> prefix: "d)", text: "Is de wettelijk vertegenwoordiger ook de eerste contactpersoon?"
- "text": "1. Wilsbekwaamheid & Wettelijke vertegenwoordiging" -> prefix: "1.", text: "Wilsbekwaamheid & Wettelijke vertegenwoordiging"
- "text": "2 Gesprek gevoerd in bijzijn van" -> prefix: "2", text: "Gesprek gevoerd in bijzijn van"
- "text": "3. Belangrijkste overeengekomen doel van medisch beleid" -> prefix: "3.", text: "Belangrijkste overeengekomen doel van medisch beleid"

Usage:
    python questionnaire_item_prefix_populator.py [--dry-run] [--input-dir INPUT_DIR]
"""

import json
import re
import argparse
from pathlib import Path
import shutil
from typing import Dict, Any, Tuple, Optional


def extract_prefix_from_text(text: str) -> Tuple[Optional[str], str]:
    """
    Extract prefix from text if it starts with a recognized pattern.
    
    Args:
        text: The original text string
        
    Returns:
        Tuple of (prefix, remaining_text) or (None, original_text) if no prefix found
    """
    if not isinstance(text, str) or not text.strip():
        return None, text
    
    # Pattern for letter followed by ) - e.g., "a)", "b)", "c)"
    letter_pattern = re.compile(r'^([a-zA-Z]\))\s*(.*)$')
    match = letter_pattern.match(text)
    if match:
        return match.group(1), match.group(2)
    
    # Pattern for number followed by . - e.g., "1.", "2.", "3."
    number_dot_pattern = re.compile(r'^(\d+\.)\s*(.*)$')
    match = number_dot_pattern.match(text)
    if match:
        return match.group(1), match.group(2)
    
    # Pattern for number without dot - e.g., "1 ", "2 "
    number_space_pattern = re.compile(r'^(\d+)\s+(.*)$')
    match = number_space_pattern.match(text)
    if match:
        return match.group(1), match.group(2)
    
    # Pattern for number followed by ) - e.g., "1)", "2)"
    number_paren_pattern = re.compile(r'^(\d+\))\s*(.*)$')
    match = number_paren_pattern.match(text)
    if match:
        return match.group(1), match.group(2)
    
    return None, text


def process_questionnaire_item(item: Dict[str, Any]) -> int:
    """
    Process a single questionnaire item and its children recursively.
    
    Args:
        item: A questionnaire item dictionary
        
    Returns:
        Number of items modified
    """
    modifications = 0
    
    # Process current item's text
    if 'text' in item and isinstance(item['text'], str):
        prefix, remaining_text = extract_prefix_from_text(item['text'])
        if prefix:
            # Create a new ordered dictionary to ensure prefix comes before text
            new_item = {}
            
            # Copy all fields in order, inserting prefix before text
            for key, value in item.items():
                if key == 'text':
                    # Insert prefix before text
                    new_item['prefix'] = prefix
                    new_item['text'] = remaining_text
                elif key != 'prefix':  # Skip existing prefix if any
                    new_item[key] = value
            
            # Update the original item with the new ordered content
            item.clear()
            item.update(new_item)
            
            modifications += 1
            print(f"  Modified item: prefix='{prefix}', text='{remaining_text[:50]}...'")
    
    # Process child items recursively
    if 'item' in item and isinstance(item['item'], list):
        for child_item in item['item']:
            modifications += process_questionnaire_item(child_item)
    
    return modifications


def process_questionnaire_file(file_path: Path, dry_run: bool = False) -> bool:
    """
    Process a single questionnaire JSON file.
    
    Args:
        file_path: Path to the questionnaire JSON file
        dry_run: If True, don't write changes to file
        
    Returns:
        True if file was modified, False otherwise
    """
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if this is a Questionnaire resource
        if not isinstance(data, dict) or data.get('resourceType') != 'Questionnaire':
            print(f"Skipping {file_path.name}: Not a Questionnaire resource")
            return False
        
        print(f"Processing {file_path.name}...")
        
        # Process all top-level items
        total_modifications = 0
        if 'item' in data and isinstance(data['item'], list):
            for item in data['item']:
                total_modifications += process_questionnaire_item(item)
        
        if total_modifications > 0:
            print(f"  Total modifications: {total_modifications}")
            
            if not dry_run:
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                shutil.copy2(file_path, backup_path)
                print(f"  Created backup: {backup_path.name}")
                
                # Write modified data back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"  Updated {file_path.name}")
            else:
                print(f"  [DRY RUN] Would modify {file_path.name}")
            
            return True
        else:
            print(f"  No modifications needed for {file_path.name}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function to process questionnaire files."""
    parser = argparse.ArgumentParser(
        description="Populate questionnaire item prefixes from text content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--input-dir', 
        type=Path, 
        default='input/resources',
        help='Directory containing questionnaire JSON files (default: input/resources)'
    )
    
    args = parser.parse_args()
    
    # Resolve input directory path
    input_dir = args.input_dir
    if not input_dir.is_absolute():
        # Assume relative to script directory's parent (repo root)
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent
        input_dir = repo_root / input_dir
    
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        return 1
    
    print(f"Looking for questionnaire files in: {input_dir}")
    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
    print()
    
    # Find and process questionnaire JSON files
    questionnaire_files = list(input_dir.glob("Questionnaire*.json"))
    
    if not questionnaire_files:
        print("No questionnaire files found matching pattern 'Questionnaire*.json'")
        return 0
    
    modified_count = 0
    for file_path in questionnaire_files:
        if process_questionnaire_file(file_path, args.dry_run):
            modified_count += 1
        print()  # Empty line between files
    
    print(f"Summary: {modified_count}/{len(questionnaire_files)} files modified")
    
    if args.dry_run and modified_count > 0:
        print("Run without --dry-run to apply changes")
    
    return 0


if __name__ == '__main__':
    exit(main())

