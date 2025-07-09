import os
import re
import argparse

def extract_mappings_from_fsh(fsh_directory, output_markdown_file):
    """
    Parses all .fsh files in a directory, extracts mapping information from
    standalone Mapping blocks, and generates a Markdown table. The ResourceType
    is derived from the .fsh filename.

    Args:
        fsh_directory (str): The path to the directory containing .fsh files.
        output_markdown_file (str): The path to the output Markdown file.
    """
    # Regex to parse a mapping rule line. Captures element, ID, and name.
    mapping_rule_pattern = re.compile(r'^\*\s*(.*?)\s*->\s*"([^"]+)"(?:\s*"([^"]+)")?')
    top_level_keyword_pattern = re.compile(r"^(Alias|Profile|Extension|Logical|Resource|Mapping|ValueSet|CodeSystem|Instance|RuleSet):")

    all_mappings = []

    print("Scanning for Mappings...")

    if not os.path.isdir(fsh_directory):
        print(f"Error: Input directory '{fsh_directory}' not found.")
        return

    # Iterate through all files in the specified FSH directory
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            # Derive the ResourceType from the filename (e.g., "Patient.fsh" -> "Patient")
            resource_type_from_file = os.path.splitext(filename)[0]
            filepath = os.path.join(fsh_directory, filename)
            print(f"Processing file: {filename} (ResourceType: {resource_type_from_file})...")
            
            in_mapping_block = False
            current_source_profile = None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()

                    # A new top-level definition (unless it's the start of the current block) or a blank line ends the current context.
                    if (top_level_keyword_pattern.match(stripped_line) and not stripped_line.startswith("Mapping:")) or not stripped_line:
                        in_mapping_block = False
                        current_source_profile = None
                    
                    if stripped_line.startswith("Mapping:"):
                        in_mapping_block = True
                        current_source_profile = None # Reset source for new mapping
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
                            
                            # Append the data using the ResourceType from the file
                            all_mappings.append((resource_type_from_file, current_source_profile, fhir_element, functional_id, functional_name))

    print(f"\nFound a total of {len(all_mappings)} mapping entries.")
    
    if all_mappings:
        output_dir = os.path.dirname(output_markdown_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        with open(output_markdown_file, 'w', encoding='utf-8') as f:
            # --- Table 1: Sorted by Resource Name ---
            f.write("### Mappings by Resource\n\n")
            f.write("| Resource (profile) | FHIR element | Functional ID | Functional name |\n")
            f.write("|---|---|---|---|\n")
            
            # Sort by Profile Name (index 1), then by FHIR element (index 2)
            for mapping in sorted(all_mappings, key=lambda x: (x[1], x[2])): 
                resource_display = f"{mapping[0]} ({mapping[1]})"
                f.write(f"| {resource_display} | `{mapping[2]}` | {mapping[3]} | {mapping[4]} |\n")
            
            f.write("\n\n")

            # --- Table 2: Sorted by Functional ID ---
            f.write("### Mappings by Functional ID\n\n")
            f.write("| Functional ID | Functional name | Resource (profile) | FHIR element  |\n")
            f.write("|---|---|---|---|\n")

            # Sort by Functional ID (index 3). Handle non-numeric IDs gracefully.
            def sort_key(item):
                try:
                    # Attempt to convert to integer for proper numeric sorting
                    return int(item[3])
                except (ValueError, TypeError):
                    # If it's not a number, return a tuple that sorts strings after numbers
                    return (float('inf'), item[3])

            for mapping in sorted(all_mappings, key=sort_key):
                resource_display = f"{mapping[0]} ({mapping[1]})"
                f.write(f"| {mapping[3]} | {mapping[4]} | {resource_display} | `{mapping[2]}`   |\n")
        
        print(f"Successfully generated Markdown file at: {output_markdown_file}")
    else:
        print("No mappings were found to generate the file.")

def main():
    parser = argparse.ArgumentParser(
        description="Extracts FHIR Shorthand (FSH) mappings to a Markdown file.",
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
    args = parser.parse_args()
    extract_mappings_from_fsh(args.fsh_dir, args.output_file)

if __name__ == "__main__":
    main()
