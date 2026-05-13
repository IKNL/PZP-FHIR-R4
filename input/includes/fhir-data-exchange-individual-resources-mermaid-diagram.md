<div class="mermaid" style="height: 800px; overflow: visible;">

sequenceDiagram
    autonumber
    participant C as ACP Actor Consulter<br>(Client)
    participant S as ACP Actor Provider<br>(Server)

    note over C, S: Prerequisite: client possesses access token & Patient ID

    rect rgb(240, 248, 255)
  
        par 
            %% 1. Procedures
            C->>S: GET /Procedure?patient=Patient/[id]<br>&code=sct|713603004<br>&_include=Procedure:encounter
            activate S
            S-->>C: 200 OK: Bundle (Procedure + Encounter)
            deactivate S
        and
            %% 2. Consent (TreatmentDirective)
            C->>S: GET /Consent?patient=Patient/[id]<br>&scope=http://terminology.hl7.org/CodeSystem/consentscope|treatment<br>&category=http://snomed.info/sct|129125009<br>&_include=Consent:actor
            activate S
            S-->>C: 200 OK: Bundle (Consent + PractitionerRole + RelatedPerson)
            deactivate S
        and
            %% 3. Consent (AdvanceCareDirective)
            C->>S: GET /Consent?patient=Patient/[id]<br>&scope=http://terminology.hl7.org/CodeSystem/consentscope|adr<br>&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd<br>&_include=Consent:actor
            activate S
            S-->>C: 200 OK: Bundle (Consent + PractitionerRole + RelatedPerson)
            deactivate S
        and
            %% 4. Goals
            C->>S: GET /Goal?patient=Patient/[id]<br>&category=http://snomed.info/sct|713603004
            activate S
            S-->>C: 200 OK: Bundle (Goal)
            deactivate S
        and
            %% 5. Observations
            C->>S: GET /Observation?patient=Patient/[id]<br>&code=http://snomed.info/sct|665671000146101,153851000146100,395091006,340171000146104,247751003,570801000146104
            activate S
            S-->>C: 200 OK: Bundle (Observation)
            deactivate S
        and
            %% 6. Devices
            C->>S: GET /DeviceUseStatement?patient=Patient/[id]<br>&device.type=http://snomed.info/sct|72506001,465460004,468542000,704707009,1263462004,1236894001<br>&_include=DeviceUseStatement:device
            activate S
            S-->>C: 200 OK: Bundle (DeviceUseStatement + Device)
            deactivate S
        and
            %% 7. CommunicationRequests
            C->>S: GET /CommunicationRequest?patient=Patient/[id]<br>&category=http://snomed.info/sct|223449006
            activate S
            S-->>C: 200 OK: Bundle (CommunicationRequest)
            deactivate S
        end
    end

    opt Resolve Additional References
        note over C: If resources contain unresolved references<br>(e.g., to Practitioner), Client performs subsequent GETs
        C->>S: GET [Reference URL]
        S-->>C: 200 OK (Referenced Resource)
    end

</div>