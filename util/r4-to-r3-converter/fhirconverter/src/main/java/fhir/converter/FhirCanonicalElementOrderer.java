package fhir.converter;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Handles canonical element ordering for FHIR StructureDefinitions according to FHIR specification.
 * 
 * This class provides comprehensive element ordering for FHIR resources, ensuring that elements
 * are arranged in the exact sequence defined by the FHIR specification. This is crucial for
 * compatibility with FHIR tools like Forge that expect strict element ordering.
 * 
 * Features:
 * - Multi-level nested element ordering
 * - Resource-specific canonical sequences
 * - Hierarchical element processing
 * - Fallback to alphabetical ordering for unknown elements
 */
public class FhirCanonicalElementOrderer {
    
    private static final Logger logger = LoggerFactory.getLogger(FhirCanonicalElementOrderer.class);
    
    /**
     * Reorders elements in a StructureDefinition differential according to FHIR canonical order
     * 
     * @param elements The JsonArray of elements to reorder
     * @param resourceType The FHIR resource type (e.g., "Patient", "Encounter")
     * @return JsonArray with elements in canonical FHIR order
     */
    public JsonArray reorderElements(JsonArray elements, String resourceType) {
        // Get canonical element order for this resource type
        List<String> canonicalOrder = getCanonicalElementOrder(resourceType);
        
        if (canonicalOrder.isEmpty()) {
            logger.debug("No canonical order defined for resource type: {}, keeping original order", resourceType);
            return elements; // Return original if no ordering defined
        }
        
        return reorderElementArray(elements, canonicalOrder, resourceType);
    }
    
    /**
     * Reorders an array of elements according to canonical FHIR order
     * Handles multi-level nested element ordering
     */
    private JsonArray reorderElementArray(JsonArray elements, List<String> canonicalOrder, String resourceType) {
        // Create a map of elements by their full path for easy lookup
        Map<String, JsonObject> elementsByPath = new LinkedHashMap<>();
        
        // Categorize elements by their full path
        for (JsonElement elementElement : elements) {
            JsonObject element = elementElement.getAsJsonObject();
            
            if (element.has("path")) {
                String path = element.get("path").getAsString();
                elementsByPath.put(path, element);
            }
        }
        
        // Build reordered array using hierarchical ordering
        JsonArray reorderedElements = new JsonArray();
        Set<String> processedPaths = new HashSet<>();
        
        // First, add the root element if it exists
        String rootPath = resourceType;
        if (elementsByPath.containsKey(rootPath)) {
            reorderedElements.add(elementsByPath.get(rootPath));
            processedPaths.add(rootPath);
            logger.debug("Added root element: {}", rootPath);
        }
        
        // Then add elements in canonical order with their nested elements
        for (String canonicalPath : canonicalOrder) {
            String fullPath = resourceType + "." + canonicalPath;
            
            // Process this element and all its nested elements recursively
            processElementAndChildren(fullPath, elementsByPath, reorderedElements, processedPaths);
        }
        
        // Add any remaining elements that weren't processed (sorted by path for consistency)
        List<String> remainingPaths = new ArrayList<>();
        for (String path : elementsByPath.keySet()) {
            if (!processedPaths.contains(path)) {
                remainingPaths.add(path);
            }
        }
        remainingPaths.sort(String::compareTo);
        
        for (String remainingPath : remainingPaths) {
            reorderedElements.add(elementsByPath.get(remainingPath));
            logger.debug("Added remaining element: {}", remainingPath);
        }
        
        return reorderedElements;
    }
    
