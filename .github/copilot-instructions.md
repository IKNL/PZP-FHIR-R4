# IKNL PZP FHIR R4 Implementation Guide - AI Coding Assistant Instructions

## Project Overview

This project is a FHIR R4 Implementation Guide for Advance Care Planning (PZP - Proactieve Zorgplanning). Key characteristics:

- **R4 is the sole focus of this repository.**
- **STU3 implementation has been moved to a separate repository.**
- **This repository focuses on R4 profile development, mapping table generation, and questionnaire resources.**
- **Dual questionnaire approach**: Complete clinical questionnaire (`ACP-zib2020`) and administrative subset (`ACP-Administrative`) for discrete FHIR resource exchange.

## Directory Structure

- `input/` – Develop all profiles, extensions, and examples here using FSH (FHIR Shorthand).
  - `input/fsh/` – FSH profile definitions, extensions, and examples
  - `input/resources/` – JSON resources (primarily Questionnaire and QuestionnaireResponse)
  - `input/pagecontent/` – Markdown files for profile introductions and IG pages
  - `input/images/` – Diagrams and visual resources
- `fsh-generated/` – Generated FHIR resources from FSH compilation.
- `output/` – Built implementation guide output.
- `util/` – Mapping generators and dataset utilities:
  - `mapping_table_generator.py` – R4 mapping table generation from ART-DECOR datasets
  - `mermaid_diagram_generator.py` – Visual diagram generation from profiles
  - `questionnaire_item_prefix_populator.py` – Questionnaire prefix processing for compliance

## Key Workflows

### 1. Standard Development Cycle
```powershell
# 1. Develop FSH profiles and examples
# Edit files in input/fsh/

# 2. Build R4 IG
./_genonce.bat                    # Build R4 IG

# 3. Generate mapping tables (optional)
python util/mapping_table_generator.py

# 4. Generate diagrams (optional)
python util/mermaid_diagram_generator.py

# 5. Process questionnaire prefixes (optional)
python util/questionnaire_item_prefix_populator.py [options]
```

### 2. Profile Development
- Edit or add StructureDefinition, ValueSet, etc. using FSH in `input/fsh/`.
- Examples should be placed in `input/examples/` or defined in FSH.
- All conformance resources are maintained in FSH format.
- **Profile introductions**: Add markdown files in `input/pagecontent/` with pattern `StructureDefinition-[ProfileId]-intro.md` to document changes compared to base profiles.

### 3. Mapping Table Generation
- **R4 mappings**: Use `util/mapping_table_generator.py`
- **Mermaid diagrams**: Use `util/mermaid_diagram_generator.py`
- Generate from ART-DECOR datasets with automatic deduplication

### 4. Questionnaire Management
Two questionnaires are maintained:
- **`Questionnaire-ACP-zib2020.json`**: Complete clinical questionnaire with all ACP elements (sections 1-8)
- **`Questionnaire-ACP-Administrative.json`**: Administrative subset focusing on:
  - Section 7: Previously recorded treatment agreements
  - Section 8: Information sharing arrangements
  - Uses same `item.linkId` values as complete questionnaire for interoperability

#### Questionnaire Prefix Processing
- **Dual resource support**: Processes both Questionnaire and QuestionnaireResponse resources
- **Prefix handling**: Adds prefix fields to Questionnaire items, removes prefixes from QuestionnaireResponse for compliance
- **CLI options**: `--questionnaire-only`, `--response-only`, `--dry-run` for targeted processing
- **Pattern detection**: Detects a), b), 1., 2. etc. prefixes in questionnaire items

#### QuestionnaireResponse Examples
Examples follow naming pattern `[PatientName]-[Date]` with `-Administrative` suffix for administrative questionnaire responses.

## Common Patterns

- **FSH Profiles:** Develop in `input/fsh/`, always inherit from Nictiz base profiles.
- **Extensions:** Use `ext-` prefix, explicit context, and standard slicing.
- **Mappings:** Include ART-DECOR mappings in all profiles.
- **Invariants:** Use FHIRPath, usually as warnings.

## File Naming Conventions

- **Generated resources:** Standard FHIR resource names (e.g., `StructureDefinition-ACP-Patient.json`)
- **FSH files:** Use meaningful names that reflect the profile purpose
- **Profile IDs:** Use `ACP-` prefix for profiles (e.g., `ACP-Patient`, `ACP-AdvanceDirective`)
- **Extension IDs:** Use `ext-` prefix (e.g., `ext-Patient.LegallyCapableMedicalTreatmentDecisions`)
- **Questionnaires:** 
  - Complete: `Questionnaire-ACP-zib2020.json`
  - Administrative: `Questionnaire-ACP-Administrative.json`
- **QuestionnaireResponses:** `[PatientName]-[Date].json` with optional `-Administrative` suffix
- **Profile introductions:** `StructureDefinition-[ProfileId]-intro.md` in `input/pagecontent/`

