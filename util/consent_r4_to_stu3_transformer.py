#!/usr/bin/env python3
"""
FHIR Conse┌─ EXTENSION URL MAPPINGS ───────────────────────────────────────────────────────┐
│ R4 Extension URL                                    │ STU3 Extension URL       │
├─────────────────────────────────────────────────────┼──────────────────────────┤
│ ext-Comment                                         │ Comment                  │
│ ext-TreatmentDirective2.AdvanceDirective           │ consent-additionalSources│
│ ext-AdvanceDirective.Disorder                      │ zib-AdvanceDirective-Disorder │
└─────────────────────────────────────────────────────┴──────────────────────────┘ource Transformer: R4 to STU3

This script transforms FHIR Consent resources from R4 to STU3 format based on 
the specific mapping requirements for the PZP project.

=== MAPPING DOCUMENTATION ===

┌─ DIRECT FIELD MAPPINGS ────────────────────────────────────────────────────────┐
│ R4 Source                          │ STU3 Target                               │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Consent (resourceType)             │ Consent (resourceType)                    │
│ Consent.id                         │ Consent.id                                │
│ Consent.meta                       │ Consent.meta                              │
│ Consent.identifier                 │ Consent.identifier                        │
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
└────────────────────────────────────────────────────┴──────────────────────────┘

┌─ PROVISION TO STU3 TRANSFORMATIONS ────────────────────────────────────────────┐
│ Source                             │ Target                                    │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ provision.actor[Patient]           │ extension:verification                    │
│                                    │ ├─ Verified = true                       │
│                                    │ ├─ VerifiedWith = Patient (SNOMED)       │
│                                    │ └─ VerificationDate = dateTime           │
│                                    │                                           │
│ provision.actor[RESPRSN]           │ consentingParty                           │
│ (Representative role)              │ └─ reference from actor.reference        │
│                                    │                                           │
│ provision.code                     │ extension:treatment                       │
│                                    │ └─ valueCodeableConcept (as array)       │
│                                    │                                           │
│ provision.code                     │ category (additional entry)               │
│ (LivingWillType mapping)           │ └─ CodeableConcept from provision.code   │
│                                    │                                           │
│ provision.period.end               │ period.end                                │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ TREATMENT PERMISSION LOGIC ───────────────────────────────────────────────────┐
│ Condition                          │ STU3 Output                               │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ IF: modifierExtension              │ modifierExtension:                        │
│     ext-TreatmentDirective2.       │ ├─ treatmentPermitted = "JA_MAAR"        │
│     SpecificationOther exists      │ │  "Ja, maar met beperkingen"            │
│                                    │ except:                                   │
│                                    │ └─ extension:restrictions =               │
│                                    │    valueString from SpecificationOther   │
│                                    │                                           │
│ ELSE IF: provision.type exists     │ modifierExtension:                        │
│                                    │ └─ treatmentPermitted:                    │
│   provision.type = "permit"        │    "JA" / "Ja"                           │
│   provision.type = "deny"          │    "NEE" / "Nee"                         │
│                                    │ except:                                   │
│                                    │ └─ type = provision.type                  │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ STU3 EXTENSION URLS ──────────────────────────────────────────────────────────┐
│ Extension Type                     │ Full URL                                  │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ treatmentPermitted                 │ zib-TreatmentDirective-TreatmentPermitted │
│ verification                       │ zib-TreatmentDirective-Verification       │
│ treatment                          │ zib-TreatmentDirective-Treatment          │
│ restrictions                       │ zib-TreatmentDirective-Restrictions       │
└────────────────────────────────────┴───────────────────────────────────────────┘

┌─ CODE SYSTEM MAPPINGS ─────────────────────────────────────────────────────────┐
│ Treatment Permission Codes         │ System: urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4 │
├────────────────────────────────────┼───────────────────────────────────────────┤
│ Code         │ Display             │ When Used                                 │
├──────────────┼─────────────────────┼───────────────────────────────────────────┤
│ JA           │ Ja                  │ provision.type = "permit"                 │
│ NEE          │ Nee                 │ provision.type = "deny"                   │
│ JA_MAAR      │ Ja, maar met        │ modifierExtension:SpecificationOther      │
│              │ beperkingen         │ exists                                    │
└──────────────┴─────────────────────┴───────────────────────────────────────────┘

Author: AI Assistant  
Date: August 25, 2025
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class ConsentTransformer:
    """Transforms FHIR Consent resources from R4 to STU3 based on PZP mapping."""
    
    def __init__(self):
        """Initialize the transformer with specific mapping rules."""
        # Extension URLs from the mapping
        self.stu3_extension_urls = {
            'comment': 'http://nictiz.nl/fhir/StructureDefinition/Comment',
            'additional_sources': 'http://nictiz.nl/fhir/StructureDefinition/consent-additionalSources',
            'treatment_permitted': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-TreatmentPermitted',
            'verification': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-Verification',
            'treatment': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-Treatment',
            'advance_directive_disorder': 'http://nictiz.nl/fhir/StructureDefinition/zib-AdvanceDirective-Disorder'
        }
        
        # R4 extension URLs to transform
        self.r4_extension_mappings = {
            'http://nictiz.nl/fhir/StructureDefinition/ext-Comment': 'comment',
            'http://nictiz.nl/fhir/StructureDefinition/ext-TreatmentDirective2.AdvanceDirective': 'additional_sources',
            'http://nictiz.nl/fhir/StructureDefinition/ext-AdvanceDirective.Disorder': 'advance_directive_disorder'
        }

    def transform_consent(self, r4_consent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single R4 Consent resource to STU3.
        
        Args:
            r4_consent: R4 Consent resource as dictionary
            
        Returns:
            STU3 Consent resource as dictionary
        """
        if r4_consent.get('resourceType') != 'Consent':
            raise ValueError(f"Expected Consent resource, got {r4_consent.get('resourceType')}")
        
        stu3_consent = {
            'resourceType': 'Consent'
        }
        
        # Direct field mappings (preserve structure)
        self._copy_standard_fields(r4_consent, stu3_consent)
        
        # Specific transformations based on mapping
        self._transform_category_snomed(r4_consent, stu3_consent)
        self._transform_extensions(r4_consent, stu3_consent)
        self._transform_provision_to_stu3_structures(r4_consent, stu3_consent)
        self._transform_period_from_provision(r4_consent, stu3_consent)
        
        # Clean up empty arrays and objects
        self._cleanup_empty_fields(stu3_consent)
        
        return stu3_consent

    def _copy_standard_fields(self, r4_consent: Dict[str, Any], stu3_consent: Dict[str, Any]) -> None:
        """Copy standard fields that map directly."""
        # Fields that map 1:1
        direct_fields = [
            'id', 'meta', 'text', 'contained', 'identifier', 'status', 
            'patient', 'dateTime', 'organization', 'source', 'policy', 'sourceAttachment'
        ]
        
        for field in direct_fields:
            if field in r4_consent:
                stu3_consent[field] = r4_consent[field]
        
        # Note: scope is excluded as per mapping (R4 only)

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
            
            if original_url in self.r4_extension_mappings:
                # Transform to STU3 extension
                mapping_key = self.r4_extension_mappings[original_url]
                stu3_url = self.stu3_extension_urls[mapping_key]
                
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
                        'url': self.stu3_extension_urls['treatment_permitted'],
                        'valueCodeableConcept': {
                            'coding': [{
                                'system': 'urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4',
                                'code': 'JA_MAAR',
                                'display': 'Ja, maar met beperkingen'
                            }]
                        }
                    })
                    # Add except with restrictions extension
                    except_item = {
                        'extension': [{
                            'url': 'http://nictiz.nl/fhir/StructureDefinition/zib-TreatmentDirective-Restrictions',
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
                'url': self.stu3_extension_urls['treatment_permitted'],
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
            'url': self.stu3_extension_urls['verification'],
            'extension': []
        }
        has_patient = False
        has_representative = False
        
        if 'actor' in provision:
            for actor in provision['actor']:
                ref = actor.get('reference', {})
                ref_type = ref.get('type', '')
                role = actor.get('role', {})
                
                # Check if this is a Patient (for verification)
                if ref_type == 'Patient':
                    has_patient = True
                    verification_ext['extension'].append({
                        'url': 'Verified',
                        'valueBoolean': True
                    })
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
                    # Add VerificationDate from Consent.dateTime if present
                    if 'dateTime' in r4_consent:
                        verification_ext['extension'].append({
                            'url': 'VerificationDate',
                            'valueDateTime': r4_consent['dateTime']
                        })
                
                # Check if this is a Representative (RESPRSN role)
                elif self._is_representative_role(role):
                    has_representative = True
                    # Add to consentingParty
                    if 'consentingParty' not in stu3_consent:
                        stu3_consent['consentingParty'] = []
                    stu3_consent['consentingParty'].append(ref)
        
        if has_patient:
            stu3_consent['extension'].append(verification_ext)

        # --- Treatment extension and LivingWillType category mapping ---
        if 'code' in provision:
            # Add to extension:treatment (for all consent types)
            stu3_consent['extension'].append({
                'url': self.stu3_extension_urls['treatment'],
                'valueCodeableConcept': provision['code'] if isinstance(provision['code'], list) else [provision['code']]
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

    # (Handled above)

        # --- Except.type (not used in STU3 example, so skip) ---

    # (No longer needed, logic inlined above)

    # (No longer needed, logic inlined above)

    def _is_representative_role(self, role: Dict[str, Any]) -> bool:
        """Check if role represents a representative (RESPRSN)."""
        if 'coding' not in role:
            return False
        
        for coding in role['coding']:
            if (coding.get('system') == 'http://terminology.hl7.org/CodeSystem/v3-RoleCode' and 
                coding.get('code') == 'RESPRSN'):
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

    def _get_verification_sub_extension_url(self, reference: Dict[str, Any]) -> str:
        """Determine verification sub-extension URL based on reference type."""
        ref_string = reference.get('reference', '')
        
        if ref_string.startswith('Patient/'):
            return 'Verified'
        elif ref_string.startswith('RelatedPerson/'):
            return 'VerifiedWith'
        elif ref_string.startswith('Practitioner/') or ref_string.startswith('PractitionerRole/'):
            return 'VerificationDate'
        else:
            return 'Verified'  # Default

    # (No longer needed, logic inlined above)

    # (No longer needed, logic inlined above)

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
        
        # Note: period.start is not mapped from R4 provision in the Excel mapping
        # but could be added if needed

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

def transform_file(input_file: Path, output_file: Path) -> None:
    """Transform a single Consent file from R4 to STU3."""
    print(f"Transforming: {input_file} -> {output_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            r4_consent = json.load(f)
        
        transformer = ConsentTransformer()
        stu3_consent = transformer.transform_consent(r4_consent)
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stu3_consent, f, indent=2, ensure_ascii=False)
            
        print(f"✓ Successfully transformed {input_file.name}")
        
    except Exception as e:
        print(f"✗ Error transforming {input_file.name}: {e}")
        raise

def transform_directory(input_dir: Path, output_dir: Path, pattern: str = "*.json") -> None:
    """Transform all Consent files in a directory."""
    input_files = list(input_dir.glob(pattern))
    
    if not input_files:
        print(f"No files found matching pattern '{pattern}' in {input_dir}")
        return
    
    print(f"Found {len(input_files)} files to transform")
    
    success_count = 0
    error_count = 0
    
    for input_file in input_files:
        try:
            # Generate output filename
            output_file = output_dir / f"converted-{input_file.name}"
            transform_file(input_file, output_file)
            success_count += 1
        except Exception as e:
            print(f"Failed to transform {input_file}: {e}")
            error_count += 1
    
    print(f"\nTransformation complete: {success_count} success, {error_count} errors")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Transform FHIR Consent resources from R4 to STU3",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('input', help="Input file or directory path")
    parser.add_argument('output', help="Output file or directory path") 
    parser.add_argument('--pattern', default="*Consent*.json", 
                       help="File pattern for directory processing (default: *Consent*.json)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist")
        sys.exit(1)
    
    try:
        if input_path.is_file():
            transform_file(input_path, output_path)
        elif input_path.is_dir():
            transform_directory(input_path, output_path, args.pattern)
        else:
            print(f"Error: '{input_path}' is neither a file nor directory")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTransformation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
