# Profiling authoring decisions taken:

## 10/07/2025
- RelatedPerson.relationship[relationship] contains distinct codes for curator/mentor and brother/sister while the form allows only the option to select them both. From the form is not possible then to map this to FHIR as you would not know which code to use. We will use the zib codes and don't give to much credit to the form here.
- PractitionerRole - "430" "ZorgverlenerRol" is not yet implemented in the Nictiz FHIR profiles, because this is mapped in the resources that refer to the PractitionerRole. It is not mapped in PractitionerRole.code. MM: zorgverlenersrol gaat eruit, is nu ook doorgevoerd in Art-Decor. Mapping dus niet nodig
- ACPMedicalPolicyGoal - Mapping on Goal in stead of Observation.

## 22/07/2025
- ExtLegallyCapableMedicalTreatmentDecisions naming is set and extension is considerd Ok.
- Patient invariant about mandating a legal contact person when LegallyCapableMedicalTreatmentDecisions is false will become a warning
- All ContactPersons will be populated in the RelatedPerson resource, optionally in the Patient.contact field. The http://hl7.org/fhir/StructureDefinition/patient-relatedPerson extension should be used to link the contact persons.
- Patient contactgegevens is in de zib 0..1 en dataset 0..1 maar in nl core 0..* - discussed with Lonekke and ok. Leave as it profiled in nl-core.
- ACPPreferredPlaceOfDeath binding is set to extensible both in ArtDecor and FHIR.
- On the question how to distingues the Encounter that took place for ACP: we will use both Encounter and Procedure with `Procedure.code` = SNOMED CT 713603004 - Advance care planning (procedure)

## 29/07/2025
- The SNOMED code 713603004 for Medical Policy Goal in `Goal.category` is not a good fit, as it is too restrictive. Goals created outside the ACP context are also in scope. Therefore, we will not use a category code for now. Searching and retrieving Goals will be based on the input parameter for the bound ValueSet.
- PreferredPlaceOfDeath is mapped to `Observation`. Although FHIR R5 suggests using `Goal` in `CarePlan` for advance directive agreements, we have decided to continue using `Observation` for this version.
- The `Observation.dataAbsentReason` element is a suitable way to communicate unknown or not-asked information. We will add mappings to these elements as well.
- For "Afspraak uitzetten ICD (BehandelAanwijzing)", we will reuse nl-core-TreatmentDirective2 and provide additional specifications on how "Afspraak uitzetten ICD (BehandelBesluit)" maps to `Consent.provision.type` and `Consent.modifierExtension[specificationOther].value[x]`. Implementers will be directed to this profiling in the call for feedback section on the main page.
- References to externally hosted ValueSets, such as GeslachtCodelijst, are not provided correctly by the IG publisher. See: https://nictiz.atlassian.net/browse/ZIBFHIR-356. If this issue persists upon publishing, we can mitigate it by removing `ValueSet.meta.source` from the zib package.


##
- Questionnaires
    - Source of Questionnaire development is outside this IG. Therefore, Questionnaires will be saved as JSON, not as FSH.
    - Copied Questionnaire resources from IKNL form builder into input/resources with prefix "Questionnaire-"
    - Added proper metadata fields (zib2017 follows a similiar pattern)
```json
{
    "name": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "title": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "resourceType": "Questionnaire",
    "status": "draft",
    "experimental": true,
    "publisher": "",
    "copyright": "Gepubliceerd door PZNL & uitgevoerd door IKNL",
    "purpose": "",
    "description": ""
```

to

```json
{
    "id": "ACP-zib2020",
    "url": "https://fhir.iknl.nl/fhir/Questionnaire/ACP-zib2020",
    "version": "beta3-20250828",
    "name": "ACPzib2020",
    "title": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "resourceType": "Questionnaire",
    "status": "draft",
    "experimental": false,
    "publisher": "Published by PZNL & executed by IKNL",
    "contact": [
        {
            "name": "IKNL",
            "telecom": [
                {
                    "system": "email",
                    "value": "info@iknl.nl",
                    "use": "work"
                }
            ]
        }
    ],
    "copyright": "This form has been compiled with the utmost care. No rights or claims can be derived from its content, which also means that any liability for possible inaccuracies in this form, for any damage, or for other consequences arising from or related to the use of this form is excluded. Copyright and related rights waived via CC0, https://creativecommons.org/publicdomain/zero/1.0/. This does not apply to information from third parties, for example a medical terminology system. The implementer alone is responsible for identifying and obtaining any necessary licenses or authorizations to utilize third party IP in connection with the specification or otherwise.",
    "purpose": "This form was developed to clearly document agreements resulting from the proactive care planning process.",
    "description": "Standardized capture of proactive care planning (advance care planning, or ACP). This form was developed to clearly document agreements resulting from the proactive care planning process. It is NOT a checklist. It can only be completed by a healthcare provider after a professional and nuanced conversation. For advice on conducting these conversations, please refer to the guideline for proactive care planning in the palliative phase and Palliaweb. If a topic has not been discussed or if the patient does not yet have an opinion, please fill in "not yet known." When transferring to a long-term care setting, consider adding conversation records about proactive care planning to the transfer documents.",
    "code": [
        {
            "code": "713603004",
            "system": "http://snomed.info/sct",
            "display": "Advance care planning (procedure)"
        }
    ],
```