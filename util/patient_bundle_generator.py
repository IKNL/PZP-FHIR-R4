#!/usr/bin/env python3
"""
Script to generate FHIR Bundle resources per patient.

This script scans the fsh-generated/resources folder for FHIR JSON files,
groups them by patient, and creates a Bundle resource containing all 
resources related to each patient.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
import uuid


def load_fhir_resource(file_path):
    """Load and parse a FHIR resource JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading {file_path}: {e}")
        return None


def should_skip_resource(resource_type):
    """Check if a resource type should be skipped in patient bundles."""
    # Skip definition and infrastructure resources
    skip_types = {
        'StructureDefinition', 
        'ValueSet', 
        'ImplementationGuide',
        'ActorDefinition',
        'SearchParameter'
    }
    return resource_type in skip_types


def extract_patient_prefix(resource_id):
    """Extract patient prefix from resource ID (e.g., 'F1-ACP' from 'F1-ACP-Patient-HendrikHartman')."""
    if not resource_id:
        return None
    
    # Pattern to match patient prefixes like F1-ACP, P2-ACP, etc.
    match = re.match(r'^([A-Z]\d+-ACP)', resource_id)
    if match:
        return match.group(1)
    
    return None


def find_patient_references_in_resource(resource):
    """Find all Patient references in a resource."""
    patient_refs = set()
    
    def search_for_patient_refs(obj, path=""):
        """Recursively search for Patient references."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if key == "reference" and isinstance(value, str) and value.startswith("Patient/"):
                    patient_id = value.replace("Patient/", "")
                    prefix = extract_patient_prefix(patient_id)
                    if prefix:
                        patient_refs.add(prefix)
                else:
                    search_for_patient_refs(value, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_for_patient_refs(item, f"{path}[{i}]")
    
    search_for_patient_refs(resource)
    return patient_refs


def create_bundle_entry(resource):
    """Create a Bundle entry for a FHIR resource."""
    resource_type = resource.get('resourceType')
    resource_id = resource.get('id')
    
    if not resource_type or not resource_id:
        return None
    
    entry = {
        "fullUrl": f"urn:uuid:{str(uuid.uuid4())}",
        "resource": resource,
        "request": {
            "method": "PUT",
            "url": f"{resource_type}/{resource_id}"
        }
    }
    
    return entry


def create_patient_bundle(patient_prefix, resources):
    """Create a Bundle resource containing all resources for a patient."""
    
    # Find the actual patient resource
    patient_resource = None
    for resource in resources:
        if resource.get('resourceType') == 'Patient':
            patient_resource = resource
            break
    
    if not patient_resource:
        print(f"Warning: No Patient resource found for prefix {patient_prefix}")
        return None
    
    patient_name = patient_resource.get('name', [{}])[0].get('text', 'Unknown')
    patient_id = patient_resource.get('id', 'Unknown')
    
    # Create the bundle
    bundle = {
        "resourceType": "Bundle",
        "id": f"{patient_prefix}-PatientBundle",
        "meta": {
            "profile": [
                "http://hl7.org/fhir/StructureDefinition/Bundle"
            ],
            "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        },
        "identifier": {
            "system": "https://api.iknl.nl/docs/pzp/r4/NamingSystem/patient-bundle",
            "value": f"{patient_prefix}-PatientBundle"
        },
        "type": "transaction",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "entry": []
    }
    
    # Add metadata
    bundle["meta"]["tag"] = [
        {
            "system": "https://api.iknl.nl/docs/pzp/r4/CodeSystem/bundle-type",
            "code": "patient-data",
            "display": "Patient Data Bundle"
        }
    ]
    
    # Add description
    total_resources = len(resources)
    resource_types = {}
    for resource in resources:
        res_type = resource.get('resourceType', 'Unknown')
        resource_types[res_type] = resource_types.get(res_type, 0) + 1
    
    # Sort entries: Patient first, then alphabetically by resource type
    sorted_resources = sorted(resources, key=lambda r: (
        0 if r.get('resourceType') == 'Patient' else 1,
        r.get('resourceType', ''),
        r.get('id', '')
    ))
    
    # Create bundle entries
    for resource in sorted_resources:
        entry = create_bundle_entry(resource)
        if entry:
            bundle["entry"].append(entry)
    
    return bundle, {
        'patient_name': patient_name,
        'patient_id': patient_id,
        'total_resources': total_resources,
        'resource_types': resource_types
    }


def group_resources_by_patient(resources_dir):
    """Group all resources by patient prefix."""
    
    resources_path = Path(resources_dir)
    if not resources_path.exists():
        print(f"Error: Resources directory not found: {resources_dir}")
        return {}
    
    patient_groups = {}
    ungrouped_resources = []
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    # Get all JSON files and sort them
    json_files = sorted(resources_path.glob("*.json"))
    
    print(f"Processing {len(json_files)} files...")
    
    for json_file in json_files:
        print(f"  Processing: {json_file.name}")
        
        # Load the FHIR resource
        resource = load_fhir_resource(json_file)
        if not resource:
            error_count += 1
            continue
        
        resource_type = resource.get('resourceType')
        resource_id = resource.get('id')
        
        # Skip certain resource types
        if should_skip_resource(resource_type):
            print(f"    Skipping {resource_type} resource")
            skipped_count += 1
            continue
        
        # Extract patient prefix from resource ID
        direct_prefix = extract_patient_prefix(resource_id)
        
        # Also check for patient references in the resource content
        referenced_prefixes = find_patient_references_in_resource(resource)
        
        # Determine which patient group(s) this resource belongs to
        target_prefixes = set()
        if direct_prefix:
            target_prefixes.add(direct_prefix)
        if referenced_prefixes:
            target_prefixes.update(referenced_prefixes)
        
        if target_prefixes:
            # Add to all relevant patient groups
            for prefix in target_prefixes:
                if prefix not in patient_groups:
                    patient_groups[prefix] = []
                patient_groups[prefix].append(resource)
            
            prefix_list = ', '.join(sorted(target_prefixes))
            if len(target_prefixes) > 1:
                print(f"    Added to patient groups: {prefix_list}")
            else:
                print(f"    Added to patient group: {prefix_list}")
            processed_count += 1
        else:
            ungrouped_resources.append((json_file.name, resource))
            print(f"    No patient association found - ungrouped")
    
    print(f"\nGrouping complete:")
    print(f"  Processed: {processed_count} resources")
    print(f"  Skipped: {skipped_count} resources") 
    print(f"  Errors: {error_count} resources")
    print(f"  Ungrouped: {len(ungrouped_resources)} resources")
    print(f"  Patient groups: {len(patient_groups)}")
    
    if ungrouped_resources:
        print(f"\nUngrouped resources:")
        for filename, resource in ungrouped_resources:
            print(f"    {filename} ({resource.get('resourceType', 'Unknown')})")
    
    return patient_groups


def generate_patient_bundles(resources_dir, output_dir):
    """Generate Bundle resources for each patient."""
    
    print("IKNL PZP FHIR R4 Patient Bundle Generator")
    print("=" * 50)
    print(f"Resources directory: {resources_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Group resources by patient
    patient_groups = group_resources_by_patient(resources_dir)
    
    if not patient_groups:
        print("No patient groups found")
        return False
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate bundles
    bundles_created = 0
    
    for patient_prefix, resources in patient_groups.items():
        print(f"\nGenerating bundle for patient group: {patient_prefix}")
        print(f"  Resources: {len(resources)}")
        
        result = create_patient_bundle(patient_prefix, resources)
        
        if result:
            bundle, metadata = result
            # Write bundle to file
            bundle_filename = f"{patient_prefix}-PatientBundle.json"
            bundle_path = output_path / bundle_filename
            
            try:
                with open(bundle_path, 'w', encoding='utf-8') as f:
                    json.dump(bundle, f, indent=2, ensure_ascii=False)
                
                print(f"  Created: {bundle_filename}")
                print(f"  Patient: {metadata['patient_name']} ({metadata['patient_id']})")
                print(f"  Total resources in bundle: {metadata['total_resources']}")
                print(f"  Resource types: {', '.join(f'{k}({v})' for k, v in sorted(metadata['resource_types'].items()))}")
                
                bundles_created += 1
                
            except IOError as e:
                print(f"  Error writing bundle: {e}")
        else:
            print(f"  Failed to create bundle for {patient_prefix}")
    
    print(f"\n{bundles_created} patient bundles created successfully!")
    return bundles_created > 0


def main():
    """Main function to run the script."""
    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Go up one level from util folder
    resources_dir = project_root / "fsh-generated" / "resources"
    output_dir = script_dir / "patient-bundles"  # Output in util folder
    
    success = generate_patient_bundles(resources_dir, output_dir)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())