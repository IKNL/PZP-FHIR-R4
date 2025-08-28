"""
FHIR Consent Resource Transformer: R4 to STU3

This module transforms FHIR Consent resources from R4 to STU3 format based on 
the specific mapping requirements for the PZP project.

=== MAPPING DOCUMENTATION ===

┌─ DIRECT FIELD MAPPINGS ────────────────────────────────────────────────────────┐
│ R4 Source                          │ STU3 Target                               │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Consent (resourceType)             │ Consent (resourceType)                    │
│ Consent.id                         │ Consent.id                                │
│ Consent.meta                       │ Consent.meta                              │
│ Consent.identifier (0..*)          │ Consent.identifier (0..1) - FIRST ONLY   │
│ Consent.status                     │ Consent.status                            │
│ Consent.patient                    │ Consent.patient                           │
│ Consent.dateTime                   │ Consent.dateTime                          │
│ Consent.policy                     │ Consent.policy                            │
│ Consent.source[x]                  │ Consent.source[x]                         │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ EXCLUDED R4 FIELDS ───────────────────────────────────────────────────────────┐
│ R4 Field                           │ Reason                                    │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Consent.scope                      │ Not supported in STU3                     │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ CATEGORY CODE TRANSFORMATIONS ────────────────────────────────────────────────┐
│ R4 Source                          │ STU3 Target                               │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ SNOMED 129125009                   │ SNOMED 11291000146105                     │
│ (no display)                       │ "Treatment instructions (record artifact)" │
│                                    │                                           │
│ consentcategorycodes#acd           │ SNOMED 11341000146107                     │
│ (Advance directive consent)        │ (Advance directive)                       │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ EXTENSION URL MAPPINGS ──────────────────────────────────────────────────────┐
│ R4 Extension URL                                   │ STU3 Extension URL       │
├────────────────────────────────────────────────────┼──────────────────────────┤
│ ext-Comment                                        │ Comment                  │
│ ext-TreatmentDirective2.AdvanceDirective           │ consent-additionalSources│
│ ext-AdvanceDirective.Disorder                      │ zib-AdvanceDirective-Disorder │
└────────────────────────────────────────────────────┴──────────────────────────┘

┌─ REPRESENTATIVE ROLE MAPPINGS ─────────────────────────────────────────────────┐
│ R4 System/Code                     │ STU3 System/Code                          │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ v3-RoleCode#POWATT                 │ v3-RoleCode#POWATT                        │
│ v3-RoleCode#HPOWATT                │ v3-RoleCode#HPOWATT                       │
│ (Direct mapping - same codes)      │ (Direct mapping - same codes)             │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ CONDITIONAL LOGIC RULES ──────────────────────────────────────────────────────┐
│ Condition                          │ Action                                    │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Category = "acd" AND               │ Add provision.code with category:         │
│ provision.extension contains       │ SNOMED 11341000146107 "Advance directive"│
│ LivingWillType                     │                                           │
└────────────────────────────────────┴───────────────────────────────────────────┘
"""

import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .base_transformer import BaseTransformer

logger = logging.getLogger(__name__)

