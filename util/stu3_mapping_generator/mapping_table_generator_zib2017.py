import json
import re
import os

def find_concepts_recursively(data):
    """
    Recursively finds all 'concept' objects within a given data structure by
    traversing through all lists and dictionary values, but explicitly ignoring
    the 'conceptList' key which contains value sets.

    Args:
        data (dict or list): The data structure to search within.

    Returns:
        list: A flat list of all found concept dictionaries.
    """
    concepts = []
    if isinstance(data, dict):
        for key, value in data.items():
            # Explicitly skip the conceptList which contains value sets/terminology
            if key == 'conceptList':
                continue

            # If we find a 'concept' key, process its list
            if key == 'concept' and isinstance(value, list):
                for concept in value:
                    concepts.append(concept)
                    # Also recurse inside this concept to find its children
                    concepts.extend(find_concepts_recursively(concept))
            # Otherwise, if the value is another structure, recurse into it
            elif isinstance(value, (dict, list)):
                concepts.extend(find_concepts_recursively(value))
    elif isinstance(data, list):
        # If the data is a list, iterate and recurse into each item
        for item in data:
            concepts.extend(find_concepts_recursively(item))
    return concepts

def extract_concepts_by_root_id(json_file_path, root_concept_id):
    """
    Extracts all concepts from the JSON dataset under a specific root concept ID.

    Args:
        json_file_path (str): The path to the JSON dataset file.
        root_concept_id (str): The OID of the root concept to start from.

    Returns:
        list: A list of concept dictionaries found under the root. Returns an empty list on error.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'. Make sure it is a valid JSON file.")
        return []

    # Use the robust recursive function to find ALL valid concepts in the file
    all_concepts_in_file = find_concepts_recursively(data)

    # Find the specific root concept node from the flat list
    root_concept_node = None
    for concept in all_concepts_in_file:
        if concept.get('id') == root_concept_id:
            root_concept_node = concept
            break

    if not root_concept_node:
        print(f"Error: Root concept with ID '{root_concept_id}' not found in the JSON file.")
        return []

    # Once the root is found, get all concepts that are descendants of it
    # by running the recursive search starting from the root node itself.
    return find_concepts_recursively(root_concept_node)

def get_zib2020_mappings(mappings_file):
    """
    Parses the mappings.md file to get the zib2020 mappings.

    Args:
        mappings_file (str): The path to the mappings.md file.

    Returns:
        dict: A dictionary where keys are normalized zib2020 concept names
              and values are tuples of (id, resource_markdown, fhir_element).
    """
    mappings = {}
    try:
        with open(mappings_file, 'r', encoding='utf-8') as f:
            # Regex to capture the ID, dataset name, the full resource markdown, and the FHIR element.
            row_regex = re.compile(r"\|\s*([\d\w]+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*`(.*?)`\s*\|")

            for line in f:
                match = row_regex.search(line)
                if match:
                    # Group 1: zib2020 ID
                    zib2020_id = match.group(1).strip()
                    # Group 2: Dataset name
                    name = match.group(2).replace('&emsp;', '').strip()
                    # Group 3: The full markdown for the resource column
                    resource_markdown = match.group(3).strip()
                    # Group 4: The FHIR element
                    fhir_element = match.group(4).strip()

                    # Normalize the name for case-insensitive lookup
                    normalized_name = name.lower()
                    if normalized_name:
                        # Store the ID, full resource markdown, and the element
                        mappings[normalized_name] = (zib2020_id, resource_markdown, fhir_element)
    except FileNotFoundError:
        print(f"Error: Mappings file not found at '{mappings_file}'")
    return mappings

def propose_mappings(zib2017_concepts, zib2020_mappings):
    """
    Proposes mappings for zib2017 concepts based on zib2020 mappings by matching names.

    Args:
        zib2017_concepts (list): A list of concept dictionaries for zib2017.
        zib2020_mappings (dict): A dictionary of known mappings for zib2020.

    Returns:
        list: A list of dictionaries, each representing a proposed mapping.
    """
    proposed_mappings = []
    # OID prefix for zib2017 data elements
    oid_prefix = '2.16.840.1.113883.2.4.3.11.60.117.2.'

    for concept in zib2017_concepts:
        concept_id = concept.get('id', '')
        
        # Filter for actual data elements from the correct dataset.
        # These have a specific OID structure and an 'iddisplay' field,
        # which distinguishes them from value set entries.
        if concept_id.startswith(oid_prefix) and 'iddisplay' in concept:
            # Extract the functional ID from the last part of the OID, as requested.
            dataset_id = concept_id.split('.')[-1]
            
            # Extract the Dutch name ('nl-NL') from the concept
            name_obj = next((n for n in concept.get('name', []) if n.get('language') == 'nl-NL'), None)
            # Use the full name if available, otherwise fall back to the shortName
            name = name_obj.get('#text', '') if name_obj else concept.get('shortName', '')

            if name:
                # Normalize the name for lookup (lowercase, strip whitespace)
                normalized_name = name.lower().strip()
                # Find the corresponding mapping from the zib2020 data
                mapping = zib2020_mappings.get(normalized_name)

                if mapping:
                    # If a match is found, use the existing mapping.
                    matched_id, resource_markdown, fhir_element = mapping
                    proposed_mappings.append({
                        'id': dataset_id, 
                        'name': name, 
                        'matched_zib2020_id': matched_id,
                        'resource': resource_markdown, 
                        'fhir_element': fhir_element
                    })
                else:
                    # If no match is found, leave the mapping empty
                    proposed_mappings.append({
                        'id': dataset_id, 
                        'name': name, 
                        'matched_zib2020_id': '',
                        'resource': '', 
                        'fhir_element': ''
                    })
    return proposed_mappings

def generate_markdown_table(proposed_mappings, output_file):
    """
    Generates a Markdown table of the proposed mappings and writes it to a file.

    Args:
        proposed_mappings (list): The list of proposed mappings to write.
        output_file (str): The path to the output .md file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#### Proposed Mappings for zib2017\n\n")
        f.write("This table provides an overview of proposed mappings for the zib2017 dataset elements. ")
        f.write("The proposals are generated by finding elements with the same name in the zib2020 dataset and reusing their mappings.\n\n")
        f.write("| ID | Dataset name | Matched zib2020 ID | Proposed Resource | Proposed FHIR element |\n")
        f.write("|---|---|---|---|---|\n")
        for mapping in proposed_mappings:
            # The 'resource' key now holds the full, pre-formatted markdown string
            resource_display = mapping['resource']
            element_display = f"`{mapping['fhir_element']}`" if mapping['fhir_element'] else ''
            f.write(f"| {mapping['id']} | {mapping['name']} | {mapping['matched_zib2020_id']} | {resource_display} | {element_display} |\n")

