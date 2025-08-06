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
import java.io.FileReader;
import java.io.IOException;

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
    private static final String ZIB2017_IDENTITY = "pall-izppz-zibs2017-v2025-03-11";
    private static final String ZIB2020_IDENTITY = "pall-izppz-v2025-03-11";
    
    public CrossVersionPostProcessor() {
        // Initialize Gson with pretty printing
        this.prettyGson = new GsonBuilder()
            .setPrettyPrinting()
            .disableHtmlEscaping()
            .create();
            
        // Load ZIB mapping
        this.zib2020ToZib2017Mapping = loadZibMapping();
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
        
        // Add ZIB2017 mappings based on ZIB2020 mappings
        addZib2017Mappings(resource);
        
        // Remove elements marked for deletion
        removeMarkedElements(resource);
        
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
}
