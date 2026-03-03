# Questionnaire and QuestionnaireResponse Governance

## Overview

This IG maintains questionnaires for Advance Care Planning (ACP) based on the zib2020 dataset, covering all aspects of ACP documentation including patient information, legal capacity, treatment goals, treatment boundaries, treatment wishes, additional information, prior agreements, and information sharing.

## Source and Format

The source Questionnaires originate from FormStudio, which connects to the ART-DECOR dataset. Because of this external source:
- Questionnaires are stored as JSON, not FSH
- Manual adjustments are required after export to ensure IG compliance
- Both zib2020-r4 and zib2017-stu3 versions follow similar patterns

## Questionnaire Creation Process

### Step 1: Export from FormStudio
Export the questionnaire from FormStudio with ART-DECOR dataset connection.

### Step 2: Adjust Metadata Fields

Transform the exported metadata to follow IG standards. Use English for all metadata fields and ensure proper resource identification.

**Before (FormStudio export):**
```json
{
    "name": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "title": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
    "resourceType": "Questionnaire",
    "status": "draft",
    "item": [ /* items */ ],
    "experimental": true,
    "publisher": "Gepubliceerd door PZNL & uitgevoerd door IKNL | Published by PZNL & executed by IKNL",
    "copyright": "Op dit formulier is copyright... | This form is subject to copyright...",
    "purpose": "Dit formulier is ontwikkeld... | This form was developed...",
    "description": "Dit formulier is ontwikkeld... | This form was developed..."
}
```

**After (IG-compliant):**
```json
{
  "resourceType": "Questionnaire",
  "id": "ACP-zib2020",
  "url": "https://api.iknl.nl/docs/pzp/r4/Questionnaire/ACP-zib2020",
  "version": "0.1.3-beta3",
  "name": "ACPzib2020",
  "title": "Uniform vastleggen proactieve zorgpanning advance care planning (ACP) o.b.v. zibs2020 - Beta3 28-08-2025",
  "status": "draft",
  "experimental": false,
  "publisher": "Published by PZNL & executed by IKNL",
  "description": "This form was developed to clearly document agreements resulting from the advance care planning (ACP) process. It is NOT a checklist. It can only be completed by a healthcare provider after a professional and nuanced conversation. For advice on conducting these conversations, please refer to the guideline for proactive care planning in the palliative phase and Palliaweb, see https://palliaweb.nl/zorgpraktijk/proactieve-zorgplanning. \nEnter 'unknown' if a topic is not discussed or if the patient does not (yet) have an opinion.When transferring to a long-term care setting, consider adding conversation records about advance care planning (ACP) to the transfer documents.",
  "purpose": "This form was developed to clearly document agreements resulting from the advance care planning (ACP) process.",
  "copyright": "This form is subject to copyright, user rights and a disclaimer, as specified for all IKNL information standards. For details, see the paragraph on Gebruikersrechten en disclaimer at https://iknl.nl/onderzoek/eenheid-van-taal.",
  "item": [ /* items */ ]
}
```

**Key metadata requirements:**
- **`id`**: Use pattern `ACP-[purpose]` (e.g., `ACP-zib2020`, `ACP-Administrative`)
- **`url`**: Canonical URL following pattern `https://api.iknl.nl/docs/pzp/r4/Questionnaire/[id]`
- **`version`**: Semantic versioning (e.g., `0.1.3-beta3`, `1.0.0-rc1`)
- **`name`**: PascalCase technical name (e.g., `ACPzib2020`, `ACPAdministrative`)
- **`title`**: Human-readable title describing purpose
- **`language`**: Set to `"nl-NL"` (questions are in Dutch)
- **`publisher`**: Use simplified form `"PZNL & IKNL"`


### Step 3: Save to Repository
Save the adjusted Questionnaire as `Questionnaire-[id].json` in `input/resources/`

### Step 4: Fix Conditional Expressions

