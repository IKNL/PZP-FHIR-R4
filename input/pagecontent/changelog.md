
### Change Log

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
