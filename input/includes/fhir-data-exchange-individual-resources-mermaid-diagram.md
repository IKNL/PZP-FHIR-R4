<div class="mermaid" style="height: 800px; overflow: visible;">

sequenceDiagram
    autonumber
    participant C as ACP Actor Consulter<br>(Client)
    participant S as ACP Actor Provider<br>(Server)

    note over C, S: Prerequisite: client possesses access token & Patient ID

    rect rgb(240, 248, 255)
  
        par 
            %% 1. Procedures
            C->>S: GET /Procedure?patient=[id]<br>&code=sct|713603004<br>&_include:Procedure:encounter
            activate S
            S-->>C: 200 OK: Bundle (Procedure + Encounter)
            deactivate S
        and
            %% 2. Consent (TreatmentDirective)
            C->>S: GET /Consent?patient=[id]<br>&scope=http://terminology.hl7.org/CodeSystem/consentscope|treatment<br>&category=http://snomed.info/sct|129125009<br>&_include=Consent:actor
            activate S
            S-->>C: 200 OK: Bundle (Consent + PractitionerRole + RelatedPerson)
            deactivate S
        and
            %% 3. Consent (AdvanceCareDirective)
            C->>S: GET /Consent?patient=[id]<br>&scope=http://terminology.hl7.org/CodeSystem/consentscope|adr<br>&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd<br>&_include=Consent:actor
            activate S
            S-->>C: 200 OK: Bundle (Consent + PractitionerRole + RelatedPerson)
            deactivate S
        and
            %% 4. Goals
            C->>S: GET /Goal?patient=[id]<br>&description=http://snomed.info/sct|385987000,1351964001,713148004
            activate S
            S-->>C: 200 OK: Bundle (Goal)
            deactivate S
        and
            %% 5. Observations
            C->>S: GET /Observation?patient=[id]<br>&code=http://snomed.info/sct|153851000146100,395091006,340171000146104,247751003
            activate S
            S-->>C: 200 OK: Bundle (Observation)
            deactivate S
        and
            %% 6. Devices
            C->>S: GET /DeviceUseStatement?patient=[id]<br>&device.type:in=https://api.iknl.nl/docs/pzp/r4/ValueSet/ACP-MedicalDeviceProductType-ICD<br>&_include:DeviceUseStatement:device
            activate S
            S-->>C: 200 OK: Bundle (DeviceUseStatement + Device)
            deactivate S
        and
            %% 7. Communication
            C->>S: GET /Communication?patient=[id]<br>&reason-code=http://snomed.info/sct|713603004
            activate S
            S-->>C: 200 OK: Bundle (Communication)
            deactivate S
        end
    end

    opt Resolve Additional References
        note over C: If resources contain unresolved references<br>(e.g., to Practitioner), Client performs subsequent GETs
        C->>S: GET [Reference URL]
        S-->>C: 200 OK (Referenced Resource)
    end

</div>