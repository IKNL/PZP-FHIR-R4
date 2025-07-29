### Project Description and Scope

This Implementation Guide (IG) supports the Advance Care Planning (ACP) information standard (Dutch: Palliatieve Zorg Planning) and is intended for use within the palliative care domain in the Netherlands. This domain involves care for patients with an incurable illness or condition from which they are expected to die.

Developed by the <a href="https://iknl.nl/en">Netherlands Comprehensive Cancer Organisation</a> (Dutch: Integraal kankercentrum Nederland (IKNL)), this guide provides technical direction for using FHIR to exchange ACP data. It is based on <a href="http://hl7.org/fhir/R4/index.html">HL7 FHIR R4</a> and builds on top of the <a href="https://simplifier.net/packages/nictiz.fhir.nl.r4.nl-core">Dutch Core R4 profiles</a>. 

This guide assumes that readers are familiar with the functional specifications of ACP and the R4 version of FHIR. For more background information and access to the functional specifications, please refer to the <a href="functioneel-ontwerp.html">following link</a>.

### Call for Feedback

This implementation guide is a work in progress, and its quality and usefulness depend on community input. We welcome feedback on all aspects of this guide, and we are particularly interested in your thoughts on the following key decisions and sections:

1. The <a href="StructureDefinition-ext-EncounterReference.html">EncounterReference extension</a> is an optional addition that enables linking the Consent, Goal, and DeviceUseStatement resources to the relevant Encounter. This helps clarify the association of these resources with the ACP context. We invite feedback on whether this extension is truly necessary.

2. The <a href="StructureDefinition-ACP-Communciation.html">Communication profile</a> has been developed to capture all communication events related to advance care planning. In particular, it documents whether the patient has been informed about their responsibility to notify others. As this is a new profile, not derived from zib/nl-core profiles, we welcome input on its structure and modelling.

3. The <a href="StructureDefinition-ACP-TreatmentDirective.html">TreatmentDirective profile</a> is reused for directives regarding deactivation of Implantable Cardioverter Defibrillators (ICD). However, this does not fully align with the zib TreatmentDirective2 for two reasons. First, ICD codes cannot be added to `Consent.provision.code` due to binding constraints, so the mapping is placed in `Consent.provision.code.text` with `OTH` as the code. A zib ticket (<a href="https://nictiz.atlassian.net/browse/ZIB-2796">ZIB-2796</a>) has been created to address this issue. Second, for `Consent.provision.type`, only the _permit_ code should be used; the other two nullflavor codes from the dataset valueset are not appropriate. The profile describes using `Consent.modifierExtension.specificationOther` to capture information about these choices. Alternatively, a specialized profile for ICDs could be created, not based on the nl-core profile but following the same structure where possible.

### Dependencies

{% include dependency-table.xhtml %}