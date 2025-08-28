"""
FHIR R4 to STU3 PractitionerRole Transformer

This module handles the transformation of PractitionerRole resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/PractitionerRole4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class PractitionerRoleTransformer(BaseTransformer):
    """Transforms PractitionerRole resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "PractitionerRole"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single PractitionerRole resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming PractitionerRole resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'PractitionerRole'
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
            # Apply PractitionerRole-specific transformations
            self._transform_available_time(r4_resource, stu3_resource)
            self._transform_not_available(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed PractitionerRole: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming PractitionerRole {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_available_time(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform availableTime array with nested structure mapping."""
        
        if "availableTime" not in r4_resource:
            return
            
        stu3_available_times = []
        
        for r4_available_time in r4_resource["availableTime"]:
            stu3_available_time = {}
            
            # Direct mappings for availableTime fields
            available_time_fields = [
                "daysOfWeek",
                "allDay", 
                "availableStartTime",
                "availableEndTime"
            ]
            
            for field in available_time_fields:
                if field in r4_available_time:
                    stu3_available_time[field] = r4_available_time[field]
            
            stu3_available_times.append(stu3_available_time)
        
        if stu3_available_times:
            stu3_resource["availableTime"] = stu3_available_times
    
    def _transform_not_available(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform notAvailable array with nested structure mapping."""
        
        if "notAvailable" not in r4_resource:
            return
            
        stu3_not_available = []
        
        for r4_not_available in r4_resource["notAvailable"]:
            stu3_not_available_item = {}
            
            # Direct mappings for notAvailable fields
            not_available_fields = [
                "description",
                "during"
            ]
            
            for field in not_available_fields:
                if field in r4_not_available:
                    stu3_not_available_item[field] = r4_not_available[field]
            
            stu3_not_available.append(stu3_not_available_item)
        
        if stu3_not_available:
            stu3_resource["notAvailable"] = stu3_not_available
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "active", 
            "period",
            "practitioner",
            "organization",
            "code",
            "specialty",
            "location",
            "healthcareService",
            "telecom",
            "availabilityExceptions",
            "endpoint"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "PractitionerRole",
            "base_mapping": "http://hl7.org/fhir/StructureMap/PractitionerRole4to3",
            "key_transformations": {
                "availableTime": "Nested structure mapping - preserves internal structure",
                "notAvailable": "Nested structure mapping - preserves internal structure",
                "Reference.type": "Removed from all Reference objects (R4-specific)"
            },
            "nested_mappings": {
                "availableTime": "daysOfWeek, allDay, availableStartTime, availableEndTime",
                "notAvailable": "description, during"
            },
            "direct_mappings": "identifier, active, period, practitioner, organization, code, specialty, location, healthcareService, telecom, availabilityExceptions, endpoint"
        }


# Mapping Documentation
PRACTITIONER_ROLE_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ active                  │ active                  │ Direct mapping                          │
│ period                  │ period                  │ Direct mapping                          │
│ practitioner            │ practitioner            │ Direct mapping                          │
│ organization            │ organization            │ Direct mapping                          │
│ code                    │ code                    │ Direct mapping                          │
│ specialty               │ specialty               │ Direct mapping                          │
│ location                │ location                │ Direct mapping                          │
│ healthcareService       │ healthcareService       │ Direct mapping                          │
│ telecom                 │ telecom                 │ Direct mapping                          │
│ availableTime           │ availableTime           │ Nested structure mapping                │
│ availableTime.daysOfWeek│ availableTime.daysOfWeek│ Direct mapping                          │
│ availableTime.allDay    │ availableTime.allDay    │ Direct mapping                          │
│ availableTime.          │ availableTime.          │ Direct mapping                          │
│   availableStartTime    │   availableStartTime    │                                         │
│ availableTime.          │ availableTime.          │ Direct mapping                          │
│   availableEndTime      │   availableEndTime      │                                         │
│ notAvailable            │ notAvailable            │ Nested structure mapping                │
│ notAvailable.description│ notAvailable.description│ Direct mapping                          │
│ notAvailable.during     │ notAvailable.during     │ Direct mapping                          │
│ availabilityExceptions  │ availabilityExceptions  │ Direct mapping                          │
│ endpoint                │ endpoint                │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

Special Transformations:
1. Reference.type fields are removed (R4-specific, not supported in STU3)
2. availableTime and notAvailable nested structures are preserved
3. All fields map directly between R4 and STU3 - no structural changes

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: practitioner, organization, location, healthcareService, endpoint references
"""

if __name__ == "__main__":
    print("PractitionerRole R4 to STU3 Transformer")
    print("=" * 50)
    print(PRACTITIONER_ROLE_MAPPING_TABLE)
