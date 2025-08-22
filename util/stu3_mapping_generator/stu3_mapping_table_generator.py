#!/usr/bin/env python3
"""
STU3 StructureDefinition Mapping Table Generator

This script:
1. Reads StructureDefinition JSON files from STU3/input/resources/
2. Extracts ZIB concept mappings from the JSON structure
3. Generates a markdown table similar to the R4 mapping table generator
4. Creates the final markdown table in STU3/input/includes/

Author: AI Assistant
Date: August 22, 2025
"""

import os
import json
import argparse
from pathlib import Path

# --- Configuration ---
# Add any concept IDs here that you want to exclude from the "Unmapped Elements" table.
UNMAPPED_IGNORE_LIST = [
    '357', '360', '447', '450', '484', '487',
    '520', '523', '560', '563', '816'
]

def find_concepts_with_depth(data, depth=0):
    """
    Recursively finds all 'concept' objects and their nesting depth.
    Depth increases for each nested 'concept' array.
    """
    if isinstance(data, dict):
        if 'concept' in data and isinstance(data['concept'], list):
            for concept in data['concept']:
                yield concept, depth
                yield from find_concepts_with_depth(concept, depth + 1)

def extract_all_json_ids(json_file_path):
    """
    Extracts all concept IDs, names, and depths from the JSON dataset
    that match the specific OID prefix and structure, starting from the
    'informatiestandaard_obv_zibs2017' root concept (for STU3).
    Returns an ordered list of concept dictionaries.
    """
    ordered_concepts = []
    oid_prefix = "2.16.840.1.113883.2.4.3.11.60.117.2."
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'. Make sure it is a valid JSON file.")
        return None

    # Find the zib2017 root concept (for STU3 we use zib2017 instead of zib2020)
    root_concept_node = None
    for concept, depth in find_concepts_with_depth(data):
        # Look for the zib2017 group 
        if concept.get('shortName') == 'informatiestandaard_obv_zibs2017':
            root_concept_node = concept
            break
            
    if not root_concept_node:
        print(f"Error: Root concept 'informatiestandaard_obv_zibs2017' not found in the JSON file.")
        return []

    for concept, depth in find_concepts_with_depth(root_concept_node, depth=0):
        concept_id = concept.get('id')
        if concept_id and concept_id.startswith(oid_prefix):
            remaining_part = concept_id[len(oid_prefix):]
            if '.' not in remaining_part:
                name = next((n.get('#text', '') for n in concept.get('name', []) if n.get('language') == 'nl-NL'), '')
                if name:
                    ordered_concepts.append({'id': remaining_part, 'name': name, 'depth': depth})

    return ordered_concepts

