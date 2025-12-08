RuleSet: MetaRules
* ^version = "1.0.0-rc1"
* ^status = #draft
* ^experimental = false
* ^publisher = "IKNL"
* ^contact.name = "IKNL"
* ^contact.telecom.system = #email
* ^contact.telecom.value = "info@iknl.nl"
* ^contact.telecom.use = #work
* ^copyright = "Copyright and related rights waived via CC0, https://creativecommons.org/publicdomain/zero/1.0/. This does not apply to information from third parties, for example a medical terminology system. The implementer alone is responsible for identifying and obtaining any necessary licenses or authorizations to utilize third party IP in connection with the specification or otherwise."

RuleSet: MetaRulesDefinitionalArtifact
* version = "1.0.0-rc1"
* date = "2025-10-29"
* status = #active
* experimental = false
* publisher = "IKNL"
* contact.name = "IKNL"
* contact.telecom.system = #email
* contact.telecom.value = "info@iknl.nl"
* contact.telecom.use = #work
* copyright = "Copyright and related rights waived via CC0, https://creativecommons.org/publicdomain/zero/1.0/. This does not apply to information from third parties, for example a medical terminology system. The implementer alone is responsible for identifying and obtaining any necessary licenses or authorizations to utilize third party IP in connection with the specification or otherwise."
* jurisdiction = urn:iso:std:iso:3166#NL "Netherlands"

RuleSet: CapabilityStatementInteractionandReferencePolicyExpectation
* interaction[0]
  * extension
    * url = $CapExpectation
    * valueCode = #SHALL
  * code = #read
* interaction[+]
  * extension
    * url = $CapExpectation
    * valueCode = #SHALL
  * code = #search-type
* referencePolicy = #resolves
  * extension
    * url = $CapExpectation
    * valueCode = #SHOULD

RuleSet: CapabilityStatementSearchParmeterClinicalPatientExpectation
* searchParam[0]
  * extension
    * url = $CapExpectation
    * valueCode = #SHALL
  * name = "patient"
  * definition = "http://hl7.org/fhir/SearchParameter/clinical-patient"
  * type = #reference

RuleSet: ObligationRules(path)
* {path} ^extension[$obligation][+].extension[code].valueCode = #SHALL:populate-if-known
* {path} ^extension[$obligation][=].extension[actor].valueCanonical = Canonical(ACPActorProvider)
* {path} ^extension[$obligation][+].extension[code].valueCode = #SHALL:no-error
* {path} ^extension[$obligation][=].extension[actor].valueCanonical = Canonical(ACPActorConsulter)
