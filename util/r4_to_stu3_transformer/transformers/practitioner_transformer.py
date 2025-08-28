"""
FHIR R4 to STU3 Practitioner Transformer

This module handles the transformation of Practitioner resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/Practitioner4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class PractitionerTransformer(BaseTransformer):
    """Transforms Practitioner resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Practitioner"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single Practitioner resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming Practitioner resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'Practitioner'
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
            # Apply Practitioner-specific transformations
            self._transform_qualification(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed Practitioner: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming Practitioner {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_qualification(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform qualification array (direct mapping for Practitioner)."""
        
        if "qualification" not in r4_resource:
            return
            
        # Qualification structure is the same in both R4 and STU3
        # Contains: identifier, code, period, issuer
        stu3_resource["qualification"] = r4_resource["qualification"]
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "active", 
            "name",
            "telecom",
            "address",
            "gender",
            "birthDate",
            "photo",
            "communication"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "Practitioner",
            "base_mapping": "http://hl7.org/fhir/StructureMap/Practitioner4to3",
            "key_transformations": {
                "qualification": "Direct mapping - structure unchanged",
                "Reference.type": "Removed from all Reference objects (R4-specific)"
            },
            "direct_mappings": "identifier, active, name, telecom, address, gender, birthDate, photo, qualification, communication"
        }


# Mapping Documentation
PRACTITIONER_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ active                  │ active                  │ Direct mapping                          │
│ name                    │ name                    │ Direct mapping                          │
│ telecom                 │ telecom                 │ Direct mapping                          │
│ address                 │ address                 │ Direct mapping                          │
│ gender                  │ gender                  │ Direct mapping                          │
│ birthDate               │ birthDate               │ Direct mapping                          │
│ photo                   │ photo                   │ Direct mapping                          │
│ qualification           │ qualification           │ Direct mapping (nested structure)      │
│ qualification.identifier│ qualification.identifier│ Direct mapping                          │
│ qualification.code      │ qualification.code      │ Direct mapping                          │
│ qualification.period    │ qualification.period    │ Direct mapping                          │
│ qualification.issuer    │ qualification.issuer    │ Direct mapping                          │
│ communication           │ communication           │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

Special Transformations:
1. Reference.type fields are removed (R4-specific, not supported in STU3)
2. All fields map directly between R4 and STU3 - no structural changes
3. Qualification nested structure maintains its format

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: qualification.issuer references
"""

if __name__ == "__main__":
    print("Practitioner R4 to STU3 Transformer")
    print("=" * 50)
    print(PRACTITIONER_MAPPING_TABLE)
