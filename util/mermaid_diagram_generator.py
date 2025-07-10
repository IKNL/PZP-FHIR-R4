import os
import re
import argparse

def generate_mermaid_diagram(fsh_directory, output_markdown_file):
    """
    Parses all .fsh files in a directory to find profiles and their
    references, then generates a Mermaid flowchart diagram in a Markdown file.

    Args:
        fsh_directory (str): The path to the directory containing .fsh files.
        output_markdown_file (str): The path to the output Markdown (.md) file.
    """
    profiles = {}  # { 'ProfileName': 'ResourceType' }
    references = []  # [ ('SourceProfile', 'element.path', 'TargetProfile') ]

    # Regex patterns to find definitions
    profile_pattern = re.compile(r"^Profile:\s*(\S+)")
    # Pattern to find references, e.g., "* subject only Reference(ACP-Patient)"
    # This now handles choices like Reference(ProfileA | ProfileB)
    reference_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.]+)\s+only\s+Reference\((\S+)\)")
    # Pattern to find references in contained items, e.g., "* item contains ACP-Observation 1..*"
    contains_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.]+)\s+contains\s+(\S+)\s")


    print("Scanning for Profiles and References...")

    if not os.path.isdir(fsh_directory):
        print(f"Error: Input directory '{fsh_directory}' not found.")
        return

    # --- Pass 1: Find all profiles and map them to their ResourceType from the filename ---
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            # Derive the ResourceType from the filename (e.g., "Patient.fsh" -> "Patient")
            resource_type_from_file = os.path.splitext(filename)[0]
            filepath = os.path.join(fsh_directory, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    profile_match = profile_pattern.match(stripped_line)
                    if profile_match:
                        profile_name = profile_match.group(1)
                        profiles[profile_name] = resource_type_from_file

    print(f"Found {len(profiles)} profiles.")

    # --- Pass 2: Find all references between profiles ---
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            filepath = os.path.join(fsh_directory, filename)
            print(f"Processing for references: {filename}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                current_profile = None
                for line in f:
                    stripped_line = line.strip()
                    profile_match = profile_pattern.match(stripped_line)
                    if profile_match:
                        current_profile = profile_match.group(1)
                        continue

                    if current_profile:
                        # Check for 'only Reference(ProfileA | ProfileB)' style
                        ref_match = reference_pattern.match(stripped_line)
                        if ref_match:
                            element_path = ref_match.group(1)
                            # Split targets in case of choices
                            possible_targets = [p.strip() for p in ref_match.group(2).split('|')]
                            for target_profile in possible_targets:
                                if target_profile in profiles:
                                    references.append((current_profile, element_path, target_profile))

                        # Check for 'contains Profile' style
                        contains_match = contains_pattern.match(stripped_line)
                        if contains_match:
                            element_path = contains_match.group(1)
                            target_profile = contains_match.group(2)
                            if target_profile in profiles:
                                references.append((current_profile, element_path, target_profile))


                    if not stripped_line:
                        current_profile = None

    print(f"Found {len(references)} references between profiles.")

    # --- Generate the Mermaid file ---
    if profiles:
        output_dir = os.path.dirname(output_markdown_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        with open(output_markdown_file, 'w', encoding='utf-8') as f:
            f.write("```mermaid\n")
            f.write("flowchart TB\n")
            
            # Define all the nodes (profiles)
            f.write("\n    %% ---- Profile Definitions ----\n")
            for name, resource_type in sorted(profiles.items()):
                # Remove "ACP" or "ACP-" prefix for the node ID
                clean_name = re.sub(r'^ACP-?', '', name)
                node_id = clean_name.replace('-', '_')
                
                # The label uses Markdown for formatting within the node
                node_label = f'"`**{resource_type}**({name})`"'
                f.write(f'    {node_id}[{node_label}]\n')

            # Define all the links (references)
            f.write("\n    %% ---- Reference Definitions ----\n")
            for source, element, target in sorted(references):
                # Remove "ACP" or "ACP-" prefix for the source and target node IDs
                clean_source_name = re.sub(r'^ACP-?', '', source)
                source_node_id = clean_source_name.replace('-', '_')

                clean_target_name = re.sub(r'^ACP-?', '', target)
                target_node_id = clean_target_name.replace('-', '_')
                
                f.write(f'    {source_node_id} -- .{element} --> {target_node_id}\n')
            
            f.write("```\n")
        
        print(f"\nSuccessfully generated Mermaid diagram file at: {output_markdown_file}")
    else:
        print("No profiles were found to generate a diagram.")

def main():
    parser = argparse.ArgumentParser(
        description="Generates a Mermaid diagram from FHIR Shorthand (FSH) profiles and references.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--fsh-dir',
        default='input/fsh',
        help="The directory containing the .fsh source files.\n(default: 'input/fsh')"
    )
    parser.add_argument(
        '--output-file',
        default='input/includes/fhir-data-model-mermaid-diagram.md',
        help="The path for the output Mermaid diagram Markdown file.\n(default: 'input/pagecontent/profile-diagram.md')"
    )
    args = parser.parse_args()
    generate_mermaid_diagram(args.fsh_dir, args.output_file)

if __name__ == "__main__":
    main()