Use [NLM Form Builder](https://formbuilder.nlm.nih.gov/) to correct invalid FHIRPath expressions:

1. Select **"Start with existing form"** → **"Import from local file"**
2. Import your adjusted Questionnaire JSON
3. Review warnings for invalid FHIRPath conditions
4. Fix conditional displays (especially boolean comparisons)
   
   **Example fix needed:**
   - Item: "Naam eerste contactpersoon" should display when:
   - Question `984` ("Is de wettelijk vertegenwoordiger ook de eerste contactpersoon?") = `Nee (0)`

### Step 5: Set Read-Only Treatment/Measurement Codes

For sections **4. Behandelgrenzen** and **5. Behandelwensen**, configure treatment codes and measurement names as:
- **Read only**: Yes
- **Value method**: Pick initial value

This simplifies QuestionnaireResponse creation. Example result:

```json
"item": [
        {
          "type": "choice",
          "linkId": "1408",
          "text": "Belangrijkste doel van behandeling ([MetingNaam])",
          "required": false,
          "repeats": false,
          "readOnly": true,
          "answerOption": [
            {
              "valueCoding": {
                "system": "http://snomed.info/sct",
                "code": "180771000146100",
                "display": "Focus van behandeling (waarneembare entiteit)"
              },
              "initialSelected": true
            }
          ]
        },
]
```

### Step 6: Export and Replace

1. In Form Builder, select top-right menu → **"Export"** → **"Export to file in FHIR R4 format"**
2. Save and replace the file in `input/resources/`

### Step 7: Expand ICD valueset
In the question concerning the 'ProductType van IC' (linkID 1008), replace the ICD code and display by the valueset values, including the system, the code and the display. Illustrated for first two answer options:
```json
"answerOption": [
                {
                  "valueCoding": {
                    "system": "http://snomed.info/sct",
                    "code": "72506001",
                    "display": "implanteerbare cardioverter-defibrillator"
                  }
                },
                {
                  "valueCoding": {
                    "system": "http://snomed.info/sct",
                    "code": "465460004",
                    "display": "univentriculaire implanteerbare cardioverter-defibrillator"
                  }
                },
]
```

### Step 8: Remove 'code' keys from questionnaire items with Python script
Run the Questionnaire Item Code Remover script (`/util\questionnaire_item_code_remover.py/`) that removes 'code' keys from all questionnaire items, including incorrect 'code' properties.

### Step 9: Register in Configuration for better presentation in IG

Add the Questionnaire to `sushi-config.yaml`:

**In `resources` section:**
```yaml
resources:
  Questionnaire/ACP-zib2020:
    name: ACP Questionnaire based on zib2020
    description: Complete clinical questionnaire for advance care planning
    exampleBoolean: false
```

**In `groups` section:**
```yaml
groups:
  Q-QR:
    name: "Structures: Questionnaire and QuestionnaireResponses"
    description: Forms used for comprehensive ACP documentation
    resources:
    - Questionnaire/ACP-zib2020
``` 

## QuestionnaireResponse Creation Process

### Step 1: Load Questionnaire
Use [LHC Forms](https://lhcforms.nlm.nih.gov/lhcforms/) to create example responses:

1. Select **"Load From File"**
2. Choose the adjusted Questionnaire from `input/resources/`

### Step 2: Fill Example Data
Complete the form with realistic example data representing a patient scenario.

### Step 3: Export Response
1. Select **"Show Form Data as FHIR SDC QuestionnaireResponse"**
2. Copy the JSON to clipboard

### Step 4: Save and Clean Up
1. Save as `QuestionnaireResponse-[PatientName]-[Date].json` in `input/resources/`
   - Example: `QuestionnaireResponse-HendrikHartman-20201001.json`
2. Enhance the exported JSON:
   - Add an `id` field following pattern `[PatientName]-[Date]`
   - Add proper `subject` and `author` references
   - Ensure `questionnaire` canonical URL matches your Questionnaire
   - Add appropriate `status` and `authored` date


### Step 5: Register in Configuration for better presentation in IG

Add QuestionnaireResponses to `sushi-config.yaml`:

**In `resources` section:**
```yaml
resources:
  QuestionnaireResponse/HendrikHartman-20221108:
    name: QuestionnaireResponse Hendrik Hartman 20221108
    description: QuestionnaireResponse example for Hendrik Hartman on 2022-11-08
    exampleBoolean: false
```

**In `groups` section:**
```yaml
groups:
  Q-QR:
    resources:
    - QuestionnaireResponse/HendrikHartman-20221108
```