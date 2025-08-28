"""
DeviceUseStatement Transformer for FHIR R4 to STU3 conversion.

This transformer handles the conversion of DeviceUseStatement resources from FHIR R4 to STU3,
implementing the mappings defined in the StructureMap:
http://hl7.org/fhir/StructureMap/DeviceUseStatement4to3

Key transformations:
- Extension-based whenUsed field extraction
- Polymorphic timing field (Timing/Period/dateTime)
- reasonCode -> indication field name change
- Reference datatype cleaning
"""

from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer


class DeviceUseStatementTransformer(BaseTransformer):
    """Transforms DeviceUseStatement resources from FHIR R4 to STU3."""
    
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "DeviceUseStatement"
    
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform a DeviceUseStatement resource from R4 to STU3.
        
        Args:
            r4_resource: The R4 DeviceUseStatement resource as a dictionary
            
        Returns:
            The transformed STU3 DeviceUseStatement resource as a dictionary
        """
        # Start with base transformation
        stu3_resource = super().transform(r4_resource)
        
        # Apply direct field mappings
        field_mappings = self.get_field_mappings()
        for r4_field, stu3_field in field_mappings.items():
            if r4_field in r4_resource:
                stu3_resource[stu3_field] = r4_resource[r4_field]
        
        # Transform specific DeviceUseStatement fields
        self._transform_when_used_extension(r4_resource, stu3_resource)
        self._transform_timing_field(r4_resource, stu3_resource)
        self._transform_reason_code(r4_resource, stu3_resource)
        self._transform_body_site_extensions(r4_resource, stu3_resource)
        self._copy_encounter_reference_extension(r4_resource, stu3_resource)
        self._transform_health_professional_extension(r4_resource, stu3_resource)
        
        # Clean references throughout the resource
        stu3_resource = self.clean_references_in_object(stu3_resource)
        
        # Transform extension URLs globally
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        
        return stu3_resource
    
    def _transform_when_used_extension(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Extract whenUsed from extensions.
        
        Looks for extension with URL:
        'http://hl7.org/fhir/3.0/StructureDefinition/extension-DeviceUseStatement.whenUsed'
        
        Maps the extension value to STU3 whenUsed field.
        """
        if 'extension' in r4_resource:
            for extension in r4_resource['extension']:
                if extension.get('url') == 'http://hl7.org/fhir/3.0/StructureDefinition/extension-DeviceUseStatement.whenUsed':
                    if 'value' in extension:
                        stu3_resource['whenUsed'] = extension['value']
                    elif 'valueDateTime' in extension:
                        stu3_resource['whenUsed'] = extension['valueDateTime']
                    elif 'valuePeriod' in extension:
                        stu3_resource['whenUsed'] = extension['valuePeriod']
                    elif 'valueTiming' in extension:
                        stu3_resource['whenUsed'] = extension['valueTiming']
                    # Look for other value[x] patterns
                    for key, value in extension.items():
                        if key.startswith('value') and key != 'value':
                            stu3_resource['whenUsed'] = value
                            break
    
    def _transform_timing_field(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform the polymorphic timing field and timingPeriod.
        
        R4 timing can be:
        - Timing
        - Period  
        - dateTime
        
        R4 also has timingPeriod as a separate field.
        All are supported in STU3 as well, so direct copy.
        """
        if 'timing' in r4_resource:
            # The timing field is polymorphic but doesn't need transformation
            # Just copy it over (base transformer handles reference cleaning if needed)
            stu3_resource['timing'] = r4_resource['timing']
        
        if 'timingPeriod' in r4_resource:
            # The timingPeriod field is also supported in STU3
            stu3_resource['timingPeriod'] = r4_resource['timingPeriod']
    
    def _transform_reason_code(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform reasonCode to indication.
        
        Simple field name change: reasonCode -> indication
        """
        if 'reasonCode' in r4_resource:
            stu3_resource['indication'] = r4_resource['reasonCode']
    
    def _transform_body_site_extensions(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
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
    
    def _copy_encounter_reference_extension(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Copy the ext-EncounterReference extension from R4 to STU3.
        
        This extension is at the root level and should be preserved in STU3.
        Extension URL: https://fhir.iknl.nl/fhir/StructureDefinition/ext-EncounterReference
        """
        if 'extension' in r4_resource:
            encounter_ref_extensions = []
            
            for extension in r4_resource['extension']:
                if extension.get('url') == 'https://fhir.iknl.nl/fhir/StructureDefinition/ext-EncounterReference':
                    encounter_ref_extensions.append(extension)
            
            if encounter_ref_extensions:
                # Ensure extension array exists in STU3 resource
                if 'extension' not in stu3_resource:
                    stu3_resource['extension'] = []
                
                # Add the EncounterReference extensions
                stu3_resource['extension'].extend(encounter_ref_extensions)
    
    def _transform_health_professional_extension(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform the ext-MedicalDevice.HealthProfessional extension from R4 to STU3.
        
        Changes the extension URL from:
        http://nictiz.nl/fhir/StructureDefinition/ext-MedicalDevice.HealthProfessional
        to:
        http://nictiz.nl/fhir/StructureDefinition/zib-MedicalDevice-Practitioner
        """
        if 'extension' in r4_resource:
            health_professional_extensions = []
            
            for extension in r4_resource['extension']:
                if extension.get('url') == 'http://nictiz.nl/fhir/StructureDefinition/ext-MedicalDevice.HealthProfessional':
                    # Create a copy of the extension with the new URL
                    stu3_extension = extension.copy()
                    stu3_extension['url'] = 'http://nictiz.nl/fhir/StructureDefinition/zib-MedicalDevice-Practitioner'
                    health_professional_extensions.append(stu3_extension)
            
            if health_professional_extensions:
                # Ensure extension array exists in STU3 resource
                if 'extension' not in stu3_resource:
                    stu3_resource['extension'] = []
                
                # Add the transformed HealthProfessional extensions
                stu3_resource['extension'].extend(health_professional_extensions)
    
    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get the direct field mappings for DeviceUseStatement transformation.
        
        Returns:
            Dictionary mapping R4 field names to STU3 field names
        """
        return {
            'identifier': 'identifier',
            'status': 'status',
            'subject': 'subject',
            'recordedOn': 'recordedOn',
            'source': 'source',
            'device': 'device',
            'bodySite': 'bodySite',
            'note': 'note'
        }
    
    def get_transformation_summary(self) -> str:
        """
        Get a summary of transformations applied by this transformer.
        
        Returns:
            A string describing the key transformations
        """
        return """
DeviceUseStatement R4 to STU3 Transformations:
+----------------------------------+----------------------------------+----------------------------------+
| R4 Field                         | STU3 Field                       | Transformation                   |
+----------------------------------+----------------------------------+----------------------------------+
| extension[whenUsed]              | whenUsed                         | Extract from extension with URL: |
|                                  |                                  | extension-DeviceUseStatement.    |
|                                  |                                  | whenUsed                         |
+----------------------------------+----------------------------------+----------------------------------+
| timing (Timing/Period/dateTime)  | timing                           | Polymorphic field - direct copy  |
+----------------------------------+----------------------------------+----------------------------------+
| timingPeriod                     | timingPeriod                     | Direct mapping                   |
+----------------------------------+----------------------------------+----------------------------------+
| reasonCode                       | indication                       | Field name change               |
+----------------------------------+----------------------------------+----------------------------------+
| identifier                       | identifier                       | Direct mapping                   |
| status                           | status                           | Direct mapping                   |
| subject                          | subject                          | Direct mapping + reference clean |
| recordedOn                       | recordedOn                       | Direct mapping                   |
| source                           | source                           | Direct mapping + reference clean |
| device                           | device                           | Direct mapping + reference clean |
| bodySite                         | bodySite                         | Direct mapping + extension URL   |
|                                  |                                  | transformation                   |
| note                             | note                             | Direct mapping                   |
+----------------------------------+----------------------------------+----------------------------------+
| extension[ext-EncounterReference]| extension[ext-EncounterReference]| Direct copy of extension         |
+----------------------------------+----------------------------------+----------------------------------+
| extension[ext-MedicalDevice.     | extension[zib-MedicalDevice-     | URL transformation:              |
| HealthProfessional]              | Practitioner]                    | ext-MedicalDevice.HealthProfes-  |
|                                  |                                  | sional -> zib-MedicalDevice-     |
|                                  |                                  | Practitioner                     |
+----------------------------------+----------------------------------+----------------------------------+

Special Cases:
- whenUsed extracted from R4 extension (reverse conversion pattern)
- Polymorphic timing field supports Timing, Period, or dateTime
- timingPeriod field copied directly from R4 to STU3
- Reference cleaning applied to subject, source, device fields
- reasonCode becomes indication in STU3
- ext-EncounterReference extension preserved at root level
- ext-MedicalDevice.HealthProfessional extension URL transformed to STU3 equivalent
- bodySite.extension[ext-AnatomicalLocation.Laterality] URL transformed to BodySite-Qualifier
"""
