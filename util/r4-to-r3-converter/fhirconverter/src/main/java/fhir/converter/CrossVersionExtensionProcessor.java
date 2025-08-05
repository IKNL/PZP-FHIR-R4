package fhir.converter;

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

/**
 * Processes R4 resources with cross-version conversion extensions and transforms them to STU3.
 * 
 * The processor handles two types of extensions:
 * 1. Simple Extensions: Direct property mapping (e.g., Communication.notDone)
 * 2. Complex Extensions: Nested structure mapping (e.g., Observation.related)
 * 
 * Extension URL Pattern: http://fhir.conversion/cross-version/{ResourceType}.{propertyName}
 */
public class CrossVersionExtensionProcessor {
    
    private static final Logger logger = LoggerFactory.getLogger(CrossVersionExtensionProcessor.class);
    private static final String EXTENSION_BASE_URL = "http://fhir.conversion/cross-version/";
    
    /**
     * Processes an R4 resource JSON and converts cross-version extensions to STU3 properties
     */
    public String processR4ToSTU3(String r4Json, String resourceType) {
        try {
            JsonParser parser = new JsonParser();
            JsonObject resource = parser.parse(r4Json).getAsJsonObject();
            
            if (!resource.has("extension")) {
                logger.debug("No extensions found in {} resource", resourceType);
                return r4Json;
            }
            
            JsonArray extensions = resource.getAsJsonArray("extension");
            List<JsonObject> crossVersionExtensions = findCrossVersionExtensions(extensions);
            
            if (crossVersionExtensions.isEmpty()) {
                logger.debug("No cross-version extensions found in {} resource", resourceType);
                return r4Json;
            }
            
            logger.info("Processing {} cross-version extensions for {} resource", 
                       crossVersionExtensions.size(), resourceType);
            
            // Process each cross-version extension
            for (JsonObject extension : crossVersionExtensions) {
                processExtension(resource, extension, resourceType);
            }
            
            // Remove processed cross-version extensions
            removeCrossVersionExtensions(resource);
            
            return resource.toString();
            
        } catch (Exception e) {
            logger.error("Failed to process cross-version extensions for {}: {}", resourceType, e.getMessage(), e);
            return r4Json; // Return original on error
        }
    }
    
    /**
     * Finds all cross-version extensions in the extension array
     */
    private List<JsonObject> findCrossVersionExtensions(JsonArray extensions) {
        List<JsonObject> crossVersionExtensions = new ArrayList<>();
        
        for (JsonElement element : extensions) {
            JsonObject extension = element.getAsJsonObject();
            if (extension.has("url")) {
                String url = extension.get("url").getAsString();
                if (url.startsWith(EXTENSION_BASE_URL)) {
                    crossVersionExtensions.add(extension);
                    logger.debug("Found cross-version extension: {}", url);
                }
            }
        }
        
        return crossVersionExtensions;
    }
    
    /**
     * Processes a single cross-version extension
     */
    private void processExtension(JsonObject resource, JsonObject extension, String resourceType) {
        String url = extension.get("url").getAsString();
        String propertyPath = url.substring(EXTENSION_BASE_URL.length());
        
        logger.debug("Processing extension: {} -> {}", url, propertyPath);
        
        if (extension.has("extension")) {
            // Complex extension with nested extensions
            processComplexExtension(resource, extension, propertyPath);
        } else if (extension.has("value") || extension.has("valueBoolean") || 
                   extension.has("valueString") || extension.has("valueReference")) {
            // Simple extension with direct value
            processSimpleExtension(resource, extension, propertyPath);
        } else {
            logger.warn("Extension {} has no recognizable value", url);
        }
    }
    
    /**
     * Processes a simple extension (direct property mapping)
     * Example: Communication.notDone = true
     */
    private void processSimpleExtension(JsonObject resource, JsonObject extension, String propertyPath) {
        String[] pathParts = propertyPath.split("\\.");
        if (pathParts.length != 2) {
            logger.warn("Invalid simple extension property path: {}", propertyPath);
            return;
        }
        
        String resourceName = pathParts[0];
        String propertyName = pathParts[1];
        
        // Extract the value
        JsonElement value = extractExtensionValue(extension);
        if (value == null) {
            logger.warn("Could not extract value from simple extension: {}", propertyPath);
            return;
        }
        
        // Set the property on the resource
        resource.add(propertyName, value);
        logger.info("✅ Applied simple extension: {}.{} = {}", resourceName, propertyName, value);
    }
    
