# PZP FHIR R4 Implementation Guide

This repository contains the FHIR R4 Implementation Guide that supports the Advance Care Planning (ACP) information standard (Dutch: Proactieve Zorgplanning) for use within the palliative care domain in the Netherlands. This domain involves care for patients with an incurable illness or condition from which they are expected to die.

Developed by the [Netherlands Comprehensive Cancer Organisation](https://iknl.nl/en) (Dutch: Integraal kankercentrum Nederland (IKNL)), this guide provides technical direction for using FHIR R4 to exchange ACP data. It builds on top of the Dutch Core R4 profiles.


## Published Implementation Guides

- **R4**: https://api.iknl.nl/docs/pzp/r4/

For the STU3 implementation guide, see the separate [STU3 repository](https://github.com/IKNL/PZP-FHIR-STU3).

## Repository Structure

This repository contains the FHIR R4 implementation guide development files:

- `input/` - FHIR Shorthand (FSH) profile definitions, examples, and resources
- `fsh-generated/` - Generated FHIR resources from FSH compilation
- `output/` - Built implementation guide output
- `util/` - Utility scripts for mapping table and diagram generation

## Quick Start

This project uses the HL7 FHIR Publisher to build the implementation guide. The profiles are defined using FHIR Shorthand (FSH).

### Build Process

**Build R4 IG**: `./_genonce.bat`
- Compiles FSH files and generates the R4 Implementation Guide

For detailed development instructions, see the [Copilot Instructions](.github/copilot-instructions.md).

