# util/ — Helper Scripts

Standalone Python utilities for the IKNL PZP FHIR R4 Implementation Guide.
None of these scripts are required by the IG build itself — they automate
common development, analysis, and testing tasks.

Each script contains full documentation (usage, examples, configuration) in
its module docstring.  **Check the configuration constants at the top of each
file** — you may need to adjust paths or URLs for your local setup.

All scripts require **Python 3.8+** and use only the standard library.

## Scripts

| Script | Purpose |
|---|---|
| `mapping_table_generator.py` | Generates a Markdown mapping table from FSH profile mappings and an ART-DECOR JSON dataset export. |
| `mermaid_diagram_generator.py` | Generates a Mermaid flowchart diagram visualising inter-profile relationships from FSH definitions. |
| `questionnaire_item_prefix_populator.py` | Moves detected prefixes (a), 1., etc.) from `item.text` to `item.prefix` in Questionnaire resources, and strips them from QuestionnaireResponse resources for FHIR compliance. |
| `questionnaire_item_code_remover.py` | Removes all `code` elements from Questionnaire items at every nesting level. |
| `strip_standards_status_extensions.py` | Strips auto-injected `standards-status` / `normative-version` extensions from compiled JSON resources and normative badges from HTML output. |
| `patient_bundle_generator.py` | Creates per-patient FHIR Bundle (transaction) resources from compiled FSH output for populating a test FHIR server. |
| `postman_collection_generator.py` | Generates a Postman collection (v2.1) with PUT and `$validate` requests for all compiled instance resources. |
