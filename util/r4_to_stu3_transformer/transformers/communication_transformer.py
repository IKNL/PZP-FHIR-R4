"""
FHIR R4 to STU3 Communication Transformer

This module handles the transformation of Communication resources from FHIR R4 to STU3,
implementing the mappings defined in the FHIR StructureMap:
http://hl7.org/fhir/StructureMap/Communication4to3

Author: AI Assistant  
Date: 2025-08-27
"""

import json
import logging
from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)


class CommunicationTransformer(BaseTransformer):
    """Transforms Communication resources from R4 to STU3 format."""
    
    def __init__(self):
        super().__init__()
        
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Communication"
        
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a single Communication resource from R4 to STU3."""
        
        if not self.can_transform(r4_resource):
            return None
            
        logger.info(f"Transforming Communication resource: {r4_resource.get('id', 'unknown')}")
        
        # Create STU3 resource structure
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'Communication'
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
            # Apply Communication-specific transformations
            self._transform_instantiates_canonical(r4_resource, stu3_resource)
            self._transform_status_and_not_done(r4_resource, stu3_resource)
            self._transform_encounter_to_context(r4_resource, stu3_resource)
            self._transform_topic_extension(r4_resource, stu3_resource)
            self._transform_payload(r4_resource, stu3_resource)
            self._copy_direct_mappings(r4_resource, stu3_resource)
            
            # Clean all Reference objects to remove R4-specific 'type' fields
            stu3_resource = self.clean_references_in_object(stu3_resource)
            
            # Transform extension URLs globally
            stu3_resource = self.transform_extensions_in_object(stu3_resource)
            
            logger.info(f"Successfully transformed Communication: {stu3_resource.get('id')}")
            return stu3_resource
            
        except Exception as e:
            logger.error(f"Error transforming Communication {r4_resource.get('id', 'unknown')}: {str(e)}")
            return None
    
    def _transform_instantiates_canonical(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform instantiatesCanonical to definition field."""
        
        if "instantiatesCanonical" in r4_resource:
            stu3_resource["definition"] = r4_resource["instantiatesCanonical"]
    
    def _transform_status_and_not_done(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform status field with special handling for 'not-done' status."""
        
        r4_status = r4_resource.get("status")
        if not r4_status:
            return
            
        # Special handling for 'not-done' status
        if r4_status == "not-done":
            # Map to 'completed' and set notDone = true (with original status value)
            stu3_resource["status"] = "completed"
            stu3_resource["notDone"] = r4_status  # Store original 'not-done' value
            
            # Transform statusReason to notDoneReason for 'not-done' status
            if "statusReason" in r4_resource:
                stu3_resource["notDoneReason"] = r4_resource["statusReason"]
                
        else:
            # Direct mapping for other statuses
            stu3_resource["status"] = r4_status
    
    def _transform_encounter_to_context(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform encounter field to context field."""
        
        if "encounter" in r4_resource:
            stu3_resource["context"] = r4_resource["encounter"]
    
    def _transform_topic_extension(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform topic extension to direct topic field."""
        
        if "extension" not in r4_resource:
            return
            
        topic_extension_url = "http://hl7.org/fhir/3.0/StructureDefinition/extension-Communication.topic"
        
        for extension in r4_resource["extension"]:
            if extension.get("url") == topic_extension_url:
                # Extract value from extension and map to topic field
                if "value" in extension:
                    stu3_resource["topic"] = extension["value"]
                elif "valueReference" in extension:
                    stu3_resource["topic"] = extension["valueReference"] 
                elif "valueCodeableConcept" in extension:
                    stu3_resource["topic"] = extension["valueCodeableConcept"]
                # Handle other value types as needed
                break
    
    def _transform_payload(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Transform payload array with polymorphic content handling."""
        
        if "payload" not in r4_resource:
            return
            
        stu3_payloads = []
        
        for r4_payload in r4_resource["payload"]:
            stu3_payload = {}
            
            # Handle polymorphic content field
            if "contentString" in r4_payload:
                stu3_payload["contentString"] = r4_payload["contentString"]
            elif "contentAttachment" in r4_payload:
                stu3_payload["contentAttachment"] = r4_payload["contentAttachment"]
            elif "contentReference" in r4_payload:
                stu3_payload["contentReference"] = r4_payload["contentReference"]
            elif "content" in r4_payload:
                # Direct content field (less common)
                stu3_payload["content"] = r4_payload["content"]
            
            # Copy any other payload fields
            for field in r4_payload:
                if field not in ["contentString", "contentAttachment", "contentReference", "content"]:
                    stu3_payload[field] = r4_payload[field]
            
            stu3_payloads.append(stu3_payload)
        
        if stu3_payloads:
            stu3_resource["payload"] = stu3_payloads
    
    def _copy_direct_mappings(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """Copy fields that map directly between R4 and STU3."""
        
        direct_mappings = [
            "identifier",
            "basedOn",
            "partOf",
            "category",
            "medium",
            "subject",
            "recipient",
            "sent",
            "received",
            "sender",
            "reasonCode",
            "reasonReference",
            "note"
        ]
        
        for field in direct_mappings:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def get_mapping_info(self) -> Dict[str, str]:
        """Return mapping information for documentation."""
        return {
            "resource_type": "Communication",
            "base_mapping": "http://hl7.org/fhir/StructureMap/Communication4to3",
            "key_transformations": {
                "instantiatesCanonical": "Mapped to 'definition' field in STU3",
                "status": "Special handling for 'not-done' status",
                "encounter": "Mapped to 'context' field in STU3",
                "extension.topic": "Topic extension mapped to direct 'topic' field",
                "payload.content": "Polymorphic content handling (string/Attachment/Reference)",
                "Reference.type": "Removed from all Reference objects (R4-specific)"
            },
            "polymorphic_fields": {
                "payload.content": "Supports string, Attachment, Reference"
            },
            "direct_mappings": "identifier, basedOn, partOf, category, medium, subject, recipient, sent, received, sender, reasonCode, reasonReference, note"
        }


# Mapping Documentation
COMMUNICATION_MAPPING_TABLE = """
┌─────────────────────────┬─────────────────────────┬─────────────────────────────────────────┐
│ R4 Field                │ STU3 Field              │ Transformation Notes                    │
├─────────────────────────┼─────────────────────────┼─────────────────────────────────────────┤
│ identifier              │ identifier              │ Direct mapping                          │
│ instantiatesCanonical   │ definition              │ Field name change                       │
│ basedOn                 │ basedOn                 │ Direct mapping                          │
│ partOf                  │ partOf                  │ Direct mapping                          │
│ status                  │ status                  │ Direct mapping (except 'not-done')     │
│ status='not-done'       │ status='completed'      │ Special case: set notDone=original     │
│                         │ notDone='not-done'      │ value, map statusReason               │
│ statusReason            │ notDoneReason           │ Only when status='not-done'             │
│ category                │ category                │ Direct mapping                          │
│ medium                  │ medium                  │ Direct mapping                          │
│ subject                 │ subject                 │ Direct mapping                          │
│ recipient               │ recipient               │ Direct mapping                          │
│ extension.topic         │ topic                   │ Extension value mapped to direct field  │
│ encounter               │ context                 │ Field name change                       │
│ sent                    │ sent                    │ Direct mapping                          │
│ received                │ received                │ Direct mapping                          │
│ sender                  │ sender                  │ Direct mapping                          │
│ reasonCode              │ reasonCode              │ Direct mapping                          │
│ reasonReference         │ reasonReference         │ Direct mapping                          │
│ payload                 │ payload                 │ Polymorphic content mapping             │
│ payload.contentString   │ payload.contentString   │ Direct mapping                          │
│ payload.contentAttachment│ payload.contentAttachment│ Direct mapping                         │
│ payload.contentReference│ payload.contentReference│ Direct mapping                          │
│ note                    │ note                    │ Direct mapping                          │
└─────────────────────────┴─────────────────────────┴─────────────────────────────────────────┘

┌─ EXTENSION MAPPINGS ───────────────────────────────────────────────────────────┐
│ R4 Extension URL                                   │ STU3 Field               │
├────────────────────────────────────────────────────┼──────────────────────────┤
│ http://hl7.org/fhir/3.0/StructureDefinition/      │ topic                    │
│   extension-Communication.topic                    │                          │
└────────────────────────────────────────────────────┴──────────────────────────┘

Special Transformations:
1. instantiatesCanonical → definition field name change
2. status='not-done' → status='completed' + notDone=original value + statusReason→notDoneReason
3. encounter → context field name change
4. Extension topic → direct topic field
5. payload.content[x] polymorphic handling (string, Attachment, Reference)
6. Reference.type fields removed (R4-specific)

Reference Datatype Transformation:
- R4 introduced the 'type' field in Reference objects
- STU3 does not support Reference.type
- All Reference objects are automatically cleaned to remove 'type' fields
- This applies to: basedOn, partOf, subject, recipient, sender, reasonReference, payload.contentReference, topic
"""

if __name__ == "__main__":
    print("Communication R4 to STU3 Transformer")
    print("=" * 50)
    print(COMMUNICATION_MAPPING_TABLE)
