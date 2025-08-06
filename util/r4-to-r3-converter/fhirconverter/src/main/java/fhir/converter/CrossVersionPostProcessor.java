package fhir.converter;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Handles post-processing rules for cross-version FHIR conversion.
 * 
 * This class contains specific post-processing logic that needs to be applied
 * after StructureMap transformations to ensure proper R4 to STU3 conversion.
 * 
 * Post-processing rules include:
 * - Element cleanup (removing marked elements)
 * - ID transformation (slice name removal)
 * - Property renaming and restructuring
 * - Validation and consistency checks
 */
public class CrossVersionPostProcessor {
    
    private static final Logger logger = LoggerFactory.getLogger(CrossVersionPostProcessor.class);
    private final Gson prettyGson;
    private final Map<String, String> zib2020ToZib2017Mapping;
    private final Map<String, Map<String, Integer>> schemaElementOrders;
    private static final String ZIB2017_IDENTITY = "pall-izppz-zibs2017-v2025-03-11";
    private static final String ZIB2020_IDENTITY = "pall-izppz-v2025-03-11";
    private static final String SCHEMA_PATH = "fhir.stu3.schema.json";
    
    public CrossVersionPostProcessor() {
        // Initialize Gson with pretty printing
        this.prettyGson = new GsonBuilder()
            .setPrettyPrinting()
            .disableHtmlEscaping()
            .create();
            
        // Load ZIB mapping
        this.zib2020ToZib2017Mapping = loadZibMapping();
        
        // Load schema-based element orders
        this.schemaElementOrders = loadSchemaElementOrders();
    }
    
    /**
     * Processes a converted STU3 resource and applies all necessary post-processing rules
     */
    public String processSTU3Resource(String stu3Json, String resourceType) {
        try {
            JsonParser parser = new JsonParser();
            JsonObject resource = parser.parse(stu3Json).getAsJsonObject();
            
            // Apply resource-specific post-processing
            switch (resourceType) {
                case "StructureDefinition":
                    return processStructureDefinition(resource);
                case "Patient":
                case "Practitioner":
                case "RelatedPerson":
                    return processPersonResource(resource, resourceType);
                default:
                    return processGenericResource(resource, resourceType);
            }
            
        } catch (Exception e) {
            logger.error("Failed to post-process {} resource: {}", resourceType, e.getMessage(), e);
            return stu3Json; // Return original on error
        }
    }
    
    /**
     * Processes StructureDefinition resources with specific cleanup rules
     */
    private String processStructureDefinition(JsonObject resource) {
        logger.debug("Post-processing StructureDefinition resource");
        
        // Clean up nameInformation slice names from element IDs
        cleanupNameInformationSliceIds(resource);
        
        // Clean up telecom slice names from element IDs and deduplicate
        cleanupTelecomSliceIds(resource);
        
        // Consolidate slices into single elements for STU3 compatibility
        consolidateSlices(resource);
        
        // Apply element transformations (remove/move/update elements)
        applyElementTransformations(resource);
        
        // Add ZIB2017 mappings based on ZIB2020 mappings
        addZib2017Mappings(resource);
        
        // Remove elements marked for deletion
        removeMarkedElements(resource);
        
        // Sort elements according to FHIR specification order
        sortElementsByFhirOrder(resource);
        
        // Validate element structure
        validateElementStructure(resource);
        
        logger.info("StructureDefinition post-processing completed successfully");
        return prettyGson.toJson(resource);
    }
    
    /**
     * Processes Person-type resources (Patient, Practitioner, RelatedPerson)
     */
    private String processPersonResource(JsonObject resource, String resourceType) {
        logger.debug("Post-processing {} resource", resourceType);
        
        // Apply person-specific transformations here if needed
        // For now, just apply generic processing
        
        logger.info("{} post-processing completed successfully", resourceType);
        return prettyGson.toJson(resource);
    }
    
    /**
     * Processes generic resources with common post-processing rules
     */
    private String processGenericResource(JsonObject resource, String resourceType) {
        logger.debug("Post-processing {} resource (generic)", resourceType);
        
        // Apply generic transformations here if needed
        
        logger.info("{} post-processing completed successfully (generic)", resourceType);
        return prettyGson.toJson(resource);
    }
    