    /**
     * Recursively processes an element and all its nested children in canonical order
     */
    private void processElementAndChildren(String parentPath, Map<String, JsonObject> elementsByPath, 
                                          JsonArray reorderedElements, Set<String> processedPaths) {
        
        // Add the parent element if it exists and hasn't been processed
        if (elementsByPath.containsKey(parentPath) && !processedPaths.contains(parentPath)) {
            reorderedElements.add(elementsByPath.get(parentPath));
            processedPaths.add(parentPath);
            logger.debug("Added canonical element: {}", parentPath);
        }
        
        // Get the canonical order for nested elements of this parent
        List<String> nestedOrder = getNestedElementOrder(parentPath);
        
        if (!nestedOrder.isEmpty()) {
            // Process nested elements in canonical order
            for (String nestedElement : nestedOrder) {
                String nestedPath = parentPath + "." + nestedElement;
                processElementAndChildren(nestedPath, elementsByPath, reorderedElements, processedPaths);
            }
        }
        
        // Find any other nested elements that weren't in the canonical order
        List<String> otherNestedPaths = new ArrayList<>();
        for (String path : elementsByPath.keySet()) {
            if (path.startsWith(parentPath + ".") && !processedPaths.contains(path)) {
                // Make sure it's a direct child, not a grandchild
                String childPortion = path.substring(parentPath.length() + 1);
                if (!childPortion.contains(".")) {
                    otherNestedPaths.add(path);
                }
            }
        }
        
        // Sort other nested paths alphabetically and process them
        otherNestedPaths.sort(String::compareTo);
        for (String otherNestedPath : otherNestedPaths) {
            processElementAndChildren(otherNestedPath, elementsByPath, reorderedElements, processedPaths);
        }
    }
    
    /**
     * Gets the canonical element order for a FHIR resource type
     * This includes comprehensive element ordering to match FHIR specification
     */
    private List<String> getCanonicalElementOrder(String resourceType) {
        List<String> canonicalOrder = new ArrayList<>();
        
        switch (resourceType) {
            case "Patient":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "active", "name", "telecom", "gender", "birthDate", 
                    // Handle deceased[x] choice types
                    "deceased[x]", "deceasedBoolean", "deceasedDateTime", 
                    "address", "maritalStatus", 
                    // Handle multipleBirth[x] choice types
                    "multipleBirth[x]", "multipleBirthBoolean", "multipleBirthInteger", 
                    "photo", "contact", "communication", "generalPractitioner",
                    "managingOrganization", "link"
                ));
                break;
                
