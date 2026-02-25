Instance: ACP-CapabilityStatementProvider
InstanceOf: CapabilityStatement
Usage: #definition
* url = "https://api.iknl.nl/docs/pzp/r4/CapabilityStatement/ACP-CapabilityStatementProvider"
* name = "ACPCapabilityStatementProvider"
* title = "ACP CapabilityStatement Provider"
* description = "This CapabilityStatement describes the rules for the [ACP Actor Provider](ActorDefinition-ACPActorProvider.html) that is responsible for providing responses to queries submitted by ACP Consultors."
* insert MetaRulesDefinitionalArtifact

* kind = #requirements
* fhirVersion = #4.0.1
* format[0] = #json
  * extension
    * url = $CapExpectation
    * valueCode = #SHALL
* format[+] = #xml
  * extension
    * url = $CapExpectation
    * valueCode = #SHALL
* rest
  * mode = #server
  * documentation = "The ACP Provider **SHALL**:
* Support at least the QuestionnaireResponse resource, or as many of the other resources defined in this CapabilityStatement for which the Provider has information available.
* Implement the RESTful behaviour according to the FHIR specification.
* Support both JSON and XML formats for all ACP resource interactions.
* Declare a CapabilityStatement identifying the list of profiles, operations, and search parameters supported.
"
  * security.description = "Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data. The exact methods may be found in the used infrastructure specification and agreements of e.g. LSP, Twiin and or Nuts."

  // ENCOUNTER RESOURCE  
  * resource[0]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Encounter
    * supportedProfile = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Encounter"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "reason-reference"
      * definition = "http://hl7.org/fhir/SearchParameter/Encounter-reason-reference"
      * type = #reference
      * documentation = "The provider **SHOULD** support chained search Procedure.code using the SNOMED CT code as defined in the ACP Procedure profile."
    * searchInclude[0] = "Encounter:reason-reference"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // PROCEDURE RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Procedure
    * supportedProfile = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Procedure"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "code"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-code"
      * type = #token
    * searchInclude[0] = "Procedure:encounter"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // CONSENT RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Consent
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-AdvanceDirective"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-TreatmentDirective"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "scope"
      * definition = "http://hl7.org/fhir/SearchParameter/Consent-scope"
      * type = #token
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/Consent-category"
      * type = #token
    * searchInclude[0] = "Consent:actor"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // GOAL RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Goal
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalPolicyGoal"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/Goal-category"
      * type = #token


  // OBSERVATION RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Observation
    // Supported profiles for Observation resource are set to SHOULD because not all Observation have to be implemented.
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-OrganDonationChoiceRegistration"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-SenseOfPurpose"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PositionRegardingEuthanasia"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PreferredPlaceOfDeath"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-SpecificCareWishes"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "code"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-code"
      * type = #token

  // DEVICEUSESTATEMENT RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #DeviceUseStatement
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalDevice"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "device"
      * definition = "http://hl7.org/fhir/SearchParameter/DeviceUseStatement-device"
      * type = #reference
      * documentation = "The provider **SHOULD** support chained search Device.type using the codes as defined in the ACP Procedure profile."
    * searchInclude[0] = "DeviceUseStatement:device"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // DEVICE RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Device
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalDevice.Product-ICD"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "type"
      * definition = "http://hl7.org/fhir/SearchParameter/Device-type"
      * type = #token
      * documentation = "The provider **SHALL** support the modifier `:in` to filter on codes defined in the ValueSet bound to type element in the ACP-MedicalDevice.Product-ICD profile."
    * searchInclude[0] = "DeviceUseStatement:device"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // COMMUNICATIONREQUEST RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #CommunicationRequest
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-InformRelativesRequest"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/CommunicationRequest-category"
      * type = #token      
  
  // RELATEDPERSON RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #RelatedPerson
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-ContactPerson"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD   

  // PRACTITIONER RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Practitioner
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-HealthProfessional-Practitioner"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD   

  // PRACTITIONERROLE RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #PractitionerRole
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-HealthProfessional-PractitionerRole"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD   

  // PATIENT RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #Patient
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Patient"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD  

  // QUESTIONNARIERESPONSE RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHOULD
    * type = #QuestionnaireResponse
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/QuestionnaireResponse-patient"
      * type = #reference
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "questionnaire"
      * definition = "http://hl7.org/fhir/SearchParameter/QuestionnaireResponse-questionnaire"
      * type = #reference
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD  

Instance: ACP-CapabilityStatementConsulter
InstanceOf: CapabilityStatement
Usage: #definition
* url = "https://api.iknl.nl/docs/pzp/r4/CapabilityStatement/ACP-CapabilityStatementConsulter"
* name = "ACPCapabilityStatementConsulter"
* title = "ACP CapabilityStatement Consulter"
* description = "This CapabilityStatement describes the rules for the [ACP Actor Consulter](ActorDefinition-ACPActorConsulter.html) that is responsible for providing responses to queries submitted by ACP Consultors."
* insert MetaRulesDefinitionalArtifact

