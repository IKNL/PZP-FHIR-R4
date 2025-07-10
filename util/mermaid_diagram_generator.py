import os
import re
import argparse
import collections

def generate_mermaid_diagram(fsh_directory, output_markdown_file):
    """
    Parses all .fsh files in a directory to find profiles, instances, and their
    references, then generates a Mermaid flowchart diagram in a Markdown file.

    Args:
        fsh_directory (str): The path to the directory containing .fsh files.
        output_markdown_file (str): The path to the output Markdown (.md) file.
    """
    profiles = {}  # { 'ProfileName': 'ResourceType' }
    instance_to_profile_map = {} # { 'InstanceName': 'ProfileName' }
    references = set()  # Use a set for references to automatically handle duplicates

    # --- Regex Patterns ---
    profile_pattern = re.compile(r"^Profile:\s*(\S+)")
    instance_pattern = re.compile(r"^Instance:\s*(\S+)")
    instance_of_pattern = re.compile(r"^InstanceOf:\s*(\S+)")
    
    profile_reference_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.]+)\s+only\s+Reference\((\S+)\)")
    contains_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.]+)\s+contains\s+(\S+)\s")
    
    # **FIXED**: Updated regex to handle complex paths with brackets and symbols.
    instance_reference_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.\-\[\]\=\+]+)\s*=\s*Reference\((\S+?)\)")


    print("Scanning for Profiles and Instances...")
    if not os.path.isdir(fsh_directory):
        print(f"Error: Input directory '{fsh_directory}' not found.")
        return

    # --- Pass 1: Find all Profiles and Instance-to-Profile mappings ---
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            filepath = os.path.join(fsh_directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                current_instance = None
                current_profile = None

                for line in f:
                    stripped_line = line.strip()
                    
                    profile_match = profile_pattern.match(stripped_line)
                    if profile_match:
                        current_profile = profile_match.group(1)
                        current_instance = None
                        
                        resource_type_from_file = os.path.splitext(filename)[0]
                        profiles[current_profile] = resource_type_from_file
                        continue

                    instance_match = instance_pattern.match(stripped_line)
                    if instance_match:
                        current_instance = instance_match.group(1)
                        current_profile = None 
                        continue
                    
                    if current_instance:
                        instance_of_match = instance_of_pattern.match(stripped_line)
                        if instance_of_match:
                            profile_name = instance_of_match.group(1)
                            instance_to_profile_map[current_instance] = profile_name
    
    print(f"Found {len(profiles)} profiles and {len(instance_to_profile_map)} instances.")

    # --- Pass 2: Find all references between profiles ---
    print("Scanning for references...")
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            filepath = os.path.join(fsh_directory, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                current_context_profile = None
                for line in f:
                    stripped_line = line.strip()

                    profile_match = profile_pattern.match(stripped_line)
                    if profile_match:
                        current_context_profile = profile_match.group(1)
                        continue
                    
                    instance_match = instance_pattern.match(stripped_line)
                    if instance_match:
                        instance_name = instance_match.group(1)
                        current_context_profile = instance_to_profile_map.get(instance_name)
                        continue
                    
                    if current_context_profile:
                        prof_ref_match = profile_reference_pattern.match(stripped_line)
                        if prof_ref_match:
                            element_path = prof_ref_match.group(1)
                            possible_targets = [p.strip() for p in prof_ref_match.group(2).split('|')]
                            for target_profile in possible_targets:
                                if target_profile in profiles:
                                    references.add((current_context_profile, element_path, target_profile))

                        contains_match = contains_pattern.match(stripped_line)
                        if contains_match:
                            element_path = contains_match.group(1)
                            target_profile = contains_match.group(2)
                            if target_profile in profiles:
                                references.add((current_context_profile, element_path, target_profile))

                        inst_ref_match = instance_reference_pattern.match(stripped_line)
                        if inst_ref_match:
                            # The captured element path will now include brackets, e.g., "participant[0].individual"
                            element_path = inst_ref_match.group(1)
                            target_instance_name = inst_ref_match.group(2).split(')')[0]
                            
                            target_profile = instance_to_profile_map.get(target_instance_name)
                            if target_profile:
                                # We simplify the element path for the diagram label for clarity
                                simple_element_path = element_path.split('[')[0]
                                references.add((current_context_profile, simple_element_path, target_profile))
                    
                    if not stripped_line:
                        current_context_profile = None

    print(f"Found {len(references)} unique references.")

    # --- Generate the Mermaid file ---
    if profiles:
        output_dir = os.path.dirname(output_markdown_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        with open(output_markdown_file, 'w', encoding='utf-8') as f:
            f.write("```mermaid\n")
            f.write("flowchart TB\n")
            
            f.write("\n    %% ---- Profile Definitions ----\n")
            profile_to_node_id = {}
            for name, resource_type in sorted(profiles.items()):
                clean_name = re.sub(r'^ACP-?', '', name)
                node_id = clean_name.replace('-', '_')
                profile_to_node_id[name] = node_id
                
                node_label = f'"`**{resource_type}**<br>({name})`"'
                f.write(f'    {node_id}[{node_label}]\n')

            f.write("\n    %% ---- Reference Definitions ----\n")
            for source, element, target in sorted(list(references)):
                if source in profile_to_node_id and target in profile_to_node_id:
                    source_node_id = profile_to_node_id[source]
                    target_node_id = profile_to_node_id[target]
                    f.write(f'    {source_node_id} -- .{element} --> {target_node_id}\n')
            
            f.write("```\n")
        
        print(f"\nSuccessfully generated Mermaid diagram file at: {output_markdown_file}")
    else:
        print("No profiles were found to generate a diagram.")

def main():
    parser = argparse.ArgumentParser(
        description="Generates a Mermaid diagram from FHIR Shorthand (FSH) profiles and references, including those found in instances.",
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
        help="The path for the output Mermaid diagram Markdown file.\n(default: 'input/includes/fhir-data-model-mermaid-diagram.md')"
    )
    args = parser.parse_args()
    generate_mermaid_diagram(args.fsh_dir, args.output_file)

if __name__ == "__main__":
    main()