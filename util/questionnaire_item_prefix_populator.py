"""
Questionnaire Item Prefix Populator

This script is used to populate the prefix of questionnaire items and fix QuestionnaireResponse items 
to ensure FHIR validation compliance. It is intended to be run as a post-processing step after 
generating FHIR Questionnaire and QuestionnaireResponse resources.

The script will:
1. For Questionnaire resources:
   - Transform/move the item.text values that start with a prefix like "a)", "b)", "1.", "2." etc 
   - Populate the item.prefix field with that value and remove it from the item.text field

2. For QuestionnaireResponse resources:
   - Remove prefixes from item.text fields to match the corresponding Questionnaire definition
   - This ensures compliance with the FHIR validation rule: "If text exists, it must match the questionnaire definition for linkId"

Examples of text that will be processed:
- Questionnaire: "text": "c) Relatie tot patiënt (2)" -> prefix: "c)", text: "Relatie tot patiënt (2)"
- QuestionnaireResponse: "text": "c) Relatie tot patiënt (2)" -> text: "Relatie tot patiënt (2)"

Usage:
    python questionnaire_item_prefix_populator.py [--dry-run] [--input-dir INPUT_DIR] [--questionnaire-only] [--response-only]
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
            print(f"  Modified Questionnaire item: prefix='{prefix}', text='{remaining_text[:50]}...'")
    
    # Process child items recursively
    if 'item' in item and isinstance(item['item'], list):
        for child_item in item['item']:
            modifications += process_questionnaire_item(child_item)
    
    return modifications


def process_questionnaire_response_item(item: Dict[str, Any]) -> int:
    """
    Process a single QuestionnaireResponse item and its children recursively.
    Removes prefixes from text to match Questionnaire definition.
    
    Args:
        item: A QuestionnaireResponse item dictionary
        
    Returns:
        Number of items modified
    """
    modifications = 0
    
    # Process current item's text - remove prefix but don't add prefix field
    if 'text' in item and isinstance(item['text'], str):
        prefix, remaining_text = extract_prefix_from_text(item['text'])
        if prefix:
            item['text'] = remaining_text
            modifications += 1
            print(f"  Modified QuestionnaireResponse item: removed prefix '{prefix}', text='{remaining_text[:50]}...'")
    
    # Process child items recursively
    if 'item' in item and isinstance(item['item'], list):
        for child_item in item['item']:
            modifications += process_questionnaire_response_item(child_item)
    
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


def process_questionnaire_response_file(file_path: Path, dry_run: bool = False) -> bool:
    """
    Process a single QuestionnaireResponse JSON file.
    
    Args:
        file_path: Path to the QuestionnaireResponse JSON file
        dry_run: If True, don't write changes to file
        
    Returns:
        True if file was modified, False otherwise
    """
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if this is a QuestionnaireResponse resource
        if not isinstance(data, dict) or data.get('resourceType') != 'QuestionnaireResponse':
            print(f"Skipping {file_path.name}: Not a QuestionnaireResponse resource")
            return False
        
        print(f"Processing {file_path.name}...")
        
        # Process all top-level items
        total_modifications = 0
        if 'item' in data and isinstance(data['item'], list):
            for item in data['item']:
                total_modifications += process_questionnaire_response_item(item)
        
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
        description="Populate questionnaire item prefixes and fix QuestionnaireResponse text content",
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
    parser.add_argument(
        '--questionnaire-only',
        action='store_true',
        help='Only process Questionnaire resources'
    )
    parser.add_argument(
        '--response-only',
        action='store_true',
        help='Only process QuestionnaireResponse resources'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.questionnaire_only and args.response_only:
        print("Error: Cannot specify both --questionnaire-only and --response-only")
        return 1
    
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
    
    total_modified = 0
    total_files = 0
    
    # Process Questionnaire files
    if not args.response_only:
        questionnaire_files = list(input_dir.glob("Questionnaire*.json"))
        
        if questionnaire_files:
            print("=== Processing Questionnaire resources ===")
            modified_count = 0
            for file_path in questionnaire_files:
                if process_questionnaire_file(file_path, args.dry_run):
                    modified_count += 1
                print()  # Empty line between files
            
            print(f"Questionnaire Summary: {modified_count}/{len(questionnaire_files)} files modified")
            total_modified += modified_count
            total_files += len(questionnaire_files)
        else:
            print("No Questionnaire files found matching pattern 'Questionnaire*.json'")
        
        print()
    
    # Process QuestionnaireResponse files  
    if not args.questionnaire_only:
        response_files = list(input_dir.glob("QuestionnaireResponse*.json"))
        
        if response_files:
            print("=== Processing QuestionnaireResponse resources ===")
            modified_count = 0
            for file_path in response_files:
                if process_questionnaire_response_file(file_path, args.dry_run):
                    modified_count += 1
                print()  # Empty line between files
            
            print(f"QuestionnaireResponse Summary: {modified_count}/{len(response_files)} files modified")
            total_modified += modified_count
            total_files += len(response_files)
        else:
            print("No QuestionnaireResponse files found matching pattern 'QuestionnaireResponse*.json'")
    
    print()
    print(f"Overall Summary: {total_modified}/{total_files} files modified")
    
    if args.dry_run and total_modified > 0:
        print("Run without --dry-run to apply changes")
    
    return 0


if __name__ == '__main__':
    exit(main())

