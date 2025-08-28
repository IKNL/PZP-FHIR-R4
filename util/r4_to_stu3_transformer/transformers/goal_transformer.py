"""
Goal Transformer for FHIR R4 to STU3 conversion.

This transformer handles the conversion of Goal resources from FHIR R4 to STU3,
implementing the mappings defined in the StructureMap:
http://hl7.org/fhir/StructureMap/Goal4to3

Key transformations:
- lifecycleStatus -> status with specific value mappings
- achievementStatus -> status based on coding system and codes
- Polymorphic start field (date/CodeableConcept)
- Polymorphic target.detail field (Quantity/Range/CodeableConcept)
- Polymorphic target.due field (date/Duration)
- Reference datatype cleaning
"""

from typing import Dict, Any, Optional, List
from .base_transformer import BaseTransformer


class GoalTransformer(BaseTransformer):
    """Transforms Goal resources from FHIR R4 to STU3."""
    
    @property
    def resource_type(self) -> str:
        """Return the FHIR resource type this transformer handles."""
        return "Goal"
    
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform a Goal resource from R4 to STU3.
        
        Args:
            r4_resource: The R4 Goal resource as a dictionary
            
        Returns:
            The transformed STU3 Goal resource as a dictionary
        """
        # Start with base transformation
        stu3_resource = super().transform(r4_resource)
        
        # Apply direct field mappings
        field_mappings = self.get_field_mappings()
        for r4_field, stu3_field in field_mappings.items():
            if r4_field in r4_resource:
                stu3_resource[stu3_field] = r4_resource[r4_field]
        
        # Transform specific Goal fields
        self._transform_status_fields(r4_resource, stu3_resource)
        self._transform_start_field(r4_resource, stu3_resource)
        self._transform_target_array(r4_resource, stu3_resource)
        self._copy_encounter_reference_extension(r4_resource, stu3_resource)
        
        # Clean references throughout the resource
        stu3_resource = self.clean_references_in_object(stu3_resource)
        
        # Transform extension URLs globally
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        
        return stu3_resource
    
    def _transform_status_fields(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform lifecycleStatus and achievementStatus to STU3 status.
        
        The logic follows the StructureMap:
        1. lifecycleStatus values: 'proposed', 'planned', 'accepted', 'on-hold', 
           'cancelled', 'entered-in-error', 'rejected' -> map directly to status
        2. lifecycleStatus 'completed' -> status = 'achieved'
        3. achievementStatus with specific codings -> status values based on code
        """
        lifecycle_status = r4_resource.get('lifecycleStatus')
        achievement_status = r4_resource.get('achievementStatus')
        
        # Handle lifecycleStatus mappings
        if lifecycle_status:
            if lifecycle_status in ['proposed', 'planned', 'accepted', 'on-hold', 
                                  'cancelled', 'entered-in-error', 'rejected']:
                stu3_resource['status'] = lifecycle_status
            elif lifecycle_status == 'active':
                stu3_resource['status'] = 'in-progress'
            elif lifecycle_status == 'completed':
                stu3_resource['status'] = 'achieved'
        
        # Handle achievementStatus mappings (can override lifecycleStatus)
        if achievement_status and 'coding' in achievement_status:
            for coding in achievement_status['coding']:
                if (coding.get('system') == 'http://terminology.hl7.org/CodeSystem/goal-achievement'):
                    code = coding.get('code')
                    if code == 'in-progress':
                        stu3_resource['status'] = 'in-progress'
                    elif code == 'sustaining':
                        # Note: StructureMap has both 'sustaining' and 'on-target' for sustaining code
                        # Using 'sustaining' as it appears first in the map
                        stu3_resource['status'] = 'sustaining'
                    elif code == 'improving':
                        stu3_resource['status'] = 'ahead-of-target'
                    elif code == 'worsening':
                        stu3_resource['status'] = 'behind-target'
        
        # If no status was set, provide a default
        if 'status' not in stu3_resource:
            # Set a reasonable default status
            stu3_resource['status'] = 'planned'
    
    def _transform_start_field(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform the polymorphic start field.
        
        R4 start can be:
        - date
        - CodeableConcept
        
        Both are supported in STU3 as well.
        """
        if 'start' in r4_resource:
            start_value = r4_resource['start']
            
            # The start field is polymorphic but doesn't need transformation
            # Just copy it over (base transformer handles reference cleaning if needed)
            stu3_resource['start'] = start_value
    
    def _transform_target_array(self, r4_resource: Dict[str, Any], stu3_resource: Dict[str, Any]) -> None:
        """
        Transform the target array elements.
        
        Each target element can have polymorphic fields:
        - detail: Quantity, Range, or CodeableConcept
        - due: date or Duration
        """
        if 'target' in r4_resource:
            stu3_targets = []
            
            for r4_target in r4_resource['target']:
                stu3_target = {}
                
                # Copy simple fields
                for field in ['measure']:
                    if field in r4_target:
                        stu3_target[field] = r4_target[field]
                
                # Handle polymorphic detail field
                if 'detail' in r4_target:
                    # detail can be Quantity, Range, or CodeableConcept
                    # No transformation needed, just copy
                    stu3_target['detail'] = r4_target['detail']
                
                # Handle polymorphic due field  
                if 'due' in r4_target:
                    # due can be date or Duration
                    # No transformation needed, just copy
                    stu3_target['due'] = r4_target['due']
                
                stu3_targets.append(stu3_target)
            
            stu3_resource['target'] = stu3_targets
    
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
    
    def get_field_mappings(self) -> Dict[str, str]:
        """
        Get the direct field mappings for Goal transformation.
        
        Returns:
            Dictionary mapping R4 field names to STU3 field names
        """
        return {
            'identifier': 'identifier',
            'category': 'category', 
            'priority': 'priority',
            'description': 'description',
            'subject': 'subject',
            'statusDate': 'statusDate',
            'statusReason': 'statusReason',
            'expressedBy': 'expressedBy',
            'addresses': 'addresses',
            'note': 'note',
            'outcomeCode': 'outcomeCode',
            'outcomeReference': 'outcomeReference'
        }
    
    def get_transformation_summary(self) -> str:
        """
        Get a summary of transformations applied by this transformer.
        
        Returns:
            A string describing the key transformations
        """
        return """
Goal R4 to STU3 Transformations:
+----------------------------------+----------------------------------+----------------------------------+
| R4 Field                         | STU3 Field                       | Transformation                   |
+----------------------------------+----------------------------------+----------------------------------+
| lifecycleStatus                  | status                           | Direct mapping for most values,  |
|                                  |                                  | 'completed' -> 'achieved'        |
+----------------------------------+----------------------------------+----------------------------------+
| achievementStatus.coding         | status                           | Based on goal-achievement system:|
|                                  |                                  | 'in-progress' -> 'in-progress'   |
|                                  |                                  | 'sustaining' -> 'sustaining'     |
|                                  |                                  | 'improving' -> 'ahead-of-target' |
|                                  |                                  | 'worsening' -> 'behind-target'   |
+----------------------------------+----------------------------------+----------------------------------+
| start (date/CodeableConcept)     | start                            | Polymorphic field - direct copy  |
+----------------------------------+----------------------------------+----------------------------------+
| target[].detail                  | target[].detail                  | Polymorphic (Quantity/Range/     |
| (Quantity/Range/CodeableConcept) |                                  | CodeableConcept) - direct copy   |
+----------------------------------+----------------------------------+----------------------------------+
| target[].due (date/Duration)     | target[].due                     | Polymorphic field - direct copy  |
+----------------------------------+----------------------------------+----------------------------------+
| identifier                       | identifier                       | Direct mapping                   |
| category                         | category                         | Direct mapping                   |
| priority                         | priority                         | Direct mapping                   |
| description                      | description                      | Direct mapping                   |
| subject                          | subject                          | Direct mapping + reference clean |
| statusDate                       | statusDate                       | Direct mapping                   |
| statusReason                     | statusReason                     | Direct mapping                   |
| expressedBy                      | expressedBy                      | Direct mapping + reference clean |
| addresses                        | addresses                        | Direct mapping + reference clean |
| note                             | note                             | Direct mapping                   |
| outcomeCode                      | outcomeCode                      | Direct mapping                   |
| outcomeReference                 | outcomeReference                 | Direct mapping + reference clean |
+----------------------------------+----------------------------------+----------------------------------+

Special Cases:
- achievementStatus overrides lifecycleStatus for status field
- Multiple polymorphic fields supported without transformation
- Reference cleaning applied to all Reference fields
"""
