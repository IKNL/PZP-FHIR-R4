"""
FHIR Encounter Resource Transformer: R4 to STU3

This module transforms FHIR Encounter resources from R4 to STU3 format.

=== MAPPING DOCUMENTATION ===

┌─ DIRECT FIELD MAPPINGS ────────────────────────────────────────────────────────┐
│ R4 Source                          │ STU3 Target                               │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Encounter (resourceType)           │ Encounter (resourceType)                  │
│ Encounter.id                       │ Encounter.id                              │
│ Encounter.meta                     │ Encounter.meta                            │
│ Encounter.identifier               │ Encounter.identifier                      │
│ Encounter.status                   │ Encounter.status                          │
│ Encounter.class                    │ Encounter.class                           │
│ Encounter.type                     │ Encounter.type                            │
│ Encounter.subject                  │ Encounter.subject                         │
│ Encounter.period                   │ Encounter.period                          │
│ Encounter.participant              │ Encounter.participant                     │
│ Encounter.serviceProvider          │ Encounter.serviceProvider                 │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ FIELD TRANSFORMATIONS ────────────────────────────────────────────────────────┐
│ R4 Field                           │ STU3 Field                                │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Encounter.classHistory             │ Encounter.statusHistory (mapped)         │
│ Encounter.reasonCode               │ Encounter.reason                          │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ EXCLUDED R4 FIELDS ───────────────────────────────────────────────────────────┐
│ R4 Field                           │ Reason                                    │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Encounter.basedOn                  │ Not supported in STU3                     │
│ Encounter.reasonReference          │ STU3 only supports reasonCode             │
└────────────────────────────────────┴───────────────────────────────────────────┘
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)

class EncounterTransformer(BaseTransformer):
    """FHIR Encounter R4 to STU3 transformer."""
    
    @property
    def resource_type(self) -> str:
        return "Encounter"
    
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform an Encounter resource from R4 to STU3."""
        if not self.can_transform(r4_resource):
            return None
        
        resource_id = r4_resource.get('id', 'unknown')
        self.log_transformation_start(resource_id)
        
        # Create STU3 resource structure
        stu3_resource = {
            'resourceType': 'Encounter'
        }
        
        # Copy basic fields
        self.copy_basic_fields(r4_resource, stu3_resource)
        
        # Transform meta if present
        if 'meta' in r4_resource:
            stu3_resource['meta'] = self.transform_meta(r4_resource['meta'])
            self.log_field_transformation('meta')
        
        # Direct field mappings
        direct_fields = [
            'identifier', 'status', 'class', 'type', 'priority', 'subject',
            'episodeOfCare', 'incomingReferral', 'participant', 'appointment',
            'period', 'length', 'serviceProvider', 'partOf'
        ]
        for field in direct_fields:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
                self.log_field_transformation(field, "direct copy")
        
        # Transform reasonCode -> reason
        if 'reasonCode' in r4_resource:
            stu3_resource['reason'] = r4_resource['reasonCode']
            self.log_field_transformation('reasonCode -> reason')
        
        # Transform classHistory -> statusHistory (if needed)
        if 'classHistory' in r4_resource:
            stu3_resource['statusHistory'] = self.transform_class_history_to_status_history(r4_resource['classHistory'])
            self.log_field_transformation('classHistory -> statusHistory')
        
        # Transform hospitalization
        if 'hospitalization' in r4_resource:
            stu3_resource['hospitalization'] = self.transform_hospitalization(r4_resource['hospitalization'])
            self.log_field_transformation('hospitalization')
        
        # Transform location
        if 'location' in r4_resource:
            stu3_resource['location'] = self.transform_location(r4_resource['location'])
            self.log_field_transformation('location')
        
        # Transform extensions
        if 'extension' in r4_resource:
            stu3_resource['extension'] = self.transform_extensions(r4_resource['extension'])
            self.log_field_transformation('extension')
        
        self.log_transformation_complete(resource_id)
        return stu3_resource
    
    def transform_class_history_to_status_history(self, r4_class_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform classHistory to statusHistory format."""
        stu3_status_history = []
        
        for class_item in r4_class_history:
            status_item = {}
            
            # Map class to status (simplified mapping)
            if 'class' in class_item:
                # This is a simplified mapping - in real scenarios you might need more complex logic
                status_item['status'] = 'in-progress'  # Default mapping
            
            # Copy period
            if 'period' in class_item:
                status_item['period'] = class_item['period']
            
            stu3_status_history.append(status_item)
        
        return stu3_status_history
    
    def transform_hospitalization(self, r4_hospitalization: Dict[str, Any]) -> Dict[str, Any]:
        """Transform hospitalization section."""
        # Hospitalization is generally compatible between R4 and STU3
        return r4_hospitalization.copy()
    
    def transform_location(self, r4_location: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform location section."""
        stu3_location = []
        
        for location in r4_location:
            stu3_loc = {}
            
            # Direct field mappings
            location_fields = ['location', 'status', 'period']
            for field in location_fields:
                if field in location:
                    stu3_loc[field] = location[field]
            
            stu3_location.append(stu3_loc)
        
        return stu3_location
    
    def transform_extensions(self, r4_extensions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform extensions with URL mappings."""
        stu3_extensions = []
        
        for ext in r4_extensions:
            stu3_ext = ext.copy()
            
            # Transform extension URLs
            original_url = ext.get('url', '')
            stu3_url = self.transform_extension_url(original_url)
            
            if stu3_url != original_url:
                stu3_ext['url'] = stu3_url
                logger.debug(f"Transformed extension URL: {original_url} -> {stu3_url}")
            
            stu3_extensions.append(stu3_ext)
        
        return stu3_extensions
    
    def transform_extension_url(self, r4_url: str) -> str:
        """Transform extension URL from R4 to STU3."""
        # Encounter-specific extension URL mappings
        url_mappings = {
            # Add specific mappings as needed
        }
        
        return url_mappings.get(r4_url, r4_url)
    
    def convert_profile_url(self, r4_profile_url: str) -> str:
        """Convert Encounter profile URL from R4 to STU3."""
        # Specific mappings for Encounter profiles
        if 'Encounter' in r4_profile_url:
            return r4_profile_url.replace('/R4/', '/STU3/')
        
        # Default conversion
        return super().convert_profile_url(r4_profile_url)


def main():
    """Main function for standalone execution."""
    import argparse
    import sys
    from pathlib import Path
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Transform FHIR Encounter resources from R4 to STU3')
    parser.add_argument('input_dir', type=Path, help='Input directory containing R4 Encounter resources')
    parser.add_argument('output_dir', type=Path, help='Output directory for STU3 Encounter resources')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.input_dir.exists():
        print(f"Error: Input directory {args.input_dir} does not exist")
        sys.exit(1)
    
    # Create transformer
    transformer = EncounterTransformer()
    
    # Process all JSON files in input directory
    json_files = list(args.input_dir.glob('*.json'))
    if not json_files:
        print(f"No JSON files found in {args.input_dir}")
        sys.exit(1)
    
    print(f"Found {len(json_files)} JSON files to process")
    
    success_count = 0
    for json_file in json_files:
        output_file = args.output_dir / f"converted-{json_file.name}"
        if transformer.transform_file(json_file, output_file):
            success_count += 1
    
    # Print statistics
    stats = transformer.get_stats()
    print(f"\nTransformation complete:")
    print(f"  Processed: {stats['processed']}")
    print(f"  Transformed: {stats['transformed']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")


if __name__ == '__main__':
    main()
