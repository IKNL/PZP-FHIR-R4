```mermaid
flowchart TB

    %% ---- Profile Definitions ----
    AdvanceDirective["`**Consent**(ACPAdvanceDirective)`"]
    ContactPerson["`**RelatedPerson**(ACPContactPerson)`"]
    Encounter["`**Encounter**(ACPEncounter)`"]
    FreedomRestrictingIntervention["`**Procedure**(ACPFreedomRestrictingIntervention)`"]
    HealthProfessionalPractitioner["`**Practitioner**(ACPHealthProfessionalPractitioner)`"]
    HealthProfessionalPractitionerRole["`**PractitionerRole**(ACPHealthProfessionalPractitionerRole)`"]
    MedicalDevice["`**DeviceUseStatement**(ACPMedicalDevice)`"]
    MedicalDeviceProductICD["`**Device**(ACPMedicalDeviceProductICD)`"]
    MedicalPolicyGoal["`**Goal**(ACPMedicalPolicyGoal)`"]
    OrganDonationChoiceRegistration["`**Observation**(ACPOrganDonationChoiceRegistration)`"]
    OtherImportantInformation["`**Observation**(ACPOtherImportantInformation)`"]
    Patient["`**Patient**(ACPPatient)`"]
    PositionRegardingEuthanasia["`**Observation**(ACPPositionRegardingEuthanasia)`"]
    PreferredPlaceOfDeath["`**Observation**(ACPPreferredPlaceOfDeath)`"]
    SpecificCareWishes["`**Observation**(ACPSpecificCareWishes)`"]
    TreatmentDirective["`**Consent**(ACPTreatmentDirective)`"]

    %% ---- Reference Definitions ----
    AdvanceDirective -- .patient --> Patient
    ContactPerson -- .patient --> Patient
    Encounter -- .participant --> ContactPerson
    Encounter -- .participant --> HealthProfessionalPractitionerRole
    Encounter -- .subject --> Patient
    FreedomRestrictingIntervention -- .subject --> Patient
    HealthProfessionalPractitionerRole -- .practitioner --> HealthProfessionalPractitioner
    MedicalDevice -- .device --> MedicalDeviceProductICD
    MedicalDevice -- .subject --> Patient
    MedicalPolicyGoal -- .subject --> Patient
    OrganDonationChoiceRegistration -- .encounter --> Encounter
    OrganDonationChoiceRegistration -- .subject --> Patient
    OtherImportantInformation -- .encounter --> Encounter
    OtherImportantInformation -- .subject --> Patient
    PositionRegardingEuthanasia -- .encounter --> Encounter
    PositionRegardingEuthanasia -- .subject --> Patient
    PreferredPlaceOfDeath -- .encounter --> Encounter
    PreferredPlaceOfDeath -- .subject --> Patient
    SpecificCareWishes -- .encounter --> Encounter
    SpecificCareWishes -- .subject --> Patient
    TreatmentDirective -- .patient --> Patient
    TreatmentDirective -- .provision.actor --> HealthProfessionalPractitionerRole
    TreatmentDirective -- .provision.actor --> Patient
```
