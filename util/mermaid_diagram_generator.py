"""
mermaid_diagram_generator.py

Generates a Mermaid flowchart diagram from FHIR Shorthand (FSH) profile
definitions, visualising the relationships between FHIR resource profiles in
the ACP Implementation Guide.

Workflow:
  1. Scans all .fsh files to discover Profile definitions and Instance-to-
     Profile mappings (Pass 1).
  2. Re-scans the .fsh files to extract inter-profile references, including
     `only Reference(...)`, `contains`, and instance-level `= Reference(...)`
     patterns (Pass 2).
  3. Produces a Markdown file containing a Mermaid flowchart with:
       - Resource-type subgraphs grouping related profiles.
       - Colour-coded nodes by functional category (Agreements, Individuals,
         Supporting information, Consultation).
       - Labelled edges showing the FHIR element paths that link resources.

Usage:
  python util/mermaid_diagram_generator.py [--fsh-dir DIR] [--output-file FILE]

Examples:
  # Default paths
  python util/mermaid_diagram_generator.py

  # Custom paths
  python util/mermaid_diagram_generator.py --fsh-dir input/fsh \\
      --output-file input/includes/fhir-data-model-mermaid-diagram.md
"""

import os
import re
import argparse
from collections import defaultdict

# =============================================================================
# Configuration — edit these values to match your project
# =============================================================================

# Default directory containing the .fsh profile files.
DEFAULT_FSH_DIR = "input/fsh"

# Default output path for the generated Mermaid diagram Markdown file.
DEFAULT_OUTPUT_FILE = "input/includes/fhir-data-model-mermaid-diagram.md"

# Maps each FHIR resource type to a functional category used for subgraph
# grouping and colour-coding in the diagram.
RESOURCE_CATEGORIES = {
    "Observation": "ACP Agreements",
    "Consent": "ACP Agreements",
    "Goal": "ACP Agreements",
    "Patient": "ACP Individuals",
    "RelatedPerson": "ACP Individuals",
    "Practitioner": "ACP Individuals",
    "PractitionerRole": "ACP Individuals",
    "DeviceUseStatement": "ACP Supporting information",
    "Device": "ACP Supporting information",
    "CommunicationRequest": "ACP Supporting information",
    "Encounter": "ACP Consultation",
    "Procedure": "ACP Consultation",
}

# Mermaid CSS class styles per category. The "default" entry is used for any
# resource type not listed in RESOURCE_CATEGORIES.
CATEGORY_STYLES = {
    "ACP Agreements": "fill:#e6f3ff,stroke:#b3d9ff,color:#000",               # Light Blue
    "ACP Individuals": "fill:#e6ffe6,stroke:#b3ffb3,color:#000",              # Light Green
    "ACP Supporting information": "fill:#fff5e6,stroke:#ffddb3,color:#000",   # Light Orange
    "ACP Consultation": "fill:#f0e6ff,stroke:#d9b3ff,color:#000",             # Light Purple
    "default": "fill:#f2f2f2,stroke:#cccccc,color:#000",                      # Default Grey
}


