### Information Standard: Documentation and Artifacts

The advance care planning (ACP) information standard defines both the functional and technical design. This implementation guide (IG) specifies how the technical design of the ACP information standard should be applied in practice. To clarify the coherence of the different documents involved, we outline their roles here.


#### Functional design (FD)
The functional design forms the basis for this IG. It entails: 
- The scope of the ACP information standard (target audience, framework and principles);
- Use cases and process descriptions for recording and consulting ACP information;
- A description of the relationship with legislation, regulations and quality guidelines;
- Functional requirements for systems;
- A statement on responsibility for recording and managing ACP information;
- A statement on data protection;
- A description of the envisioned infrastructure for ACP data exchange;
- An overview of involved parties and their corresponding roles.

[Functioneel Ontwerp](link-naar-document.pdf)  



#### Technical design (FHIR IG)
This IG is the technical design. 
It describes how the ACP information standard is specifically implemented in HL7 FHIR, including:
- FHIR profiles and extensions;
- Use of terminology (SNOMED CT, local codes);
- Constraints and business rules;
- Examples – to support suppliers with implementation and conformance assessment.
  

[FHIR IG – Technical design](api.iknl.nl/pzp/fhir/index.html)  



#### Datasets, Terminology and scenario's
Other important artefacts of the ACP information standard can be found on [ART-DECOR](https://decor.nictiz.nl/ad/#/pall-izppz-/project/overview):
-  **Datasets** – PZP dataset and ACP form describing the structure of the information.  
-  **Terminology & code systems** – Description of the used value sets with mappings to SNOMED CT, or domain specific codes.  
-  **Scenarios & sequence diagrams** – Explanation and visualization of how actors and systems exchange information.