class ConsentTransformer(BaseTransformer):
    """FHIR Consent R4 to STU3 transformer."""
    
    @property
    def resource_type(self) -> str:
        return "Consent"
    
    def transform_resource(self, r4_resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Transform a Consent resource from R4 to STU3 using the complete original logic."""
        if not self.can_transform(r4_resource):
            return None
        
        resource_id = r4_resource.get('id', 'unknown')
        self.log_transformation_start(resource_id)
        
        # Create STU3 resource structure with ordered fields
        stu3_resource = {}
        
        # 1. Resource type and id (always first)
        stu3_resource['resourceType'] = 'Consent'
        if 'id' in r4_resource:
            stu3_resource['id'] = r4_resource['id']
        
        # 2. Meta (early)
        if 'meta' in r4_resource:
            stu3_resource['meta'] = self.transform_meta(r4_resource['meta'])
            self.log_field_transformation('meta')
        
        # 3. Extensions and contained (early structural elements)
        if 'text' in r4_resource:
            stu3_resource['text'] = r4_resource['text']
        if 'contained' in r4_resource:
            stu3_resource['contained'] = r4_resource['contained']
        
        # 4. Identifier (single object in STU3)
        if 'identifier' in r4_resource and r4_resource['identifier']:
            if isinstance(r4_resource['identifier'], list) and len(r4_resource['identifier']) > 0:
                stu3_resource['identifier'] = r4_resource['identifier'][0]
            elif not isinstance(r4_resource['identifier'], list):
                stu3_resource['identifier'] = r4_resource['identifier']
        
        # 5. Status (required)
        if 'status' in r4_resource:
            stu3_resource['status'] = r4_resource['status']
        
        # 6. Category (transformed)
        self._transform_category_snomed(r4_resource, stu3_resource)
        
        # 7. Patient reference
        if 'patient' in r4_resource:
            stu3_resource['patient'] = r4_resource['patient']
        
        # 8. Date and time fields
        if 'dateTime' in r4_resource:
            stu3_resource['dateTime'] = r4_resource['dateTime']
        
        # 9. Extensions (transformed)
        self._transform_extensions(r4_resource, stu3_resource)
        
        # 10. Organization and source fields
        if 'organization' in r4_resource:
            stu3_resource['organization'] = r4_resource['organization']
        if 'source' in r4_resource:
            stu3_resource['source'] = r4_resource['source']
        if 'sourceAttachment' in r4_resource:
            stu3_resource['sourceAttachment'] = r4_resource['sourceAttachment']
        
        # 11. Policy
        if 'policy' in r4_resource:
            stu3_resource['policy'] = r4_resource['policy']
        
        # 12. Provision transformations (creates modifierExtension, except, etc.)
        self._transform_provision_to_stu3_structures(r4_resource, stu3_resource)
        self._transform_period_from_provision(r4_resource, stu3_resource)
        
        # Clean up empty arrays and objects
        self._cleanup_empty_fields(stu3_resource)
        
        # Clean all Reference objects to remove R4-specific 'type' fields  
        stu3_resource = self.clean_references_in_object(stu3_resource)
        
        # Transform extension URLs globally
        stu3_resource = self.transform_extensions_in_object(stu3_resource)
        
        self.log_transformation_complete(resource_id)
        return stu3_resource

    def _transform_category_snomed(self, r4_consent: Dict[str, Any], stu3_consent: Dict[str, Any]) -> None:
        """Transform category codes: SNOMED 129125009 -> 11291000146105 and consentcategorycodes#acd -> SNOMED 11341000146107."""
        if 'category' not in r4_consent:
            return
        stu3_categories = []
        for category in r4_consent['category']:
            stu3_category = category.copy()
            if 'coding' in stu3_category:
                for coding in stu3_category['coding']:
                    # Transform SNOMED 129125009 -> 11291000146105 (Treatment instructions)
                    if (coding.get('system') == 'http://snomed.info/sct' and coding.get('code') == '129125009'):
                        coding['code'] = '11291000146105'
                        coding['display'] = 'Treatment instructions (record artifact)'
                    # Transform consentcategorycodes#acd -> SNOMED 11341000146107 (Advance directive)
                    elif (coding.get('system') == 'http://terminology.hl7.org/CodeSystem/consentcategorycodes' and 
                          coding.get('code') == 'acd'):
                        coding['system'] = 'http://snomed.info/sct'
                        coding['code'] = '11341000146107'
                        # Remove display if present, let terminology server provide it
                        if 'display' in coding:
                            del coding['display']
            stu3_categories.append(stu3_category)
        stu3_consent['category'] = stu3_categories

    def _transform_extensions(self, r4_consent: Dict[str, Any], stu3_consent: Dict[str, Any]) -> None:
        """Transform extensions based on mapping: comment and additionalAdvanceDirective."""
        if 'extension' not in r4_consent:
            return
            
        stu3_extensions = []
        
        for extension in r4_consent['extension']:
            original_url = extension.get('url')
            
            # Extension URL mappings
            url_mappings = {
                'http://nictiz.nl/fhir/StructureDefinition/ext-Comment': 
                    'http://nictiz.nl/fhir/StructureDefinition/Comment',
                'http://nictiz.nl/fhir/StructureDefinition/ext-TreatmentDirective2.AdvanceDirective': 
                    'http://nictiz.nl/fhir/StructureDefinition/consent-additionalSources',
                'http://nictiz.nl/fhir/StructureDefinition/ext-AdvanceDirective.Disorder': 
                    'http://nictiz.nl/fhir/StructureDefinition/zib-AdvanceDirective-Disorder'
            }
            
            if original_url in url_mappings:
                # Transform to STU3 extension
                stu3_url = url_mappings[original_url]
                
                stu3_extension = extension.copy()
                stu3_extension['url'] = stu3_url
                stu3_extensions.append(stu3_extension)
            else:
                # Keep other extensions as-is
                stu3_extensions.append(extension)
        
        if stu3_extensions:
            stu3_consent['extension'] = stu3_extensions

    def _transform_provision_to_stu3_structures(self, r4_consent: Dict[str, Any], stu3_consent: Dict[str, Any]) -> None:
        """Transform R4 provision to various STU3 structures per mapping, matching the provided STU3 example."""
        if 'provision' not in r4_consent:
            return
        provision = r4_consent['provision']
        # Ensure arrays exist
        if 'extension' not in stu3_consent:
            stu3_consent['extension'] = []
        if 'modifierExtension' not in stu3_consent:
            stu3_consent['modifierExtension'] = []
        if 'except' not in stu3_consent:
            stu3_consent['except'] = []

        # STU3 extension URLs
        stu3_extension_urls = {
            'treatment_permitted': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-TreatmentPermitted',
            'verification': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-Verification',
            'treatment': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-Treatment',
            'restrictions': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-Restrictions'
        }

        # --- TreatmentPermitted logic ---
        # Check for specificationOther modifierExtension (exact URL match)
        found_specification_other = False
        specification_other_url = 'http://nictiz.nl/fhir/StructureDefinition/ext-TreatmentDirective2.SpecificationOther'
        
        if 'modifierExtension' in r4_consent:
            for mod_ext in r4_consent['modifierExtension']:
                if mod_ext.get('url') == specification_other_url:
                    found_specification_other = True
                    # Add modifierExtension:treatmentPermitted (JA_MAAR)
                    stu3_consent['modifierExtension'].append({
                        'url': stu3_extension_urls['treatment_permitted'],
                        'valueCodeableConcept': {
                            'coding': [{
                                'system': 'urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4',
                                'code': 'JA_MAAR',
                                'display': 'Ja, maar met beperkingen'
                            }]
                        }
                    })
                    # Add except with restrictions extension and type='deny' for JA_MAAR
                    except_item = {
                        'type': 'deny',
                        'extension': [{
                            'url': stu3_extension_urls['restrictions'],
                            'valueString': mod_ext.get('valueString', '')
                        }]
                    }
                    stu3_consent['except'].append(except_item)
                    break  # Only process first occurrence
        
        # If specificationOther not found, use provision.type for treatmentPermitted
        if not found_specification_other and 'type' in provision:
            code_map = {
                'permit': ('JA', 'Ja'),
                'deny': ('NEE', 'Nee')
            }
            code, display = code_map.get(provision['type'], (provision['type'], provision['type']))
            stu3_consent['modifierExtension'].append({
                'url': stu3_extension_urls['treatment_permitted'],
                'valueCodeableConcept': {
                    'coding': [{
                        'system': 'urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4',
                        'code': code,
                        'display': display
                    }]
                }
            })
            # Also add except.type for provision.type mapping
            except_item = {
                'type': provision['type']
            }
            stu3_consent['except'].append(except_item)

        # --- Verification extension and Representative mapping ---
        # Check for Patient (verification) and RESPRSN (consentingParty)
        verification_ext = {
            'url': stu3_extension_urls['verification'],
            'extension': []
        }
        has_verification_actors = False
        has_representative = False
        
        if 'actor' in provision:
            for actor in provision['actor']:
                ref = actor.get('reference', {})
                ref_type = ref.get('type', '')
                role = actor.get('role', {})
                
                # Check if this is a Patient (for verification)
                if ref_type == 'Patient':
                    has_verification_actors = True
                    # Add VerifiedWith for Patient
                    verification_ext['extension'].append({
                        'url': 'VerifiedWith',
                        'valueCodeableConcept': {
                            'coding': [{
                                'system': 'http://snomed.info/sct',
                                'code': '116154003',
                                'display': 'Patient'
                            }]
                        }
                    })
                
                # Check if this is a RelatedPerson with CONSENTER role
                elif ref_type == 'RelatedPerson' and self._is_consenter_role(role):
                    has_verification_actors = True
                    # Use display text from reference if available, otherwise fallback to "ContactPerson"
                    display_text = ref.get('display', 'ContactPerson')
                    # Add VerifiedWith for RelatedPerson
                    verification_ext['extension'].append({
                        'url': 'VerifiedWith',
                        'valueCodeableConcept': {
                            'coding': [{
                                'system': 'http://hl7.org/fhir/v3/NullFlavor',
                                'code': 'OTH',
                                'display': 'Other'
                            }],
                            'text': display_text
                        }
                    })
                
                # Check if this is a Representative (RESPRSN role)
                elif self._is_representative_role(role):
                    has_representative = True
                    # Add to consentingParty
                    if 'consentingParty' not in stu3_consent:
                        stu3_consent['consentingParty'] = []
                    stu3_consent['consentingParty'].append(ref)
        
        # If we have verification actors, add the common verification fields and the extension
        if has_verification_actors:
            # Add common Verified and VerificationDate at the beginning
            verification_ext['extension'].insert(0, {
                'url': 'Verified',
                'valueBoolean': True
            })
            # Add VerificationDate from Consent.dateTime if present
            if 'dateTime' in r4_consent:
                verification_ext['extension'].insert(1, {
                    'url': 'VerificationDate',
                    'valueDateTime': r4_consent['dateTime']
                })
            
            stu3_consent['extension'].append(verification_ext)

        # --- Treatment extension and LivingWillType category mapping ---
        if 'code' in provision:
            # Add to extension:treatment (for all consent types)
            # STU3: valueCodeableConcept is 0..1, so take first code only
            treatment_code = provision['code'][0] if isinstance(provision['code'], list) else provision['code']
            stu3_consent['extension'].append({
                'url': stu3_extension_urls['treatment'],
                'valueCodeableConcept': treatment_code
            })
            
            # Add provision.code as additional category entries (LivingWillType mapping)
            # Only for AdvanceDirectives (identified by consentcategorycodes#acd)
            if self._is_advance_directive(r4_consent):
                if 'category' not in stu3_consent:
                    stu3_consent['category'] = []
                
                # Add each code from provision.code as a separate category
                codes_to_add = provision['code'] if isinstance(provision['code'], list) else [provision['code']]
                for code in codes_to_add:
                    stu3_consent['category'].append(code)

    def _is_representative_role(self, role: Dict[str, Any]) -> bool:
        """Check if role represents a representative (RESPRSN)."""
        if 'coding' not in role:
            return False
        
        for coding in role['coding']:
            if (coding.get('system') == 'http://terminology.hl7.org/CodeSystem/v3-RoleCode' and 
                coding.get('code') == 'RESPRSN'):
                return True
        return False

    def _is_consenter_role(self, role: Dict[str, Any]) -> bool:
        """Check if role represents a consenter (CONSENTER)."""
        if 'coding' not in role:
            return False
        
        for coding in role['coding']:
            if (coding.get('system') == 'http://terminology.hl7.org/CodeSystem/v3-RoleCode' and 
                coding.get('code') == 'CONSENTER'):
                return True
        return False

    def _is_advance_directive(self, r4_consent: Dict[str, Any]) -> bool:
        """Check if this is an AdvanceDirective based on category containing consentcategorycodes#acd."""
        if 'category' not in r4_consent:
            return False
        
        for category in r4_consent['category']:
            if 'coding' not in category:
                continue
            for coding in category['coding']:
                # Check for original R4 category code
                if (coding.get('system') == 'http://terminology.hl7.org/CodeSystem/consentcategorycodes' and 
                    coding.get('code') == 'acd'):
                    return True
                # Also check for already transformed SNOMED code (in case this is called after transformation)
                elif (coding.get('system') == 'http://snomed.info/sct' and 
                      coding.get('code') == '11341000146107'):
                    return True
        return False

    def _transform_period_from_provision(self, r4_consent: Dict[str, Any], stu3_consent: Dict[str, Any]) -> None:
        """Transform provision.period.end to period.end (DateExpired -> EndDate)."""
        if 'provision' not in r4_consent:
            return
            
        provision = r4_consent['provision']
        if 'period' not in provision:
            return
            
        provision_period = provision['period']
        
        # Create STU3 period if needed
        if 'period' not in stu3_consent:
            stu3_consent['period'] = {}
        
        # Map provision.period.end to period.end
        if 'end' in provision_period:
            stu3_consent['period']['end'] = provision_period['end']

    def _cleanup_empty_fields(self, stu3_consent: Dict[str, Any]) -> None:
        """Remove empty arrays and objects from the STU3 consent to comply with FHIR requirements."""
        # List of fields that should be removed if empty
        fields_to_cleanup = [
            'extension', 'modifierExtension', 'except', 'category', 'consentingParty'
        ]
        
        for field in fields_to_cleanup:
            if field in stu3_consent:
                value = stu3_consent[field]
                # Remove if it's an empty list or empty dict
                if (isinstance(value, list) and len(value) == 0) or \
                   (isinstance(value, dict) and len(value) == 0):
                    del stu3_consent[field]
    
    def convert_profile_url(self, r4_profile_url: str) -> str:
        """Convert Consent profile URL from R4 to STU3."""
        # Specific mappings for Consent profiles
        if 'ACP-AdvanceDirective' in r4_profile_url:
            return r4_profile_url.replace('/R4/', '/STU3/')
        elif 'ACP-TreatmentDirective2' in r4_profile_url:
            return r4_profile_url.replace('/R4/', '/STU3/')
        
        # Default conversion
        return super().convert_profile_url(r4_profile_url)


def main():
    """Main function for standalone execution."""
    import argparse
    import sys
    from pathlib import Path
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Transform FHIR Consent resources from R4 to STU3')
    parser.add_argument('input_dir', type=Path, help='Input directory containing R4 Consent resources')
    parser.add_argument('output_dir', type=Path, help='Output directory for STU3 Consent resources')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.input_dir.exists():
        print(f"Error: Input directory {args.input_dir} does not exist")
        sys.exit(1)
    
    # Create transformer
    transformer = ConsentTransformer()
    
    # Process all JSON files in input directory
    json_files = list(args.input_dir.glob('*.json'))
    if not json_files:
        print(f"No JSON files found in {args.input_dir}")
        sys.exit(1)
    
    print(f"Found {len(json_files)} JSON files to process")
    
    success_count = 0
    for json_file in json_files:
        output_file = args.output_dir / f"converted-{json_file.name}"
        if transformer.transform_file(json_file, output_file):
            success_count += 1
    
    # Print statistics
    stats = transformer.get_stats()
    print(f"\nTransformation complete:")
    print(f"  Processed: {stats['processed']}")
    print(f"  Transformed: {stats['transformed']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")


if __name__ == '__main__':
    main()
