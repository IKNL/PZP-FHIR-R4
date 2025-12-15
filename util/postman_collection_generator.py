#!/usr/bin/env python3
"""
Script to generate a Postman collection for FHIR resources.

This script scans the fsh-generated/resources folder for FHIR JSON files,
extracts the resourceType and id, and creates PUT requests to localhost:4080
for each resource (excluding StructureDefinition and ValueSet resources).
"""

import json
import os
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
    """Check if a resource type should be skipped."""
    skip_types = {'StructureDefinition', 'ValueSet'}
    return resource_type in skip_types


def create_postman_requests(resource, file_name):
    """Create Postman request items for a FHIR resource (PUT + validation)."""
    resource_type = resource.get('resourceType')
    resource_id = resource.get('id')
    
    if not resource_type or not resource_id:
        print(f"Warning: Missing resourceType or id in {file_name}")
        return []
    
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
                "raw": f"localhost:4080/{resource_type}/{resource_id}",
                "host": [
                    "localhost"
                ],
                "port": "4080",
                "path": [
                    resource_type,
                    resource_id
                ]
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
                "raw": f"localhost:4080/{resource_type}/{resource_id}/$validate",
                "host": [
                    "localhost"
                ],
                "port": "4080",
                "path": [
                    resource_type,
                    resource_id,
                    "$validate"
                ]
            }
        },
        "response": []
    }
    
    return [put_request, validate_request]


def generate_postman_collection(resources_dir):
    """Generate a complete Postman collection from FHIR resources."""
    
    # Initialize collection structure
    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": "IKNL PZP FHIR R4 Resources",
            "description": f"Generated Postman collection for FHIR resources\nGenerated on: {datetime.now().isoformat()}\nExcludes: StructureDefinition and ValueSet resources",
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
        requests = create_postman_requests(resource, json_file.name)
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
    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Go up one level from util folder
    resources_dir = project_root / "fsh-generated" / "resources"
    output_file = script_dir / "IKNL_PZP_FHIR_R4_Collection.postman_collection.json"  # Output in util folder
    
    print("IKNL PZP FHIR R4 Postman Collection Generator")
    print("=" * 50)
    print(f"Resources directory: {resources_dir}")
    print(f"Output file: {output_file}")
    print()
    
    # Generate the collection
    result = generate_postman_collection(resources_dir)
    
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