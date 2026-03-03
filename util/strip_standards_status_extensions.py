"""
strip_standards_status_extensions.py

Removes unwanted ``structuredefinition-standards-status`` and
``structuredefinition-normative-version`` extensions from compiled FHIR
resources, and their corresponding normative badges from generated HTML.

These extensions are automatically injected by SUSHI but can cause issues
with validation or publication workflows.  They will be removed in a future
SUSHI / .NET SDK version.  See the related Zulip thread:
https://chat.fhir.org/#narrow/channel/215610-shorthand/topic/.E2.9C.94.20Issue.20adding.20extension.20when.20base.20has.20extensions.20in.20snap.2E.2E.2E/with/561905267

Workflow:
  1. Scans ``fsh-generated/resources/`` for JSON files and recursively
     strips the target extension objects.
  2. Scans ``output/`` for StructureDefinition HTML files and removes
     normative status ``<a>`` badges.

Usage:
  python util/strip_standards_status_extensions.py [--dry-run]

Examples:
  # Preview changes
  python util/strip_standards_status_extensions.py --dry-run

  # Apply changes
  python util/strip_standards_status_extensions.py
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# =============================================================================
# Configuration — edit these values to match your project
# =============================================================================

# Directory containing compiled FHIR JSON resources (output of SUSHI).
FSH_GENERATED_DIR = "fsh-generated/resources"

# IG Publisher output directory containing HTML files.
OUTPUT_DIR = "output"

# Extension URLs to remove from JSON resources.
EXTENSIONS_TO_REMOVE = {
    "http://hl7.org/fhir/StructureDefinition/structuredefinition-standards-status",
    "http://hl7.org/fhir/StructureDefinition/structuredefinition-normative-version"
}


def strip_extensions_from_list(extensions: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """
    Remove unwanted extensions from an extension list.
    
    Args:
        extensions: List of extension objects
        
    Returns:
        Tuple of (filtered extensions list, count of removed extensions)
    """
    if not extensions:
        return extensions, 0
    
    original_count = len(extensions)
    filtered = [ext for ext in extensions if ext.get("url") not in EXTENSIONS_TO_REMOVE]
    removed_count = original_count - len(filtered)
    
    return filtered, removed_count


def strip_extensions_recursive(obj: Any) -> int:
    """
    Recursively search for and remove unwanted extensions from a FHIR resource.
    
    Args:
        obj: FHIR resource or any nested object
        
    Returns:
        Total count of removed extensions
    """
    total_removed = 0
    
    if isinstance(obj, dict):
        # Check if this dict has an 'extension' key
        if "extension" in obj and isinstance(obj["extension"], list):
            filtered, removed = strip_extensions_from_list(obj["extension"])
            total_removed += removed
            
            # Update or remove the extension key
            if filtered:
                obj["extension"] = filtered
            else:
                del obj["extension"]
        
        # Recurse into all values
        for value in obj.values():
            total_removed += strip_extensions_recursive(value)
    
    elif isinstance(obj, list):
        # Recurse into all list items
        for item in obj:
            total_removed += strip_extensions_recursive(item)
    
    return total_removed


def process_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Process a single JSON file to remove unwanted extensions.
    
    Args:
        file_path: Path to the JSON file
        dry_run: If True, don't write changes to disk
        
    Returns:
        Tuple of (whether changes were made, count of removed extensions)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Strip extensions
        removed_count = strip_extensions_recursive(data)
        
        if removed_count > 0 and not dry_run:
            # Write back with consistent formatting
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
        
        return removed_count > 0, removed_count
    
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Warning: Could not parse JSON in {file_path.name}: {e}")
        return False, 0
    except Exception as e:
        print(f"  ⚠️  Error processing {file_path.name}: {e}")
        return False, 0


def process_html_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, int]:
    """
    Process a single HTML file to remove normative status badges.
    
    The badges look like:
    <a style="..." href="http://hl7.org/fhir/R4/versions.html#std-process" title="Standards Status =Normative">N</a>
    
    Args:
        file_path: Path to the HTML file
        dry_run: If True, don't write changes to disk
        
    Returns:
        Tuple of (whether changes were made, count of removed badges)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match normative status badges
        # Matches <a> tags with href to versions.html#std-process and title containing "Standards Status"
        pattern = r'<a\s+style="[^"]*"\s+href="http://hl7\.org/fhir/R4/versions\.html#std-process"\s+title="Standards Status\s*=\s*Normative">N</a>'
        
        # Count matches
        matches = re.findall(pattern, content)
        removed_count = len(matches)
        
        if removed_count > 0:
            # Remove all matches
            new_content = re.sub(pattern, '', content)
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            return True, removed_count
        
        return False, 0
    
    except Exception as e:
        print(f"  ⚠️  Error processing {file_path.name}: {e}")
        return False, 0


