### Project Description and Scope

This Implementation Guide (IG) supports the Advance Care Planning (ACP) information standard (Dutch: Palliatieve Zorg Planning) and is intended for use within the palliative care domain in the Netherlands. This domain involves care for patients with an incurable illness or condition from which they are expected to die.

Developed by the <a href="https://iknl.nl/en">Netherlands Comprehensive Cancer Organisation</a> (Dutch: Integraal kankercentrum Nederland (IKNL)), this guide provides technical direction for using FHIR to exchange ACP data. It is based on <a href="http://hl7.org/fhir/R4/index.html">HL7 FHIR R4</a> and builds on top of the <a href="https://simplifier.net/packages/nictiz.fhir.nl.r4.nl-core">Dutch Core R4 profiles</a>. 

This guide assumes that readers are familiar with the functional specifications of ACP and the **STU3** version of FHIR.

### Call for Feedback

This implementation guide is a work in progress, and its quality and usefulness depend on community input. We welcome feedback on all aspects of this guide, and we are particularly interested in your thoughts on the following decisions and sections:

1. The <a href="StructureDefinition-ext-EncounterReference.html">EncounterReference extension</a> is an optional extension that enables linking the Consent, Goal, and DeviceUseStatement resources to a relevant Encounter. We invite feedback on whether this extension is truly necessary.

2. The <a href="StructureDefinition-ACP-Communication.html">Communication profile</a> has been developed to capture all communication events related to advance care planning. It specifically documents whether the patient has been informed about their responsibility discuss treatment agreements with relatives. As this profile is newly created rather than derived from zib/nl-core profiles, we welcome input on its structure and modeling approach.

3. The <a href="Questionnaire-ACP-zib2017.html">ACP Questionnaire</a> has been developed based on the ACP form dataset and aims to preserve the zib structure as much as possible. We welcome any feedback on its design and implementation.

### Dependencies

{% include dependency-table.xhtml %}