Instance: ACPActorProviderCapabilityStatement
InstanceOf: CapabilityStatement
Usage: #definition
* url = "https://api.iknl.nl/docs/pzp/r4/CapabilityStatement/ACP-ActorProviderCapabilityStatement"
* name = "ACPActorProviderCapabilityStatement"
* title = "ACP Actor Provider CapabilityStatement"
* description = "This CapabilityStatement describes the basic rules for the [ACP Actor Provider](ActorDefinition-ACPActorProvider.html) that is responsible for providing responses to queries submitted by ACP Consultors. The complete list of FHIR profiles, RESTful operations, and search parameters supported by ACP Actor Providers are defined in this CapabilityStatement."
* insert MetaRulesDefinitionalArtifact

* kind = #requirements
* fhirVersion = #4.0.1
* format[0] = #json
  * extension
    * url = "$CapExpectation"
    * valueCode = #SHALL
* format[+] = #xml
  * extension
    * url = "$CapExpectation"
    * valueCode = #SHALL
* rest
  * mode = #server
  * documentation = "TODO"
  * security.description = "Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data. The exact methods may be found in the used infrastructure specification and agreements of e.g. LSP, Twiin and or Nuts."
  * resource[0]

    // ENCOUNTER RESOURCE
    * extension
      * url = "$CapExpectation"
      * valueCode = #SHOULD
    * type = #Encounter
    * supportedProfile = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Encounter"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "reason-reference"
      * definition = "http://hl7.org/fhir/SearchParameter/Encounter-reason-reference"
      * type = #reference
      * documentation = "The provider **SHOULD** support chained search Procedure.code using the SNOMED CT code as defined in the ACP Procedure profile."
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-patient"
      * type = #reference
    * searchInclude[0] = "Encounter:reason-reference"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD

  // PROCEDURE RESOURCE
  * resource[+]
    * extension
      * url = "$CapExpectation"
      * valueCode = #SHOULD
    * type = #Procedure
    * supportedProfile = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Procedure"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "code"
      * definition = "http://hl7.org/fhir/SearchParameter/Procedure-code"
      * type = #token
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/Procedure-subject"
      * type = #reference
    * searchInclude[0] = "Procedure:encounter"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD

  // CONSENT RESOURCE 
  * resource[+]
    * extension
      * url = "$CapExpectation"
      * valueCode = #SHOULD
    * type = #Consent
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-AdvanceDirective"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD 
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-TreatmentDirective"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "scope"
      * definition = "http://hl7.org/fhir/SearchParameter/Consent-scope"
      * type = #token
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/Consent-category"
      * type = #token
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-patient"
      * type = #reference
    * searchInclude[0] = "Consent:actor"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD

  // GOAL RESOURCE 
  * resource[+]
    * extension
      * url = "$CapExpectation"
      * valueCode = #SHOULD
    * type = #Goal
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Medical-Policy-Goal"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "description"
      * definition = "http://hl7.org/fhir/SearchParameter/Goal-description"
      * type = #token
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-patient"
      * type = #reference
    * searchInclude[0] = "Consent:actor"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD


  // OBSERVATION RESOURCE 
  * resource[+]
    * extension
      * url = "$CapExpectation"
      * valueCode = #SHOULD
    * type = #Observation
    // Supported profiles for Observation resource are set to SHOULD because not all Observation have to be implemented.
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-OrganDonationChoiceRegistration"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD 
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-OtherImportantInformation"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PositionRegardingEuthanasia"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PreferredPlaceOfDeath"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PreferredPlaceOfDeath"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "code"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-code"
      * type = #token
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-patient"
      * type = #reference


  // DeviceUseStatement RESOURCE 
  * resource[+]
    * extension
      * url = "$CapExpectation"
      * valueCode = #SHOULD
    * type = #DeviceUseStatement
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalDevice"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "device"
      * definition = "http://hl7.org/fhir/SearchParameter/DeviceUseStatement-device"
      * type = #reference
    * searchParam[+]
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-patient"
      * type = #reference
    * searchInclude[0] = "DeviceUseStatement:device"
      * extension
        * url = "$CapExpectation"
        * valueCode = #SHOULD

