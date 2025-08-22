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
- `util/` – Mapping tools, conversion scripts, and dataset utilities.

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
- The Java-based converter in `util/r4-to-r3-converter/` converts only resource instances.
- **All StructureDefinitions are automatically excluded** from conversion.
- Examples include Patient, Observation, Consent, etc.

### 4. Mapping Table Generation
- Use `util/mapping_table_generator.py` to generate mapping tables from ART-DECOR datasets.
- Deduplication is handled in the script; review output for accuracy.

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

### 3. Debugging Conversion Issues
- **Validation logs**: `util/r4-to-r3-converter/fhirconverter/debug-logs/`
- **StructureMap validation**: Uses custom `MapFileValidator`
- **Extension analysis**: Check temporary conversion extensions in debug output

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

## Conversion Architecture Understanding

### Extension-Based Bridge Pattern
The converter cannot directly transform R4→STU3 due to HAPI FHIR limitations, so it uses:
1. **R4→R4 + Extensions**: StructureMaps add temporary conversion hints
2. **Extension Processor**: Converts extensions to native STU3 properties

### StructureMap Files
- Located in `util/r4-to-r3-converter/maps/r4/`
- Handle complex business logic transformations
- Add temporary extensions with pattern: `http://fhir.conversion/cross-version/{ResourceType}.{property}`

### ZIB Version Mapping
- `matched_concepts_between_zib2017_and_zib2020.json`: Maps concept IDs between zib versions
- Essential for maintaining compatibility between R4 (zib2020) and STU3 (zib2017)

## Key Files to Understand

### Configuration
- `R4/sushi-config.yaml`: Primary IG configuration, dependencies
- `R4/ig.ini`: IG Publisher settings
- `decisions.md`: **Critical** - documents all profiling decisions and rationale

### Build Infrastructure
- `R4/_genonce.bat`: Windows IG Publisher runner with offline detection
- `convert-r4-to-stu3.bat`: Main conversion orchestrator
- `util/r4-to-r3-converter/fhirconverter/convert.bat`: Java converter entry point

### Analysis Tools
- `util/mapping_table_generator.py`: Generates mapping tables from ART-DECOR datasets
- `util/r4-to-r3-converter/analyze_conversion.py`: Post-conversion analysis

## Integration Dependencies

### External Systems
- **Nictiz FHIR packages**: Core Dutch profiles (use exact versions in sushi-config.yaml)
- **ART-DECOR datasets**: Source of truth for concept mappings
- **SNOMED CT**: Primary terminology (alias: `$snomed`)

### Build Dependencies
- **Java 8+**: Required for IG Publisher and custom converter
- **SUSHI**: FSH compilation (auto-updated by IG Publisher)
- **Python 3.8+**: For utility scripts and analysis tools

## Common Gotchas

1. **Always develop in R4 first** - STU3 is generated, never edit directly
2. **Conversion extensions are temporary** - they disappear in final STU3 output
3. **zib version alignment** - R4 uses zib2020, STU3 uses zib2017 mappings
4. **Windows batch scripts** - Development workflow assumes Windows environment
5. **Internet connectivity** - IG Publisher checks online/offline mode for terminology validation

## When Making Changes

1. **Profile changes**: Edit FSH files in `R4/input/fsh/`, follow existing patterns
2. **Conversion issues**: Check StructureMaps in `maps/r4/` and Java converter logic
3. **Dataset alignment**: Update mappings when ART-DECOR datasets change
4. **Cross-version compatibility**: Always test full conversion pipeline after changes
