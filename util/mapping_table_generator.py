import os
import re
import argparse
import json

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
    that match the specific OID prefix and structure.
    Returns a dictionary: {id: {'name': str, 'depth': int}}
    """
    all_json_concepts = {}
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

    # Start depth at -1 to effectively remove one level of indentation.
    for concept, depth in find_concepts_with_depth(data, depth=-1):
        concept_id = concept.get('id')
        if concept_id and concept_id.startswith(oid_prefix):
            remaining_part = concept_id[len(oid_prefix):]
            if '.' not in remaining_part:
                name = next((n.get('#text', '') for n in concept.get('name', []) if n.get('language') == 'nl-NL'), '')
                if name:
                    all_json_concepts[remaining_part] = {'name': name, 'depth': depth}

    return all_json_concepts

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
    Parses all .fsh files in a directory, extracts mapping information,
    and generates Markdown tables with indentation and hyperlinks.
    """
    mapping_rule_pattern = re.compile(r'^\*\s*(.*?)\s*->\s*"([^"]+)"(?:\s*"([^"]+)")?')
    top_level_keyword_pattern = re.compile(r"^(Alias|Profile|Extension|Logical|Resource|Mapping|ValueSet|CodeSystem|Instance|RuleSet):")

    profile_ids = extract_profile_ids(fsh_directory)
    json_concepts = extract_all_json_ids(json_file_path)
    if json_concepts is None:
        return

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
                            
                            concept_data = json_concepts.get(functional_id)
                            if concept_data:
                                depth = concept_data['depth']
                                # Only add indentation if depth is positive
                                indentation = "&emsp;" * depth if depth > 0 else ""
                                dataset_name = indentation + concept_data['name']
                            else:
                                dataset_name = "Name not found in JSON"
                            
                            all_mappings.append((resource_type_from_file, current_source_profile, fhir_element, functional_id, dataset_name))
                            mapped_ids.add(functional_id)

    print(f"\nFound a total of {len(all_mappings)} mapping entries.")
    
    output_dir = os.path.dirname(output_markdown_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        if all_mappings:
            f.write("##### Mappings by dataset ID\n\n")
            f.write("| Dataset ID | Dataset name | Resource | FHIR element |\n")
            f.write("|---|---|---|---|\n")

            def sort_key(item):
                try:
                    return int(item[3])
                except (ValueError, TypeError):
                    return (float('inf'), item[3])

            for mapping in sorted(all_mappings, key=sort_key):
                resource_type, profile_name, fhir_element, functional_id, dataset_name = mapping
                profile_id = profile_ids.get(profile_name, profile_name)
                resource_display = f'{resource_type} (<a href="StructureDefinition-{profile_id}.html">{profile_name}</a>)'
                f.write(f"| {functional_id} | {dataset_name} | {resource_display} | `{fhir_element}`  |\n")
        else:
            f.write("No mappings were found.\n")

        print(f"\nChecking for unmapped concepts in {json_file_path}...")
        unmapped_ids = {k: v['name'] for k, v in json_concepts.items() if k not in mapped_ids}

        f.write("\n\n##### Overview of Unmapped Elements\n\n")
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
        default='input/includes/mappings.md',
        help="The path for the output Markdown file.\n(default: 'input/pagecontent/mappings.md')"
    )
    parser.add_argument(
        '--json-file',
        default='util/DS_pzp_dataset_vastleggen_(download_2025-07-17T15_40_47)-zib2020.json',
        help="Path to the JSON dataset file to check for unmapped concepts."
    )
    args = parser.parse_args()
    extract_mappings_from_fsh(args.fsh_dir, args.output_file, args.json_file)

if __name__ == "__main__":
    main()