def extract_mappings_from_stu3_json(stu3_resources_dir, output_markdown_file, json_file_path):
    """
    Parses all StructureDefinition JSON files in STU3/input/resources/,
    extracts mappings, and generates Markdown tables for mapped, unmapped, 
    and orphan mappings, handling multiple mappings per ID.
    """
    if not os.path.isdir(stu3_resources_dir):
        print(f"Error: STU3 resources directory '{stu3_resources_dir}' not found.")
        return

    json_concepts = extract_all_json_ids(json_file_path)
    if json_concepts is None:
        return

    json_concept_ids = {concept['id'] for concept in json_concepts}
    # Map functional_id -> list of mappings
    mappings_map = {}

    print("Scanning STU3 StructureDefinition files for mappings...")
    
    total_mappings_count = 0
    processed_files = 0
    
    # Process all JSON files in the resources directory
    for filename in sorted(os.listdir(stu3_resources_dir)):
        if not filename.endswith('.json'):
            continue
            
        # Only process StructureDefinition files
        if not filename.startswith('StructureDefinition-'):
            continue
            
        filepath = os.path.join(stu3_resources_dir, filename)
        print(f"Processing file: {filename}...")
        processed_files += 1
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                structure_def = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"  Warning: Could not parse {filename}: {e}")
            continue
        
        # Verify it's a StructureDefinition
        if structure_def.get('resourceType') != 'StructureDefinition':
            print(f"  Skipping {filename} - not a StructureDefinition")
            continue
            
        # Extract profile information
        profile_name = structure_def.get('name', filename.replace('.json', ''))
        profile_id = structure_def.get('id', profile_name)
        resource_type = structure_def.get('type', 'Unknown')
        
        # Extract mappings from differential elements
        if 'differential' not in structure_def or 'element' not in structure_def['differential']:
            print(f"  No differential elements found in {filename}")
            continue
            
        for element in structure_def['differential']['element']:
            element_path = element.get('path', '')
            element_id = element.get('id', '')
            
            # Look for mappings in this element
            if 'mapping' not in element:
                continue
                
            for mapping in element['mapping']:
                # Look for ZIB mappings (typically have identity starting with specific patterns)
                identity = mapping.get('identity', '')
                map_value = mapping.get('map', '')
                
                # Skip if no map value
                if not map_value:
                    continue
                
                # Extract functional ID from map value (assuming it's a numeric ID)
                # This may need adjustment based on your actual mapping format
                functional_id = None
                
                # Try to extract numeric ID from various formats
                if map_value.isdigit():
                    functional_id = map_value
                elif ' ' in map_value and map_value.split()[0].isdigit():
                    functional_id = map_value.split()[0]
                elif map_value.startswith('"') and '"' in map_value[1:]:
                    # Handle quoted format like "123 Description"
                    quoted_content = map_value[1:map_value.index('"', 1)]
                    if quoted_content.split()[0].isdigit():
                        functional_id = quoted_content.split()[0]
                
                if functional_id:
                    mapping_details = (resource_type, profile_name, profile_id, element_path)
                    
                    # If the ID is new, create a list. Otherwise, append to the existing list.
                    if functional_id not in mappings_map:
                        mappings_map[functional_id] = []
                    mappings_map[functional_id].append(mapping_details)
                    total_mappings_count += 1

    print(f"\nProcessed {processed_files} StructureDefinition files.")
    print(f"Found a total of {total_mappings_count} mapping entries.")
    
    # Generate markdown output
    output_dir = os.path.dirname(output_markdown_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        f.write("#### Mappings by dataset ID\n\n")
        f.write("This table provides an overview of all zib2017 dataset elements that are mapped to STU3 FHIR profiles in this implementation guide.\n\n")
        f.write("| ID | Dataset name | Resource | FHIR element |\n")
        f.write("|---|---|---|---|\n")

        mapped_ids = set()
        unmapped_concepts = []
        rows_written = 0

        for concept in json_concepts:
            functional_id = concept['id']
            if functional_id in mappings_map:
                # Iterate over all mappings for this ID
                for mapping in mappings_map[functional_id]:
                    resource_type, profile_name, profile_id, fhir_element = mapping
                    
                    depth = concept['depth']
                    indentation = "&emsp;" * depth if depth > 0 else ""
                    dataset_name = indentation + concept['name']
                    
                    resource_display = f'{resource_type} (<a href="StructureDefinition-{profile_id}.html">{profile_name}</a>)'
                    f.write(f"| {functional_id} | {dataset_name} | {resource_display} | `{fhir_element}`  |\n")
                    rows_written += 1
                mapped_ids.add(functional_id)
            elif functional_id not in UNMAPPED_IGNORE_LIST:
                unmapped_concepts.append(concept)
                
        if rows_written == 0:
            f.write("| | No mappings were found matching the JSON dataset. | | |\n")

        f.write("\n\n##### Overview of Unmapped Elements\n\n")
        if unmapped_concepts:
            f.write("| ID | Name |\n")
            f.write("|---|---|\n")
            for concept in unmapped_concepts:
                f.write(f"| {concept['id']} | {concept['name']} |\n")
        else:
            f.write("All relevant elements from the JSON dataset are mapped or ignored.\n")

        f.write("\n\n##### Overview of Orphan Mappings\n\n")
        orphan_mappings = {fid: data for fid, data in mappings_map.items() if fid not in json_concept_ids}
        
        if orphan_mappings:
            f.write("| ID | Resource | FHIR element |\n")
            f.write("|---|---|---|\n")
            for functional_id, mappings in sorted(orphan_mappings.items()):
                for mapping in mappings:
                    resource_type, profile_name, profile_id, fhir_element = mapping
                    resource_display = f'{resource_type} (<a href="StructureDefinition-{profile_id}.html">{profile_name}</a>)'
                    f.write(f"| {functional_id} | {resource_display} | `{fhir_element}` |\n")
        else:
            f.write("No orphan mappings found (all mappings in StructureDefinition files correspond to an ID in the JSON dataset).\n")

        # Add summary statistics
        f.write("\n\n##### Summary\n\n")
        total_concepts = len(json_concepts)
        mapped_concepts = len(mapped_ids)
        coverage_percent = (mapped_concepts / total_concepts * 100) if total_concepts > 0 else 0
        
        f.write(f"- **Total zib2017 concepts**: {total_concepts}\n")
        f.write(f"- **Mapped to STU3**: {mapped_concepts}\n")
        f.write(f"- **Coverage**: {coverage_percent:.1f}%\n")
        f.write(f"- **Unmapped**: {len(unmapped_concepts)}\n")
        f.write(f"- **Orphan mappings**: {len(orphan_mappings)}\n")

    print(f"Successfully generated STU3 mapping table at: {output_markdown_file}")

def main():
    """
    Main function to generate STU3 mapping table.
    """
    parser = argparse.ArgumentParser(
        description="Extracts STU3 StructureDefinition mappings to a Markdown file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--stu3-dir', default='../../STU3/input/resources', 
                       help="Directory containing STU3 StructureDefinition JSON files.\n(default: '../../STU3/input/resources')")
    parser.add_argument('--output-file', default='../../STU3/input/includes/zib2017_stu3_mappings.md', 
                       help="Path for the output Markdown file.\n(default: '../../STU3/input/includes/zib2017_stu3_mappings.md')")
    parser.add_argument('--json-file', default='../DS_pzp_dataset_raadplegen_(download_2025-07-29T11_58_18).json', 
                       help="Path to the JSON dataset file.")
    
    args = parser.parse_args()
    
    print("=== STU3 StructureDefinition Mapping Table Generator ===")
    print(f"STU3 Resources Directory: {args.stu3_dir}")
    print(f"Dataset File: {args.json_file}")
    print(f"Output File: {args.output_file}")
    print()
    
    extract_mappings_from_stu3_json(args.stu3_dir, args.output_file, args.json_file)

if __name__ == "__main__":
    main()
