## Namingconventions

### Naming Segments

The naming conventions defined in this project are constructed using the following naming segments:

**[BaseURL]:** the base URL is 'https://fhir.iknl.nl/fhir/PZP/'.

**[ResourceType]:** The FHIR resource type e.g. 'StructureDefinition', 'CodeSystem', 'ConceptMap', 'Patient' or 'MedicationStatement'.

**[BusinessName]:** The business name of the concept a resource reflects.

**[ResourceTypeAbbreviation]:** A two-letter abbreviation for terminology Resources Type. For a CodeSystem this is 'CS' and for a ValueSet this is 'VS'.

**[ProfileId]:** The Profile Logical ID.

**[ActorAbbreviation]:** An abbreviation for the actor e.g. XXX is '[TO ADD]' and XXX is '[TO ADD]'.

### Profiles
The following naming conventions apply to the FHIR ACP profiles defined in this guide.

**1. Logical ID**

The **logical id** of the profile shall be in the form **[ResourceType]-ACP-[BusinessName]** e.g.
* StructureDefinition-ACP-AgreedMedicalPolicty
* StructureDefinition-ACP-Patient

**2. URL**

The **url** of the profile shall be in the form
**[BaseURL]/StructureDefinition/[ResourceType]-ACP-[BusinessName]** e.g. 
* https&#58;//https://fhir.iknl.nl/fhir/PZP/StructureDefinition/ACP-AgreedMedicalPolicty
* https&#58;//https://fhir.iknl.nl/fhir/PZP/StructureDefinition/ACP-Patient

**3. Name**

The **name** of the profile - specifically the `.name` element - shall be in the form **ACP[BusinessName]** e.g. 
* ACPAgreedMedicalPolicty
* ACPPatient

**4. Title**

The **title** of the profile - specifically the `.title` element - shall be in the form **ACP [BusinessName]** e.g. 
* ACP AgreedMedicalPolicty
* ACP Patient

**5. Filename**

The **filename** of the profile shall be in the form **[ResourceType]-ACP-[BusinessName]** e.g. 
* StructureDefinition-ACP-AgreedMedicalPolicty
* StructureDefinition-ACP-Patient
