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
    - Added proper metadata fields (zib2017 follows a similiar pattern) -> see two json structures below for more details.
    - Copied Questionnaire resources from IKNL form builder into input/resources with prefix "Questionnaire-"[id]-[version]
    - Using https://formbuilder.nlm.nih.gov/ fix the conditional expressions in the Questionnaires. It goes wrong for all Booleans apperantly. So the conditional display for 5.2.6 e) Naam eerste contactpersoon neesd to be set so that: 
     5.2.5 - d) Is de wettelijk vertegenwoordiger ook de eerste contactpersoon? = Nee (0)
    - Need to set conditional expression for "Afspraak uitzetten ICD (BehandelBesluit)" on  "h) Heeft de patiënt een ICD?"
    - Using https://formbuilder.nlm.nih.gov/ set all the measurement names and 'behandeling' readonly and initial value selected

    ```json
    {
          "type": "choice",
          "linkId": "1408",
          "text": "Belangrijkste doel van behandeling ([MetingNaam])",
          "required": false,
          "repeats": false,
          "readOnly": true,
          "answerOption": [
            {
              "valueCoding": {
                "system": "http://snomed.info/sct",
                "code": "180771000146100",
                "display": "Focus van behandeling (waarneembare entiteit)"
              },
              "initialSelected": true
            }
          ]
        },
    ``` 


    
```json
{
{
    "name": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "title": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "resourceType": "Questionnaire",
    "status": "draft",
    "item": [
    ---snip---   
    ],
    "experimental": true,
    "publisher": "Gepubliceerd door PZNL & uitgevoerd door IKNL | Published by PZNL & executed by IKNL",
    "copyright": "Op dit formulier is copyright, gebruikersrechten en een disclaimer van toepassing, zoals die gespecificeerd zijn voor alle informatiestandaarden van IKNL, zie voor de details het onderdeel Gebruikersrechten en disclaimer op https://iknl.nl/onderzoek/eenheid-van-taal. | \nThis form is subject to copyright, user rights and a disclaimer, as specified for all IKNL information standards. For details, see the paragraph on Gebruikersrechten en disclaimer at https://iknl.nl/onderzoek/eenheid-van-taal.",
    "purpose": "Dit formulier is ontwikkeld om afspraken voortkomend uit het proces van proactieve zorgplanning (PZP) eenduidig vast te leggen. | \nThis form was developed to clearly document agreements resulting from the advance care planning (ACP) process.",
    "description": "Dit formulier is ontwikkeld om afspraken voortkomend uit het proces van proactieve zorgplanning (PZP) eenduidig vast te leggen. Het is GEEN afvinklijst. Het kan alleen na deskundig en genuanceerd gesprek door een zorgverlener worden ingevuld. Voor adviezen over het voeren van deze gesprekken word verwezen naar de richtlijn proactieve zorgplanning in de palliatieve fase en Palliaweb, zie https://palliaweb.nl/zorgpraktijk/proactieve-zorgplanning. \nVul 'nog onbekend' in als een onderwerp niet is besproken of als de patiënt (nog) geen mening heeft. Overweeg bij overplaatsing naar een langdurige zorgsetting gespreksverslagen over proactieve zorgplanning aan de overdracht toe te voegen. | \nThis form was developed to clearly document agreements resulting from the advance care planning (ACP) process. It is NOT a checklist. It can only be completed by a healthcare provider after a professional and nuanced conversation. For advice on conducting these conversations, please refer to the guideline for proactive care planning in the palliative phase and Palliaweb, see https://palliaweb.nl/zorgpraktijk/proactieve-zorgplanning. \nEnter 'unknown' if a topic is not discussed or if the patient does not (yet) have an opinion.When transferring to a long-term care setting, consider adding conversation records about advance care planning (ACP) to the transfer documents."
}
```

to

```json
{
    "id": "ACP-zib2020",
    "url": "https://api.iknl.nl/docs/r4/pzp/Questionnaire/ACP-zib2020",
    "version": "beta3-20250828",
    "name": "ACPzib2020",    
    "title": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "resourceType": "Questionnaire",
    "status": "draft",
    "experimental": true,
    "publisher": "Published by PZNL & executed by IKNL",
    "copyright": "This form is subject to copyright, user rights and a disclaimer, as specified for all IKNL information standards. For details, see the paragraph on Gebruikersrechten en disclaimer at https://iknl.nl/onderzoek/eenheid-van-taal.",
    "purpose": "This form was developed to clearly document agreements resulting from the advance care planning (ACP) process.",
    "description": "This form was developed to clearly document agreements resulting from the advance care planning (ACP) process. It is NOT a checklist. It can only be completed by a healthcare provider after a professional and nuanced conversation. For advice on conducting these conversations, please refer to the guideline for proactive care planning in the palliative phase and Palliaweb, see https://palliaweb.nl/zorgpraktijk/proactieve-zorgplanning. \nEnter 'unknown' if a topic is not discussed or if the patient does not (yet) have an opinion.When transferring to a long-term care setting, consider adding conversation records about advance care planning (ACP) to the transfer documents.",
    
```