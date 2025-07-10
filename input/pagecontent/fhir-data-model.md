To provide guidance on how to map ACP data concepts to HL7 FHIR, several ACP profiles have been created. These profiles have a traceable relationship with their ART-DECOR dataset counterpart(s) based on the element mapping mechanism in FHIR. The version of the ART-DECOR dataset used for the mapping is registered in the `StructureDefinition.mapping.identity` element. To relate a FHIR profile element to a concept from the ART-DECOR dataset, the item ID is defined in the `ElementDefinition.mapping`. 

The diagram below shows the FHIR data model. It provides an overview which FHIR profiles are needed and how they’re connected for collecting and processing ACP data. Since the data model is fairly complex with many links between profiles, the data model is divided into three categories: **ACP Consultation**, **ACP Agreements**, and **Supporting Information**.

The **ACP Consultation** theme captures the interaction where a patient's wishes and agreements related to advance care planning are discussed. This consultation may occur in various forms and at different times. In some cases, instead of a direct conversation, a structured questionnaire may be used to collect the same information i.e. the ACP questionnaire developed by IKNL.

Profiles under the **ACP Agreements** theme capture specific advance care planning wishes or positions that have been discussed and agreed upon during an ACP consultation. The way this information is collected determines which FHIR profiles are used to represent it:
* When the information is collected through a conversation, the relevant data is captured in using various resources e.g. Observations and Communication, depending on the nature of the information.

* When the information is collected through completion of the ACP questionnaire, the resulting data is represented using the QuestionnaireResponse resource.

Both approaches achieve the same goal of documenting the patient's ACP wishes.

The **Supporting Information** theme includes all contextual information about the individuals involved in the ACP Consultation and Agreements.


<a href="fhir-data-model-mermaid-diagram.html">FHIR data model diagram</a>


### ACP Consultation
#### ACP Encounter
The ACP Encounter [ADD link] profile captures details of the conversation regarding a patient’s advance care planning (ACP) wishes and preferences. It connects the participants involved with the outcomes arising from the conversation. The ACP Consultation profile is currently the only profile falling under this category.

### Supporting Information
The ACP Patient, Practitioner(Role), and RelatedPerson profiles are used to capture administrative information about the patient, the healthcare provider, and any other individuals accompanying the patient throughout their care journey. They are all derived from the nl core profiles.

### ACP Form
As mentioned previously, a patient's ACP agreements and wishes can be captured through the completion of a structured questionnaire. IKNL has developed such a questionnaire, designed to capture all relevant aspects of a patient’s advance care planning preferences. This is implemented as a dedicated FHIR Questionnaire instance.

The FHIR Questionnaire defines a structured set of questions, along with standardized answer options using appropriate terminology, to guide consistent and complete data collection in accordance with the ACP Form. [ADD link]

Please note that, within the current data model design, the Questionnaire resource is not technically indispensable for the collection and exchange of ACP data. As the other available resources can be used as well. Nevertheless, leveraging the Questionnaire instance for ACP data collection offers a significant advantage in terms of standardised and structured formatting. Each question within the ACP form is encapsulated within the Questionnaire, uniquely identified by the Question Reference mapped to the `.item.linkId` elements. This allows access to all definitions in a programmer-friendly manner.

It is important to note that the Questionnaire instances provide limited capabilities around rendering in the user interface of the PROMs provider platform. For example, the instances do not provide instructions on how questions should be displayed or how users should navigate through them.


### Mapping ArtDecor dataset to FHIR


<a href="mappings.html">Mappings</a>
