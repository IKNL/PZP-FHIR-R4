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
