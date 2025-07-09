## Retrieve ACP

### QuestionaireResponse

A search on the `/QuestionnaireResponse` end point

> GET [base]/QuestionnaireResponse?questionnaire=https://fhir.iknl.nl/fhir/ACP/Questionnaire/ACP-Form



### Resources

To get all the TreatmentDirective: 

> GET [base]/Consent?scope=http://terminology.hl7.org/CodeSystem/consentscope|treatment&category=http://snomed.info/sct|129125009

To get all the AdvanceDirectives:

> GET [base]/Consent?scope=http://terminology.hl7.org/CodeSystem/consentscope|adr&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd

> GET [base]/Encounter

> GET [base]/Goal

> GET [base]/Observation?code=http://snomed.info/sct|153851000146100,395091006,340171000146104,247751003

> GET [base]/DeviceUseStatement?
> 