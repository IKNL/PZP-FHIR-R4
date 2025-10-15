# IKNL PZP FHIR R4 Implementation Guide - AI Coding Assistant Instructions

## Project Overview

This project is a FHIR R4 Implementation Guide for Advance Care Planning (PZP). Key characteristics:

- **R4 is the sole focus of this repository.**
- **STU3 implementation has been moved to a separate repository.**
- **This repository focuses on R4 profile development and mapping table generation.**

## Directory Structure

- `input/` – Develop all profiles, extensions, and examples here using FSH (FHIR Shorthand).
- `fsh-generated/` – Generated FHIR resources from FSH compilation.
- `output/` – Built implementation guide output.
- `util/` – Mapping generators and dataset utilities:
  - `mapping_table_generator.py` – R4 mapping table generation from ART-DECOR datasets
  - `mermaid_diagram_generator.py` – Visual diagram generation from profiles

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
```

### 2. Profile Development
- Edit or add StructureDefinition, ValueSet, etc. using FSH in `input/fsh/`.
- Examples should be placed in `input/examples/` or defined in FSH.
- All conformance resources are maintained in FSH format.

### 3. Mapping Table Generation
- **R4 mappings**: Use `util/mapping_table_generator.py`
- **Mermaid diagrams**: Use `util/mermaid_diagram_generator.py`
- Generate from ART-DECOR datasets with automatic deduplication

## Common Patterns

- **FSH Profiles:** Develop in `input/fsh/`, always inherit from Nictiz base profiles.
- **Extensions:** Use `ext-` prefix, explicit context, and standard slicing.
- **Mappings:** Include ART-DECOR mappings in all profiles.
- **Invariants:** Use FHIRPath, usually as warnings.

## File Naming Conventions

- **Generated resources:** Standard FHIR resource names (e.g., `StructureDefinition-ACP-Patient.json`)
- **FSH files:** Use meaningful names that reflect the profile purpose
- **Examples:** Should have descriptive identifiers

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
- `sushi-config.yaml`: Primary IG configuration, dependencies
- `ig.ini`: IG Publisher settings
- `decisions.md`: **Critical** - documents all profiling decisions and rationale

### Build Infrastructure
- `_genonce.bat`: Windows IG Publisher runner with offline detection

### Analysis Tools
- `util/mapping_table_generator.py`: R4 mapping tables from ART-DECOR datasets
- `util/mermaid_diagram_generator.py`: Visual diagram generation

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
2. **Dataset alignment**: Update mappings when ART-DECOR datasets change
3. **Build validation**: Always test the build after making changes
4. **Mapping updates**: Regenerate mapping tables and diagrams as needed