## Gotchas & Best Practices

1. **Always use FSH for profile development.**
2. **Include comprehensive mappings to ART-DECOR datasets.**
3. **Mapping tables must be deduplicated.**
4. **Test the build after changes.**
5. **Follow Nictiz base profile inheritance patterns.**

## When Making Changes

- **Profiles/Extensions:** Edit FSH in `input/fsh/`.
- **Examples:** Add to `input/examples/` or define in FSH.
- **Mappings:** Regenerate and review mapping tables as needed.
- **Build validation:** Always run `./_genonce.bat` after changes.

---

_Last updated: 2025-10. Updated to reflect R4-only repository structure._

## Project-Specific Patterns

### FSH Profile Conventions
```fsh
Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient  // Always inherit from Nictiz
Id: ACP-Patient                                                    // ACP- prefix pattern
Title: "ACP Patient"                                                   // Human-readable
Description: "A person who receives medical..."                   // Clinical context
* insert MetaRules                                                 // Consistent metadata
```

### Extension Pattern
```fsh
Extension: ExtPatientLegallyCapableMedicalTreatmentDecisions
Id: ext-Patient.LegallyCapableMedicalTreatmentDecisions                  // ext- prefix
Context: Patient                                                   // Explicit context
* extension ^slicing.discriminator.type = #value                  // Standard slicing
```

### Dataset Mappings
All profiles include comprehensive mappings to ART-DECOR datasets:
```fsh
Mapping: MapACPPatient
Target: "https://decor.nictiz.nl/ad/..."                         // ART-DECOR reference
* extension[legallyCapable] -> "762" "Wilsbekwaamheid..."         // Concept ID mapping
```

### Invariant Conventions
```fsh
Invariant: ACP-Patient-1
Description: "If the patient is not legally capable..."
* severity = #warning                                              // Usually warnings
* expression = "extension.where(url='...').value = false implies..." // FHIRPath
```

## Key Files to Understand

### Configuration
- `sushi-config.yaml`: Primary IG configuration, dependencies, resource groups
  - **Group `Q-QR-Complete`**: Complete ACP questionnaire and responses
  - **Group `Q-QR-Administrative`**: Administrative questionnaire subset for discrete resource exchange
  - **Group `AD`**: Actor definitions for consulter and provider roles
- `ig.ini`: IG Publisher settings
- `decisions.md`: Documents profiling decisions and rationale

### Build Infrastructure
- `_genonce.bat`: Windows IG Publisher runner with offline detection
- `_gencontinuous.bat`: Continuous build with auto-refresh

### Analysis Tools
- `util/mapping_table_generator.py`: R4 mapping tables from ART-DECOR datasets
- `util/mermaid_diagram_generator.py`: Visual diagram generation
- `util/questionnaire_item_prefix_populator.py`: Questionnaire/QuestionnaireResponse prefix processing

## Integration Dependencies

### External Systems
- **Nictiz FHIR packages**: Core Dutch profiles (use exact versions in sushi-config.yaml)
- **ART-DECOR datasets**: Source of truth for concept mappings
- **SNOMED CT**: Primary terminology (alias: `$snomed`)

### Build Dependencies
- **Java 8+**: Required for IG Publisher
- **SUSHI**: FSH compilation (auto-updated by IG Publisher)
- **Python 3.8+**: For utility scripts and analysis tools

## When Making Changes

1. **Profile changes**: Edit FSH files in `input/fsh/`, follow existing patterns
2. **Profile documentation**: Add/update `StructureDefinition-[ProfileId]-intro.md` in `input/pagecontent/` to explain changes
3. **Questionnaire changes**: 
   - Edit JSON files in `input/resources/`
   - Maintain consistent `item.linkId` values between complete and administrative questionnaires
   - Update metadata fields (`title`, `description`, `purpose`, `language`, `subjectType`, `jurisdiction`)
4. **QuestionnaireResponse examples**: 
   - Create matching examples for both complete and administrative questionnaires
   - Add to `sushi-config.yaml` resources and appropriate group
5. **Dataset alignment**: Update mappings when ART-DECOR datasets change
6. **Build validation**: Always test the build after making changes (`./_genonce.bat`)
7. **Mapping updates**: Regenerate mapping tables and diagrams as needed

## Questionnaire Metadata Best Practices

When creating or updating Questionnaire resources:
- **`title`**: Clear, human-readable title indicating purpose
- **`description`**: Comprehensive explanation of questionnaire purpose and scope
- **`purpose`**: Supporting statement about intended use
- **`language`**: Specify language code (e.g., `"nl-NL"` for Dutch)
- **`subjectType`**: Array of applicable resource types (e.g., `["Patient"]`)
- **`jurisdiction`**: Use ISO 3166 country codes for Netherlands
- **`publisher`**: Use simplified form `"PZNL & IKNL"`
- **Cross-referencing**: Note relationships between questionnaires in description (e.g., subset relationships, shared linkIds)
