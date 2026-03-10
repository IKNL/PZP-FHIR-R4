#!/usr/bin/env python3
"""
patient_bundle_generator.py

Generates FHIR Bundle (transaction) resources per patient from the compiled
FSH output.  This is a standalone utility that is **not** part of the IG
build pipeline — it is intended to create ready-to-POST bundles for
populating a FHIR server with test data.

Workflow:
  1. Scans the fsh-generated/resources folder for FHIR JSON files.
  2. Also scans the extra-resources-dir (default: input/resources) for
     additional instance resources, e.g. QuestionnaireResponses.
  3. Groups instance resources by patient using Patient references found
     anywhere in each resource.
  4. Creates one Bundle (type "transaction") per patient group containing
     all associated resources, with PUT requests for each entry.
  5. Creates one shared Bundle for resources not linked to any patient
     (e.g. Practitioner, PractitionerRole, Organization).

Usage:
  python util/patient_bundle_generator.py [--resources-dir DIR]
                                          [--extra-resources-dir DIR]
                                          [--output-dir DIR]

Examples:
  # Default paths
  python util/patient_bundle_generator.py

  # Custom paths
  python util/patient_bundle_generator.py \\
      --resources-dir fsh-generated/resources \\
      --extra-resources-dir input/resources \\
      --output-dir util/patient-bundles
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path
import uuid

# =============================================================================
# Configuration — edit these values to match your project
# =============================================================================

# Directory containing the compiled FHIR JSON resources (output of SUSHI).
DEFAULT_RESOURCES_DIR = "fsh-generated/resources"

# Additional directory scanned for instance resources (e.g. QuestionnaireResponses
# authored outside the FSH build, stored as plain JSON).
DEFAULT_EXTRA_RESOURCES_DIR = "input/resources"

# Output directory where the generated Bundle files are written.
DEFAULT_OUTPUT_DIR = "util/patient-bundles"

# FHIR resource types that should be skipped (definition / infrastructure
# resources that are not relevant for patient or shared bundles).
SKIP_RESOURCE_TYPES = {
    'StructureDefinition',
    'ValueSet',
    'CodeSystem',
    'ImplementationGuide',
    'ActorDefinition',
    'SearchParameter',
    'CapabilityStatement',
    'Questionnaire',
}

# Base URL used for Bundle identifiers and tags.
BUNDLE_SYSTEM_BASE = "https://api.iknl.nl/docs/pzp/r4"


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
    return resource_type in SKIP_RESOURCE_TYPES


def find_patient_references(resource):
    """Return the set of Patient resource IDs referenced anywhere in *resource*.

    Recursively walks the JSON structure looking for
    ``{"reference": "Patient/<id>"}`` entries.
    """
    patient_ids = set()

    def _walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "reference" and isinstance(value, str) and value.startswith("Patient/"):
                    patient_ids.add(value[len("Patient/"):])
                else:
                    _walk(value)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item)

    _walk(resource)
    return patient_ids


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


def create_patient_bundle(patient_id, patient_resource, associated_resources):
    """Create a Bundle resource containing the Patient and all associated resources."""
    patient_name = patient_resource.get('name', [{}])[0].get('text', 'Unknown')

    all_resources = [patient_resource] + associated_resources

    # Create the bundle
    bundle = {
        "resourceType": "Bundle",
        "id": f"{patient_id}-PatientBundle",
        "meta": {
            "profile": [
                "http://hl7.org/fhir/StructureDefinition/Bundle"
            ],
            "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "tag": [
                {
                    "system": f"{BUNDLE_SYSTEM_BASE}/CodeSystem/bundle-type",
                    "code": "patient-data",
                    "display": "Patient Data Bundle"
                }
            ]
        },
        "identifier": {
            "system": f"{BUNDLE_SYSTEM_BASE}/NamingSystem/patient-bundle",
            "value": f"{patient_id}-PatientBundle"
        },
        "type": "transaction",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "entry": []
    }

    # Collect resource-type counts
    total_resources = len(all_resources)
    resource_types = {}
    for resource in all_resources:
        res_type = resource.get('resourceType', 'Unknown')
        resource_types[res_type] = resource_types.get(res_type, 0) + 1

    # Sort entries: Patient first, then alphabetically by resource type / id
    sorted_resources = sorted(all_resources, key=lambda r: (
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


def discover_patients_and_resources(resources_dir, extra_resources_dir=None):
    """Load all FHIR instance resources and discover Patient resources.

    Scans *resources_dir* first, then optionally *extra_resources_dir* for
    additional instance resources (e.g. QuestionnaireResponses stored as plain
    JSON outside the FSH build).

    Returns:
        patients:   dict mapping Patient resource ID → Patient resource dict
        instances:  list of (filename, resource) tuples for non-Patient,
                    non-skipped instance resources
    """
    resources_path = Path(resources_dir)
    if not resources_path.exists():
        print(f"Error: Resources directory not found: {resources_dir}")
        return {}, []

    patients = {}       # patient_id → resource dict
    instances = []      # [(filename, resource), …]
    skipped_count = 0
    error_count = 0

    # Collect all JSON files: primary dir first, then extra dir (if provided).
    all_json_files = sorted(resources_path.glob("*.json"))
    if extra_resources_dir:
        extra_path = Path(extra_resources_dir)
        if extra_path.exists():
            extra_files = sorted(extra_path.glob("*.json"))
            print(f"Scanning {len(all_json_files)} file(s) in '{resources_dir}' "
                  f"+ {len(extra_files)} file(s) in '{extra_resources_dir}'...\n")
            all_json_files = all_json_files + extra_files
        else:
            print(f"Warning: Extra resources directory not found: {extra_resources_dir}")
            print(f"Scanning {len(all_json_files)} file(s) in '{resources_dir}'...\n")
    else:
        print(f"Scanning {len(all_json_files)} files...\n")

    # --- Pass 1: discover all Patient resources ---
    print("Pass 1 - discovering Patient resources...")
    for json_file in all_json_files:
        resource = load_fhir_resource(json_file)
        if not resource:
            error_count += 1
            continue

        resource_type = resource.get('resourceType')

        if should_skip_resource(resource_type):
            skipped_count += 1
            continue

        if resource_type == 'Patient':
            patient_id = resource.get('id')
            patient_name = resource.get('name', [{}])[0].get('text', patient_id)
            patients[patient_id] = resource
            print(f"  Found Patient: {patient_name} ({patient_id})")
        else:
            instances.append((json_file.name, resource))

    print(f"\n  {len(patients)} Patient resource(s) found")
    print(f"  {len(instances)} instance resource(s) to group")
    print(f"  {skipped_count} definition resource(s) skipped")
    if error_count:
        print(f"  {error_count} file(s) could not be loaded")

    return patients, instances


def create_shared_bundle(ungrouped_resources):
    """Create a Bundle resource containing all non-patient-linked resources.

    These are resources such as Practitioner, PractitionerRole, and
    Organization that are referenced by patient-linked resources but do not
    themselves carry a direct Patient reference.
    """
    bundle = {
        "resourceType": "Bundle",
        "id": "SharedResourcesBundle",
        "meta": {
            "profile": [
                "http://hl7.org/fhir/StructureDefinition/Bundle"
            ],
            "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "tag": [
                {
                    "system": f"{BUNDLE_SYSTEM_BASE}/CodeSystem/bundle-type",
                    "code": "shared-data",
                    "display": "Shared Resources Bundle"
                }
            ]
        },
        "identifier": {
            "system": f"{BUNDLE_SYSTEM_BASE}/NamingSystem/shared-bundle",
            "value": "SharedResourcesBundle"
        },
        "type": "transaction",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "entry": []
    }

    resource_types = {}
    sorted_resources = sorted(
        ungrouped_resources,
        key=lambda r: (r.get('resourceType', ''), r.get('id', ''))
    )

    for resource in sorted_resources:
        entry = create_bundle_entry(resource)
        if entry:
            bundle["entry"].append(entry)
            res_type = resource.get('resourceType', 'Unknown')
            resource_types[res_type] = resource_types.get(res_type, 0) + 1

    return bundle, {
        'total_resources': len(sorted_resources),
        'resource_types': resource_types
    }


def group_resources_by_patient(patients, instances):
    """Group instance resources by the Patient(s) they reference.

    Args:
        patients:  dict of patient_id → Patient resource
        instances: list of (filename, resource) tuples

    Returns:
        groups:    dict of patient_id → list of associated resources
        ungrouped: list of (filename, resource) tuples with no patient reference
    """
    known_patient_ids = set(patients.keys())
    groups = {pid: [] for pid in known_patient_ids}
    ungrouped = []

    print("\nPass 2 - grouping resources by Patient reference...")
    for filename, resource in instances:
        referenced_ids = find_patient_references(resource) & known_patient_ids

        if referenced_ids:
            for pid in referenced_ids:
                groups[pid].append(resource)
            ref_list = ', '.join(sorted(referenced_ids))
            print(f"  {filename} -> {ref_list}")
        else:
            ungrouped.append((filename, resource))
            print(f"  {filename} -> (no patient reference)")

    return groups, ungrouped


def generate_patient_bundles(resources_dir, output_dir, extra_resources_dir=None):
    """Generate Bundle resources for each patient and one shared resources bundle."""

    print("IKNL PZP FHIR R4 Patient Bundle Generator")
    print("=" * 50)
    print(f"Resources directory:       {resources_dir}")
    if extra_resources_dir:
        print(f"Extra resources directory: {extra_resources_dir}")
    print(f"Output directory:          {output_dir}")
    print()

    # Discover patients and load all instance resources
    patients, instances = discover_patients_and_resources(resources_dir, extra_resources_dir)

    if not patients:
        print("\nNo Patient resources found — nothing to bundle.")
        return False

    # Group non-Patient resources by referenced patient
    groups, ungrouped = group_resources_by_patient(patients, instances)

    if ungrouped:
        print(f"\n{len(ungrouped)} resource(s) not associated with any patient "
              f"(will go into shared bundle):")
        for filename, resource in ungrouped:
            print(f"    {filename} ({resource.get('resourceType', 'Unknown')})")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate one bundle per patient
    bundles_created = 0

    for patient_id, patient_resource in patients.items():
        associated = groups.get(patient_id, [])
        patient_name = patient_resource.get('name', [{}])[0].get('text', patient_id)
        print(f"\nGenerating bundle for: {patient_name} ({patient_id})")
        print(f"  Associated resources: {len(associated)}")

        result = create_patient_bundle(patient_id, patient_resource, associated)

        if result:
            bundle, metadata = result
            bundle_filename = f"{patient_id}-PatientBundle.json"
            bundle_path = output_path / bundle_filename

            try:
                with open(bundle_path, 'w', encoding='utf-8') as f:
                    json.dump(bundle, f, indent=2, ensure_ascii=False)

                print(f"  Created: {bundle_filename}")
                print(f"  Total resources in bundle: {metadata['total_resources']}")
                print(f"  Resource types: {', '.join(f'{k}({v})' for k, v in sorted(metadata['resource_types'].items()))}")
                bundles_created += 1

            except IOError as e:
                print(f"  Error writing bundle: {e}")
        else:
            print(f"  Failed to create bundle for {patient_id}")

    # Generate shared resources bundle for ungrouped resources
    if ungrouped:
        ungrouped_resources = [resource for _, resource in ungrouped]
        print(f"\nGenerating shared resources bundle ({len(ungrouped_resources)} resource(s))...")
        bundle, metadata = create_shared_bundle(ungrouped_resources)
        bundle_filename = "SharedResourcesBundle.json"
        bundle_path = output_path / bundle_filename

        try:
            with open(bundle_path, 'w', encoding='utf-8') as f:
                json.dump(bundle, f, indent=2, ensure_ascii=False)

            print(f"  Created: {bundle_filename}")
            print(f"  Total resources in bundle: {metadata['total_resources']}")
            print(f"  Resource types: {', '.join(f'{k}({v})' for k, v in sorted(metadata['resource_types'].items()))}")
            bundles_created += 1

        except IOError as e:
            print(f"  Error writing shared bundle: {e}")

    print(f"\n{bundles_created} bundle(s) created successfully!")
    return bundles_created > 0


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(
        description="Generates FHIR Bundle (transaction) resources per patient from compiled FSH output.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--resources-dir', default=DEFAULT_RESOURCES_DIR,
        help=f"Directory containing compiled FHIR JSON resources.\n(default: '{DEFAULT_RESOURCES_DIR}')"
    )
    parser.add_argument(
        '--extra-resources-dir', default=DEFAULT_EXTRA_RESOURCES_DIR,
        help=f"Additional directory with instance resources (e.g. QuestionnaireResponses).\n"
             f"Pass an empty string to disable.\n(default: '{DEFAULT_EXTRA_RESOURCES_DIR}')"
    )
    parser.add_argument(
        '--output-dir', default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for the generated Bundle files.\n(default: '{DEFAULT_OUTPUT_DIR}')"
    )
    args = parser.parse_args()

    # Resolve relative paths from the project root (parent of util/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    resources_dir = project_root / args.resources_dir
    output_dir = project_root / args.output_dir
    extra_resources_dir = (project_root / args.extra_resources_dir) if args.extra_resources_dir else None

    success = generate_patient_bundles(resources_dir, output_dir, extra_resources_dir)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())