"""
FHIR R4 to STU3 Patient Transformer

This module handles the transformation of Patient resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/Patient4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class PatientTransformer(BaseTransformer):
    """Transforms Patient resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Patient"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single Patient resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming Patient resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'Patient'
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
            # Apply Patient-specific transformations
            self._transform_extensions(r4_resource, stu3_resource)
            self._transform_contact(r4_resource, stu3_resource)
            self._transform_communication(r4_resource, stu3_resource)
            self._transform_link(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed Patient: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming Patient {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_extensions(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform extensions, preserving specific extensions for STU3."""
        
        if "extension" not in r4_resource:
            return
            
        stu3_extensions = []
        
        # Extensions to preserve as-is
        preserved_extensions = [
            "https://fhir.iknl.nl/fhir/StructureDefinition/ext-LegallyCapable-MedicalTreatmentDecisions"
        ]
        
        for r4_extension in r4_resource["extension"]:
            extension_url = r4_extension.get("url")
            
            # Preserve specific extensions without modification
            if extension_url in preserved_extensions:
                stu3_extensions.append(r4_extension.copy())
                logger.info(f"Preserved extension: {extension_url}")
            else:
                # For other extensions, copy as-is (can be extended later if needed)
                stu3_extensions.append(r4_extension.copy())
        
        if stu3_extensions:
            stu3_resource["extension"] = stu3_extensions
    
    def _transform_contact(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform contact array (direct mapping for Patient)."""
        
        if "contact" not in r4_resource:
            return
            
        # Contact structure is the same in both R4 and STU3
        stu3_resource["contact"] = r4_resource["contact"]
    
    def _transform_communication(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform communication array (direct mapping for Patient)."""
        
        if "communication" not in r4_resource:
            return
            
        # Communication structure is the same in both R4 and STU3
        stu3_resource["communication"] = r4_resource["communication"]
    
    def _transform_link(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform link array (direct mapping for Patient)."""
        
        if "link" not in r4_resource:
            return
            
        # Link structure is the same in both R4 and STU3
        stu3_resource["link"] = r4_resource["link"]
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "active", 
            "name",
            "telecom",
            "gender",
            "birthDate",
            "deceased",
            "address",
            "maritalStatus",
            "multipleBirth",
            "photo",
            "generalPractitioner",
            "managingOrganization"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "Patient",
            "base_mapping": "http://hl7.org/fhir/StructureMap/Patient4to3",
            "key_transformations": {
                "Reference.type": "Removed from all Reference objects (R4-specific)",
                "contact": "Direct mapping - structure unchanged",
                "communication": "Direct mapping - structure unchanged", 
                "link": "Direct mapping - structure unchanged",
                "extension": "Preserves specific extensions as-is"
            },
            "preserved_extensions": {
                "ext-LegallyCapable-MedicalTreatmentDecisions": "https://fhir.iknl.nl/fhir/StructureDefinition/ext-LegallyCapable-MedicalTreatmentDecisions"
            },
            "excluded_features": {
                "patient-animal": "Animal extension mapping not implemented"
            },
            "direct_mappings": "identifier, active, name, telecom, gender, birthDate, deceased, address, maritalStatus, multipleBirth, photo, contact, communication, generalPractitioner, managingOrganization, link"
        }


# Mapping Documentation
PATIENT_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ active                  │ active                  │ Direct mapping                          │
│ name                    │ name                    │ Direct mapping                          │
│ telecom                 │ telecom                 │ Direct mapping                          │
│ gender                  │ gender                  │ Direct mapping                          │
│ birthDate               │ birthDate               │ Direct mapping                          │
│ deceased                │ deceased                │ Direct mapping (boolean/dateTime)      │
│ address                 │ address                 │ Direct mapping                          │
│ maritalStatus           │ maritalStatus           │ Direct mapping                          │
│ multipleBirth           │ multipleBirth           │ Direct mapping (boolean/integer)       │
│ photo                   │ photo                   │ Direct mapping                          │
│ extension               │ extension               │ Preserved as-is for specific extensions│
│ contact                 │ contact                 │ Direct mapping (nested structure)      │
│ contact.relationship    │ contact.relationship    │ Direct mapping                          │
│ contact.name            │ contact.name            │ Direct mapping                          │
│ contact.telecom         │ contact.telecom         │ Direct mapping                          │
│ contact.address         │ contact.address         │ Direct mapping                          │
│ contact.gender          │ contact.gender          │ Direct mapping                          │
│ contact.organization    │ contact.organization    │ Direct mapping                          │
│ contact.period          │ contact.period          │ Direct mapping                          │
│ communication           │ communication           │ Direct mapping (nested structure)      │
│ communication.language  │ communication.language  │ Direct mapping                          │
│ communication.preferred │ communication.preferred │ Direct mapping                          │
│ generalPractitioner     │ generalPractitioner     │ Direct mapping                          │
│ managingOrganization    │ managingOrganization    │ Direct mapping                          │
│ link                    │ link                    │ Direct mapping (nested structure)      │
│ link.other              │ link.other              │ Direct mapping                          │
│ link.type               │ link.type               │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

┌─ PRESERVED EXTENSIONS ─────────────────────────────────────────────────────────┐
│ Extension URL                                                                  │ Notes                                     │
├────────────────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────┤
│ https://fhir.iknl.nl/fhir/StructureDefinition/                                │ Legal capacity for medical treatment     │
│ ext-LegallyCapable-MedicalTreatmentDecisions                                   │ decisions - preserved as-is               │
└────────────────────────────────────────────────────────────────────────────────┴───────────────────────────────────────────┘

┌─ EXCLUDED FEATURES ────────────────────────────────────────────────────────────┐
│ R4 Feature                         │ Reason                                    │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ patient-animal extension           │ Not implemented - veterinary use case    │
│                                    │ not required for current project         │
└────────────────────────────────────┴───────────────────────────────────────────┘

Special Transformations:
1. Reference.type fields are removed (R4-specific, not supported in STU3)
2. All nested structures (contact, communication, link) maintain their format
3. deceased and multipleBirth support both primitive and complex datatypes
4. Animal extension mapping is intentionally excluded
5. ext-LegallyCapable-MedicalTreatmentDecisions extension is preserved as-is

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: generalPractitioner, managingOrganization, link.other, contact.organization
"""

if __name__ == "__main__":
    print("Patient R4 to STU3 Transformer")
    print("=" * 50)
    print(PATIENT_MAPPING_TABLE)
