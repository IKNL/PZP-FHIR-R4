### 1.0.0-rc3
| Issue | Short Description |
|-------|-------------------|
| [#137](https://github.com/IKNL/PZP-FHIR-R4/issues/137) | Replaced legally capable extension on Patient with an Observation to better support representation of legal capacity. |
| [#132](https://github.com/IKNL/PZP-FHIR-R4/issues/132) | Updated `Procedure.code` to support multiple ACP procedure codes and ensure compliance with zib/nl-core terminology requirements. |
| [#157](https://github.com/IKNL/PZP-FHIR-R4/issues/157) | Updated CommunicationRequest cardinalities by requiring `subject`, `requester` and `sender`, and adding an invariant to ensure either `authoredOn` or a reference to Encounter. |
| [#151](https://github.com/IKNL/PZP-FHIR-R4/issues/151) | Corrected search URLs by fixing code parameter syntax to ensure proper OR behavior. |
| [#136](https://github.com/IKNL/PZP-FHIR-R4/issues/136) | Improved search query documentation by clarifying how to retrieve specific data items such as ContactPerson (e.g. legal representative). |
| [#135](https://github.com/IKNL/PZP-FHIR-R4/issues/135) | Updated questionnaire answer options to use `answerValueSet` references where possible and improve alignment with terminology, resolving validation issues. |
| [#138](https://github.com/IKNL/PZP-FHIR-R4/issues/138) | Updated a couple questionnaire items from `choice` to `boolean` to resolve validation issues and align with the dataset. |
| [#126](https://github.com/IKNL/PZP-FHIR-R4/issues/126) | Updated questionnaire to align with latest dataset changes, including support for 'other' treatment directives and addition of missing 'MeetMethode' elements. |
| [#131](https://github.com/IKNL/PZP-FHIR-R4/issues/131) | Replaced fixed questionnaire answer options for 'Functie (specialisme)' with AGB and UZI value sets. |
| [#138](https://github.com/IKNL/PZP-FHIR-R4/issues/138) | Updated yes/no questions in the questionnaire to use `boolean` instead of `choice`. |
| [#133](https://github.com/IKNL/PZP-FHIR-R4/issues/133) | Aligned API documentation by correcting CommunicationRequest category code in sequence diagram and updating CapabilityStatement to use CommunicationRequest. |
| [#129](https://github.com/IKNL/PZP-FHIR-R4/issues/129) | Clarified ContactPerson artifact documentation for `.relationship:roleAdditional` slice. |
| [#127](https://github.com/IKNL/PZP-FHIR-R4/issues/127) | Added missing `subject` references to QuestionnaireResponse examples and improved consistency of author/source formatting. |
| [#156](https://github.com/IKNL/PZP-FHIR-R4/issues/156) | Applied QA fixes including ValueSet renaming to avoid duplicate titles. |

### 1.0.0-rc2

| Issue | Short Description |
|-------|-------------------|
| [#90](https://github.com/IKNL/PZP-FHIR-R4/issues/90) | Refined the Medical Policy Goal profile by adding an ACP-specific SNOMED category, updating search parameters to use category-based retrieval and including the ‘unknown’ option to the valueset. |
| [#83](https://github.com/IKNL/PZP-FHIR-R4/issues/83) | Aligned the `ACP‑OtherImportantInformation` profile metadata with the intended SNOMED concept by renaming the profile to `ACPSenseOfPurpose`, updating identity elements for consistency. |
| [#84](https://github.com/IKNL/PZP-FHIR-R4/issues/84) | Corrected invalid `_include:` syntax in multiple search URLs and aligned all queries by standardizing the use of  `subject=Patient/[id]` notation.|
| [#92](https://github.com/IKNL/PZP-FHIR-R4/issues/92) | Added an `ACP` prefix to all `StructureDefinition.title` elements. |
| [#81](https://github.com/IKNL/PZP-FHIR-R4/issues/81) | Added `Observation.method.code` to clarify that the organ‑donation finding is patient‑reported and improved description.|
| [#93](https://github.com/IKNL/PZP-FHIR-R4/issues/93) | Expanded and refined the obligations guidance in the IG by adding the missing obligation flag for `Consent.provision.code` in the TreatmentDirective, and clarifying the overall obligation design principles and mapping approach.|
| [#55](https://github.com/IKNL/PZP-FHIR-R4/issues/55) | Added a brief routing statement to the General API Requirements to clarify message/endpoint routing expectations. |
| [#95](https://github.com/IKNL/PZP-FHIR-R4/issues/95) | Added the missing `role` field for the first contact person in the FHIR questionnaire and updated the birthdate datatype from `dateTime` to `date`.|
| [#64](https://github.com/IKNL/PZP-FHIR-R4/issues/64) | Removed unnecessary constraints on `Procedure.performer.actor` in the ACP Procedure profile.|
| [#70](https://github.com/IKNL/PZP-FHIR-R4/issues/70) | Addedd data‑exchange sequence diagrams. |
| [#71](https://github.com/IKNL/PZP-FHIR-R4/issues/71) | Removed the `EncounterReference` extension |
| [#101](https://github.com/IKNL/PZP-FHIR-R4/issues/101) | Added a reference to IHE‑ITI‑119 as an example mechanism for obtaining the Patient ID. |
| [#43](https://github.com/IKNL/PZP-FHIR-R4/issues/43) | Prettified and standardized the search queries. |
| [#50](https://github.com/IKNL/PZP-FHIR-R4/issues/50) | Fixed incorrect handling of obligation extensions. |
| [#54](https://github.com/IKNL/PZP-FHIR-R4/issues/54) | Removed the outdated `Beta3 28‑08‑2025` from the questionnaire title. |
| [#56](https://github.com/IKNL/PZP-FHIR-R4/issues/56) | Reorganized the R4 and STU3 example sets for consistency and aligned naming across all examples. |
| [#59](https://github.com/IKNL/PZP-FHIR-R4/issues/59) | Improved rendering of advance directive extension in the IG. |
| [#62](https://github.com/IKNL/PZP-FHIR-R4/issues/62) | Improved how impactful differences from base profiles are shown in the IG. |
| [#63](https://github.com/IKNL/PZP-FHIR-R4/issues/63) | Redesigned Communication profile into CommunicationRequest profile. |
| [#73](https://github.com/IKNL/PZP-FHIR-R4/issues/73) | Corrected typo in comment provision.code.text. |
| [#82](https://github.com/IKNL/PZP-FHIR-R4/issues/82) | Added an obligation flag for `Observation.performer`. |
| [#99](https://github.com/IKNL/PZP-FHIR-R4/issues/99) | Made all ICD SNOMED codes explicit in the ValueSet ACP-MedicalDeviceProductType-ICD and search URLs to reduce implementation burden. | 
| [#107](https://github.com/IKNL/PZP-FHIR-R4/issues/107) | Added the missing contact‑person role code `310141000146103` for "schriftelijk gemachtigde" and relaxed the cardinality constraints. |
| [#113](https://github.com/IKNL/PZP-FHIR-R4/issues/113) | Removed incorrect uses of `Questionnaire.item.code` and cleaned up all item code fields. |
|[#91](https://github.com/IKNL/PZP-FHIR-R4/issues/91)  | Updated the IG text and homepage to clearly separate the STU3/zib2017 and R4/zib2020 versions.|

### 1.0.0-rc1

| Issue | Short Description |
|-------|---------|
| [#44](https://github.com/IKNL/PZP-FHIR-R4/issues/44) | Updated the Goal search query to directly use SNOMED codes instead of referencing the `ACP-MedicalPolicyGoal` value set, following HL7 validation feedback. |
| [#40](https://github.com/IKNL/PZP-FHIR-R4/issues/40) | Added obligation extensions and updated IG documentation to clearly indicate which elements are relevant for the ACP/PZP use case. |
| [#37](https://github.com/IKNL/PZP-FHIR-R4/issues/37) | Updated the canonical URLs in the Implementation Guide to align with the hosting location and prepare for release. |
| [#31](https://github.com/IKNL/PZP-FHIR-R4/issues/31) | Separated STU3-related examples and utilities into a dedicated repository to comply with HL7 IG tooling requirements. |
| [#30](https://github.com/IKNL/PZP-FHIR-R4/issues/30) | Updated textual references to reflect new naming conventions for PZP/ACP datasets and forms; package name remains unchanged. |
| [#29](https://github.com/IKNL/PZP-FHIR-R4/issues/29) | Replaced the SNOMED OID with the correct URI (`http://snomed.info/sct`) in the Device value set. |
| [#28](https://github.com/IKNL/PZP-FHIR-R4/issues/28) | Updated Questionnaire items to use the `prefix` element for numbering (e.g., "1.", "a)"), improving structure and FHIR compliance. |
| [#26](https://github.com/IKNL/PZP-FHIR-R4/issues/26) | Replaced "ja" and "nee" with "wel uitvoeren" and "niet uitvoeren" in the treatment directive documentation for clarity. |
| [#25](https://github.com/IKNL/PZP-FHIR-R4/issues/25) | Commented out the `displayLanguage` parameter to prevent automatic Dutch translations in the IG profiles. |
| [#23](https://github.com/IKNL/PZP-FHIR-R4/issues/23) | Updated ValueSet displays to consistently use Dutch terms without additional qualifiers, aligning with Nictiz conventions. |
| [#22](https://github.com/IKNL/PZP-FHIR-R4/issues/22) | Included links to the GitHub repository and issue tracker in both the STU3 and R4 Implementation Guides. |
| [#19](https://github.com/IKNL/PZP-FHIR-R4/issues/19) | History to the IG following HL7 guidelines, including setup for canonical alignment. |
| [#18](https://github.com/IKNL/PZP-FHIR-R4/issues/18) | Set up a process to publish FHIR packages on Simplifier.net, with plans for future automation via pipeline. |
| [#14](https://github.com/IKNL/PZP-FHIR-R4/issues/14) | Added automated validation for R4 IG using a CI pipeline; STU3 support is pending improvements to Firely tooling. |
| [#9](https://github.com/IKNL/PZP-FHIR-R4/issues/9) | Resolved a build error by updating resource instances and using IG Publisher v2.0.17 which handles multiple `name` elements. |
| [#45](https://github.com/IKNL/PZP-FHIR-R4/issues/45) | Will define server and client responsibilities for supporting exchange methods, including conformance statements and enriched ActorDefinitions. |
| [#24](https://github.com/IKNL/PZP-FHIR-R4/issues/24) | Proposed solutions for both STU3 and R4 to support an "unknown" value for the Treatment directive using custom or reused extensions; examples and test data updated accordingly. |
| [#17](https://github.com/IKNL/PZP-FHIR-R4/issues/17) | Updated terminology (e.g., "Palliatieve Zorg Planning" → "Proactieve Zorgplanning") and improved documentation text without affecting implementers. |
| [#15](https://github.com/IKNL/PZP-FHIR-R4/issues/15) | Identified and planned fixes for unresolved QA issues in STU3 examples, primarily by improving the conversion scripts from R4. |
