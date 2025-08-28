"""
FHIR R4 to STU3 Procedure Transformer

This module handles the transformation of Procedure resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/Procedure4to3

Author: AI Assistant
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class ProcedureTransformer(BaseTransformer):
    """Transforms Procedure resources from R4 to STU3 format."""
    
    # EventStatus concept map from the FHIR StructureMap
    EVENT_STATUS_MAP = {
        "entered-in-error": "entered-in-error",
        "in-progress": "in-progress", 
        "on-hold": "suspended",
        "aborted": "stopped",
        "completed": "completed",
        "preparation": "preparation",
        "stopped": "aborted",
        "suspended": "suspended",
        "unknown": "unknown"
    }
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Procedure"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a single Procedure resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming Procedure resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'Procedure'
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
            # Apply Procedure-specific transformations
            self._transform_status_and_not_done(r4_resource, stu3_resource)
            self._transform_encounter_to_context(r4_resource, stu3_resource)
            self._transform_extensions(r4_resource, stu3_resource)
            self._transform_performer(r4_resource, stu3_resource)
            self._transform_focal_device(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            self._transform_body_site_extensions(stu3_resource)
            self._add_consultation_category_for_acp(stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed Procedure: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming Procedure {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_status_and_not_done(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform status field with special handling for 'not-done' status."""
        
        r4_status = r4_resource.get("status")
        if not r4_status:
            return
            
        # Special handling for 'not-done' status
        if r4_status == "not-done":
            # Map to 'suspended' and set notDone = true
            stu3_resource["status"] = "suspended"
            stu3_resource["notDone"] = True
            
            # Transform statusReason to notDoneReason for 'not-done' status
            if "statusReason" in r4_resource:
                stu3_resource["notDoneReason"] = r4_resource["statusReason"]
                
        else:
            # Use EventStatus concept map for other statuses
            mapped_status = self.EVENT_STATUS_MAP.get(r4_status, r4_status)
            stu3_resource["status"] = mapped_status
    
    def _transform_encounter_to_context(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform encounter field to context field."""
        
        if "encounter" in r4_resource:
            stu3_resource["context"] = r4_resource["encounter"]
    
    def _transform_extensions(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform extensions with URL mappings from R4 to STU3."""
        
        if "extension" not in r4_resource:
            return
            
        stu3_extensions = []
        
        # Extension URL mappings
        extension_url_mappings = {
            "http://nictiz.nl/fhir/StructureDefinition/ext-Procedure.ProcedureMethod": 
                "http://hl7.org/fhir/StructureDefinition/procedure-method"
        }
        
        for r4_extension in r4_resource["extension"]:
            stu3_extension = r4_extension.copy()
            
            # Transform extension URL if mapping exists
            original_url = r4_extension.get("url")
            if original_url in extension_url_mappings:
                stu3_extension["url"] = extension_url_mappings[original_url]
                logger.info(f"Mapped extension URL: {original_url} -> {stu3_extension['url']}")
            
            stu3_extensions.append(stu3_extension)
        
        if stu3_extensions:
            stu3_resource["extension"] = stu3_extensions
    
    def _transform_performer(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform performer array with function->role mapping."""
        
        if "performer" not in r4_resource:
            return
            
        stu3_performers = []
        for r4_performer in r4_resource["performer"]:
            stu3_performer = {}
            
            # Map function to role
            if "function" in r4_performer:
                stu3_performer["role"] = r4_performer["function"]
                
            # Direct mappings
            for field in ["actor", "onBehalfOf"]:
                if field in r4_performer:
                    stu3_performer[field] = r4_performer[field]
            
            stu3_performers.append(stu3_performer)
        
        if stu3_performers:
            stu3_resource["performer"] = stu3_performers
    
    def _transform_focal_device(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform focalDevice array (direct mapping for this resource)."""
        
        if "focalDevice" in r4_resource:
            # focalDevice structure is the same in both versions
            stu3_resource["focalDevice"] = r4_resource["focalDevice"]
    
    def _transform_body_site_extensions(self, stu3_resource: Dict[str, Any]) -> None:
        """
        Transform bodySite extensions from R4 to STU3.
        
        Changes extension URL from:
        http://nictiz.nl/fhir/StructureDefinition/ext-AnatomicalLocation.Laterality
        to:
        http://nictiz.nl/fhir/StructureDefinition/BodySite-Qualifier
        """
        if 'bodySite' in stu3_resource:
            # Handle both single bodySite and array of bodySites
            body_sites = stu3_resource['bodySite'] if isinstance(stu3_resource['bodySite'], list) else [stu3_resource['bodySite']]
            
            for body_site in body_sites:
                if 'extension' in body_site:
                    for extension in body_site['extension']:
                        if extension.get('url') == 'http://nictiz.nl/fhir/StructureDefinition/ext-AnatomicalLocation.Laterality':
                            extension['url'] = 'http://nictiz.nl/fhir/StructureDefinition/BodySite-Qualifier'
                            logger.debug(f"Transformed bodySite extension URL: ext-AnatomicalLocation.Laterality -> BodySite-Qualifier")
    
    def _add_consultation_category_for_acp(self, stu3_resource: Dict[str, Any]) -> None:
        """
        Add consultation category when the procedure code is "Advance care planning (procedure)".
        
        When code.coding contains SNOMED code "713603004" (Advance care planning (procedure)),
        automatically populate category with SNOMED code "11429006" (Consultation (procedure)).
        """
        # Check if the procedure has the ACP code
        if 'code' in stu3_resource and 'coding' in stu3_resource['code']:
            has_acp_code = False
            
            for coding in stu3_resource['code']['coding']:
                if (coding.get('code') == '713603004' and 
                    coding.get('system') == 'http://snomed.info/sct'):
                    has_acp_code = True
                    break
            
            if has_acp_code:
                # Only add category if it doesn't already exist or is empty
                if 'category' not in stu3_resource or not stu3_resource['category']:
                    consultation_category = {
                        "coding": [
                            {
                                "code": "11429006",
                                "system": "http://snomed.info/sct",
                                "display": "Consultation (procedure)"
                            }
                        ]
                    }
                    stu3_resource['category'] = consultation_category
                    logger.debug(f"Added consultation category for ACP procedure")
                else:
                    # Category already exists, check if it needs the consultation coding
                    category = stu3_resource['category']
                    if 'coding' in category:
                        # Check if consultation code already exists
                        has_consultation_code = any(
                            coding.get('code') == '11429006' and 
                            coding.get('system') == 'http://snomed.info/sct'
                            for coding in category['coding']
                        )
                        
                        if not has_consultation_code:
                            # Add consultation coding to existing category
                            category['coding'].append({
                                "code": "11429006",
                                "system": "http://snomed.info/sct",
                                "display": "Consultation (procedure)"
                            })
                            logger.debug(f"Added consultation coding to existing category for ACP procedure")
                    else:
                        # Category exists but has no coding array
                        category['coding'] = [
                            {
                                "code": "11429006",
                                "system": "http://snomed.info/sct",
                                "display": "Consultation (procedure)"
                            }
                        ]
                        logger.debug(f"Added consultation coding array to existing category for ACP procedure")
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "instantiatesCanonical", 
            "instantiatesUri",
            "basedOn",
            "partOf",
            "category",
            "code",
            "subject",
            "performed",
            "recorder", 
            "asserter",
            "location",
            "reasonCode",
            "reasonReference",
            "bodySite",
            "outcome",
            "report",
            "complication",
            "complicationDetail",
            "followUp",
            "note",
            "usedReference",
            "usedCode"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "Procedure",
            "base_mapping": "http://hl7.org/fhir/StructureMap/Procedure4to3",
            "key_transformations": {
                "status": "Uses EventStatus concept map, special handling for 'not-done'",
                "encounter": "Mapped to 'context' field in STU3",
                "performer.function": "Mapped to 'performer.role' in STU3",
                "statusReason": "Mapped to 'notDoneReason' when status='not-done'",
                "notDone": "Set to true when R4 status='not-done'",
                "extension.url": "Extension URLs mapped from Nictiz R4 to HL7 STU3",
                "Reference.type": "Removed from all Reference objects (R4-specific)",
                "category": "Auto-populated with 'Consultation (procedure)' for ACP procedures"
            },
            "extension_mappings": {
                "http://nictiz.nl/fhir/StructureDefinition/ext-Procedure.ProcedureMethod": 
                    "http://hl7.org/fhir/StructureDefinition/procedure-method"
            },
            "unsupported_elements": {
                "NL-CM:14.1.11": "Procedure.bodySite.extension:ProcedureLaterality.valueCode",
                "NL-CM:14.1.7": "Procedure.focalDevice.manipulated"
            },
            "direct_mappings": "identifier, instantiatesCanonical, instantiatesUri, basedOn, partOf, category, code, subject, performed, recorder, asserter, location, reasonCode, reasonReference, bodySite, outcome, report, complication, complicationDetail, followUp, note, usedReference, usedCode, focalDevice"
        }


# Mapping Documentation
PROCEDURE_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ instantiatesCanonical   │ instantiatesCanonical   │ Direct mapping                          │
│ instantiatesUri         │ instantiatesUri         │ Direct mapping                          │
│ basedOn                 │ basedOn                 │ Direct mapping                          │
│ partOf                  │ partOf                  │ Direct mapping                          │
│ status                  │ status                  │ EventStatus concept map + special       │
│                         │                         │ handling for 'not-done'                │
│ status='not-done'       │ status='suspended'      │ Special case: set notDone=true          │
│                         │ notDone=true            │                                         │
│ statusReason            │ notDoneReason           │ Only when status='not-done'             │
│ category                │ category                │ Direct mapping                          │
│ code                    │ code                    │ Direct mapping                          │
│ subject                 │ subject                 │ Direct mapping                          │
│ encounter               │ context                 │ Field name change                       │
│ extension               │ extension               │ URL mapping applied                     │
│ performed               │ performed               │ Direct mapping                          │
│ recorder                │ recorder                │ Direct mapping                          │
│ asserter                │ asserter                │ Direct mapping                          │
│ performer               │ performer               │ Transform nested structure              │
│ performer.function      │ performer.role          │ Field name change in nested object     │
│ performer.actor         │ performer.actor         │ Direct mapping                          │
│ performer.onBehalfOf    │ performer.onBehalfOf    │ Direct mapping                          │
│ location                │ location                │ Direct mapping                          │
│ reasonCode              │ reasonCode              │ Direct mapping                          │
│ reasonReference         │ reasonReference         │ Direct mapping                          │
│ bodySite                │ bodySite                │ Direct mapping                          │
│ outcome                 │ outcome                 │ Direct mapping                          │
│ report                  │ report                  │ Direct mapping                          │
│ complication            │ complication            │ Direct mapping                          │
│ complicationDetail      │ complicationDetail      │ Direct mapping                          │
│ followUp                │ followUp                │ Direct mapping                          │
│ note                    │ note                    │ Direct mapping                          │
│ focalDevice             │ focalDevice             │ Direct mapping (structure unchanged)    │
│ usedReference           │ usedReference           │ Direct mapping                          │
│ usedCode                │ usedCode                │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

Extension URL Mappings:
┌──────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────┐
│ R4 Extension URL                                                             │ STU3 Extension URL                                         │
├──────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────┤
│ http://nictiz.nl/fhir/StructureDefinition/ext-Procedure.ProcedureMethod      │ http://hl7.org/fhir/StructureDefinition/procedure-method  │
└──────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────┘

EventStatus Concept Map:
┌─────────────────┬─────────────────┐
│ R4 Status       │ STU3 Status     │
├─────────────────┼─────────────────┤
│ entered-in-error│ entered-in-error│
│ in-progress     │ in-progress     │
│ on-hold         │ suspended       │
│ aborted         │ stopped         │
│ completed       │ completed       │
│ preparation     │ preparation     │
│ stopped         │ aborted         │
│ suspended       │ suspended       │
│ unknown         │ unknown         │
│ not-done        │ suspended       │ (+ notDone=true, statusReason→notDoneReason)
└─────────────────┴─────────────────┘

┌─ UNSUPPORTED ELEMENTS ─────────────────────────────────────────────────────────┐
│ NL-CM Concept                      │ R4 Path                                  │ Reason                                     │
├────────────────────────────────────┼───────────────────────────────────────────┼────────────────────────────────────────────┤
│ NL-CM:14.1.11 ProcedureLaterality  │ Procedure.bodySite.extension:             │ Complex extension not yet supported       │
│                                    │ ProcedureLaterality.valueCode             │ in transformer                            │
│ NL-CM:14.1.7 Device Manipulated    │ Procedure.focalDevice.manipulated        │ Complex nested structure requires         │
│                                    │                                           │ specialized handling                      │
└────────────────────────────────────┴───────────────────────────────────────────┴────────────────────────────────────────────┘

Special Transformations:
1. status='not-done' becomes status='suspended' + notDone=true + statusReason→notDoneReason
2. encounter field becomes context field  
3. performer.function becomes performer.role
4. Extension URLs are mapped from Nictiz R4 to HL7 STU3 equivalents
5. Reference.type fields are removed (R4-specific, not supported in STU3)
6. Auto-population of category field for ACP procedures:
   - When code.coding contains SNOMED "713603004" (Advance care planning (procedure))
   - Automatically adds/updates category with SNOMED "11429006" (Consultation (procedure))
   - Preserves existing category codings if present

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to all reference fields (basedOn, partOf, subject, encounter/context, etc.)
"""

if __name__ == "__main__":
    print("Procedure R4 to STU3 Transformer")
    print("=" * 50)
    print(PROCEDURE_MAPPING_TABLE)
