
### Change Log
#### 1.0.0-rc2
| Issue | Short Description |
|-------|-------------------|
| [#90](https://github.com/IKNL/PZP-FHIR-R4/issues/90) | Revisited the Medical Policy Goal profile to address reported inconsistencies and improve its alignment with the intended “medical policy” semantics. |
| [#83](https://github.com/IKNL/PZP-FHIR-R4/issues/83) | Updated ACP-OtherImportantInformation metadata and identity to ensure consistent naming/canonical identity across generated artifacts. |
| [#84](https://github.com/IKNL/PZP-FHIR-R4/issues/84) | Fixed search URL formatting by replacing an incorrect `_include:"` pattern with `_include=` to make queries valid and consistent. |
| [#92](https://github.com/IKNL/PZP-FHIR-R4/issues/92) | Added an `ACP` prefix to all `StructureDefinition.title` elements to improve recognizability and consistency in rendered IG pages. |
| [#81](https://github.com/IKNL/PZP-FHIR-R4/issues/81) | Resolved issues in the ACP Organ Donation Choice Registration content (questionnaire/profiles/terminology as applicable). |
| [#93](https://github.com/IKNL/PZP-FHIR-R4/issues/93) | Expanded the obligations section in the IG to better explain mandatory expectations and obligation flags. |
| [#55](https://github.com/IKNL/PZP-FHIR-R4/issues/55) | Added a brief routing statement to the General API Requirements to clarify message/endpoint routing expectations. |
| [#108](https://github.com/IKNL/PZP-FHIR-R4/issues/108) | Added a role for the first contact person in the FHIR questionnaire and changed the birthdate datatype to `date`. |
| [#95](https://github.com/IKNL/PZP-FHIR-R4/issues/95) | Removed unnecessary constraints in the ACP Procedure profile to reduce over‑constraining and improve implementability. |
| [#64](https://github.com/IKNL/PZP-FHIR-R4/issues/64) | Completed or fixed missing sequence diagrams to ensure the IG documentation fully reflects expected interactions. |
| [#70](https://github.com/IKNL/PZP-FHIR-R4/issues/70) | Added or corrected references to sequence diagrams where they were missing in the documentation. |
| [#71](https://github.com/IKNL/PZP-FHIR-R4/issues/71) | Clarified the EncounterReference extension to support linking relevant resources to an Encounter. |
| [#72](https://github.com/IKNL/PZP-FHIR-R4/issues/72) | Set `provision.actor:agreementParty.role` to a fixed value `CONSENTER` for consistent interpretation. |
| [#101](https://github.com/IKNL/PZP-FHIR-R4/issues/101) | Added a reference to IHE ITI‑119 (for section 4.2 item 2) to align guidance with established interoperability practice. |
| [#7](https://github.com/IKNL/PZP-FHIR-R4/issues/7) | Restructured/rewrote IG headings and overall information architecture to improve readability and navigation. |
| [#43](https://github.com/IKNL/PZP-FHIR-R4/issues/43) | Prettified and standardized the search queries to improve clarity for implementers. |
| [#48](https://github.com/IKNL/PZP-FHIR-R4/issues/48) | Documented necessary modifications to Form Studio output to produce a valid FHIR Questionnaire. |
| [#50](https://github.com/IKNL/PZP-FHIR-R4/issues/50) | Addressed a SUSHI `ElementDefinition.base` extension issue occurring when inserting Obligation extensions. |
| [#54](https://github.com/IKNL/PZP-FHIR-R4/issues/54) | Removed outdated “Beta3 28‑08‑2025” text from the questionnaire title. |
| [#56](https://github.com/IKNL/PZP-FHIR-R4/issues/56) | Reviewed and improved the organisation of examples to make them easier to locate and interpret. |
| [#57](https://github.com/IKNL/PZP-FHIR-R4/issues/57) | Aligned STU3 value sets with R4 value sets for consistent terminology use across versions. |
| [#59](https://github.com/IKNL/PZP-FHIR-R4/issues/59) | Investigated and addressed unexpected `0..0` cardinality rendering in TreatmentDirective. |
| [#62](https://github.com/IKNL/PZP-FHIR-R4/issues/62) | Improved how impactful differences from base profiles are shown in the IG. |
| [#63](https://github.com/IKNL/PZP-FHIR-R4/issues/63) | Redesigned the Communication profile to better support the intended data capture. |
| [#74](https://github.com/IKNL/PZP-FHIR-R4/issues/74) | Explained the rationale for prefixes like F1, P1 etc. in documentation. |
| [#73](https://github.com/IKNL/PZP-FHIR-R4/issues/73) | Corrected binding to apply to `provision.text` instead of `provision.code`. |
| [#82](https://github.com/IKNL/PZP-FHIR-R4/issues/82) | Added an obligation flag for `Observation.performer`. |
#### 1.0.0-rc1

| Issue | Short Description | Changes |
|-------|-------------------|---------|
| [#44](https://github.com/IKNL/PZP-FHIR-R4/issues/44) | Replaced value set reference in Goal search query with SNOMED codes. | Updated the Goal search query to directly use SNOMED codes instead of referencing the `ACP-MedicalPolicyGoal` value set, following HL7 validation feedback. |
| [#40](https://github.com/IKNL/PZP-FHIR-R4/issues/40) | Clarified how profiles deviate from base profiles using obligation flags. | Added obligation extensions and updated IG documentation to clearly indicate which elements are relevant for the ACP/PZP use case. |
| [#37](https://github.com/IKNL/PZP-FHIR-R4/issues/37) | Adjusted Canonical URLs in the IG. | Updated the canonical URLs in the Implementation Guide to align with the hosting location and prepare for release. |
| [#31](https://github.com/IKNL/PZP-FHIR-R4/issues/31) | Moved STU3 and zib2017 examples to a separate IG. | Separated STU3-related examples and utilities into a dedicated repository to comply with HL7 IG tooling requirements. |
| [#30](https://github.com/IKNL/PZP-FHIR-R4/issues/30) | Aligned naming conventions with ART-DECOR updates. | Updated textual references to reflect new naming conventions for PZP/ACP datasets and forms; package name remains unchanged. |
| [#29](https://github.com/IKNL/PZP-FHIR-R4/issues/29) | Corrected SNOMED OID in Device value set. | Replaced the SNOMED OID with the correct URI (`http://snomed.info/sct`) in the Device value set. |
| [#28](https://github.com/IKNL/PZP-FHIR-R4/issues/28) | Moved question numbering to `item.prefix` in Questionnaire. | Updated Questionnaire items to use the `prefix` element for numbering (e.g., "1.", "a)"), improving structure and FHIR compliance. |
| [#26](https://github.com/IKNL/PZP-FHIR-R4/issues/26) | Updated terminology in treatment directive documentation. | Replaced "ja" and "nee" with "wel uitvoeren" and "niet uitvoeren" in the treatment directive documentation for clarity. |
| [#25](https://github.com/IKNL/PZP-FHIR-R4/issues/25) | Disabled Dutch translations in profiles. | Commented out the `displayLanguage` parameter to prevent automatic Dutch translations in the IG profiles. |
| [#23](https://github.com/IKNL/PZP-FHIR-R4/issues/23) | Standardized display texts in ValueSets and examples. | Updated ValueSet displays to consistently use Dutch terms without additional qualifiers, aligning with Nictiz conventions. |
| [#22](https://github.com/IKNL/PZP-FHIR-R4/issues/22) | Added Github Link to the IG's | Included links to the GitHub repository and issue tracker in both the STU3 and R4 Implementation Guides. |
| [#19](https://github.com/IKNL/PZP-FHIR-R4/issues/19) | Implemented IG publication history | history to the IG following HL7 guidelines, including setup for canonical alignment. |
| [#18](https://github.com/IKNL/PZP-FHIR-R4/issues/18) | Enabled publication of packages on Simplifier.net. | Set up a process to publish FHIR packages on Simplifier.net, with plans for future automation via pipeline. |
| [#14](https://github.com/IKNL/PZP-FHIR-R4/issues/14) | Implemented automated QA validation. | Added automated validation for R4 IG using a CI pipeline; STU3 support is pending improvements to Firely tooling. |
| [#9](https://github.com/IKNL/PZP-FHIR-R4/issues/9) | Fixed IG publisher error for STU3 caused by duplicate names. | Resolved a build error by updating resource instances and using IG Publisher v2.0.17 which handles multiple `name` elements. |
| [#45](https://github.com/IKNL/PZP-FHIR-R4/issues/45) | Define actor roles and obligations for data exchange. | Will define server and client responsibilities for supporting exchange methods, including conformance statements and enriched ActorDefinitions. |
| [#24](https://github.com/IKNL/PZP-FHIR-R4/issues/24) | Add "unknown" option to treatment directive. | Proposed solutions for both STU3 and R4 to support an "unknown" value for the Treatment directive using custom or reused extensions; examples and test data updated accordingly. |
| [#17](https://github.com/IKNL/PZP-FHIR-R4/issues/17) | Apply non-impactful textual improvements. | Updated terminology (e.g., "Palliatieve Zorg Planning" → "Proactieve Zorgplanning") and improved documentation text without affecting implementers. |
| [#15](https://github.com/IKNL/PZP-FHIR-R4/issues/15) | Fix remaining QA errors in STU3 IG. | Identified and planned fixes for unresolved QA issues in STU3 examples, primarily by improving the conversion scripts from R4. |
