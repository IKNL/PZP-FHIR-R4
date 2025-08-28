"""
Device Transformer for FHIR R4 to STU3 conversion.

This transformer handles the conversion of Device resources from FHIR R4 to STU3,
implementing the mappings defined in the StructureMap:
http://hl7.org/fhir/StructureMap/Device4to3

Key transformations:
- udiCarrier (R4) -> udi (STU3) with nested field mappings
- modelNumber -> model field name change
- version.value -> version field flattening
- deviceName.name -> udi.name field mapping
- Reference datatype cleaning
"""

from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer


class DeviceTransformer(BaseTransformer):
    """Transforms Device resources from FHIR R4 to STU3."""
    
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Device"
    
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform a Device resource from R4 to STU3.
        
        Args:
            r4_resource: The R4 Device resource as a dictionary
            
        Returns:
            The transformed STU3 Device resource as a dictionary
        """
        # Start with base transformation
        stu3_resource = super().transform(r4_resource)
        
        # Apply direct field mappings
        field_mappings = self.get_field_mappings()
        for r4_field, stu3_field in field_mappings.items():
            if r4_field in r4_resource:
                stu3_resource[stu3_field] = r4_resource[r4_field]
        
        # Transform specific Device fields
        self._transform_udi_carrier(r4_resource, stu3_resource)
        self._transform_model_number(r4_resource, stu3_resource)
        self._transform_version(r4_resource, stu3_resource)
        self._transform_device_name(r4_resource, stu3_resource)
        
        # Clean references throughout the resource
        stu3_resource = self.clean_references_in_object(stu3_resource)
        
        # Transform extension URLs globally
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        
        return stu3_resource
    
    def _transform_udi_carrier(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform udiCarrier from R4 to udi in STU3.
        
        R4 has udiCarrier array with nested structure.
        STU3 has udi object with flattened structure.
        
        Maps:
        - udiCarrier.deviceIdentifier -> udi.deviceIdentifier
        - udiCarrier.jurisdiction -> udi.jurisdiction
        - udiCarrier.carrierHRF -> udi.carrierHRF
        - udiCarrier.carrierAIDC -> udi.carrierAIDC
        - udiCarrier.issuer -> udi.issuer
        - udiCarrier.entryType -> udi.entryType
        """
        if 'udiCarrier' in r4_resource:
            udi_carriers = r4_resource['udiCarrier']
            
            # Take the first udiCarrier element to map to STU3 udi
            # (STU3 udi is not an array, so we can only map one)
            if udi_carriers and len(udi_carriers) > 0:
                first_carrier = udi_carriers[0]
                stu3_udi = {}
                
                # Map the nested fields
                field_mappings = {
                    'deviceIdentifier': 'deviceIdentifier',
                    'jurisdiction': 'jurisdiction', 
                    'carrierHRF': 'carrierHRF',
                    'carrierAIDC': 'carrierAIDC',
                    'issuer': 'issuer',
                    'entryType': 'entryType'
                }
                
                for r4_field, stu3_field in field_mappings.items():
                    if r4_field in first_carrier:
                        stu3_udi[stu3_field] = first_carrier[r4_field]
                
                if stu3_udi:
                    stu3_resource['udi'] = stu3_udi
    
    def _transform_model_number(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform modelNumber to model.
        
        Simple field name change: modelNumber -> model
        """
        if 'modelNumber' in r4_resource:
            stu3_resource['model'] = r4_resource['modelNumber']
    
    def _transform_version(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform version structure.
        
        R4: version[].value
        STU3: version (direct string)
        
        Takes the first version's value.
        """
        if 'version' in r4_resource:
            versions = r4_resource['version']
            
            # Take the first version element
            if versions and len(versions) > 0:
                first_version = versions[0]
                if 'value' in first_version:
                    stu3_resource['version'] = first_version['value']
    
    def _transform_device_name(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform deviceName to udi.name.
        
        R4: deviceName[].name
        STU3: udi.name
        
        Takes the first deviceName's name and adds it to the udi structure.
        """
        if 'deviceName' in r4_resource:
            device_names = r4_resource['deviceName']
            
            # Take the first deviceName element
            if device_names and len(device_names) > 0:
                first_device_name = device_names[0]
                if 'name' in first_device_name:
                    # Ensure udi object exists
                    if 'udi' not in stu3_resource:
                        stu3_resource['udi'] = {}
                    
                    stu3_resource['udi']['name'] = first_device_name['name']
    
    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get the direct field mappings for Device transformation.
        
        Returns:
            Dictionary mapping R4 field names to STU3 field names
        """
        return {
            'identifier': 'identifier',
            'status': 'status',
            'type': 'type',
            'lotNumber': 'lotNumber',
            'manufacturer': 'manufacturer',
            'manufactureDate': 'manufactureDate',
            'expirationDate': 'expirationDate',
            'patient': 'patient',
            'owner': 'owner',
            'contact': 'contact',
            'location': 'location',
            'url': 'url',
            'note': 'note',
            'safety': 'safety'
        }
    
    def get_transformation_summary(self) -> str:
        """
        Get a summary of transformations applied by this transformer.
        
        Returns:
            A string describing the key transformations
        """
        return """
Device R4 to STU3 Transformations:
+----------------------------------+----------------------------------+----------------------------------+
| R4 Field                         | STU3 Field                       | Transformation                   |
+----------------------------------+----------------------------------+----------------------------------+
| udiCarrier[]                     | udi                              | Array to object: take first     |
|   .deviceIdentifier              |   .deviceIdentifier             | element, map nested fields       |
|   .jurisdiction                  |   .jurisdiction                  |                                  |
|   .carrierHRF                    |   .carrierHRF                    |                                  |
|   .carrierAIDC                   |   .carrierAIDC                   |                                  |
|   .issuer                        |   .issuer                        |                                  |
|   .entryType                     |   .entryType                     |                                  |
+----------------------------------+----------------------------------+----------------------------------+
| modelNumber                      | model                            | Field name change               |
+----------------------------------+----------------------------------+----------------------------------+
| version[].value                  | version                          | Array to scalar: take first     |
|                                  |                                  | element's value                  |
+----------------------------------+----------------------------------+----------------------------------+
| deviceName[].name                | udi.name                         | Array to udi field: take first  |
|                                  |                                  | element's name                   |
+----------------------------------+----------------------------------+----------------------------------+
| identifier                       | identifier                       | Direct mapping                   |
| status                           | status                           | Direct mapping                   |
| type                             | type                             | Direct mapping                   |
| lotNumber                        | lotNumber                        | Direct mapping                   |
| manufacturer                     | manufacturer                     | Direct mapping                   |
| manufactureDate                  | manufactureDate                  | Direct mapping                   |
| expirationDate                   | expirationDate                   | Direct mapping                   |
| patient                          | patient                          | Direct mapping + reference clean |
| owner                            | owner                            | Direct mapping + reference clean |
| contact                          | contact                          | Direct mapping                   |
| location                         | location                         | Direct mapping + reference clean |
| url                              | url                              | Direct mapping                   |
| note                             | note                             | Direct mapping                   |
| safety                           | safety                           | Direct mapping                   |
+----------------------------------+----------------------------------+----------------------------------+

Special Cases:
- udiCarrier array becomes single udi object (first element used)
- deviceName array contributes to udi.name (first element used)
- version array becomes scalar version field (first element's value used)
- Reference cleaning applied to patient, owner, location fields
"""