def process_directory(directory: Path, file_pattern: str, processor_func, dry_run: bool = False, label: str = "files") -> Tuple[int, int]:
    """
    Process all files matching a pattern in a directory.
    
    Args:
        directory: Directory to process
        file_pattern: Glob pattern for files to process
        processor_func: Function to process each file
        dry_run: If True, don't write changes to disk
        label: Label for the file type being processed
        
    Returns:
        Tuple of (modified count, total items removed)
    """
    if not directory.exists():
        print(f"  ⚠️  Directory not found: {directory}")
        return 0, 0
    
    files = list(directory.glob(file_pattern))
    
    if not files:
        print(f"  ℹ️  No {label} found in {directory}")
        return 0, 0
    
    print(f"  Found {len(files)} {label}")
    
    modified_count = 0
    total_removed = 0
    
    for file in sorted(files):
        was_modified, removed_count = processor_func(file, dry_run)
        
        if was_modified:
            modified_count += 1
            total_removed += removed_count
            status = "Would modify" if dry_run else "Modified"
            item_label = "extension(s)" if file_pattern.endswith('.json') else "badge(s)"
            print(f"    ✓ {status}: {file.name} ({removed_count} {item_label} removed)")
    
    return modified_count, total_removed


def main():
    """Main execution function."""
    # Parse command line arguments
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("🔍 Running in DRY-RUN mode - no files will be modified\n")
    
    # Find the script's directory and construct paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    fsh_generated_dir = project_root / FSH_GENERATED_DIR
    output_dir = project_root / OUTPUT_DIR
    
    # Track totals
    total_json_modified = 0
    total_json_extensions = 0
    total_html_modified = 0
    total_html_badges = 0
    
    # Process fsh-generated JSON files
    print("=" * 70)
    print("📂 Processing fsh-generated/resources/")
    print("=" * 70)
    
    if fsh_generated_dir.exists():
        modified, removed = process_directory(
            fsh_generated_dir, 
            "*.json", 
            process_file, 
            dry_run, 
            "JSON files"
        )
        total_json_modified += modified
        total_json_extensions += removed
    else:
        print(f"  ⚠️  Directory not found: {fsh_generated_dir}")
    
    print()
    
    # Process output HTML files
    print("=" * 70)
    print("📂 Processing output/ HTML files")
    print("=" * 70)
    
    if output_dir.exists():
        # Only process StructureDefinition HTML files
        html_files = [f for f in output_dir.glob("StructureDefinition-*.html")]
        
        if html_files:
            print(f"  Found {len(html_files)} StructureDefinition HTML files")
            
            for html_file in sorted(html_files):
                was_modified, removed_count = process_html_file(html_file, dry_run)
                
                if was_modified:
                    total_html_modified += 1
                    total_html_badges += removed_count
                    status = "Would modify" if dry_run else "Modified"
                    print(f"    ✓ {status}: {html_file.name} ({removed_count} badge(s) removed)")
        else:
            print("  ℹ️  No StructureDefinition HTML files found")
    else:
        print(f"  ⚠️  Directory not found: {output_dir}")
    
    # Final summary
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    if dry_run:
        print(f"JSON files that would be modified: {total_json_modified}")
        print(f"HTML files that would be modified: {total_html_modified}")
    else:
        print(f"✅ JSON files modified: {total_json_modified}")
        print(f"✅ HTML files modified: {total_html_modified}")
    
    print(f"🗑️  Total extensions removed: {total_json_extensions}")
    print(f"🗑️  Total normative badges removed: {total_html_badges}")
    
    if dry_run and (total_json_modified > 0 or total_html_modified > 0):
        print("\n💡 Run without --dry-run to apply changes")


if __name__ == "__main__":
    main()
