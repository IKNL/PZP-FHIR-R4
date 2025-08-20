#!/usr/bin/env python3
"""
Generate complete manual_overrides.yaml template from integration.json
"""

import json
import yaml
from pathlib import Path

def generate_manual_overrides_template():
    """Generate a complete manual_overrides.yaml template with all ZIB2017 concepts"""
    
    # Load integration.json
    integration_file = Path(__file__).parent / 'integration.json'
    with open(integration_file, 'r', encoding='utf-8') as f:
        records = json.load(f)
    
    # Generate the template structure
    template = {
        'overrides': {}
    }
    
    output_lines = [
        "# manual_overrides.yaml",
        "# Provide manual mapping overrides for ZIB2017 dataset concepts to STU3 profiles.",
        "# Uncomment and modify the entries you want to override.",
        "# Structure:",
        "# overrides:",
        "#   '<dataset_id>':",
        "#     - zib_concept_id: 'NL-CM:xx.x.x'",
        "#       resource: <ResourceType>",
        "#       profile_id: <ProfileId>",
        "#       element_path: <FHIR element path>",
        "#       element_id: <element id>",
        "",
        "overrides:",
        "  # Uncomment and modify entries below as needed",
        ""
    ]
    
    # Process each record in dataset order
    for record in records:
        dataset_id = record.get('dataset_id', '')
        name = record.get('name', '')
        depth = record.get('depth', 0)
        zib_refs = record.get('zib_refs', [])
        stu3_mappings = record.get('stu3_mappings', [])
        
        # Create indentation for hierarchy
        indent = '  ' * depth
        
        # Add comment with dataset info
        output_lines.append(f"  # {dataset_id}: {indent}{name}")
        
        if stu3_mappings:
            # Use existing mapping as template
            for mapping in stu3_mappings:
                zib_concept_id = mapping.get('zib_concept_id', '')
                resource = mapping.get('resource', '')
                profile_id = mapping.get('profile_id', '')
                element_path = mapping.get('element_path', '')
                element_id = mapping.get('element_id', '')
                
                output_lines.extend([
                    f"  # '{dataset_id}':",
                    f"  #   - zib_concept_id: '{zib_concept_id}'",
                    f"  #     resource: {resource}",
                    f"  #     profile_id: {profile_id}",
                    f"  #     element_path: '{element_path}'",
                    f"  #     element_id: '{element_id}'",
                    ""
                ])
                break  # Only use first mapping as template
        else:
            # No mapping exists, create placeholder
            zib_ref = zib_refs[0] if zib_refs else 'NL-CM:XX.X.X'
            output_lines.extend([
                f"  # '{dataset_id}':",
                f"  #   - zib_concept_id: '{zib_ref}'",
                f"  #     resource: <ResourceType>",
                f"  #     profile_id: <ProfileId>",
                f"  #     element_path: '<FHIR element path>'",
                f"  #     element_id: '<element id>'",
                ""
            ])
    
    # Add the one active override from current file
    output_lines.extend([
        "  # Active overrides (uncommented entries will be used)",
        "  '772':",
        "    - zib_concept_id: 'NL-CM-15.1.13'",
        "      resource: Encounter", 
        "      profile_id: ACP-Encounter",
        "      element_path: 'Encounter.diagnosis.condition'",
        "      element_id: 'Encounter.diagnosis.condition'"
    ])
    
    # Write to file
    output_file = Path(__file__).parent / 'manual_overrides_complete.yaml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Generated complete manual overrides template: {output_file}")
    print(f"Total concepts: {len(records)}")

if __name__ == "__main__":
    generate_manual_overrides_template()