    /**
     * Processes a complex extension (nested structure mapping)
     * Example: Observation.related = { type: "has-member", target: Reference }
     */
    private void processComplexExtension(JsonObject resource, JsonObject extension, String propertyPath) {
        String[] pathParts = propertyPath.split("\\.");
        if (pathParts.length != 2) {
            logger.warn("Invalid complex extension property path: {}", propertyPath);
            return;
        }
        
        String resourceName = pathParts[0];
        String propertyName = pathParts[1];
        
        // Extract nested extensions
        JsonArray nestedExtensions = extension.getAsJsonArray("extension");
        Map<String, JsonElement> nestedValues = new HashMap<>();
        
        for (JsonElement nested : nestedExtensions) {
            JsonObject nestedExt = nested.getAsJsonObject();
            if (nestedExt.has("url")) {
                String nestedUrl = nestedExt.get("url").getAsString();
                JsonElement nestedValue = extractExtensionValue(nestedExt);
                if (nestedValue != null) {
                    nestedValues.put(nestedUrl, nestedValue);
                }
            }
        }
        
        if (nestedValues.isEmpty()) {
            logger.warn("No nested values found in complex extension: {}", propertyPath);
            return;
        }
        
        // Create the complex object based on the property type
        JsonObject complexObject = createComplexObject(propertyName, nestedValues);
        
        if (complexObject != null) {
            // Add to array property (most complex properties are arrays)
            addToArrayProperty(resource, propertyName, complexObject);
            logger.info("✅ Applied complex extension: {}.{} with {} nested properties", 
                       resourceName, propertyName, nestedValues.size());
        }
    }
    
    /**
     * Creates a complex object based on property type and nested values
     */
    private JsonObject createComplexObject(String propertyName, Map<String, JsonElement> nestedValues) {
        JsonObject complexObject = new JsonObject();
        
        switch (propertyName) {
            case "related":
                // Observation.related structure
                if (nestedValues.containsKey("type")) {
                    complexObject.add("type", nestedValues.get("type"));
                }
                if (nestedValues.containsKey("target")) {
                    complexObject.add("target", nestedValues.get("target"));
                }
                break;
                
            case "actor":
                // Consent.actor structure  
                if (nestedValues.containsKey("role")) {
                    complexObject.add("role", nestedValues.get("role"));
                }
                if (nestedValues.containsKey("reference")) {
                    complexObject.add("reference", nestedValues.get("reference"));
                }
                break;
                
            default:
                // Generic complex object - add all nested values
                nestedValues.forEach(complexObject::add);
                break;
        }
        
        return complexObject.size() > 0 ? complexObject : null;
    }
    
    /**
     * Adds an object to an array property, creating the array if it doesn't exist
     */
    private void addToArrayProperty(JsonObject resource, String propertyName, JsonObject object) {
        if (!resource.has(propertyName)) {
            resource.add(propertyName, new JsonArray());
        }
        
        JsonElement property = resource.get(propertyName);
        if (property.isJsonArray()) {
            property.getAsJsonArray().add(object);
        } else {
            // Convert single value to array
            JsonArray array = new JsonArray();
            array.add(property);
            array.add(object);
            resource.add(propertyName, array);
        }
    }
    
    /**
     * Extracts the value from an extension, handling different value types
     */
    private JsonElement extractExtensionValue(JsonObject extension) {
        // Debug: Log the full extension structure
        logger.debug("Extension structure: {}", extension.toString());
        
        // Try different value property names
        String[] valueProps = {"value", "valueBoolean", "valueString", "valueReference", 
                              "valueCode", "valueInteger", "valueDecimal"};
        
        for (String valueProp : valueProps) {
            if (extension.has(valueProp)) {
                logger.debug("Found value property: {} = {}", valueProp, extension.get(valueProp));
                return extension.get(valueProp);
            }
        }
        
        // Log all available properties for debugging
        logger.warn("No recognized value property found. Available properties: {}", extension.keySet());
        
        return null;
    }
    
    /**
     * Removes all cross-version extensions from the resource
     */
    private void removeCrossVersionExtensions(JsonObject resource) {
        if (!resource.has("extension")) {
            return;
        }
        
        JsonArray extensions = resource.getAsJsonArray("extension");
        JsonArray filteredExtensions = new JsonArray();
        
        for (JsonElement element : extensions) {
            JsonObject extension = element.getAsJsonObject();
            if (extension.has("url")) {
                String url = extension.get("url").getAsString();
                if (!url.startsWith(EXTENSION_BASE_URL)) {
                    filteredExtensions.add(extension);
                }
            }
        }
        
        if (filteredExtensions.size() == 0) {
            resource.remove("extension");
        } else {
            resource.add("extension", filteredExtensions);
        }
    }
    
    /**
     * Checks if the processor supports a specific resource type
     */
    public boolean supports(String resourceType) {
        // Support all resource types that might have cross-version extensions
        return resourceType != null;
    }
}