def generate_mermaid_diagram(fsh_directory, output_markdown_file):
    """
    Parses FSH files to generate a Mermaid diagram with categorized and styled
    subgraphs, including labeled links between them.
    """
    resource_categories = RESOURCE_CATEGORIES
    category_styles = CATEGORY_STYLES


    # --- Data Structures ---
    profiles = {}  # { 'ProfileName': 'ResourceType' }
    instance_to_profile_map = {} # { 'InstanceName': 'ProfileName' }
    detailed_references = set() # { (source_profile, element_path, target_profile) }

    # --- Regex Patterns ---
    profile_pattern = re.compile(r"^Profile:\s*(\S+)")
    instance_pattern = re.compile(r"^Instance:\s*(\S+)")
    instance_of_pattern = re.compile(r"^InstanceOf:\s*(\S+)")
    
    profile_reference_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.]+)\s+only\s+Reference\((\S+)\)")
    contains_pattern = re.compile(r"^\*\s*([a-zA-Z0-9\.]+)\s+contains\s+(\S+)\s")
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
                current_instance, current_profile = None, None
                for line in f:
                    stripped_line = line.strip()
                    if profile_match := profile_pattern.match(stripped_line):
                        current_profile = profile_match.group(1)
                        resource_type = os.path.splitext(filename)[0]
                        profiles[current_profile] = resource_type
                    elif instance_match := instance_pattern.match(stripped_line):
                        current_instance = instance_match.group(1)
                    elif current_instance and (instance_of_match := instance_of_pattern.match(stripped_line)):
                        instance_to_profile_map[current_instance] = instance_of_match.group(1)

    # --- Pass 2: Find all detailed, profile-level references with their paths ---
    for filename in sorted(os.listdir(fsh_directory)):
        if filename.endswith(".fsh"):
            filepath = os.path.join(fsh_directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                current_context_profile = None
                for line in f:
                    stripped_line = line.strip()
                    if profile_match := profile_pattern.match(stripped_line):
                        current_context_profile = profile_match.group(1)
                    elif instance_match := instance_pattern.match(stripped_line):
                        current_context_profile = instance_to_profile_map.get(instance_match.group(1))
                    
                    if current_context_profile:
                        for pattern in [profile_reference_pattern, contains_pattern, instance_reference_pattern]:
                            if match := pattern.match(stripped_line):
                                element_path, target_str = match.groups()
                                simple_element_path = element_path.split('[')[0]
                                target_profiles = []
                                
                                if pattern == instance_reference_pattern:
                                    if p_name := instance_to_profile_map.get(target_str.split(')')[0]):
                                        target_profiles.append(p_name)
                                else:
                                    target_profiles.extend(p.strip() for p in target_str.split('|'))
                                
                                for target_profile in target_profiles:
                                    if target_profile in profiles:
                                        detailed_references.add((current_context_profile, simple_element_path, target_profile))

    # --- Mermaid File Generation ---
    if not profiles:
        print("No profiles found.")
        return
        
    output_dir = os.path.dirname(output_markdown_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    resource_to_profiles = defaultdict(list)
    for profile, resource in profiles.items():
        resource_to_profiles[resource].append(profile)

    resource_references = defaultdict(set)
    for source_profile, element_path, target_profile in detailed_references:
        if source_profile in profiles and target_profile in profiles:
            source_resource = profiles[source_profile]
            target_resource = profiles[target_profile]
            if source_resource != target_resource:
                resource_references[(source_resource, target_resource)].add(element_path)

    with open(output_markdown_file, 'w', encoding='utf-8') as f:
        f.write("#### Data Model Overview Diagram\n")
        f.write('<div class="mermaid" style="height: 700px; overflow: visible;">\n')
        f.write("flowchart TB\n\n")

        f.write("    %% ---- Style Definitions for Categories ----\n")
        # Create a mapping from category name to a simple class index (C0, C1, etc.)
        category_class_map = {name: f"C{i}" for i, name in enumerate(category_styles.keys())}
        for category, style in category_styles.items():
            class_name = category_class_map[category]
            f.write(f'    classDef {class_name} {style}\n')
        f.write("\n")

        f.write("    %% ---- Subgraph Definitions ----\n")
        # Sort resource types, placing Observation last to appear on the right
        sorted_resources = sorted(resource_to_profiles.items(), key=lambda x: (x[0] == "Observation", x[0]))
        
        for resource_type, profile_list in sorted_resources:
            f.write(f'    subgraph "{resource_type}"\n')
            for profile_name in sorted(profile_list):
                f.write(f'        {profile_name}\n')
            f.write("    end\n\n")

        f.write("    %% ---- Style Assignments ----\n")
        for resource_type, profile_list in sorted(resource_to_profiles.items()):
            category = resource_categories.get(resource_type, "default")
            class_name = category_class_map[category]
            # Apply the class to all nodes in the subgraph
            for profile_name in profile_list:
                f.write(f'    class {profile_name} {class_name}\n')
        f.write("\n")

        f.write("    %% ---- Resource Type References ----\n")
        for (source_resource, target_resource), paths in sorted(resource_references.items()):
            label = ", ".join(sorted(list(paths)))
            f.write(f'    {source_resource} -- "{label}" --> {target_resource}\n')
        
        f.write("</div>\n")
    
    print(f"\nSuccessfully generated final Mermaid diagram at: {output_markdown_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Generates a categorized and styled Mermaid diagram with labeled links between subgraphs.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--fsh-dir', default=DEFAULT_FSH_DIR, help=f"Directory containing .fsh files.\n(default: '{DEFAULT_FSH_DIR}')")
    parser.add_argument('--output-file', default=DEFAULT_OUTPUT_FILE, help=f"Path for the output diagram file.\n(default: '{DEFAULT_OUTPUT_FILE}')")
    args = parser.parse_args()
    generate_mermaid_diagram(args.fsh_dir, args.output_file)

if __name__ == "__main__":
    main()