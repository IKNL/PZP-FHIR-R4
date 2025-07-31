This page provides an overview of the FHIR resources used to represent the ACP dataset, many of which are based on nl-core profiles.

### ACP Questionnaire
A patient's ACP preferences can be captured using a structured form, such as the one developed by IKNL. This implementation guide provides a corresponding FHIR Questionnaire resource to ensure standardized data collection. [ADD link and improve] 

### FHIR Data Model Overview
The diagram below illustrates the FHIR data model for this implementation guide. To enhance clarity, the resources are grouped into four logical categories that represent key aspects of the ACP process: Agreements, Individuals, Supporting Information, and Consultation. 

* **Consultation**: Represents the core event where the advance care plan is discussed.
* **Agreements**: This category encompasses the documented outcomes of the ACP process, including the patient's goals, preferences, and formal advance directives.
* **Individuals**: Includes all persons and professional involved in the care process, such as the patient, health professionals, and the patient's designated contacts or legal representatives.
* **Supporting Information**: Provides additional clinical context relevant to the patient's agreements, such as related medical procedures or the use of specific medical devices.

{% include fhir-data-model-mermaid-diagram.md %}

### Associating ACP dataset to FHIR 

The FHIR profiles in this guide are directly traceable to the ACP dataset elements published in ART-DECOR.

Each StructureDefinition contains a mapping in `StructureDefinition.mapping.uri` that resolves to the specific version of the ACP dataset used. Furthermore, every element within a profile is individually mapped to its corresponding dataset element using the `ElementDefinition.mapping` property. A user-friendly rendering of these mappings is available on the "Mappings" tab of each profile page.

#### Note on referenced zibs

The ACP dataset is built from reusable components known as Zorginformatiebouwstenen (zibs). A zib can reference other zibs to create a comprehensive clinical picture. The ACP dataset, however, only includes the first level of these references. If a nested zib (i.e., a zib referenced by another) was not deemed essential for the primary ACP use case, it was not added to the dataset and is therefore not profiled or mapped in this guide.

Nevertheless, the FHIR profiles in this guide are based on the nl-core (zib) profiles and remain open by design. If a system contains deeper information that is not explicitly profiled in this ACP guide, it is encouraged to include it.

For example, the zib AdvanceDirective can reference the zib Problem to which the directive applies. While this guide does not define a specific ACP profile for the target Problem, this data provides important context. When including such information, systems should make it available by conforming to the general-purpose nl-core profiles for those resources.

{% include mappings.md %}