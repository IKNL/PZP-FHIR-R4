# IKNL PZP FHIR Implementation Guide - AI Coding Assistant Instructions

## Project Overview

This is a **dual-version FHIR Implementation Guide** for **Advance Care Planning (PZP)** that maintains both **FHIR R4** and **STU3** versions. The project converts from R4 (primary development) to STU3 using sophisticated custom tooling, based on **Dutch zib (Zorginformatiebouwsteen)** 2020 standards.

## Architecture & Key Concepts

### Dual IG Structure
- **`R4/`**: Primary development using FSH (FHIR Shorthand) with SUSHI/IG Publisher
- **`STU3/`**: Generated from R4 via custom conversion pipeline
- **`util/r4-to-r3-converter/`**: Complex Java-based conversion engine with "Extension-Based Cross-Version Bridge" pattern

### Core Technologies
- **FSH (FHIR Shorthand)**: All profiles, extensions, examples in `R4/input/fsh/`
- **SUSHI**: Generates FHIR JSON from FSH
- **IG Publisher**: Creates final implementation guide
- **Custom Java Converter**: Handles R4→STU3 transformation using StructureMaps + temporary extensions

### Dutch Healthcare Context
- Based on **Nictiz zib 2020** profiles (`nictiz.fhir.nl.r4.zib2020: 0.12.0-beta.1`)
- Uses **SNOMED CT**, **Dutch coding systems**, and **ART-DECOR** dataset mappings
- Focuses on **palliative care** and **advance care planning** workflows

## Critical Development Workflows

### 1. Standard Development Cycle
```powershell
# 1. Develop in R4 directory
cd R4
./_genonce.bat                    # Build R4 IG

# 2. Convert R4 to STU3 (from repo root)
convert-r4-to-stu3.bat           # Automated conversion pipeline

# 3. Build STU3 IG
cd STU3
./_genonce.bat                    # Build STU3 IG

# 4. Review conversion analysis
# Check: util/r4-to-r3-converter/CONVERSION_ANALYSIS_REPORT.md
```

### 2. Conversion Pipeline Details
The `convert-r4-to-stu3.bat` script:
- Validates StructureMap files
- Runs Java conversion (`fhirconverter/convert.bat`)
- Copies converted resources to `STU3/input/resources/`
- Generates analysis reports

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
