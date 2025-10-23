RuleSet: MetaRules
* ^version = "0.1.0"
* ^status = #draft
* ^experimental = false
* ^publisher = "IKNL"
* ^contact.name = "IKNL"
* ^contact.telecom.system = #email
* ^contact.telecom.value = "info@iknl.nl"
* ^contact.telecom.use = #work
* ^copyright = "Copyright and related rights waived via CC0, https://creativecommons.org/publicdomain/zero/1.0/. This does not apply to information from third parties, for example a medical terminology system. The implementer alone is responsible for identifying and obtaining any necessary licenses or authorizations to utilize third party IP in connection with the specification or otherwise."


RuleSet: ObligationRules(path)
* {path} ^extension[+].url = "http://hl7.org/fhir/StructureDefinition/obligation"
* {path} ^extension[=].extension[+].url = "code"
* {path} ^extension[=].extension[=].valueCode = #SHALL:populate-if-known
* {path} ^extension[=].extension[+].url = "actor"
* {path} ^extension[=].extension[=].valueCanonical = Canonical(ACPActorResponder)

* {path} ^extension[+].url = "http://hl7.org/fhir/StructureDefinition/obligation"
* {path} ^extension[=].extension[+].url = "code"
* {path} ^extension[=].extension[=].valueCode = #SHALL:no-error
* {path} ^extension[=].extension[+].url = "actor"
* {path} ^extension[=].extension[=].valueCanonical = Canonical(ACPActorRequester)

