#!/usr/bin/env python3
"""
postman_collection_generator.py

Generates a Postman collection (v2.1) containing PUT and $validate requests
for every FHIR instance resource produced by SUSHI.  This is a standalone
utility that is **not** part of the IG build pipeline — it is intended to
quickly populate and validate resources on a local (or remote) FHIR server.

Workflow:
  1. Scans the compiled resources directory for FHIR JSON files.
  2. Skips definition / infrastructure resource types (StructureDefinition,
     ValueSet, etc.).
  3. For each remaining instance resource, creates:
       - A PUT request to upload the resource.
       - A GET $validate request to validate it server-side.
  4. Writes the complete Postman collection to a JSON file.

Usage:
  python util/postman_collection_generator.py [--resources-dir DIR]
                                              [--output-file FILE]
                                              [--fhir-base URL]

Examples:
  # Default (localhost:4080)
  python util/postman_collection_generator.py

  # Against a remote FHIR server
  python util/postman_collection_generator.py --fhir-base https://fhir.example.com
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path
import uuid

# =============================================================================
# Configuration — edit these values to match your project / environment
# =============================================================================

# Directory containing the compiled FHIR JSON resources (output of SUSHI).
DEFAULT_RESOURCES_DIR = "fsh-generated/resources"

# Output file path for the generated Postman collection.
DEFAULT_OUTPUT_FILE = "util/IKNL_PZP_FHIR_R4_Collection.postman_collection.json"

# Base URL of the target FHIR server (scheme + host + optional port).
# Used for all generated PUT and $validate requests.
DEFAULT_FHIR_BASE = "http://localhost:4080"

# Human-readable name for the generated Postman collection.
COLLECTION_NAME = "IKNL PZP FHIR R4 Resources"

# FHIR resource types that should be skipped (definition / infrastructure
# resources that are not useful to PUT to a FHIR server).
SKIP_RESOURCE_TYPES = {
    'StructureDefinition',
    'ValueSet',
    'ImplementationGuide',
    'ActorDefinition',
    'SearchParameter',
    'CapabilityStatement',
}


def load_fhir_resource(file_path):
    """Load and parse a FHIR resource JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading {file_path}: {e}")
        return None


def should_skip_resource(resource_type):
    """Check if a resource type should be skipped."""
    return resource_type in SKIP_RESOURCE_TYPES


def create_postman_requests(resource, file_name, fhir_base):
    """Create Postman request items for a FHIR resource (PUT + validation)."""
    resource_type = resource.get('resourceType')
    resource_id = resource.get('id')
    
    if not resource_type or not resource_id:
        print(f"Warning: Missing resourceType or id in {file_name}")
        return []

    # Parse the base URL into host / port / protocol components for Postman
    from urllib.parse import urlparse
    parsed = urlparse(fhir_base if '://' in fhir_base else f'http://{fhir_base}')
    protocol = parsed.scheme or 'http'
    host_parts = (parsed.hostname or 'localhost').split('.')
    port = str(parsed.port) if parsed.port else ('443' if protocol == 'https' else '80')
    base_path = [seg for seg in (parsed.path or '').split('/') if seg]
    
    # Create the PUT request
    put_request = {
        "name": f"PUT {resource_type}/{resource_id}",
        "request": {
            "method": "PUT",
            "header": [
                {
                    "key": "Content-Type",
                    "value": "application/fhir+json",
                    "type": "text"
                }
            ],
            "body": {
                "mode": "raw",
                "raw": json.dumps(resource, indent=2),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            },
            "url": {
                "raw": f"{fhir_base}/{resource_type}/{resource_id}",
                "protocol": protocol,
                "host": host_parts,
                "port": port,
                "path": base_path + [resource_type, resource_id]
            }
        },
        "response": []
    }
    
    # Create the validation request
    validate_request = {
        "name": f"VALIDATE {resource_type}/{resource_id}",
        "request": {
            "method": "GET",
            "header": [
                {
                    "key": "Accept",
                    "value": "application/fhir+json",
                    "type": "text"
                }
            ],
            "url": {
                "raw": f"{fhir_base}/{resource_type}/{resource_id}/$validate",
                "protocol": protocol,
                "host": host_parts,
                "port": port,
                "path": base_path + [resource_type, resource_id, "$validate"]
            }
        },
        "response": []
    }
    
    return [put_request, validate_request]


