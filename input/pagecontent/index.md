### Project Description and Scope

This Implementation Guide (IG) supports the Advance Care Planning (ACP) information standard (Dutch: informatiestandaard Proactieve Zorgplanning) and is intended for use within the palliative care domain in the Netherlands. This domain involves care for patients with an incurable illness or condition from which they are expected to die.

Developed by the <a href="https://iknl.nl/en">Netherlands Comprehensive Cancer Organisation</a> (Dutch: Integraal Kankercentrum Nederland (IKNL)), this guide provides technical direction for using FHIR to exchange ACP data. It is based on <a href="http://hl7.org/fhir/R4/index.html">HL7 FHIR R4</a> and builds on top of the <a href="https://simplifier.net/packages/nictiz.fhir.nl.r4.nl-core">Dutch Core R4 profiles</a>. 

This guide assumes that readers are familiar with the functional specifications of ACP and the R4 version of FHIR.

### Version
You are currently viewing the <strong>FHIR R4</strong> version of the IG for the ACP information standard.  
If you are looking for the <strong>STU3</strong> version, you can find it here: <a href="https://api.iknl.nl/docs/pzp/stu3/">Advance Care Planning STU3 HCIM 2017.</a>

### How to Read this Guide
This guide is divided into several pages which are listed at the top of each page in the menu bar. 

* [Home](index.html): This page provides the introduction and scope of this implementation guide. 
* [Information Standard](information-standard.html): This page describes the documents that together comprise the ACP information standard. 
* [Data Model](data-model.html): This page provides an overview of the FHIR profiles used to represent the ACP dataset and includes mappings between the dataset and FHIR artifacts.
* [Data Exchange](data-exchange.html): This page describes the two transaction methods for exchanging a patient's Advance Care Planning (ACP) information using RESTful API and includes the client requests that can be used to retrieve the ACP information. 
* [Artifacts](artifacts.html): This page provides a list of the FHIR artifacts defined as part of this implementation guide, including actor definitions, profiles, value sets, examples, questionnaires, questionnaire responses and capability statements.
* [Change Log](changelog.html):This page summarizes changes introduced in each published release of the implementation guide.
* [Downloads](downloads.html): This page provides links to downloadable artifacts.

### Dependencies

{% include dependency-table.xhtml %}
