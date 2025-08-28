# PZP FHIR Implementation Guide

This repository contains Implementation Guides (IG) in both FHIR R4 and STU3 that support the Advance Care Planning (ACP) information standard (Dutch: Proactieve Zorgplanning) for use within the palliative care domain in the Netherlands. This domain involves care for patients with an incurable illness or condition from which they are expected to die.

Developed by the [Netherlands Comprehensive Cancer Organisation](https://iknl.nl/en) (Dutch: Integraal kankercentrum Nederland (IKNL)), this guide provides technical direction for using FHIR to exchange ACP data. It builds on top of the Dutch Core STU3/R4 profiles.

## Published Implementation Guides

- **R4**: https://as-iknl-api-documentatie.azurewebsites.net/docs/pzp/r4/
- **STU3**: https://as-iknl-api-documentatie.azurewebsites.net/docs/pzp/stu3/

## Repository Structure

- `R4/` - Primary FHIR R4 implementation guide development
- `STU3/` - FHIR STU3 implementation guide (resources instance examples converted from R4)
- `util/` - Utility scripts and conversion tools for R4→STU3 transformation - mainly AI developed based.

## Quick Start

This project uses the HL7 FHIR Publisher to build the implementation guides. The R4 version uses FHIR Shorthand (FSH) for profile definitions.

### Build Process

1. **Build R4 IG**: `cd R4 && ./_genonce.bat`
   - Compiles FSH files and generates the R4 Implementation Guide
   
3. **Build STU3 IG**: `cd STU3 && ./_genonce.bat`
   - Builds the STU3 Implementation Guide with converted examples (run conversion first)

For detailed development instructions, see the [Copilot Instructions](.github/copilot-instructions.md).