            case "Practitioner":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "active", "name", "telecom", "address", "gender", "birthDate", "photo",
                    "qualification", "communication"
                ));
                break;
                
            case "RelatedPerson":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "active", "patient", "relationship", "name", "telecom", "gender", "birthDate",
                    "address", "photo", "period", "communication"
                ));
                break;
                
            case "Encounter":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "status", "statusHistory", "class", "classHistory", "type", "priority", "subject",
                    "episodeOfCare", "incomingReferral", "participant", "appointment", "period", "length", "reason",
                    "diagnosis", "account", "hospitalization", "location", "serviceProvider", "partOf"
                ));
                break;
                
            case "Condition":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "clinicalStatus", "verificationStatus", "category", "severity", "code", "bodySite",
                    "subject", "context", 
                    // Handle onset[x] choice types
                    "onset[x]", "onsetDateTime", "onsetAge", "onsetPeriod", "onsetRange", "onsetString",
                    // Handle abatement[x] choice types  
                    "abatement[x]", "abatementDateTime", "abatementAge", "abatementBoolean", "abatementPeriod", "abatementRange", "abatementString",
                    "assertedDate", "asserter", "stage", "evidence", "note"
                ));
                break;
                
            case "Observation":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "basedOn", "status", "category", "code", "subject", "context", 
                    // Handle effective[x] choice types - all possible variants
                    "effective[x]", "effectiveDateTime", "effectivePeriod", "effectiveTiming", "effectiveInstant",
                    "issued", "performer", 
                    // Handle value[x] choice types - all possible variants
                    "value[x]", "valueQuantity", "valueCodeableConcept", "valueString", "valueBoolean", "valueInteger",
                    "valueRange", "valueRatio", "valueSampledData", "valueTime", "valueDateTime", "valuePeriod",
                    "dataAbsentReason", "interpretation", "comment", "bodySite",
                    "method", "specimen", "device", "referenceRange", "related", "component"
                ));
                break;
                
            case "Procedure":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "definition", "basedOn", "partOf", "status", "notDone", "notDoneReason", "category",
                    "code", "subject", "context", 
                    // Handle performed[x] choice types
                    "performed[x]", "performedDateTime", "performedPeriod", "performedString", "performedAge", "performedRange",
                    "performer", "location", "reasonCode", "reasonReference",
                    "bodySite", "outcome", "report", "complication", "complicationDetail", "followUp", "note",
                    "focalDevice", "usedReference", "usedCode"
                ));
                break;
                
            case "Organization":
                canonicalOrder.addAll(List.of(
                    "id", "meta", "implicitRules", "language", "text", "contained", "extension", "modifierExtension",
                    "identifier", "active", "type", "name", "alias", "telecom", "address", "partOf", "contact", "endpoint"
                ));
                break;
                
            default:
                logger.debug("No canonical order defined for resource type: {}", resourceType);
                break;
        }
        
        return canonicalOrder;
    }
    
    /**
     * Gets the canonical order for nested elements within a specific parent element
     * This defines the ordering for child elements based on FHIR specification
     */
    private List<String> getNestedElementOrder(String parentPath) {
        List<String> nestedOrder = new ArrayList<>();
        
        // Define nested element orders based on FHIR specification
        switch (parentPath) {
            // Common meta element ordering (applies to all resources)
            case "Patient.meta":
            case "Practitioner.meta":
            case "RelatedPerson.meta":
            case "Encounter.meta":
            case "Condition.meta":
            case "Observation.meta":
            case "Procedure.meta":
            case "Organization.meta":
                nestedOrder.addAll(List.of("versionId", "lastUpdated", "profile", "security", "tag"));
                break;
                
            // Common text element ordering (applies to all resources)
            case "Patient.text":
            case "Practitioner.text":
            case "RelatedPerson.text":
            case "Encounter.text":
            case "Condition.text":
            case "Observation.text":
            case "Procedure.text":
            case "Organization.text":
                nestedOrder.addAll(List.of("status", "div"));
                break;
                
            // Common identifier element ordering (applies to most resources)
            case "Patient.identifier":
            case "Practitioner.identifier":
            case "RelatedPerson.identifier":
            case "Encounter.identifier":
            case "Condition.identifier":
            case "Observation.identifier":
            case "Procedure.identifier":
            case "Organization.identifier":
                nestedOrder.addAll(List.of("use", "type", "system", "value", "period", "assigner"));
                break;
                
            // Patient-specific nested elements
            case "Patient.name":
                nestedOrder.addAll(List.of("use", "text", "family", "given", "prefix", "suffix", "period"));
                break;
                
            case "Patient.telecom":
                nestedOrder.addAll(List.of("system", "value", "use", "rank", "period"));
                break;
                
            case "Patient.address":
                nestedOrder.addAll(List.of("use", "type", "text", "line", "city", "district", "state", "postalCode", "country", "period"));
                break;
                
            case "Patient.contact":
                nestedOrder.addAll(List.of("relationship", "name", "telecom", "address", "gender", "organization", "period"));
                break;
                
            case "Patient.communication":
                nestedOrder.addAll(List.of("language", "preferred"));
                break;
                
            case "Patient.link":
                nestedOrder.addAll(List.of("other", "type"));
                break;
                
            // Practitioner-specific nested elements
            case "Practitioner.name":
                nestedOrder.addAll(List.of("use", "text", "family", "given", "prefix", "suffix", "period"));
                break;
                
            case "Practitioner.telecom":
                nestedOrder.addAll(List.of("system", "value", "use", "rank", "period"));
                break;
                
            case "Practitioner.address":
                nestedOrder.addAll(List.of("use", "type", "text", "line", "city", "district", "state", "postalCode", "country", "period"));
                break;
                
            case "Practitioner.qualification":
                nestedOrder.addAll(List.of("identifier", "code", "period", "issuer"));
                break;
                
            case "Practitioner.communication":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            // RelatedPerson-specific nested elements
            case "RelatedPerson.patient":
                nestedOrder.addAll(List.of("reference", "display"));
                break;
                
            case "RelatedPerson.relationship":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "RelatedPerson.name":
                nestedOrder.addAll(List.of("use", "text", "family", "given", "prefix", "suffix", "period"));
                break;
                
            case "RelatedPerson.telecom":
                nestedOrder.addAll(List.of("system", "value", "use", "rank", "period"));
                break;
                
            case "RelatedPerson.address":
                nestedOrder.addAll(List.of("use", "type", "text", "line", "city", "district", "state", "postalCode", "country", "period"));
                break;
                
            case "RelatedPerson.period":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            case "RelatedPerson.communication":
                nestedOrder.addAll(List.of("language", "preferred"));
                break;
                
            // Encounter-specific nested elements
            case "Encounter.statusHistory":
                nestedOrder.addAll(List.of("status", "period"));
                break;
                
            case "Encounter.classHistory":
                nestedOrder.addAll(List.of("class", "period"));
                break;
                
            case "Encounter.type":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Encounter.priority":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Encounter.participant":
                nestedOrder.addAll(List.of("type", "period", "individual"));
                break;
                
            case "Encounter.participant.type":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Encounter.participant.period":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            case "Encounter.period":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            case "Encounter.length":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Encounter.reason":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Encounter.diagnosis":
                nestedOrder.addAll(List.of("condition", "role", "rank"));
                break;
                
            case "Encounter.diagnosis.role":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Encounter.hospitalization":
                nestedOrder.addAll(List.of("preAdmissionIdentifier", "origin", "admitSource", "reAdmission", 
                                          "dietPreference", "specialCourtesy", "specialArrangement", "destination", 
                                          "dischargeDisposition"));
                break;
                
            case "Encounter.location":
                nestedOrder.addAll(List.of("location", "status", "period"));
                break;
                
            case "Encounter.location.period":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            // Observation-specific nested elements
            case "Observation.category":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.code":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            // Handle effective[x] choice types - all variants
            case "Observation.effectiveDateTime":
                // DateTime values don't have nested structure
                break;
                
            case "Observation.effectivePeriod":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            case "Observation.effectiveTiming":
                nestedOrder.addAll(List.of("event", "repeat", "code"));
                break;
                
            case "Observation.effectiveInstant":
                // Instant values don't have nested structure
                break;
                
            case "Observation.performer":
                nestedOrder.addAll(List.of("reference", "display"));
                break;
                
            // Handle value[x] choice types - all variants
            case "Observation.valueQuantity":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Observation.valueCodeableConcept":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.valueString":
                // String values don't have nested structure
                break;
                
            case "Observation.valueBoolean":
                // Boolean values don't have nested structure
                break;
                
            case "Observation.valueInteger":
                // Integer values don't have nested structure
                break;
                
            case "Observation.valueRange":
                nestedOrder.addAll(List.of("low", "high"));
                break;
                
            case "Observation.valueRatio":
                nestedOrder.addAll(List.of("numerator", "denominator"));
                break;
                
            case "Observation.valueSampledData":
                nestedOrder.addAll(List.of("origin", "period", "factor", "lowerLimit", "upperLimit", "dimensions", "data"));
                break;
                
            case "Observation.valueTime":
                // Time values don't have nested structure
                break;
                
            case "Observation.valueDateTime":
                // DateTime values don't have nested structure
                break;
                
            case "Observation.valuePeriod":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            case "Observation.dataAbsentReason":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.interpretation":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.bodySite":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.method":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.specimen":
                nestedOrder.addAll(List.of("reference", "display"));
                break;
                
            case "Observation.device":
                nestedOrder.addAll(List.of("reference", "display"));
                break;
                
            case "Observation.referenceRange":
                nestedOrder.addAll(List.of("low", "high", "type", "appliesTo", "age", "text"));
                break;
                
            case "Observation.referenceRange.low":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Observation.referenceRange.high":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Observation.referenceRange.type":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.referenceRange.appliesTo":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.referenceRange.age":
                nestedOrder.addAll(List.of("low", "high"));
                break;
                
            case "Observation.related":
                nestedOrder.addAll(List.of("type", "target"));
                break;
                
            case "Observation.related.target":
                nestedOrder.addAll(List.of("reference", "display"));
                break;
                
            case "Observation.component":
                nestedOrder.addAll(List.of("code", 
                    // Handle component value[x] choice types
                    "value[x]", "valueQuantity", "valueCodeableConcept", "valueString", "valueBoolean", "valueInteger",
                    "valueRange", "valueRatio", "valueSampledData", "valueTime", "valueDateTime", "valuePeriod",
                    "dataAbsentReason", "interpretation", "referenceRange"));
                break;
                
            case "Observation.component.code":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            // Handle component value[x] choice types - all variants
            case "Observation.component.valueQuantity":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Observation.component.valueCodeableConcept":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.component.valueString":
                // String values don't have nested structure
                break;
                
            case "Observation.component.valueBoolean":
                // Boolean values don't have nested structure
                break;
                
            case "Observation.component.valueInteger":
                // Integer values don't have nested structure
                break;
                
            case "Observation.component.valueRange":
                nestedOrder.addAll(List.of("low", "high"));
                break;
                
            case "Observation.component.valueRatio":
                nestedOrder.addAll(List.of("numerator", "denominator"));
                break;
                
            case "Observation.component.valueSampledData":
                nestedOrder.addAll(List.of("origin", "period", "factor", "lowerLimit", "upperLimit", "dimensions", "data"));
                break;
                
            case "Observation.component.valueTime":
                // Time values don't have nested structure
                break;
                
            case "Observation.component.valueDateTime":
                // DateTime values don't have nested structure
                break;
                
            case "Observation.component.valuePeriod":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            case "Observation.component.dataAbsentReason":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.component.interpretation":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.component.referenceRange":
                nestedOrder.addAll(List.of("low", "high", "type", "appliesTo", "age", "text"));
                break;
                
            case "Observation.component.referenceRange.low":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Observation.component.referenceRange.high":
                nestedOrder.addAll(List.of("value", "comparator", "unit", "system", "code"));
                break;
                
            case "Observation.component.referenceRange.type":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.component.referenceRange.appliesTo":
                nestedOrder.addAll(List.of("coding", "text"));
                break;
                
            case "Observation.component.referenceRange.age":
                nestedOrder.addAll(List.of("low", "high"));
                break;
                
            // Common period element ordering
            case "Patient.name.period":
            case "Patient.telecom.period":
            case "Patient.address.period":
            case "Patient.contact.period":
            case "Practitioner.name.period":
            case "Practitioner.telecom.period":
            case "Practitioner.address.period":
            case "Practitioner.qualification.period":
            case "RelatedPerson.name.period":
            case "RelatedPerson.telecom.period":
            case "RelatedPerson.address.period":
                nestedOrder.addAll(List.of("start", "end"));
                break;
                
            default:
                // For unknown nested paths, return empty list to use alphabetical fallback
                break;
        }
        
        return nestedOrder;
    }
    
    /**
     * Checks if canonical ordering is supported for the given resource type
     * 
     * @param resourceType The FHIR resource type
     * @return true if canonical ordering is available for this resource type
     */
    public boolean supportsResourceType(String resourceType) {
        return !getCanonicalElementOrder(resourceType).isEmpty();
    }
    
    /**
     * Gets the list of supported resource types for canonical ordering
     * 
     * @return List of supported FHIR resource types
     */
    public List<String> getSupportedResourceTypes() {
        return List.of("Patient", "Practitioner", "RelatedPerson", "Encounter", "Condition", 
                      "Observation", "Procedure", "Organization");
    }
}
