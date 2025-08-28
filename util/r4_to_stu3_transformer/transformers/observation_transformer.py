"""
FHIR R4 to STU3 Observation Transformer

This module handles the transformation of Observation resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/Observation4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class ObservationTransformer(BaseTransformer):
    """Transforms Observation resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Observation"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single Observation resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming Observation resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'Observation'
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
            # Apply Observation-specific transformations
            self._transform_encounter_to_context(r4_resource, stu3_resource)
            self._transform_value_polymorphic(r4_resource, stu3_resource)
            self._transform_note_to_comment(r4_resource, stu3_resource)
            self._transform_has_member_and_derived_from(r4_resource, stu3_resource)
            self._transform_extension_based_related(r4_resource, stu3_resource)
            self._transform_reference_range(r4_resource, stu3_resource)
            self._transform_component(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed Observation: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming Observation {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_encounter_to_context(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform encounter field to context field."""
        
        if "encounter" in r4_resource:
            stu3_resource["context"] = r4_resource["encounter"]
    
    def _transform_value_polymorphic(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform polymorphic value[x] field from R4 to STU3."""
        
        # List of all possible value[x] field names
        value_fields = [
            "valueQuantity",
            "valueCodeableConcept", 
            "valueString",
            "valueBoolean",
            "valueRange",
            "valueRatio",
            "valueSampledData",
            "valueTime",
            "valueDateTime",
            "valuePeriod"
        ]
        
        # Find which value[x] field exists and copy it
        for value_field in value_fields:
            if value_field in r4_resource:
                stu3_resource[value_field] = r4_resource[value_field]
                logger.debug(f"Mapped {value_field} to STU3")
                break  # Only one value[x] field should exist
    
    def _transform_note_to_comment(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform first note to comment string (Annotation2string)."""
        
        if "note" in r4_resource and r4_resource["note"]:
            # Take first note and extract text
            first_note = r4_resource["note"][0]
            if isinstance(first_note, dict) and "text" in first_note:
                stu3_resource["comment"] = first_note["text"]
            elif isinstance(first_note, str):
                stu3_resource["comment"] = first_note
    
    def _transform_has_member_and_derived_from(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform hasMember and derivedFrom to related array."""
        
        related_items = []
        
        # Transform hasMember to related with type 'has-member'
        if "hasMember" in r4_resource:
            for member in r4_resource["hasMember"]:
                related_item = {
                    "type": "has-member",
                    "target": member
                }
                related_items.append(related_item)
        
        # Transform derivedFrom to related with type 'derived-from'  
        if "derivedFrom" in r4_resource:
            for derived in r4_resource["derivedFrom"]:
                related_item = {
                    "type": "derived-from",
                    "target": derived
                }
                related_items.append(related_item)
        
        if related_items:
            if "related" not in stu3_resource:
                stu3_resource["related"] = []
            stu3_resource["related"].extend(related_items)
    
    def _transform_extension_based_related(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform R4 extensions to STU3 related array."""
        
        if "extension" not in r4_resource:
            return
            
        # Extension URL to related type mappings
        extension_mappings = {
            "http://hl7.org/fhir/3.0/StructureDefinition/Observation.sequelTo": "sequel-to",
            "http://hl7.org/fhir/3.0/StructureDefinition/Observation.replaces": "replaces", 
            "http://hl7.org/fhir/3.0/StructureDefinition/Observation.qualifiedBy": "qualified-by",
            "http://hl7.org/fhir/3.0/StructureDefinition/Observation.interferedBy": "interfered-by"
        }
        
        related_items = []
        
        for extension in r4_resource["extension"]:
            extension_url = extension.get("url")
            if extension_url in extension_mappings:
                # Extract Reference from extension.valueReference
                if "valueReference" in extension:
                    related_item = {
                        "type": extension_mappings[extension_url],
                        "target": extension["valueReference"]
                    }
                    related_items.append(related_item)
        
        if related_items:
            if "related" not in stu3_resource:
                stu3_resource["related"] = []
            stu3_resource["related"].extend(related_items)
    
    def _transform_reference_range(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform referenceRange array (direct mapping)."""
        
        if "referenceRange" in r4_resource:
            # ReferenceRange structure is the same in both versions
            stu3_resource["referenceRange"] = r4_resource["referenceRange"]
    
    def _transform_component(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform component array with polymorphic value[x] handling."""
        
        if "component" not in r4_resource:
            return
            
        stu3_components = []
        
        for r4_component in r4_resource["component"]:
            stu3_component = {}
            
            # Copy direct fields
            component_direct_fields = [
                "code",
                "dataAbsentReason", 
                "interpretation",
                "referenceRange"
            ]
            
            for field in component_direct_fields:
                if field in r4_component:
                    stu3_component[field] = r4_component[field]
            
            # Handle polymorphic value[x] field in component
            value_fields = [
                "valueQuantity",
                "valueCodeableConcept", 
                "valueString",
                "valueRange",
                "valueRatio",
                "valueSampledData",
                "valueTime",
                "valueDateTime",
                "valuePeriod"
            ]
            
            for value_field in value_fields:
                if value_field in r4_component:
                    stu3_component[value_field] = r4_component[value_field]
                    break
            
            stu3_components.append(stu3_component)
        
        if stu3_components:
            stu3_resource["component"] = stu3_components
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "basedOn",
            "status",
            "category", 
            "code",
            "subject",
            "effective",  # Handles both dateTime and Period
            "issued",
            "performer",
            # value[x] handled separately in _transform_value_polymorphic
            "dataAbsentReason",
            "interpretation",
            "bodySite",
            "method",
            "specimen",
            "device"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "Observation",
            "base_mapping": "http://hl7.org/fhir/StructureMap/Observation4to3",
            "key_transformations": {
                "encounter": "Mapped to 'context' field in STU3",
                "note": "First note.text mapped to 'comment' string in STU3",
                "hasMember": "Mapped to related array with type 'has-member'",
                "derivedFrom": "Mapped to related array with type 'derived-from'",
                "extensions": "Specific extensions mapped to related array",
                "Reference.type": "Removed from all Reference objects (R4-specific)"
            },
            "extension_mappings": {
                "Observation.sequelTo": "related type 'sequel-to'",
                "Observation.replaces": "related type 'replaces'",
                "Observation.qualifiedBy": "related type 'qualified-by'", 
                "Observation.interferedBy": "related type 'interfered-by'"
            },
            "polymorphic_fields": {
                "value[x]": "Supports valueQuantity, valueCodeableConcept, valueString, valueBoolean, valueRange, valueRatio, valueSampledData, valueTime, valueDateTime, valuePeriod",
                "effective[x]": "Supports effectiveDateTime, effectivePeriod"
            },
            "direct_mappings": "identifier, basedOn, status, category, code, subject, effective, issued, performer, dataAbsentReason, interpretation, bodySite, method, specimen, device, referenceRange"
        }


# Mapping Documentation
OBSERVATION_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ basedOn                 │ basedOn                 │ Direct mapping                          │
│ status                  │ status                  │ Direct mapping                          │
│ category                │ category                │ Direct mapping                          │
│ code                    │ code                    │ Direct mapping                          │
│ subject                 │ subject                 │ Direct mapping                          │
│ encounter               │ context                 │ Field name change                       │
│ effective               │ effective               │ Direct mapping (dateTime/Period)       │
│ issued                  │ issued                  │ Direct mapping                          │
│ performer               │ performer               │ Direct mapping                          │
│ value[x]                │ value[x]                │ Polymorphic field mapping               │
│ dataAbsentReason        │ dataAbsentReason        │ Direct mapping                          │
│ interpretation          │ interpretation          │ Direct mapping                          │
│ note[0].text            │ comment                 │ First note text becomes comment string  │
│ bodySite                │ bodySite                │ Direct mapping                          │
│ method                  │ method                  │ Direct mapping                          │
│ specimen                │ specimen                │ Direct mapping                          │
│ device                  │ device                  │ Direct mapping                          │
│ referenceRange          │ referenceRange          │ Direct mapping (nested structure)      │
│ hasMember               │ related                 │ Mapped to related with type='has-member'│
│ derivedFrom             │ related                 │ Mapped to related with type='derived-from'│
│ component               │ component               │ Direct mapping (nested structure)      │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

┌─ EXTENSION MAPPINGS ───────────────────────────────────────────────────────────┐
│ R4 Extension URL                                   │ STU3 related.type            │
├────────────────────────────────────────────────────┼──────────────────────────────┤
│ http://hl7.org/fhir/3.0/StructureDefinition/      │ sequel-to                    │
│   Observation.sequelTo                             │                              │
│ http://hl7.org/fhir/3.0/StructureDefinition/      │ replaces                     │
│   Observation.replaces                             │                              │
│ http://hl7.org/fhir/3.0/StructureDefinition/      │ qualified-by                 │
│   Observation.qualifiedBy                          │                              │
│ http://hl7.org/fhir/3.0/StructureDefinition/      │ interfered-by                │
│   Observation.interferedBy                         │                              │
└────────────────────────────────────────────────────┴──────────────────────────────┘

┌─ POLYMORPHIC VALUE TYPES ──────────────────────────────────────────────────────┐
│ Field: value[x] - Supported Types:                                            │
│   valueQuantity, valueCodeableConcept, valueString, valueBoolean,             │
│   valueRange, valueRatio, valueSampledData, valueTime, valueDateTime,         │
│   valuePeriod                                                                  │
│ Field: effective[x] - Supported Types:                                        │
│   effectiveDateTime, effectivePeriod                                          │
│ Transformation: Direct field mapping - no type conversion needed              │
└────────────────────────────────────────────────────────────────────────────────┘

Complex Transformations:
1. encounter → context field name change
2. note[0].text → comment string (first note only)
3. hasMember → related array with type 'has-member'
4. derivedFrom → related array with type 'derived-from'  
5. Extensions → related array with specific types
6. Reference.type fields removed (R4-specific)

Nested Structures:
- referenceRange: low, high, type, appliesTo, age, text
- component: code, value[x], dataAbsentReason, interpretation, referenceRange
"""

if __name__ == "__main__":
    print("Observation R4 to STU3 Transformer")
    print("=" * 50)
    print(OBSERVATION_MAPPING_TABLE)