def generate_postman_collection(resources_dir, fhir_base):
    """Generate a complete Postman collection from FHIR resources."""
    
    skip_list = ', '.join(sorted(SKIP_RESOURCE_TYPES))

    # Initialize collection structure
    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": COLLECTION_NAME,
            "description": (
                f"Generated Postman collection for FHIR resources\n"
                f"Generated on: {datetime.now().isoformat()}\n"
                f"FHIR server: {fhir_base}\n"
                f"Excludes: {skip_list}"
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }
    
    # Process all JSON files in the resources directory
    resources_path = Path(resources_dir)
    if not resources_path.exists():
        print(f"Error: Resources directory not found: {resources_dir}")
        return None
    
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    # Get all JSON files and sort them for consistent ordering
    json_files = sorted(resources_path.glob("*.json"))
    
    for json_file in json_files:
        print(f"Processing: {json_file.name}")
        
        # Load the FHIR resource
        resource = load_fhir_resource(json_file)
        if not resource:
            error_count += 1
            continue
        
        resource_type = resource.get('resourceType')
        
        # Skip certain resource types
        if should_skip_resource(resource_type):
            print(f"  Skipping {resource_type} resource")
            skipped_count += 1
            continue
        
        # Create Postman requests (PUT + validation)
        requests = create_postman_requests(resource, json_file.name, fhir_base)
        if requests:
            for request in requests:
                collection["item"].append(request)
            processed_count += 1
            print(f"  Added: {resource_type}/{resource.get('id', 'unknown')} (PUT + validation)")
        else:
            error_count += 1
    
    print(f"\nProcessing complete:")
    print(f"  Processed: {processed_count} resources")
    print(f"  Skipped: {skipped_count} resources")
    print(f"  Errors: {error_count} resources")
    print(f"  Total files: {len(json_files)}")
    
    return collection, processed_count


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(
        description="Generates a Postman collection (v2.1) with PUT and $validate requests for compiled FHIR instance resources.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--resources-dir', default=DEFAULT_RESOURCES_DIR,
        help=f"Directory containing compiled FHIR JSON resources.\n(default: '{DEFAULT_RESOURCES_DIR}')"
    )
    parser.add_argument(
        '--output-file', default=DEFAULT_OUTPUT_FILE,
        help=f"Output path for the Postman collection JSON file.\n(default: '{DEFAULT_OUTPUT_FILE}')"
    )
    parser.add_argument(
        '--fhir-base', default=DEFAULT_FHIR_BASE,
        help=f"Base URL of the target FHIR server.\n(default: '{DEFAULT_FHIR_BASE}')"
    )
    args = parser.parse_args()

    # Resolve relative paths from the project root (parent of util/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    resources_dir = project_root / args.resources_dir
    output_file = project_root / args.output_file
    fhir_base = args.fhir_base.rstrip('/')
    
    print("IKNL PZP FHIR R4 Postman Collection Generator")
    print("=" * 50)
    print(f"Resources directory: {resources_dir}")
    print(f"Output file: {output_file}")
    print(f"FHIR server: {fhir_base}")
    print()
    
    # Generate the collection
    result = generate_postman_collection(resources_dir, fhir_base)
    
    if not result:
        print("Failed to generate collection")
        return 1
    
    collection, processed_count = result
    
    # Write the collection to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(collection, f, indent=2, ensure_ascii=False)
        print(f"\nPostman collection saved to: {output_file}")
        print(f"Collection contains {len(collection['item'])} requests ({processed_count} resources × 2 operations each)")
        
        # Print summary of resource types
        resource_types = {}
        for item in collection['item']:
            # Extract resource type from the request name (skip validation requests for counting)
            name_parts = item['name'].split(' ')
            if len(name_parts) >= 2 and name_parts[0] == 'PUT':  # Only count PUT requests
                resource_path = name_parts[1]  # e.g., "Patient/F1-ACP-Patient-HendrikHartman"
                resource_type = resource_path.split('/')[0]
                resource_types[resource_type] = resource_types.get(resource_type, 0) + 1
        
        print(f"\nResource types included:")
        for resource_type, count in sorted(resource_types.items()):
            print(f"  {resource_type}: {count} resources")
        
    except IOError as e:
        print(f"Error writing output file: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())