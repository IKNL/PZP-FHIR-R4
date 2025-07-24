Instance: Communication-reason-code
InstanceOf: SearchParameter
Usage: #definition
* url = "https://fhir.iknl.nl/fhir/SearchParameter/Communication-reason-code"
* version = "4.0.1"
* name = "ReasonCode"
* status = #draft
* experimental = false
* date = "2025-07-24T15:21:02+11:00"
* publisher = "IKNL"
* contact[0].telecom.system = #email
* contact[=].telecom.value = "info@iknl.nl"
* description = "ReasonCode for the Communication"
* code = #reason-code
* base = #Communication
* type = #token
* expression = "Communication.reasonCode"