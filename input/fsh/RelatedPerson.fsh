
Profile: ACPContactPerson
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-ContactPerson
Id: ACP-ContactPerson
Title: "ACP ContactPerson"
Description: "A contact is a person not being a healthcare professional who is involved in the patient’s care, such as family members, caregivers, mental caretakers, guardians and legal representatives."
* insert MetaRules
* relationship 1..*
* relationship[role] ^sliceName = "role"
* relationship[role] 1..1
// TODO: relationship[relationship] contains explicited, distinct codes for curator/mentor and brother/sister while the form allows only the option to select them both. From the form is not possible then to map this to FHIR as you would not know which code to use. 
* relationship[relationship] ^sliceName = "relationship"
* relationship[relationship] ^comment = "When someone is or **will be** a legal representative (as indicated on the form), then a relationship code `24` from code system  _urn:oid:2.16.840.1.113883.2.4.3.11.22.472_ is added."

Mapping: MapACPContactPerson
Id: pall-izppz-v2025-03-11
Title: "ACP ContactPerson"
Source: ACPContactPerson
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "441" "Wettelijk vertegenwoordiger (Contactpersoon)" // TODO how to know/decide if someone is a wettelijk vertegenwoordiger or not? If the relationship code is 24, then it is a wettelijk vertegenwoordiger?
* name -> "442" "Naamgegevens"
// TODO: decide if we want to go into providing mappings inside these data type profiles. 
* telecom -> "454" "Contactgegevens"
* address -> "463" "Adresgegevens"
* relationship[role] -> "475" "Rol"
* relationship[relationship] -> "476" "Relatie"

* -> "478" "Eerste contactpersoon (Contactpersoon)" 
* name -> "479" "Naamgegevens"
* telecom -> "454" "Contactgegevens"
* address -> "500" "Adresgegevens" // TODO why is Adresgegevens 0..1 in scenario/dataset here? While for Wettelijke vertegenwoordiger is 0..*?
* relationship[role] -> "512" "Rol"
* relationship[relationship] -> "513" "Relatie"

* -> "554" "Gesprek gevoerd in bijzijn van (Contactpersoon)" 
* name -> "555" "Naamgegevens"
* relationship[role] -> "588" "Rol" // TODO because this is 0..* in the scenario/dataset, do we need to have two profiles for ContactPerson?
* relationship[relationship] -> "589" "Relatie"

Instance: F1-ACP-ContactPerson-HendrikHartman
InstanceOf: ACPContactPerson
Title: "Wettelijk vertegenwoordiger Hendrik Hartman"
Usage: #example
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* patient.type = "Patient"
* relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#01 "Eerste relatie/contactpersoon"
* relationship[+] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24 "Wettelijke vertegenwoordiger"
* relationship[+] = $v3-RoleCode#BRO "Broer"
* name[0].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name[=].extension.valueCode = #NL1
* name[=].use = #official
* name[=].text = "Michiel Hartman"
* name[=].family = "Hartman"
* name[=].family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[=].family.extension[=].valueString = "Hartman"
* name[=].family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-prefix"
* name[=].given[0] = "Michiel"
* name[=].given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[=].given[=].extension.valueCode = #BR
* name[+].use = #usual
* name[=].given = "Michiel"
* telecom[0].system = #email
* telecom[=].value = "michiel.hartman@iknl.nl"
* telecom[=].use = #work