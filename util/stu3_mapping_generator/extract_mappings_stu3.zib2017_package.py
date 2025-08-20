#!/usr/bin/env python3
"""
Standalone script to extract all mapping entries from STU3 StructureDefinition JSON files.
"""
import os
import json
from pathlib import Path

def extract_mappings_from_file(file_path):
    """
    Extract id, path, and mapping array from a StructureDefinition JSON file.
    Returns a list of mapping entries.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Ensure it's a StructureDefinition
    if data.get('resourceType') != 'StructureDefinition':
        return []
    entries = []
    for element in data.get('differential', {}).get('element', []):
        maps = element.get('mapping')
        if maps:
            entries.append({
                'id': element.get('id'),
                'path': element.get('path'),
                'mapping': maps
            })
    return entries


def main():
    # Directory containing the profile JSON files
    base_dir = Path(__file__).parent / 'nictiz.fhir.nl.stu3.zib2017#2.2.20' / 'package'
    output_file = Path(__file__).parent / 'all_nictiz_zib20217_profile_mappings.json'

    all_mappings = []
    if not base_dir.exists():
        print(f"Profiles directory not found: {base_dir}")
        return

    for fname in sorted(os.listdir(base_dir)):
        if fname.endswith('.json'):
            file_path = base_dir / fname
            try:
                mappings = extract_mappings_from_file(file_path)
                all_mappings.extend(mappings)
            except Exception as e:
                print(f"Failed to parse {fname}: {e}")

    # Write combined JSON
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(all_mappings, out, indent=2, ensure_ascii=False)

    print(f"Extracted {len(all_mappings)} mapping entries to {output_file}")

if __name__ == '__main__':
    main()
