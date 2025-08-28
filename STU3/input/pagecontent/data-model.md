This page provides an overview of the FHIR resources used to represent the ACP dataset, many of which are based on nl-core profiles.

### ACP Questionnaire

A patient's ACP preferences can be documented using a structured form, such as the one developed by IKNL. This implementation guide provides a corresponding <a href="Questionnaire-ACP-zib2017.html">FHIR Questionnaire resource</a> to ensure standardized and interoperable data capture.

The Questionnaire's primary function is to specify its identity and question identifiers required to capture answers in a QuestionnaireResponse. The Questionnaire is based on the ACP form dataset and aims to preserve the zib structure as much as possible. To ensure the intended meaning is preserved in both the Questionnaire and QuestionnaireResponse, some questions correspond to zib concepts with preset answer codes that are marked as readOnly. This approach tightly couples the Questionnaire and QuestionnaireResponse to the underlying zib data model. The Questionnaire is not specifically designed for direct use in a user interface, though this is possible. For optimal user interaction, the questionnaire may need customization, for example, hiding preselected and read-only questions.

Two example QuestionnaireResponse resources, based on this Questionnaire, are included:

* <a href="QuestionnaireResponse-HendrikHartman-20201001.html">QuestionnaireResponse for Hendrik Hartman (01-01-2020)</a>
* <a href="QuestionnaireResponse-HendrikHartman-20221108.html">QuestionnaireResponse for Hendrik Hartman (08-11-2022)</a>


### Associating ACP dataset to FHIR 

The FHIR profiles in this guide are directly linked to the ACP dataset elements published in ART-DECOR.

Each StructureDefinition includes a `StructureDefinition.mapping.uri` that points to the specific version of the ACP dataset used. Additionally, every element within a profile is individually mapped to its corresponding dataset element using the `ElementDefinition.mapping` property. A user-friendly rendering of these mappings is available on the "Mappings" tab of each profile page.

These mappings provide a straightforward way to highlight the elements that are especially relevant for the ACP use case, without the need to set or define mustSupport flags. As a result, the profile's differential table now shows all elements marked as relevant.

#### Note on referenced zibs

The ACP dataset is built from reusable components known as Zorginformatiebouwstenen (zibs). A zib can reference other zibs to create a comprehensive clinical picture. The ACP dataset, however, only includes the first level of these references. If a nested zib (i.e., a zib referenced by another) was not deemed essential for the primary ACP use case, it was not added to the dataset and is therefore not profiled or mapped in this guide.

Nevertheless, the FHIR profiles in this guide are based on the nl-core (zib) profiles and remain open by design. If a system contains deeper information that is not explicitly profiled in this ACP guide, it is encouraged to include it.

For example, the zib AdvanceDirective can reference the zib Problem to which the directive applies. While this guide does not define a specific ACP profile for the target Problem, this data provides important context. When including such information, systems should make it available by conforming to the general-purpose nl-core profiles for those resources.

{% include zib2017_stu3_mappings.md %}