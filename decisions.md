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