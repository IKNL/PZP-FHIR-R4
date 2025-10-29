Instance: ACPActorProviderCapabilityStatement
InstanceOf: CapabilityStatement
Usage: #definition
* url = "http://hl7.org.au/fhir/core/CapabilityStatement/au-core-responder"
* version = "2.0.0-ci-build"
* name = "ACPActorProviderCapabilityStatement"
* title = "ACP Actor Provider CapabilityStatement"
* insert MetaRulesDefinitionalArtifact
* description = "This CapabilityStatement describes the basic rules for the [ACP Actor Provider](ActorDefinition-ACPActorProvider.html) that is responsible for providing responses to queries submitted by ACP Consultors. The complete list of FHIR profiles, RESTful operations, and search parameters supported by ACP Actor Providers are defined in this CapabilityStatement."

* kind = #requirements
* fhirVersion = #4.0.1
* format[0] = #json
* format[+] = #xml
* format[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* format[=].extension.valueCode = #SHALL
* format[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* format[=].extension.valueCode = #SHOULD
// * implementationGuide[0] = "http://nictiz.nl/fhir/StructureDefinition/nl-core"
// * implementationGuide[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
// * implementationGuide[=].extension.valueCode = #SHALL

* rest.mode = #server
* rest.documentation = "TODO"
* rest.security.description = "Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data. The exact methods may be found in the used infrastructure specification and agreements of e.g. LSP, Twiin and or Nuts."

* rest.resource[0].extension[0].url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].extension[=].valueCode = #SHALL


* rest.resource[=].type = #Encounter
* rest.resource[=].supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-Encounter"
* rest.resource[=].supportedProfile[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].supportedProfile[=].extension.valueCode = #SHALL
* rest.resource[=].interaction[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].interaction[=].extension.valueCode = #SHALL
* rest.resource[=].interaction[=].code = #read
* rest.resource[=].interaction[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].interaction[=].extension.valueCode = #SHALL
* rest.resource[=].interaction[=].code = #search-type
* rest.resource[=].referencePolicy = #resolves
* rest.resource[=].referencePolicy.extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].referencePolicy.extension.valueCode = #SHOULD


* rest.resource[=].searchParam[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].searchParam[=].extension.valueCode = #SHALL
* rest.resource[=].searchParam[=].name = "reason-reference"
* rest.resource[=].searchParam[=].definition = "http://hl7.org/fhir/SearchParameter/Encounter-reason-reference"
* rest.resource[=].searchParam[=].type = #reference
* rest.resource[=].searchParam[=].documentation = "The consulter **SHALL** provide at least an id value and **MAY** provide both the Type and id values.\n\nThe responder **SHALL** support both."
* rest.resource[=].searchParam[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].searchParam[=].extension.valueCode = #SHALL
* rest.resource[=].searchParam[=].name = "patient"
* rest.resource[=].searchParam[=].definition = "http://hl7.org.au/fhir/core/SearchParameter/au-core-clinical-patient"
* rest.resource[=].searchParam[=].type = #reference
* rest.resource[=].searchParam[=].documentation = "The consulter **SHALL** provide at least an id value and **MAY** provide both the Type and id values.\n\nThe responder **SHALL** support both.\n\nThe consulter **SHOULD** support chained search patient.identifier using IHI, Medicare Number, and DVA Number identifiers as defined in the AU Core Patient profile.\n\nThe responder **SHOULD** support chained search patient.identifier using IHI, Medicare Number, and DVA Number identifiers as defined in the AU Core Patient profile."
* rest.resource[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].extension.valueCode = #SHOULD
* rest.resource[=].type = #Observation
* rest.resource[=].supportedProfile[0] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-OrganDonationChoiceRegistration"
* rest.resource[=].supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-OtherImportantInformation"
* rest.resource[=].supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PositionRegardingEuthanasia"
* rest.resource[=].supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PreferredPlaceOfDeath"
* rest.resource[=].supportedProfile[+] = "https://api.iknl.nl/docs/pzp/r4/StructureDefinition/ACP-PreferredPlaceOfDeath"
* rest.resource[=].supportedProfile[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].supportedProfile[=].extension.valueCode = #SHALL
* rest.resource[=].supportedProfile[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].supportedProfile[=].extension.valueCode = #SHALL
* rest.resource[=].supportedProfile[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].supportedProfile[=].extension.valueCode = #SHALL
* rest.resource[=].supportedProfile[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].supportedProfile[=].extension.valueCode = #SHALL
* rest.resource[=].supportedProfile[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].interaction[0].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].interaction[=].extension.valueCode = #SHALL
* rest.resource[=].interaction[=].code = #read
* rest.resource[=].interaction[+].extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].interaction[=].extension.valueCode = #SHALL
* rest.resource[=].interaction[=].code = #search-type
* rest.resource[=].referencePolicy = #resolves
* rest.resource[=].referencePolicy.extension.url = "http://hl7.org/fhir/StructureDefinition/capabilitystatement-expectation"
* rest.resource[=].referencePolicy.extension.valueCode = #SHOULD