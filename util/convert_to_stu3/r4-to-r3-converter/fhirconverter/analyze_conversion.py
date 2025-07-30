#!/usr/bin/env python3
"""
FHIR R4 to STU3 Conversion Analysis Tool
Analyzes the differences between source R4 files and converted STU3 files.
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict, Counter

def load_json_file(file_path):
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_all_keys(obj, prefix=""):
    """Recursively get all keys from a JSON object."""
    keys = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.add(full_key)
            keys.update(get_all_keys(value, full_key))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            keys.update(get_all_keys(item, prefix))
    return keys

def compare_files(source_file, output_file):
    """Compare source and output files and return differences."""
    source_data = load_json_file(source_file)
    output_data = load_json_file(output_file)
    
    if not source_data or not output_data:
        return None
    
    source_keys = get_all_keys(source_data)
    output_keys = get_all_keys(output_data)
    
    return {
        'source_file': source_file.name,
        'output_file': output_file.name,
        'resource_type': source_data.get('resourceType', 'Unknown'),
        'keys_removed': source_keys - output_keys,
        'keys_added': output_keys - source_keys,
        'keys_retained': source_keys & output_keys,
        'source_key_count': len(source_keys),
        'output_key_count': len(output_keys)
    }

def analyze_all_files():
    """Analyze all source and output files."""
    source_dir = Path("../source")
    output_dir = Path("../output-structuremap")
    
    if not source_dir.exists() or not output_dir.exists():
        print("Error: Source or output directory not found!")
        return
    
    results = []
    all_removed_keys = Counter()
    all_added_keys = Counter()
    resource_type_changes = defaultdict(lambda: {'removed': Counter(), 'added': Counter()})
    
    # Find all source JSON files
    source_files = list(source_dir.glob("*.json"))
    source_files = [f for f in source_files if not f.name.endswith("-STU3.json")]
    
    print(f"Analyzing {len(source_files)} source files...")
    print("=" * 80)
    
    for source_file in sorted(source_files):
        # Find corresponding output file
        output_filename = source_file.stem + "-StructureMap-STU3.json"
        output_file = output_dir / output_filename
        
        if not output_file.exists():
            print(f"Warning: Output file not found for {source_file.name}")
            continue
        
        result = compare_files(source_file, output_file)
        if result:
            results.append(result)
            
            # Aggregate statistics
            all_removed_keys.update(result['keys_removed'])
            all_added_keys.update(result['keys_added'])
            resource_type_changes[result['resource_type']]['removed'].update(result['keys_removed'])
            resource_type_changes[result['resource_type']]['added'].update(result['keys_added'])
    
    # Print detailed analysis
    print(f"\nSUMMARY: Analyzed {len(results)} file pairs")
    print("=" * 80)
    
    # Overall statistics
    total_keys_removed = sum(len(r['keys_removed']) for r in results)
    total_keys_added = sum(len(r['keys_added']) for r in results)
    
    print(f"Total unique keys removed across all files: {total_keys_removed}")
    print(f"Total unique keys added across all files: {total_keys_added}")
    
    # Most common changes
    print(f"\nMOST COMMONLY REMOVED KEYS (R4 -> STU3):")
    print("-" * 50)
    for key, count in all_removed_keys.most_common(10):
        print(f"  {key:<40} (removed from {count} files)")
    
    print(f"\nMOST COMMONLY ADDED KEYS (STU3 specific):")
    print("-" * 50)
    for key, count in all_added_keys.most_common(10):
        print(f"  {key:<40} (added to {count} files)")
    
    # Resource type breakdown
    print(f"\nCHANGES BY RESOURCE TYPE:")
    print("-" * 50)
    for resource_type, changes in sorted(resource_type_changes.items()):
        files_of_type = sum(1 for r in results if r['resource_type'] == resource_type)
        removed_count = sum(changes['removed'].values())
        added_count = sum(changes['added'].values())
        
        print(f"{resource_type} ({files_of_type} files):")
        print(f"  Keys removed: {removed_count}")
        print(f"  Keys added: {added_count}")
        
        if changes['removed']:
            print(f"  Most removed: {changes['removed'].most_common(3)}")
        if changes['added']:
            print(f"  Most added: {changes['added'].most_common(3)}")
        print()
    
    # Individual file details
    print(f"\nDETAILED FILE-BY-FILE ANALYSIS:")
    print("-" * 80)
    for result in results:
        print(f"\nFile: {result['source_file']}")
        print(f"Resource Type: {result['resource_type']}")
        print(f"Keys: {result['source_key_count']} -> {result['output_key_count']} ({result['output_key_count'] - result['source_key_count']:+d})")
        
        if result['keys_removed']:
            print(f"  Removed ({len(result['keys_removed'])}): {', '.join(sorted(result['keys_removed']))}")
        
        if result['keys_added']:
            print(f"  Added ({len(result['keys_added'])}): {', '.join(sorted(result['keys_added']))}")

if __name__ == "__main__":
    analyze_all_files()
