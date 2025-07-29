import os
import re
import argparse
import json

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
    'informatiestandaard_obv_zibs2020' root concept.
    Returns an ordered list of concept dictionaries.
    """
    ordered_concepts = []
    root_concept_id = "2.16.840.1.113883.2.4.3.11.60.117.2.350"
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

    root_concept_node = None
    for concept, depth in find_concepts_with_depth(data):
        if concept.get('id') == root_concept_id:
            root_concept_node = concept
            break
            
    if not root_concept_node:
        print(f"Error: Root concept with ID '{root_concept_id}' not found in the JSON file.")
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

def extract_profile_ids(fsh_directory):
    """
    Scans all .fsh files to create a map of Profile names to their corresponding IDs.
    """
    profile_id_map = {}
    profile_pattern = re.compile(r"^Profile:\s*(\S+)")
    id_pattern = re.compile(r"^Id:\s*(\S+)")
    top_level_keyword_pattern = re.compile(r"^(Alias|Profile|Extension|Logical|Resource|Mapping|ValueSet|CodeSystem|Instance|RuleSet):")

    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            filepath = os.path.join(fsh_directory, filename)
            current_profile_name = None
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    
                    if top_level_keyword_pattern.match(stripped_line):
                        current_profile_name = None 

                    profile_match = profile_pattern.match(stripped_line)
                    if profile_match:
                        current_profile_name = profile_match.group(1)
                        profile_id_map[current_profile_name] = current_profile_name
                        continue 

                    if current_profile_name:
                        id_match = id_pattern.match(stripped_line)
                        if id_match:
                            profile_id = id_match.group(1)
                            profile_id_map[current_profile_name] = profile_id
                            current_profile_name = None
    return profile_id_map

def extract_mappings_from_fsh(fsh_directory, output_markdown_file, json_file_path):
    """
    Parses all .fsh files, extracts mappings, and generates Markdown tables
    for mapped, unmapped, and orphan mappings, handling multiple mappings per ID.
    """
    mapping_rule_pattern = re.compile(r'^\*\s*(.*?)\s*->\s*"([^"]+)"(?:\s*"([^"]+)")?')
    top_level_keyword_pattern = re.compile(r"^(Alias|Profile|Extension|Logical|Resource|Mapping|ValueSet|CodeSystem|Instance|RuleSet):")

    profile_ids = extract_profile_ids(fsh_directory)
    json_concepts = extract_all_json_ids(json_file_path)
    if json_concepts is None:
        return

    json_concept_ids = {concept['id'] for concept in json_concepts}
    # Change mappings_map to hold a list of mappings for each ID
    mappings_map = {}

    print("Scanning for Mappings...")
    if not os.path.isdir(fsh_directory):
        print(f"Error: Input directory '{fsh_directory}' not found.")
        return

    total_mappings_count = 0
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            resource_type_from_file = os.path.splitext(filename)[0]
            filepath = os.path.join(fsh_directory, filename)
            print(f"Processing file: {filename} (ResourceType: {resource_type_from_file})...")
            
            in_mapping_block, current_source_profile = False, None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()

                    if (top_level_keyword_pattern.match(stripped_line) and not stripped_line.startswith("Mapping:")) or not stripped_line:
                        in_mapping_block, current_source_profile = False, None
                    
                    if stripped_line.startswith("Mapping:"):
                        in_mapping_block, current_source_profile = True, None
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
                            fhir_element, functional_id, _ = rule_match.groups()
                            mapping_details = (resource_type_from_file, current_source_profile, fhir_element.strip())
                            
                            # If the ID is new, create a list. Otherwise, append to the existing list.
                            if functional_id not in mappings_map:
                                mappings_map[functional_id] = []
                            mappings_map[functional_id].append(mapping_details)
                            total_mappings_count += 1

    print(f"\nFound a total of {total_mappings_count} mapping entries.")
    
    output_dir = os.path.dirname(output_markdown_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        f.write("#### Mappings by dataset ID\n\n")
        f.write("This table provides an overview of all dataset elements that are mapped to FHIR profiles in this implementation guide.\n\n")
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
                    resource_type, profile_name, fhir_element = mapping
                    
                    depth = concept['depth']
                    indentation = "&emsp;" * depth if depth > 0 else ""
                    dataset_name = indentation + concept['name']
                    
                    profile_id = profile_ids.get(profile_name, profile_name)
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
                    resource_type, profile_name, fhir_element = mapping
                    profile_id = profile_ids.get(profile_name, profile_name)
                    resource_display = f'{resource_type} (<a href="StructureDefinition-{profile_id}.html">{profile_name}</a>)'
                    f.write(f"| {functional_id} | {resource_display} | `{fhir_element}` |\n")
        else:
            f.write("No orphan mappings found (all mappings in FSH files correspond to an ID in the JSON dataset).\n")

    print(f"Successfully generated Markdown file at: {output_markdown_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Extracts FHIR Shorthand (FSH) mappings to a Markdown file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--fsh-dir', default='input/fsh', help="Directory containing .fsh files.\n(default: 'input/fsh')")
    parser.add_argument('--output-file', default='input/includes/mappings.md', help="Path for the output Markdown file.\n(default: 'input/includes/mappings.md')")
    parser.add_argument('--json-file', default='util/DS_pzp_dataset_raadplegen_(download_2025-07-29T11_58_18).json', help="Path to the JSON dataset file.")
    args = parser.parse_args()
    extract_mappings_from_fsh(args.fsh_dir, args.output_file, args.json_file)

if __name__ == "__main__":
    main()