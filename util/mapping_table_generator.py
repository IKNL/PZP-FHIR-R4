import os
import re
import argparse
import json

def find_concepts(data):
    """
    Recursively finds all 'concept' objects in the given data.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'concept':
                if isinstance(value, list):
                    for item in value:
                        yield item
                        yield from find_concepts(item)
            elif isinstance(value, (dict, list)):
                yield from find_concepts(value)
    elif isinstance(data, list):
        for item in data:
            yield from find_concepts(item)

def extract_all_json_ids(json_file_path):
    """
    Extracts all concept IDs from the JSON dataset that match the specific OID prefix
    and structure.
    """
    all_json_ids = {}
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

    for concept in find_concepts(data):
        concept_id = concept.get('id')
        if concept_id and concept_id.startswith(oid_prefix):
            remaining_part = concept_id[len(oid_prefix):]
            if '.' not in remaining_part:
                name = next((n.get('#text', '') for n in concept.get('name', []) if n.get('language') == 'nl-NL'), '')
                if name:
                    all_json_ids[remaining_part] = name

    return all_json_ids

def extract_mappings_from_fsh(fsh_directory, output_markdown_file, json_file_path):
    """
    Parses all .fsh files in a directory, extracts mapping information,
    and generates Markdown tables, including a table of unmapped concepts.
    """
    mapping_rule_pattern = re.compile(r'^\*\s*(.*?)\s*->\s*"([^"]+)"(?:\s*"([^"]+)")?')
    top_level_keyword_pattern = re.compile(r"^(Alias|Profile|Extension|Logical|Resource|Mapping|ValueSet|CodeSystem|Instance|RuleSet):")

    all_mappings = []
    mapped_ids = set()

    print("Scanning for Mappings...")

    if not os.path.isdir(fsh_directory):
        print(f"Error: Input directory '{fsh_directory}' not found.")
        return

    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            resource_type_from_file = os.path.splitext(filename)[0]
            filepath = os.path.join(fsh_directory, filename)
            print(f"Processing file: {filename} (ResourceType: {resource_type_from_file})...")
            
            in_mapping_block = False
            current_source_profile = None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()

                    if (top_level_keyword_pattern.match(stripped_line) and not stripped_line.startswith("Mapping:")) or not stripped_line:
                        in_mapping_block = False
                        current_source_profile = None
                    
                    if stripped_line.startswith("Mapping:"):
                        in_mapping_block = True
                        current_source_profile = None
                        continue

                    if not in_mapping_block:
                        continue

                    if stripped_line.startswith("Source:"):
                        parts = stripped_line.split(':', 1)
                        if len(parts) > 1:
                            current_source_profile = parts[1].strip()
                        continue

                    if current_source_profile:
                        rule_match = mapping_rule_pattern.match(line)
                        if rule_match:
                            fhir_element = rule_match.group(1).strip()
                            functional_id = rule_match.group(2).strip()
                            functional_name = rule_match.group(3).strip() if rule_match.group(3) else ""
                            
                            all_mappings.append((resource_type_from_file, current_source_profile, fhir_element, functional_id, functional_name))
                            mapped_ids.add(functional_id)

    print(f"\nFound a total of {len(all_mappings)} mapping entries.")
    
    output_dir = os.path.dirname(output_markdown_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        if all_mappings:
            f.write("## Mappings by Resource\n\n")
            f.write("| Resource | FHIR element | Functional ID | Functional name |\n")
            f.write("|---|---|---|---|\n")
            
            for mapping in sorted(all_mappings, key=lambda x: (x[1], x[2])): 
                resource_display = f"{mapping[0]} ({mapping[1]})"
                f.write(f"| {resource_display} | `{mapping[2]}` | {mapping[3]} | {mapping[4]} |\n")
            
            f.write("\n\n")

            f.write("## Mappings by Functional ID\n\n")
            f.write("| Functional ID | Resource | FHIR element | Functional name |\n")
            f.write("|---|---|---|---|\n")

            def sort_key(item):
                try:
                    return int(item[3])
                except (ValueError, TypeError):
                    return (float('inf'), item[3])

            for mapping in sorted(all_mappings, key=sort_key):
                resource_display = f"{mapping[0]} ({mapping[1]})"
                f.write(f"| {mapping[3]} | {resource_display} | `{mapping[2]}` | {mapping[4]} |\n")
        else:
            f.write("No mappings were found.\n")

        print(f"\nChecking for unmapped concepts in {json_file_path}...")
        all_json_ids = extract_all_json_ids(json_file_path)
        
        if all_json_ids is not None:
            unmapped_ids = {k: v for k, v in all_json_ids.items() if k not in mapped_ids}

            f.write("\n\n## Overview of Unmapped Elements\n\n")
            if unmapped_ids:
                f.write("| ID | Name |\n")
                f.write("|---|---|\n")
                for oid_suffix, name in sorted(unmapped_ids.items()):
                    f.write(f"| {oid_suffix} | {name} |\n")
            else:
                f.write("All relevant elements from the JSON dataset are mapped.\n")
    
    print(f"Successfully generated Markdown file at: {output_markdown_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Extracts FHIR Shorthand (FSH) mappings to a Markdown file and checks for unmapped concepts.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--fsh-dir',
        default='input/fsh',
        help="The directory containing the .fsh source files.\n(default: 'input/fsh')"
    )
    parser.add_argument(
        '--output-file',
        default='input/pagecontent/mappings.md',
        help="The path for the output Markdown file.\n(default: 'input/pagecontent/mappings.md')"
    )
    parser.add_argument(
        '--json-file',
        default='util/DS_pzp_dataset_vastleggen_(download_2025-07-07T05_47_26)-zib2020.json',
        help="Path to the JSON dataset file to check for unmapped concepts."
    )
    args = parser.parse_args()
    extract_mappings_from_fsh(args.fsh_dir, args.output_file, args.json_file)

if __name__ == "__main__":
    main()