# IKNL PZP FHIR Implementation Guide - AI Coding Assistant Instructions

## Project Overview

This project is a dual-version FHIR Implementation Guide for Advance Care Planning (PZP), supporting both FHIR R4 and STU3. The current strategy is:

- **R4 is the primary development target.**
- **STU3 conformance resources (StructureDefinition, ValueSet, etc.) are maintained manually.**
- **Only resource instances (examples) are converted automatically from R4 to STU3.**
- **Mapping table generation is simplified and deduplicated.**

## Directory Structure

- `R4/` – Develop all profiles, extensions, and examples here using FSH (FHIR Shorthand).
- `STU3/` – Manual conformance resources and auto-converted example instances.
- `util/` – Conversion tools, mapping generators, and dataset utilities:
  - `r4_to_stu3_transformer/` – Python-based R4→STU3 resource transformation system
  - `r4_mapping_and_mermaid_generator/` – R4 mapping table and diagram generation
  - `stu3_mapping_generator/` – STU3-specific mapping table generation

## Key Workflows

### 1. Standard Development Cycle
```powershell
# 1. Develop in R4 directory
cd R4
./_genonce.bat                    # Build R4 IG

# 2. Convert R4 examples to STU3 (from repo root)
convert-r4-to-stu3.bat             # Only resource instances are converted

# 3. Build STU3 IG (manual conformance resources)
cd STU3
./_genonce.bat                    # Build STU3 IG
```

### 2. Manual Maintenance of STU3 Conformance Resources
- Edit or add StructureDefinition, ValueSet, etc. directly in `STU3/input/resources/`.
- **Do not edit auto-converted example files (prefixed with `converted-`).**
- Conformance resources should be prefixed with `manual-` for clarity.

### 3. Resource Instance Conversion
- **Python-based converter**: Modern system in `util/r4_to_stu3_transformer/` with auto-discovery pattern
- **All StructureDefinitions are automatically excluded** from conversion
- Examples include Patient, Observation, Consent, etc.
- Supports complex transformations with PractitionerRole reference resolution

### 4. Mapping Table Generation
- **R4 mappings**: Use `util/r4_mapping_and_mermaid_generator/mapping_table_generator.py`
- **STU3 mappings**: Use `util/stu3_mapping_generator/stu3_mapping_table_generator.py`
- **Mermaid diagrams**: Use `util/r4_mapping_and_mermaid_generator/mermaid_diagram_generator.py`
- Generate from ART-DECOR datasets with automatic deduplication

## Conversion Pipeline (Examples Only)
- **StructureDefinitions**: Completely excluded from automatic conversion.
- **ValueSets**: Handled manually (not converted).
- **Resource Instances**: Automatically converted using StructureMaps.
- **Complex Resources**: Implementation Guides excluded from conversion.

## Common Patterns

- **FSH Profiles:** Develop in `R4/input/fsh/`, always inherit from Nictiz base profiles.
- **Extensions:** Use `ext-` prefix, explicit context, and standard slicing.
- **Mappings:** Include ART-DECOR mappings in all profiles.
- **Invariants:** Use FHIRPath, usually as warnings.

## File Naming Conventions

- **R4 generated resources:** Standard FHIR resource names (e.g., `StructureDefinition-ACP-Patient.json`)
- **STU3 converted instances:** `converted-{ResourceType}-{ID}.json` (no `-STU3` suffix)
- **STU3 manual conformance:** `manual-{ResourceType}-{ID}.json`

## Gotchas & Best Practices

1. **Always develop in R4 first.**
2. **STU3 conformance resources are manual only.**
3. **Only resource instances are auto-converted.**
4. **StructureDefinitions are never auto-converted.**
5. **Mapping tables must be deduplicated.**
6. **Test the full pipeline after changes.**

## When Making Changes

- **Profiles/Extensions:** Edit FSH in `R4/input/fsh/`.
- **STU3 Conformance:** Edit JSON directly in `STU3/input/resources/` with `manual-` prefix.
- **Examples:** Review auto-converted files after running the pipeline.
- **Mappings:** Regenerate and review mapping tables as needed.

---

_Last updated: 2025-08. Simplified to exclude StructureDefinition conversion._

## Project-Specific Patterns

### FSH Profile Conventions
```fsh
Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient  // Always inherit from Nictiz
Id: ACP-Patient                                                    // ACP- prefix pattern
Title: "Patient"                                                   // Human-readable
Description: "A person who receives medical..."                   // Clinical context
* insert MetaRules                                                 // Consistent metadata
```

### Extension Pattern
```fsh
Extension: ExtLegallyCapableMedicalTreatmentDecisions
Id: ext-LegallyCapable-MedicalTreatmentDecisions                  // ext- prefix
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
- `R4/sushi-config.yaml`: Primary IG configuration, dependencies
- `R4/ig.ini`: IG Publisher settings
- `decisions.md`: **Critical** - documents all profiling decisions and rationale

### Build Infrastructure
- `R4/_genonce.bat`: Windows IG Publisher runner with offline detection
- `STU3/_genonce.bat`: Windows IG Publisher runner for STU3

### Analysis Tools
- `util/r4_mapping_and_mermaid_generator/mapping_table_generator.py`: R4 mapping tables from ART-DECOR datasets
- `util/stu3_mapping_generator/stu3_mapping_table_generator.py`: STU3-specific mapping tables
- `util/r4_mapping_and_mermaid_generator/mermaid_diagram_generator.py`: Visual diagram generation
- `util/r4_to_stu3_transformer/fhir_r4_to_stu3_transformer.py`: Python-based R4→STU3 converter

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

1. **Profile changes**: Edit FSH files in `R4/input/fsh/`, follow existing patterns
2. **Conversion issues**: Check Python transformer logic in `util/r4_to_stu3_transformer/`
3. **Dataset alignment**: Update mappings when ART-DECOR datasets change
4. **Cross-version compatibility**: Always test full conversion pipeline after changes