* kind = #requirements
* fhirVersion = #4.0.1
* format[0] = #json
  * extension
    * url = $CapExpectation
    * valueCode = #SHOULD
* format[+] = #xml
  * extension
    * url = $CapExpectation
    * valueCode = #SHOULD
* rest
  * mode = #client
  * documentation = " The ACP Consulter **SHALL**:
* Support all ACP resource interactions as defined in this CapabilityStatement.
* Implement the RESTful behaviour according to the FHIR specification.
* Support JSON and/or XML formats for all ACP resource interactions.
"
  * security.description = "Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data. The exact methods may be found in the used infrastructure specification and agreements of e.g. LSP, Twiin and or Nuts."

  // ENCOUNTER RESOURCE  
  * resource[0]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Encounter
    * supportedProfile = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Encounter"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "reason-reference"
      * definition = "http://hl7.org/fhir/SearchParameter/Encounter-reason-reference"
      * type = #reference
      * documentation = "The provider **SHOULD** support chained search Procedure.code using the SNOMED CT code as defined in the ACP Procedure profile."
    * searchInclude[0] = "Encounter:reason-reference"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // PROCEDURE RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Procedure
    * supportedProfile = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Procedure"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "code"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-code"
      * type = #token
    * searchInclude[0] = "Procedure:encounter"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // CONSENT RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Consent
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-AdvanceDirective"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-TreatmentDirective"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "scope"
      * definition = "http://hl7.org/fhir/SearchParameter/Consent-scope"
      * type = #token
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/Consent-category"
      * type = #token
    * searchInclude[0] = "Consent:actor"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // GOAL RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Goal
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalPolicyGoal"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/Goal-category"
      * type = #token

  // OBSERVATION RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Observation
    // Supported profiles for Observation resource are set to SHOULD because not all Observation have to be implemented.
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-OrganDonationChoiceRegistration"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-SenseOfPurpose"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PositionRegardingEuthanasia"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PreferredPlaceOfDeath"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-SpecificCareWishes"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "code"
      * definition = "http://hl7.org/fhir/SearchParameter/clinical-code"
      * type = #token

  // DEVICEUSESTATEMENT RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #DeviceUseStatement
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalDevice"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "device"
      * definition = "http://hl7.org/fhir/SearchParameter/DeviceUseStatement-device"
      * type = #reference
      * documentation = "The provider **SHALL** support chained search Device.type using the codes as defined in the ACP Procedure profile."
    * searchInclude[0] = "DeviceUseStatement:device"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // DEVICE RESOURCE 
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Device
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-MedicalDevice.Product-ICD"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "type"
      * definition = "http://hl7.org/fhir/SearchParameter/Device-type"
      * type = #token
      * documentation = "The provider **SHALL** support the modifier `:in` to filter on codes defined in the ValueSet bound to type element in the ACP-MedicalDevice.Product-ICD profile."
    * searchInclude[0] = "DeviceUseStatement:device"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD

  // COMMUNICATIONREQUEST RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Communication
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-InformRelativesRequest"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * insert CapabilityStatementSearchParmeterClinicalPatientExpectation
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "category"
      * definition = "http://hl7.org/fhir/SearchParameter/CommunicationRequest-category"
      * type = #token      

  // RELATEDPERSON RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #RelatedPerson
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-ContactPerson"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD   

  // PRACTITIONER RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Practitioner
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-HealthProfessional-Practitioner"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD   

  // PRACTITIONERROLE RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #PractitionerRole
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-HealthProfessional-PractitionerRole"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD   

  // PATIENT RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #Patient
    * supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Patient"
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD 
    * interaction[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * code = #read
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD  

  // QUESTIONNARIERESPONSE RESOURCE
  * resource[+]
    * extension
      * url = $CapExpectation
      * valueCode = #SHALL
    * type = #QuestionnaireResponse
    * insert CapabilityStatementInteractionandReferencePolicyExpectation
    * searchParam[0]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "patient"
      * definition = "http://hl7.org/fhir/SearchParameter/QuestionnaireResponse-patient"
      * type = #reference
    * searchParam[+]
      * extension
        * url = $CapExpectation
        * valueCode = #SHALL
      * name = "questionnaire"
      * definition = "http://hl7.org/fhir/SearchParameter/QuestionnaireResponse-questionnaire"
      * type = #reference
    * referencePolicy = #resolves
      * extension
        * url = $CapExpectation
        * valueCode = #SHOULD  