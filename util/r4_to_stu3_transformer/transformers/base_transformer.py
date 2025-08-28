"""
Base transformer class for FHIR R4 to STU3 conversion.
Provides common functionality and interface for all resource-specific transformers.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class BaseTransformer(ABC):
    """
    Abstract base class for FHIR R4 to STU3 resource transformers.
    """
    
    def __init__(self):
        self.stats = {
            'processed': 0,
            'transformed': 0,
            'skipped': 0,
            'errors': 0
        }
    
    @property
    @abstractmethod
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        pass
    
    @abstractmethod
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform a single R4 resource to STU3.
        
        Args:
            r4_resource: The R4 resource as a dictionary
            
        Returns:
            The transformed STU3 resource, or None if transformation should be skipped
        """
        pass
    
    def can_transform(self, resource: Dict[str, Any]) -> bool:
        """
        Check if this transformer can handle the given resource.
        
        Args:
            resource: The FHIR resource to check
            
        Returns:
            True if this transformer can handle the resource
        """
        return resource.get('resourceType') == self.resource_type
    
    def transform_file(self, input_file: Path, output_file: Path) -> bool:
        """
        Transform a single file from R4 to STU3.
        
        Args:
            input_file: Path to the R4 resource file
            output_file: Path where the STU3 resource should be saved
            
        Returns:
            True if transformation was successful, False otherwise
        """
        try:
            logger.debug(f"Processing {input_file}")
            
            with open(input_file, 'r', encoding='utf-8') as f:
                r4_resource = json.load(f)
            
            self.stats['processed'] += 1
            
            if not self.can_transform(r4_resource):
                logger.warning(f"Resource type {r4_resource.get('resourceType')} not supported by {self.__class__.__name__}")
                self.stats['skipped'] += 1
                return False
            
            stu3_resource = self.transform_resource(r4_resource)
            
            if stu3_resource is None:
                logger.info(f"Transformation skipped for {input_file}")
                self.stats['skipped'] += 1
                return False
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stu3_resource, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully transformed {input_file} -> {output_file}")
            self.stats['transformed'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error transforming {input_file}: {e}")
            self.stats['errors'] += 1
            return False
    
    def get_stats(self) -> Dict[str, int]:
        """Return transformation statistics."""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset transformation statistics."""
        for key in self.stats:
            self.stats[key] = 0
    
    def transform(self, r4_resource: Dict[str, Any]) -> Dict[str, Any]:
        """
        Basic transformation that handles common fields and sets up STU3 resource structure.
        
        Args:
            r4_resource: The R4 resource as a dictionary
            
        Returns:
            STU3 resource with basic fields transformed
        """
        stu3_resource = {}
        
        # 1. Resource type (always first)
        stu3_resource['resourceType'] = r4_resource.get('resourceType')
        
        # 2. Resource id
        if 'id' in r4_resource:
            stu3_resource['id'] = r4_resource['id']
        
        # 3. Meta element
        if 'meta' in r4_resource:
            stu3_resource['meta'] = self.transform_meta(r4_resource['meta'])
        
        # 4. Basic FHIR fields
        basic_fields = ['implicitRules', 'language', 'text']
        for field in basic_fields:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
        
        return stu3_resource
    
    # Common utility methods for transformers
    
    def copy_basic_fields(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]):
        """Copy basic FHIR fields that are common between R4 and STU3."""
        basic_fields = ['id', 'meta', 'implicitRules', 'language', 'text']
        
        for field in basic_fields:
            if field in r4_resource:
                stu3_resource[field] = r4_resource[field]
    
    def transform_meta(self, r4_meta: Dict[str, Any]) -> Dict[str, Any]:
        """Transform meta element from R4 to STU3."""
        stu3_meta = {}
        
        # Copy basic meta fields
        meta_fields = ['versionId', 'lastUpdated', 'source']
        for field in meta_fields:
            if field in r4_meta:
                stu3_meta[field] = r4_meta[field]
        
        # Transform profiles - update URLs for STU3
        if 'profile' in r4_meta:
            stu3_profiles = []
            for profile in r4_meta['profile']:
                # Convert R4 profile URLs to STU3 equivalents
                stu3_profile = self.convert_profile_url(profile)
                stu3_profiles.append(stu3_profile)
            stu3_meta['profile'] = stu3_profiles
        
        # Copy tags and security
        for field in ['tag', 'security']:
            if field in r4_meta:
                stu3_meta[field] = r4_meta[field]
        
        return stu3_meta
    
    def convert_profile_url(self, r4_profile_url: str) -> str:
        """Convert R4 profile URL to STU3 equivalent."""
        # Default: just replace R4 with STU3 in the URL
        # Subclasses can override for more specific mappings
        return r4_profile_url.replace('/R4/', '/STU3/').replace('4.0', '3.0')
    
    def transform_identifier(self, r4_identifier: Dict[str, Any]) -> Dict[str, Any]:
        """Transform identifier from R4 to STU3."""
        # Identifiers are generally compatible between versions
        return r4_identifier.copy()
    
    def transform_coding(self, r4_coding: Dict[str, Any]) -> Dict[str, Any]:
        """Transform coding from R4 to STU3."""
        # Codings are generally compatible between versions
        return r4_coding.copy()
    
    def transform_codeable_concept(self, r4_concept: Dict[str, Any]) -> Dict[str, Any]:
        """Transform CodeableConcept from R4 to STU3."""
        stu3_concept = {}
        
        if 'coding' in r4_concept:
            stu3_concept['coding'] = [self.transform_coding(coding) for coding in r4_concept['coding']]
        
        if 'text' in r4_concept:
            stu3_concept['text'] = r4_concept['text']
        
        return stu3_concept
    
    def transform_reference(self, r4_reference: Dict[str, Any]) -> Dict[str, Any]:
        """Transform Reference from R4 to STU3, removing R4-specific fields."""
        stu3_reference = {}
        
        # Copy all fields except 'type' which was added in R4
        for key, value in r4_reference.items():
            if key != 'type':  # 'type' field is R4-specific, not supported in STU3
                stu3_reference[key] = value
        
        return stu3_reference
    
    def clean_references_in_object(self, obj: Any) -> Any:
        """Recursively clean Reference objects in any FHIR object/structure."""
        if isinstance(obj, dict):
            # Check if this looks like a Reference object
            if 'reference' in obj and 'type' in obj:
                # This is a Reference with the R4-specific 'type' field
                return self.transform_reference(obj)
            else:
                # Recursively process all dictionary values
                cleaned_obj = {}
                for key, value in obj.items():
                    cleaned_obj[key] = self.clean_references_in_object(value)
                return cleaned_obj
        elif isinstance(obj, list):
            # Recursively process all list items
            return [self.clean_references_in_object(item) for item in obj]
        else:
            # Primitive values - return as-is
            return obj
    
    def transform_extensions_in_object(self, obj: Any) -> Any:
        """
        Recursively transform extension URLs in any FHIR object/structure.
        
        This method applies global extension URL transformations that need to happen
        across all resource types and all nested structures.
        """
        if isinstance(obj, dict):
            # Check if this is an extension array
            if 'extension' in obj and isinstance(obj['extension'], list):
                # Transform extension URLs in this extension array
                obj['extension'] = self.transform_extension_urls(obj['extension'])
            
            # Recursively process all dictionary values
            transformed_obj = {}
            for key, value in obj.items():
                transformed_obj[key] = self.transform_extensions_in_object(value)
            return transformed_obj
        elif isinstance(obj, list):
            # Recursively process all list items
            return [self.transform_extensions_in_object(item) for item in obj]
        else:
            # Primitive values - return as-is
            return obj
    
    def transform_extension_urls(self, extensions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform extension URLs from R4 to STU3 format.
        
        This method handles global extension URL transformations that apply
        across all resource types.
        """
        transformed_extensions = []
        
        for ext in extensions:
            transformed_ext = ext.copy()
            original_url = ext.get('url', '')
            
            # Apply global URL transformations
            new_url = self.apply_global_extension_url_mappings(original_url)
            
            if new_url != original_url:
                transformed_ext['url'] = new_url
                logger.debug(f"Transformed extension URL: {original_url} -> {new_url}")
            
            # Recursively transform nested extensions
            if 'extension' in transformed_ext and isinstance(transformed_ext['extension'], list):
                transformed_ext['extension'] = self.transform_extension_urls(transformed_ext['extension'])
            
            transformed_extensions.append(transformed_ext)
        
        return transformed_extensions
    
    def apply_global_extension_url_mappings(self, url: str) -> str:
        """
        Apply global extension URL mappings that apply to all resource types.
        
        Args:
            url: The original R4 extension URL
            
        Returns:
            The transformed STU3 extension URL
        """
        # Global extension URL mappings
        global_mappings = {
            'http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification': 
                'http://nictiz.nl/fhir/StructureDefinition/code-specification',
            'http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType':
                'http://nictiz.nl/fhir/StructureDefinition/zib-AddressInformation-AddressType'
        }
        
        return global_mappings.get(url, url)
    
    def log_transformation_start(self, resource_id: str):
        """Log the start of a transformation."""
        logger.debug(f"Starting transformation of {self.resource_type} {resource_id}")
    
    def log_transformation_complete(self, resource_id: str):
        """Log the completion of a transformation."""
        logger.debug(f"Completed transformation of {self.resource_type} {resource_id}")
    
    def log_field_transformation(self, field_name: str, details: str = ""):
        """Log a field transformation."""
        if details:
            logger.debug(f"Transformed field '{field_name}': {details}")
        else:
            logger.debug(f"Transformed field '{field_name}'")
    
    def transform_practitioner_role_reference(self, reference_obj: Dict[str, Any], practitioner_role_resources: Dict[str, Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Transform a PractitionerRole reference to STU3 pattern.
        
        In STU3, PractitionerRole references should be:
        1. Main reference points to the Practitioner (from PractitionerRole.practitioner) 
        2. PractitionerRole reference preserved in practitionerrole-reference extension
        
        Args:
            reference_obj: The reference object that may contain a PractitionerRole reference
            practitioner_role_resources: Optional dict of PractitionerRole resources for resolution
            
        Returns:
            Transformed reference object for STU3
        """
        # Check if this is a PractitionerRole reference
        if reference_obj.get('type') == 'PractitionerRole' or (
            'reference' in reference_obj and 
            reference_obj['reference'].startswith('PractitionerRole/')
        ):
            # Extract PractitionerRole reference info
            practitioner_role_ref = reference_obj.get('reference', '')
            practitioner_role_display = reference_obj.get('display', '')
            
            # Create the STU3 reference structure
            stu3_reference = {}
            
            # Try to resolve the PractitionerRole to get the Practitioner reference
            practitioner_ref = None
            practitioner_display = None
            
            if practitioner_role_resources and practitioner_role_ref:
                # Extract the PractitionerRole ID
                practitioner_role_id = practitioner_role_ref.replace('PractitionerRole/', '')
                practitioner_role_resource = practitioner_role_resources.get(practitioner_role_id)
                
                if practitioner_role_resource and 'practitioner' in practitioner_role_resource:
                    practitioner_data = practitioner_role_resource['practitioner']
                    practitioner_ref = practitioner_data.get('reference')
                    practitioner_display = practitioner_data.get('display')
            
            # Set the main reference to Practitioner if available, otherwise keep original
            if practitioner_ref:
                stu3_reference['reference'] = practitioner_ref
                if practitioner_display:
                    stu3_reference['display'] = practitioner_display
            else:
                # Fallback: keep original reference but log warning
                logger.warning(f"Could not resolve PractitionerRole reference {practitioner_role_ref} to Practitioner")
                stu3_reference['reference'] = practitioner_role_ref
                if practitioner_role_display:
                    stu3_reference['display'] = practitioner_role_display
            
            # Add the PractitionerRole reference as an extension
            practitioner_role_extension = {
                'url': 'http://nictiz.nl/fhir/StructureDefinition/practitionerrole-reference',
                'valueReference': {
                    'reference': practitioner_role_ref
                }
            }
            if practitioner_role_display:
                practitioner_role_extension['valueReference']['display'] = practitioner_role_display
            
            stu3_reference['extension'] = [practitioner_role_extension]
            
            return stu3_reference
        else:
            # Not a PractitionerRole reference, just clean normally
            return self.transform_reference(reference_obj)
    
    def process_practitioner_role_references_in_object(self, obj: Any, practitioner_role_resources: Dict[str, Dict[str, Any]] = None) -> Any:
        """
        Recursively process PractitionerRole references in any FHIR object/structure.
        
        Args:
            obj: The object to process
            practitioner_role_resources: Optional dict of PractitionerRole resources for resolution
            
        Returns:
            Processed object with PractitionerRole references transformed
        """
        if isinstance(obj, dict):
            # Check if this looks like a Reference object with PractitionerRole
            if 'reference' in obj and (
                obj.get('type') == 'PractitionerRole' or
                (isinstance(obj.get('reference'), str) and obj['reference'].startswith('PractitionerRole/'))
            ):
                return self.transform_practitioner_role_reference(obj, practitioner_role_resources)
            else:
                # Recursively process all dictionary values
                processed_obj = {}
                for key, value in obj.items():
                    processed_obj[key] = self.process_practitioner_role_references_in_object(value, practitioner_role_resources)
                return processed_obj
        elif isinstance(obj, list):
            # Recursively process all list items
            return [self.process_practitioner_role_references_in_object(item, practitioner_role_resources) for item in obj]
        else:
            # Primitive values - return as-is
            return obj