def generate_json_output(proposed_mappings, output_file):
    """
    Generates a JSON file containing only the successfully matched mappings.

    Args:
        proposed_mappings (list): The list of proposed mappings.
        output_file (str): The path for the output .json file.
    """
    # Filter for mappings that have a matched zib2020 ID
    matched_mappings = [m for m in proposed_mappings if m['matched_zib2020_id']]

    # Create a new list with only the required keys
    json_data = [
        {
            "zib2017_id": mapping['id'],
            "zib2020_id": mapping['matched_zib2020_id'],
            "concept_name": mapping['name']
        }
        for mapping in matched_mappings
    ]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)


def main():
    """
    Main function to orchestrate the mapping proposal process.
    """
    # --- Configuration ---
    # Define the file paths.
    json_file = 'util/DS_pzp_dataset_raadplegen_(download_2025-07-29T11_58_18).json'
    mappings_file = 'R4/input/includes/mappings.md'
    markdown_output_file = 'util/proposed_mappings_zib2017.md'
    json_output_file = 'util/r4-to-r3-converter/fhirconverter/matched_concepts_between_zib2017_and_zib2020.json'

    # The root OID for the zib2017 dataset within the JSON file.
    zib2017_root_id = "2.16.840.1.113883.2.4.3.11.60.117.2.217"

    print("Starting the mapping proposal process...")

    # 1. Extract concepts for zib2017 from the main dataset file.
    print(f"Extracting zib2017 concepts using root ID: {zib2017_root_id}...")
    zib2017_concepts = extract_concepts_by_root_id(json_file, zib2017_root_id)
    if not zib2017_concepts:
        print("Could not extract zib2017 concepts. Exiting.")
        return

    # 2. Get the existing, known mappings for zib2020.
    print(f"Loading existing zib2020 mappings from '{mappings_file}'...")
    zib2020_mappings = get_zib2020_mappings(mappings_file)
    if not zib2020_mappings:
        print("Could not load zib2020 mappings. The resulting proposals will be empty.")

    # 3. Propose new mappings for zib2017 based on name matching.
    print("Generating proposed mappings for zib2017...")
    proposed = propose_mappings(zib2017_concepts, zib2020_mappings)
    
    # 4. Write the results to the output files.
    print(f"Writing Markdown table to '{markdown_output_file}'...")
    generate_markdown_table(proposed, markdown_output_file)
    print(f"Successfully generated mapping table with {len(proposed)} elements.")

    print(f"Writing JSON output to '{json_output_file}'...")
    generate_json_output(proposed, json_output_file)
    print("Successfully generated JSON output file.")


    # --- Statistics Calculation ---
    print("\n--- Mapping Statistics ---")
    
    matched_count = 0
    used_zib2020_names = set()

    for mapping in proposed:
        if mapping['matched_zib2020_id']:
            matched_count += 1
            # Use the same normalization to ensure the lookup is consistent
            used_zib2020_names.add(mapping['name'].lower().strip())
    
    unmatched_count = len(proposed) - matched_count

    print(f"Total zib2017 elements processed: {len(proposed)}")
    print(f"Elements matched with zib2020:   {matched_count}")
    print(f"Elements not matched:            {unmatched_count}")
    
    # Find zib2020 mappings that were not used
    all_zib2020_names = set(zib2020_mappings.keys())
    unused_zib2020_names = all_zib2020_names - used_zib2020_names
    
    unused_zib2020_ids = [zib2020_mappings[name][0] for name in unused_zib2020_names]

    print(f"\nFound {len(unused_zib2020_ids)} zib2020 mappings that were not used for any zib2017 element.")
    if unused_zib2020_ids:
        print("IDs of unused zib2020 mappings:", ", ".join(sorted(unused_zib2020_ids)))

    print("\nProcess finished successfully!")


if __name__ == '__main__':
    main()