    /**
     * Cleans up nameInformation slice names from element IDs for Patient, Practitioner, and RelatedPerson
     */
    private void cleanupNameInformationSliceIds(JsonObject resource) {
        try {
            int cleanedCount = 0;
            
            // Clean up snapshot elements
            if (resource.has("snapshot") && resource.getAsJsonObject("snapshot").has("element")) {
                JsonArray elements = resource.getAsJsonObject("snapshot").getAsJsonArray("element");
                cleanedCount += cleanupElementIds(elements, "snapshot");
            }
            
            // Clean up differential elements
            if (resource.has("differential") && resource.getAsJsonObject("differential").has("element")) {
                JsonArray elements = resource.getAsJsonObject("differential").getAsJsonArray("element");
                cleanedCount += cleanupElementIds(elements, "differential");
            }
            
            if (cleanedCount > 0) {
                logger.info("✅ Cleaned up {} nameInformation slice names from element IDs", cleanedCount);
            }
            
        } catch (Exception e) {
            logger.error("Failed to cleanup nameInformation slice IDs: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Helper method to clean up element IDs in an element array
     */
    private int cleanupElementIds(JsonArray elements, String section) {
        int cleanedCount = 0;
        
        for (JsonElement elementElement : elements) {
            JsonObject element = elementElement.getAsJsonObject();
            
            if (element.has("id")) {
                String id = element.get("id").getAsString();
                
                if (id != null && id.contains(":nameInformation")) {
                    // Check if this is a Patient, Practitioner, or RelatedPerson element
                    if (id.startsWith("Patient.name:nameInformation") ||
                        id.startsWith("Practitioner.name:nameInformation") ||
                        id.startsWith("RelatedPerson.name:nameInformation")) {
                        
                        String cleanedId = id.replace(":nameInformation", "");
                        element.addProperty("id", cleanedId);
                        cleanedCount++;
                        
                        logger.debug("Cleaned element ID in {}: {} -> {}", section, id, cleanedId);
                    }
                }
            }
        }
        
        return cleanedCount;
    }
    
    /**
     * Cleans up telecom slice names from element IDs and deduplicates elements with same path
     */
    private void cleanupTelecomSliceIds(JsonObject resource) {
        try {
            int cleanedCount = 0;
            
            // Clean up snapshot elements
            if (resource.has("snapshot") && resource.getAsJsonObject("snapshot").has("element")) {
                JsonArray elements = resource.getAsJsonObject("snapshot").getAsJsonArray("element");
                cleanedCount += cleanupAndDeduplicateTelecomElements(elements, "snapshot");
            }
            
            // Clean up differential elements
            if (resource.has("differential") && resource.getAsJsonObject("differential").has("element")) {
                JsonArray elements = resource.getAsJsonObject("differential").getAsJsonArray("element");
                cleanedCount += cleanupAndDeduplicateTelecomElements(elements, "differential");
            }
            
            if (cleanedCount > 0) {
                logger.info("✅ Cleaned up {} telecom slice names and deduplicated elements", cleanedCount);
            }
            
        } catch (Exception e) {
            logger.error("Failed to cleanup telecom slice IDs: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Helper method to clean up telecom element IDs and deduplicate elements in an element array
     */
    private int cleanupAndDeduplicateTelecomElements(JsonArray elements, String section) {
        int processedCount = 0;
        Map<String, JsonObject> pathToElementMap = new HashMap<>();
        List<JsonObject> elementsToKeep = new ArrayList<>();
        
        for (JsonElement elementElement : elements) {
            JsonObject element = elementElement.getAsJsonObject();
            
            if (element.has("id")) {
                String id = element.get("id").getAsString();
                String originalId = id;
                
                // Check if this is a telecom element for Patient, Practitioner, or RelatedPerson
                if (id != null && id.contains(".telecom:") &&
                    (id.startsWith("Patient.telecom:") ||
                     id.startsWith("Practitioner.telecom:") ||
                     id.startsWith("RelatedPerson.telecom:"))) {
                    
                    // Remove telecom slice names
                    String cleanedId = id.replaceAll(":telephoneNumbers", "").replaceAll(":emailAddresses", "");
                    element.addProperty("id", cleanedId);
                    processedCount++;
                    
                    logger.debug("Cleaned telecom element ID in {}: {} -> {}", section, originalId, cleanedId);
                    
                    // Check for deduplication based on path
                    if (element.has("path")) {
                        String path = element.get("path").getAsString();
                        String cleanedPath = path.replaceAll(":telephoneNumbers", "").replaceAll(":emailAddresses", "");
                        
                        if (pathToElementMap.containsKey(cleanedPath)) {
                            // Merge with existing element
                            JsonObject existingElement = pathToElementMap.get(cleanedPath);
                            mergeElementMappings(existingElement, element);
                            logger.debug("Merged telecom element mappings for path: {}", cleanedPath);
                        } else {
                            // First element with this path
                            pathToElementMap.put(cleanedPath, element);
                            elementsToKeep.add(element);
                        }
                    } else {
                        elementsToKeep.add(element);
                    }
                } else {
                    // Non-telecom element, keep as-is
                    elementsToKeep.add(element);
                }
            } else {
                // Element without ID, keep as-is
                elementsToKeep.add(element);
            }
        }
        
        // Replace the elements array with deduplicated elements
        if (processedCount > 0) {
            // Clear the array and rebuild it
            while (elements.size() > 0) {
                elements.remove(0);
            }
            for (JsonObject element : elementsToKeep) {
                elements.add(element);
            }
        }
        
        return processedCount;
    }
    
    /**
     * Merges mapping properties from source element into target element
     */
    private void mergeElementMappings(JsonObject targetElement, JsonObject sourceElement) {
        if (sourceElement.has("mapping")) {
            JsonArray sourceMappings = sourceElement.getAsJsonArray("mapping");
            
            if (targetElement.has("mapping")) {
                JsonArray targetMappings = targetElement.getAsJsonArray("mapping");
                
                // Add source mappings to target, avoiding duplicates
                for (JsonElement sourceMappingElement : sourceMappings) {
                    JsonObject sourceMapping = sourceMappingElement.getAsJsonObject();
                    boolean isDuplicate = false;
                    
                    // Check if this mapping already exists
                    for (JsonElement targetMappingElement : targetMappings) {
                        JsonObject targetMapping = targetMappingElement.getAsJsonObject();
                        if (areMappingsEqual(sourceMapping, targetMapping)) {
                            isDuplicate = true;
                            break;
                        }
                    }
                    
                    if (!isDuplicate) {
                        targetMappings.add(sourceMapping);
                    }
                }
            } else {
                // Target has no mappings, copy all from source
                targetElement.add("mapping", sourceMappings);
            }
        }
    }
    
    /**
     * Checks if two mapping objects are equal (same identity and map values)
     */
    private boolean areMappingsEqual(JsonObject mapping1, JsonObject mapping2) {
        String identity1 = mapping1.has("identity") ? mapping1.get("identity").getAsString() : "";
        String identity2 = mapping2.has("identity") ? mapping2.get("identity").getAsString() : "";
        String map1 = mapping1.has("map") ? mapping1.get("map").getAsString() : "";
        String map2 = mapping2.has("map") ? mapping2.get("map").getAsString() : "";
        
        return identity1.equals(identity2) && map1.equals(map2);
    }
    
    /**
     * Consolidates slices into single elements for STU3 compatibility
     */
    private void consolidateSlices(JsonObject resource) {
        try {
            if (!resource.has("differential") || 
                !resource.getAsJsonObject("differential").has("element")) {
                return;
            }
            
            JsonArray elements = resource.getAsJsonObject("differential").getAsJsonArray("element");
            List<JsonObject> consolidatedElements = new ArrayList<>();
            Map<String, SliceGroup> sliceGroups = new HashMap<>();
            
            // Group elements by their slice patterns
            for (JsonElement elementElement : elements) {
                JsonObject element = elementElement.getAsJsonObject();
                
                if (element.has("id")) {
                    String id = element.get("id").getAsString();
                    SliceConsolidationResult result = analyzeSliceElement(id, element);
                    
                    if (result.shouldConsolidate) {
                        // Group slice elements for consolidation
                        if (!sliceGroups.containsKey(result.baseElementId)) {
                            sliceGroups.put(result.baseElementId, new SliceGroup(result.baseElementId, result.basePath));
                        }
                        sliceGroups.get(result.baseElementId).addSliceElement(result.sliceName, element);
                    } else {
                        // Keep non-slice elements as-is
                        consolidatedElements.add(element);
                    }
                }
            }
            
            // Consolidate slice groups
            int consolidatedCount = 0;
            for (SliceGroup group : sliceGroups.values()) {
                JsonObject consolidatedElement = group.consolidate();
                if (consolidatedElement != null) {
                    consolidatedElements.add(consolidatedElement);
                    consolidatedCount++;
                    logger.debug("Consolidated slice group: {}", group.baseElementId);
                }
            }
            
            if (consolidatedCount > 0) {
                // Replace the elements array
                while (elements.size() > 0) {
                    elements.remove(0);
                }
                for (JsonObject element : consolidatedElements) {
                    elements.add(element);
                }
                logger.info("✅ Consolidated {} slice groups into single elements", consolidatedCount);
            }
            
        } catch (Exception e) {
            logger.error("Failed to consolidate slices: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Analyzes an element to determine if it should be part of slice consolidation
     */
    private SliceConsolidationResult analyzeSliceElement(String id, JsonObject element) {
        SliceConsolidationResult result = new SliceConsolidationResult();
        
        // Check for participant slice pattern: "ResourceType.participant:sliceName.individual"
        if (id.matches(".*\\.participant:[^.]+\\.individual$")) {
            String[] parts = id.split("\\.");
            String resourceType = parts[0];
            String sliceName = parts[1].split(":")[1]; // Extract slice name
            
            result.shouldConsolidate = true;
            result.baseElementId = resourceType + ".participant.individual";
            result.basePath = resourceType + ".participant.individual";
            result.sliceName = sliceName;
            result.consolidationType = "participant.individual";
            
            return result;
        }
        
        // Check for base participant slice: "ResourceType.participant:sliceName"
        if (id.matches(".*\\.participant:[^.]+$")) {
            // Skip base slice elements - they will be removed during consolidation
            result.shouldConsolidate = true;
            result.baseElementId = "SKIP_BASE_SLICE";
            return result;
        }
        
        // Future: Add more slice patterns here (telecom, name, etc.)
        
        result.shouldConsolidate = false;
        return result;
    }
    
    /**
     * Result of slice element analysis
     */
    private static class SliceConsolidationResult {
        boolean shouldConsolidate = false;
        String baseElementId;
        String basePath;
        String sliceName;
        String consolidationType;
    }
    
    /**
     * Groups slice elements for consolidation
     */
    private static class SliceGroup {
        final String baseElementId;
        final String basePath;
        final Map<String, JsonObject> sliceElements = new HashMap<>();
        
        SliceGroup(String baseElementId, String basePath) {
            this.baseElementId = baseElementId;
            this.basePath = basePath;
        }
        
        void addSliceElement(String sliceName, JsonObject element) {
            if (sliceName != null) {
                sliceElements.put(sliceName, element);
            }
        }
        
        JsonObject consolidate() {
            if (sliceElements.isEmpty()) {
                return null;
            }
            
            JsonObject consolidated = new JsonObject();
            consolidated.addProperty("id", baseElementId);
            consolidated.addProperty("path", basePath);
            
            // Consolidate types from all slice elements
            JsonArray consolidatedTypes = new JsonArray();
            JsonArray consolidatedMappings = new JsonArray();
            
            for (JsonObject sliceElement : sliceElements.values()) {
                // Merge types
                if (sliceElement.has("type")) {
                    JsonArray types = sliceElement.getAsJsonArray("type");
                    for (JsonElement type : types) {
                        consolidatedTypes.add(type);
                    }
                }
                
                // Merge mappings
                if (sliceElement.has("mapping")) {
                    JsonArray mappings = sliceElement.getAsJsonArray("mapping");
                    for (JsonElement mapping : mappings) {
                        consolidatedMappings.add(mapping);
                    }
                }
                
                // Copy other properties from first element (min, max, etc.)
                if (consolidated.size() == 2) { // Only id and path so far
                    for (String key : sliceElement.keySet()) {
                        if (!key.equals("id") && !key.equals("path") && 
                            !key.equals("type") && !key.equals("mapping") &&
                            !key.equals("sliceName")) {
                            consolidated.add(key, sliceElement.get(key));
                        }
                    }
                }
            }
            
            if (consolidatedTypes.size() > 0) {
                consolidated.add("type", consolidatedTypes);
            }
            
            if (consolidatedMappings.size() > 0) {
                consolidated.add("mapping", consolidatedMappings);
            }
            
            return consolidated;
        }
    }
    
    /**
     * Applies element transformations (remove, move, update) based on predefined rules
     */
    private void applyElementTransformations(JsonObject resource) {
        try {
            if (!resource.has("differential") || 
                !resource.getAsJsonObject("differential").has("element")) {
                return;
            }
            
            JsonArray elements = resource.getAsJsonObject("differential").getAsJsonArray("element");
            List<JsonObject> transformedElements = new ArrayList<>();
            
            // Get transformation rules
            List<ElementTransformationRule> rules = getElementTransformationRules(resource);
            
            int removedCount = 0;
            int movedCount = 0;
            
            for (JsonElement elementElement : elements) {
                JsonObject element = elementElement.getAsJsonObject();
                
                if (element.has("id")) {
                    String id = element.get("id").getAsString();
                    ElementTransformationRule matchingRule = findMatchingRule(id, rules);
                    
                    if (matchingRule != null) {
                        switch (matchingRule.action) {
                            case REMOVE:
                                removedCount++;
                                logger.debug("Removing element: {}", id);
                                // Skip this element (don't add to transformedElements)
                                break;
                                
                            case MOVE:
                                JsonObject movedElement = moveElement(element, matchingRule);
                                transformedElements.add(movedElement);
                                movedCount++;
                                logger.debug("Moved element: {} -> {}", id, matchingRule.newId);
                                break;
                                
                            default:
                                transformedElements.add(element);
                                break;
                        }
                    } else {
                        // No rule matches, keep element as-is
                        transformedElements.add(element);
                    }
                } else {
                    // Element without ID, keep as-is
                    transformedElements.add(element);
                }
            }
            
            if (removedCount > 0 || movedCount > 0) {
                // Replace the elements array
                while (elements.size() > 0) {
                    elements.remove(0);
                }
                for (JsonObject element : transformedElements) {
                    elements.add(element);
                }
                logger.info("✅ Applied element transformations: {} removed, {} moved", removedCount, movedCount);
            }
            
        } catch (Exception e) {
            logger.error("Failed to apply element transformations: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Gets transformation rules for the current StructureDefinition
     */
    private List<ElementTransformationRule> getElementTransformationRules(JsonObject resource) {
        List<ElementTransformationRule> rules = new ArrayList<>();
        
        // Get the StructureDefinition type to apply type-specific rules
        String resourceType = resource.has("type") ? resource.get("type").getAsString() : "";
        
        if ("Encounter".equals(resourceType)) {
            // Encounter-specific transformation rules - MOVED TO STRUCTUREMAP for performance
            // Simple remove/transform operations are now handled in ElementDefinition.map
            
            // NOTE: The following rules have been moved to StructureMap:
            // - Remove reasonCode:deviatingResult and its children
            // - Remove reasonReference (except procedure slice) 
            // - Transform reasonReference:procedure to diagnosis.condition
            
            // Complex slice consolidation still handled here in post-processing
        }
        
        // Add more resource type rules here as needed
        
        return rules;
    }
    
    /**
     * Finds a matching transformation rule for the given element ID
     */
    private ElementTransformationRule findMatchingRule(String elementId, List<ElementTransformationRule> rules) {
        for (ElementTransformationRule rule : rules) {
            if (rule.sourceId.equals(elementId)) {
                return rule;
            }
        }
        return null;
    }
    
    /**
     * Moves an element by updating its ID and path
     */
    private JsonObject moveElement(JsonObject element, ElementTransformationRule rule) {
        JsonObject movedElement = element.deepCopy();
        
        // Update ID and path
        movedElement.addProperty("id", rule.newId);
        movedElement.addProperty("path", rule.newPath);
        
        // Remove sliceName if it exists (since we're moving to a new location)
        movedElement.remove("sliceName");
        
        return movedElement;
    }
    
    /**
     * Element transformation rule
     */
    private static class ElementTransformationRule {
        final String sourceId;
        final ElementTransformationAction action;
        final String newId;
        final String newPath;
        
        // Constructor for REMOVE action
        ElementTransformationRule(String sourceId, ElementTransformationAction action) {
            this.sourceId = sourceId;
            this.action = action;
            this.newId = null;
            this.newPath = null;
        }
        
        // Constructor for MOVE action
        ElementTransformationRule(String sourceId, ElementTransformationAction action, String newId, String newPath) {
            this.sourceId = sourceId;
            this.action = action;
            this.newId = newId;
            this.newPath = newPath;
        }
    }
    
    /**
     * Element transformation actions
     */
    private enum ElementTransformationAction {
        REMOVE,
        MOVE
    }
    
    /**
     * Removes elements marked for deletion during StructureMap processing
     */
    private void removeMarkedElements(JsonObject resource) {
        try {
            // Process differential elements
            if (resource.has("differential")) {
                JsonObject differential = resource.getAsJsonObject("differential");
                if (differential.has("element")) {
                    JsonArray elements = differential.getAsJsonArray("element");
                    JsonArray cleanedElements = new JsonArray();
                    
                    int removedCount = 0;
                    for (JsonElement elementElement : elements) {
                        JsonObject element = elementElement.getAsJsonObject();
                        
                        // Check if this element should be removed
                        if (element.has("id")) {
                            String id = element.get("id").getAsString();
                            
                            // Remove explicitly marked elements
                            if ("element-to-be-removed-in-postprocess".equals(id)) {
                                removedCount++;
                                logger.debug("Removing marked element with ID: {}", id);
                                continue; // Skip this element
                            }
                            
                            // Remove empty name elements that only have id and path
                            if (isEmptyNameElement(element, id)) {
                                removedCount++;
                                logger.debug("Removing empty name element with ID: {}", id);
                                continue; // Skip this element
                            }
                        }
                        
                        // Keep this element
                        cleanedElements.add(element);
                    }
                    
                    if (removedCount > 0) {
                        logger.info("✅ Removed {} StructureDefinition elements marked for cleanup", removedCount);
                        differential.add("element", cleanedElements);
                    }
                }
            }
            
        } catch (Exception e) {
            logger.error("Failed to remove marked elements: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Checks if an element is an empty name element that should be removed
     */
    private boolean isEmptyNameElement(JsonObject element, String id) {
        // Check if this is a Patient.name, Practitioner.name, or RelatedPerson.name element
        if ("Patient.name".equals(id) || "Practitioner.name".equals(id) || "RelatedPerson.name".equals(id)) {
            // Check if element has exactly 2 properties: id and path, nothing else
            if (element.size() == 2 && element.has("id") && element.has("path")) {
                String path = element.get("path").getAsString();
                // Remove if id matches path exactly (confirming it's a duplicate base element)
                boolean shouldRemove = id.equals(path);
                if (shouldRemove) {
                    logger.debug("Found duplicate empty name element: id={}, path={}", id, path);
                }
                return shouldRemove;
            }
        }
        
        return false;
    }
    
    /**
     * Validates the structure of elements in a StructureDefinition
     */
    private void validateElementStructure(JsonObject resource) {
        try {
            // Basic validation - ensure we have required properties
            if (!resource.has("kind")) {
                logger.warn("StructureDefinition missing 'kind' property");
            }
            
            if (!resource.has("type")) {
                logger.warn("StructureDefinition missing 'type' property");
            }
            
            // Validate snapshot/differential structure
            boolean hasSnapshot = resource.has("snapshot");
            boolean hasDifferential = resource.has("differential");
            
            if (!hasSnapshot && !hasDifferential) {
                logger.warn("StructureDefinition has neither snapshot nor differential");
            }
            
            logger.debug("StructureDefinition validation complete");
            
        } catch (Exception e) {
            logger.error("Failed to validate element structure: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Checks if the post-processor supports a specific resource type
     */
    public boolean supports(String resourceType) {
        // Support all resource types for now
        return resourceType != null;
    }
    
    /**
     * Gets the list of supported post-processing operations
     */
    public String[] getSupportedOperations() {
        return new String[]{
            "cleanupNameInformationSliceIds",
            "cleanupTelecomSliceIds",
            "consolidateSlices",
            "applyElementTransformations",
            "addZib2017Mappings",
            "removeMarkedElements", 
            "validateElementStructure"
        };
    }
    
    /**
     * Loads the ZIB2020 to ZIB2017 mapping from the JSON file
     */
    private Map<String, String> loadZibMapping() {
        Map<String, String> mapping = new HashMap<>();
        
        try {
            String mappingFilePath = "matched_concepts_between_zib2017_and_zib2020.json";
            JsonParser parser = new JsonParser();
            JsonArray mappings = parser.parse(new FileReader(mappingFilePath)).getAsJsonArray();
            
            for (JsonElement element : mappings) {
                JsonObject mappingObj = element.getAsJsonObject();
                String zib2020Id = mappingObj.get("zib2020_id").getAsString();
                String zib2017Id = mappingObj.get("zib2017_id").getAsString();
                mapping.put(zib2020Id, zib2017Id);
            }
            
            logger.info("✅ Loaded {} ZIB2020→ZIB2017 mappings", mapping.size());
            
        } catch (Exception e) {
            logger.error("Failed to load ZIB mapping file: {}", e.getMessage(), e);
        }
        
        return mapping;
    }
    
    /**
     * Loads schema-based element orders for FHIR resources from JSON schema files
     */
    private Map<String, Map<String, Integer>> loadSchemaElementOrders() {
        Map<String, Map<String, Integer>> resourceOrders = new HashMap<>();
        
        try {
            // Common FHIR resource types that might be used in StructureDefinitions
            String[] resourceTypes = {"Patient", "Practitioner", "RelatedPerson", "Encounter", 
                                    "Observation", "Condition", "Procedure", "MedicationStatement", 
                                    "CarePlan", "Goal", "Consent", "QuestionnaireResponse"};
            
            for (String resourceType : resourceTypes) {
                Map<String, Integer> elementOrder = loadElementOrderFromSchema(resourceType);
                if (!elementOrder.isEmpty()) {
                    resourceOrders.put(resourceType, elementOrder);
                }
            }
            
            logger.info("✅ Loaded schema-based element orders for {} resource types", resourceOrders.size());
            
        } catch (Exception e) {
            logger.error("Failed to load schema element orders: {}", e.getMessage(), e);
        }
        
        return resourceOrders;
    }
    
    /**
     * Loads element order from a specific FHIR resource schema file
     */
    private Map<String, Integer> loadElementOrderFromSchema(String resourceType) {
        Map<String, Integer> elementOrder = new LinkedHashMap<>();
        
        try {
            Path schemaPath = Paths.get(SCHEMA_PATH, resourceType + ".schema.json");
            if (!Files.exists(schemaPath)) {
                logger.debug("Schema file not found: {}", schemaPath);
                return elementOrder;
            }
            
            String schemaContent = new String(Files.readAllBytes(schemaPath));
            JsonParser parser = new JsonParser();
            JsonObject schema = parser.parse(schemaContent).getAsJsonObject();
            
            // Navigate to the resource definition properties
            if (schema.has("definitions")) {
                JsonObject definitions = schema.getAsJsonObject("definitions");
                if (definitions.has(resourceType)) {
                    JsonObject resourceDef = definitions.getAsJsonObject(resourceType);
                    if (resourceDef.has("allOf")) {
                        JsonArray allOf = resourceDef.getAsJsonArray("allOf");
                        for (JsonElement element : allOf) {
                            JsonObject allOfItem = element.getAsJsonObject();
                            if (allOfItem.has("properties")) {
                                JsonObject properties = allOfItem.getAsJsonObject("properties");
                                int order = 0;
                                for (Map.Entry<String, JsonElement> property : properties.entrySet()) {
                                    String propertyName = property.getKey();
                                    elementOrder.put(resourceType + "." + propertyName, order * 10);
                                    order++;
                                }
                                break; // Found the properties, stop looking
                            }
                        }
                    }
                }
            }
            
            logger.debug("Loaded {} element orders for {}", elementOrder.size(), resourceType);
            
        } catch (Exception e) {
            logger.warn("Failed to load schema for {}: {}", resourceType, e.getMessage());
        }
        
        return elementOrder;
    }
    
    /**
     * Adds ZIB2017 mappings to StructureDefinition elements based on existing ZIB2020 mappings
     */
    private void addZib2017Mappings(JsonObject resource) {
        try {
            boolean hasAddedMappings = false;
            int totalMappingsAdded = 0;
            
            // Process differential elements
            if (resource.has("differential")) {
                JsonObject differential = resource.getAsJsonObject("differential");
                if (differential.has("element")) {
                    JsonArray elements = differential.getAsJsonArray("element");
                    
                    for (JsonElement elementElement : elements) {
                        JsonObject element = elementElement.getAsJsonObject();
                        
                        if (element.has("mapping")) {
                            JsonArray mappings = element.getAsJsonArray("mapping");
                            List<JsonObject> newMappingsToAdd = new ArrayList<>();
                            
                            // Check each existing mapping for ZIB2020 mappings
                            for (JsonElement mappingElement : mappings) {
                                JsonObject mapping = mappingElement.getAsJsonObject();
                                
                                // Check if this is a ZIB2020 mapping
                                if (mapping.has("identity") && mapping.has("map") &&
                                    ZIB2020_IDENTITY.equals(mapping.get("identity").getAsString())) {
                                    
                                    String zib2020Id = mapping.get("map").getAsString();
                                    
                                    // Check if we have a corresponding ZIB2017 mapping
                                    if (zib2020ToZib2017Mapping.containsKey(zib2020Id)) {
                                        String zib2017Id = zib2020ToZib2017Mapping.get(zib2020Id);
                                        
                                        // Check if ZIB2017 mapping doesn't already exist
                                        if (!hasZib2017Mapping(mappings, zib2017Id)) {
                                            // Create new ZIB2017 mapping
                                            JsonObject newMapping = new JsonObject();
                                            newMapping.addProperty("identity", ZIB2017_IDENTITY);
                                            newMapping.addProperty("map", zib2017Id);
                                            
                                            // Copy comment if it exists
                                            if (mapping.has("comment")) {
                                                newMapping.addProperty("comment", mapping.get("comment").getAsString());
                                            }
                                            
                                            newMappingsToAdd.add(newMapping);
                                            
                                            logger.debug("Prepared ZIB2017 mapping: {} → {} for element {}",
                                                       zib2020Id, zib2017Id, element.get("id").getAsString());
                                        }
                                    }
                                }
                            }
                            
                            // Add all new mappings to this element
                            for (JsonObject newMapping : newMappingsToAdd) {
                                mappings.add(newMapping);
                                totalMappingsAdded++;
                                hasAddedMappings = true;
                            }
                        }
                    }
                }
            }
            
            // Add ZIB2017 mapping identity to root if we added any mappings
            if (hasAddedMappings) {
                addZib2017MappingIdentity(resource);
                logger.info("✅ Added {} ZIB2017 mappings to StructureDefinition elements", totalMappingsAdded);
            }
            
        } catch (Exception e) {
            logger.error("Failed to add ZIB2017 mappings: {}", e.getMessage(), e);
        }
    }
    
    /**
     * Checks if a ZIB2017 mapping with the given ID already exists
     */
    private boolean hasZib2017Mapping(JsonArray mappings, String zib2017Id) {
        for (JsonElement mappingElement : mappings) {
            JsonObject mapping = mappingElement.getAsJsonObject();
            if (mapping.has("identity") && mapping.has("map") &&
                ZIB2017_IDENTITY.equals(mapping.get("identity").getAsString()) &&
                zib2017Id.equals(mapping.get("map").getAsString())) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Adds ZIB2017 mapping identity to the StructureDefinition root if not already present
     */
    private void addZib2017MappingIdentity(JsonObject resource) {
        if (!resource.has("mapping")) {
            resource.add("mapping", new JsonArray());
        }
        
        JsonArray mappings = resource.getAsJsonArray("mapping");
        
        // Check if ZIB2017 mapping identity already exists
        for (JsonElement mappingElement : mappings) {
            JsonObject mapping = mappingElement.getAsJsonObject();
            if (mapping.has("identity") && 
                ZIB2017_IDENTITY.equals(mapping.get("identity").getAsString())) {
                return; // Already exists
            }
        }
        
        // Add ZIB2017 mapping identity
        JsonObject zib2017Mapping = new JsonObject();
        zib2017Mapping.addProperty("identity", ZIB2017_IDENTITY);
        zib2017Mapping.addProperty("uri", "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48");
        zib2017Mapping.addProperty("name", "PZP dataset zibs2017");
        
        mappings.add(zib2017Mapping);
        
        logger.debug("Added ZIB2017 mapping identity to StructureDefinition root");
    }
    
    /**
     * Sorts elements in a StructureDefinition differential according to FHIR specification order
     * Uses JSON schemas to determine the correct ordering for the target resource type
     */
    private void sortElementsByFhirOrder(JsonObject resource) {
        if (!resource.has("differential") || !resource.getAsJsonObject("differential").has("element")) {
            return;
        }
        
        // Determine the resource type this StructureDefinition is defining
        String targetResourceType = null;
        if (resource.has("type")) {
            targetResourceType = resource.get("type").getAsString();
        }
        
        if (targetResourceType == null) {
            logger.debug("Cannot determine target resource type for StructureDefinition, skipping element sorting");
            return;
        }
        
        // Create a final copy for use in lambda
        final String resourceType = targetResourceType;
        
        JsonArray elements = resource.getAsJsonObject("differential").getAsJsonArray("element");
        if (elements.size() <= 1) {
            return;
        }
        
        // Convert to list for sorting
        List<JsonElement> elementList = new ArrayList<>();
        for (JsonElement element : elements) {
            elementList.add(element);
        }
        
        // Sort by FHIR specification order using schema-based ordering
        elementList.sort((a, b) -> {
            String pathA = a.getAsJsonObject().get("path").getAsString();
            String pathB = b.getAsJsonObject().get("path").getAsString();
            return compareFhirPathsUsingSchema(pathA, pathB, resourceType);
        });
        
        // Replace the original array with sorted elements
        JsonArray sortedElements = new JsonArray();
        for (JsonElement element : elementList) {
            sortedElements.add(element);
        }
        resource.getAsJsonObject("differential").add("element", sortedElements);
        
        logger.debug("Sorted {} elements for {} according to FHIR specification order", elements.size(), resourceType);
    }
    
    /**
     * Compares two FHIR element paths according to FHIR specification ordering
     * Uses schema-based ordering for the target resource type
     */
    private int compareFhirPathsUsingSchema(String pathA, String pathB, String targetResourceType) {
        // Get schema-based FHIR specification order for each path
        int orderA = getSchemaElementOrder(pathA, targetResourceType);
        int orderB = getSchemaElementOrder(pathB, targetResourceType);
        
        // Compare by FHIR specification order
        if (orderA != orderB) {
            return Integer.compare(orderA, orderB);
        }
        
        // If same order (or both unknown), fall back to path comparison
        return pathA.compareTo(pathB);
    }
    
    /**
     * Get the FHIR specification order for an element path using schema-based ordering
     */
    private int getSchemaElementOrder(String path, String targetResourceType) {
        // Root element (e.g., "Encounter") should always come first
        if (path.equals(targetResourceType)) {
            return 0;
        }
        
        // Check if we have schema-based ordering for this resource type
        Map<String, Integer> resourceOrdering = schemaElementOrders.get(targetResourceType);
        if (resourceOrdering != null && resourceOrdering.containsKey(path)) {
            return resourceOrdering.get(path);
        }
        
        // For sub-elements (e.g., "Encounter.period.start"), try parent element
        String[] pathParts = path.split("\\.");
        if (pathParts.length > 2) {
            String parentPath = pathParts[0] + "." + pathParts[1];
            if (resourceOrdering != null && resourceOrdering.containsKey(parentPath)) {
                int parentOrder = resourceOrdering.get(parentPath);
                // Add small offset for sub-elements based on their position
                int subElementOffset = 0;
                for (int i = 2; i < pathParts.length; i++) {
                    subElementOffset += i;
                }
                return parentOrder + subElementOffset;
            }
        }
        
        // Fall back to element name-based ordering for unknown paths
        return getElementOrderByNameAndDepth(path);
    }
    
    /**
     * Compares two FHIR element paths according to FHIR specification ordering
     * Uses predefined order mapping based on official FHIR resource definitions
     */
    private int compareFhirPaths(String pathA, String pathB) {
        // Get FHIR specification order for each path
        int orderA = getFhirElementOrder(pathA);
        int orderB = getFhirElementOrder(pathB);
        
        // Compare by FHIR specification order
        if (orderA != orderB) {
            return Integer.compare(orderA, orderB);
        }
        
        // If same order (or both unknown), fall back to path comparison
        return pathA.compareTo(pathB);
    }
    
    /**
     * Get the FHIR specification order for an element path
     * Based on the official FHIR resource definitions and @Child order annotations
     */
    private int getFhirElementOrder(String path) {
        // Create a comprehensive mapping based on FHIR specification
        // This follows the order defined in FHIR resource definitions
        
        // Handle full path mappings first
        switch (path) {
            // Common resource elements (appear in most resources)
            case "Encounter.id": return 10;
            case "Encounter.meta": return 20;
            case "Encounter.implicitRules": return 30;
            case "Encounter.language": return 40;
            case "Encounter.text": return 50;
            case "Encounter.contained": return 60;
            case "Encounter.extension": return 70;
            case "Encounter.modifierExtension": return 80;
            
            // Encounter-specific elements (based on FHIR R4 specification)
            case "Encounter.identifier": return 100;
            case "Encounter.status": return 110;
            case "Encounter.statusHistory": return 120;
            case "Encounter.class": return 130;
            case "Encounter.classHistory": return 140;
            case "Encounter.type": return 150;
            case "Encounter.serviceType": return 160;
            case "Encounter.priority": return 170;
            case "Encounter.subject": return 180;
            case "Encounter.episodeOfCare": return 190;
            case "Encounter.basedOn": return 200;
            case "Encounter.participant": return 210;
            case "Encounter.appointment": return 220;
            case "Encounter.period": return 230;
            case "Encounter.length": return 240;
            case "Encounter.reasonCode": return 250;
            case "Encounter.reasonReference": return 260;
            case "Encounter.diagnosis": return 270;
            case "Encounter.account": return 280;
            case "Encounter.hospitalization": return 290;
            case "Encounter.location": return 300;
            case "Encounter.serviceProvider": return 310;
            case "Encounter.partOf": return 320;
            
            // Sub-elements (maintain relative order within parent)
            case "Encounter.participant.type": return 211;
            case "Encounter.participant.period": return 212;
            case "Encounter.participant.individual": return 213;
            case "Encounter.period.start": return 231;
            case "Encounter.period.end": return 232;
            case "Encounter.diagnosis.condition": return 271;
            case "Encounter.diagnosis.use": return 272;
            case "Encounter.diagnosis.rank": return 273;
            
            // Patient elements (for reference)
            case "Patient.id": return 10;
            case "Patient.meta": return 20;
            case "Patient.identifier": return 100;
            case "Patient.active": return 110;
            case "Patient.name": return 120;
            case "Patient.telecom": return 130;
            case "Patient.gender": return 140;
            case "Patient.birthDate": return 150;
            case "Patient.address": return 160;
            case "Patient.contact": return 170;
            
            // Practitioner elements (for reference)
            case "Practitioner.id": return 10;
            case "Practitioner.meta": return 20;
            case "Practitioner.identifier": return 100;
            case "Practitioner.active": return 110;
            case "Practitioner.name": return 120;
            case "Practitioner.telecom": return 130;
            case "Practitioner.address": return 140;
            case "Practitioner.gender": return 150;
            case "Practitioner.birthDate": return 160;
            case "Practitioner.qualification": return 170;
            
            // RelatedPerson elements (for reference)
            case "RelatedPerson.id": return 10;
            case "RelatedPerson.meta": return 20;
            case "RelatedPerson.identifier": return 100;
            case "RelatedPerson.active": return 110;
            case "RelatedPerson.patient": return 120;
            case "RelatedPerson.relationship": return 130;
            case "RelatedPerson.name": return 140;
            case "RelatedPerson.telecom": return 150;
            case "RelatedPerson.gender": return 160;
            case "RelatedPerson.birthDate": return 170;
            case "RelatedPerson.address": return 180;
            
            default:
                // For unknown paths, determine order by element name and depth
                return getElementOrderByNameAndDepth(path);
        }
    }
    
    /**
     * Get order for elements by their name and path depth when full path is not in the mapping
     */
    private int getElementOrderByNameAndDepth(String path) {
        String[] parts = path.split("\\.");
        String elementName = parts[parts.length - 1];
        int depth = parts.length;
        
        // Base order by element name
        int baseOrder = getElementOrderByName(elementName);
        
        // Adjust by depth (deeper elements get higher numbers)
        return baseOrder + (depth - 1) * 1000;
    }
    
    /**
     * Get base order for common FHIR element names
     */
    private int getElementOrderByName(String elementName) {
        switch (elementName) {
            case "id": return 10;
            case "meta": return 20;
            case "implicitRules": return 30;
            case "language": return 40;
            case "text": return 50;
            case "contained": return 60;
            case "extension": return 70;
            case "modifierExtension": return 80;
            case "identifier": return 100;
            case "active": return 110;
            case "status": return 110;
            case "name": return 120;
            case "telecom": return 130;
            case "address": return 140;
            case "gender": return 150;
            case "birthDate": return 160;
            case "subject": return 180;
            case "participant": return 210;
            case "period": return 230;
            case "start": return 231;
            case "end": return 232;
            case "diagnosis": return 270;
            case "condition": return 271;
            default: return 500; // Unknown elements get middle priority
        }
    }
}
