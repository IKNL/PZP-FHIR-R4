"""
FHIR R4 to STU3 RelatedPerson Transformer

This module handles the transformation of RelatedPerson resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/RelatedPerson4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class RelatedPersonTransformer(BaseTransformer):
    """Transforms RelatedPerson resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "RelatedPerson"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single RelatedPerson resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming RelatedPerson resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'RelatedPerson'
        if 'id' in r4_resource:
            stu3_resource['id'] = r4_resource['id']
        
        # 2. Meta (early)
        if 'meta' in r4_resource:
            stu3_resource['meta'] = self.transform_meta(r4_resource['meta'])
            
        # 3. Basic structural elements
        if 'text' in r4_resource:
            stu3_resource['text'] = r4_resource['text']
        if 'contained' in r4_resource:
            stu3_resource['contained'] = r4_resource['contained']
        
        try:
            # Apply RelatedPerson-specific transformations
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally  
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed RelatedPerson: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming RelatedPerson {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "active", 
            "patient",
            "relationship",
            "name",
            "telecom",
            "gender",
            "birthDate",
            "address",
            "photo",
            "period"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "RelatedPerson",
            "base_mapping": "http://hl7.org/fhir/StructureMap/RelatedPerson4to3",
            "key_transformations": {
                "Reference.type": "Removed from all Reference objects (R4-specific)"
            },
            "direct_mappings": "identifier, active, patient, relationship, name, telecom, gender, birthDate, address, photo, period"
        }


# Mapping Documentation
RELATED_PERSON_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ active                  │ active                  │ Direct mapping                          │
│ patient                 │ patient                 │ Direct mapping                          │
│ relationship            │ relationship            │ Direct mapping                          │
│ name                    │ name                    │ Direct mapping                          │
│ telecom                 │ telecom                 │ Direct mapping                          │
│ gender                  │ gender                  │ Direct mapping                          │
│ birthDate               │ birthDate               │ Direct mapping                          │
│ address                 │ address                 │ Direct mapping                          │
│ photo                   │ photo                   │ Direct mapping                          │
│ period                  │ period                  │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

Special Transformations:
1. Reference.type fields are removed (R4-specific, not supported in STU3)
2. All fields map directly between R4 and STU3 - no structural changes

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: patient reference
"""

if __name__ == "__main__":
    print("RelatedPerson R4 to STU3 Transformer")
    print("=" * 50)
    print(RELATED_PERSON_MAPPING_TABLE)
