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
        
        // Special handling for Consent.except which has deeply nested structure
        if ("except".equals(propertyName) && "Consent".equals(resourceName)) {
            processExceptExtension(resource, extension, propertyPath);
            return;
        }
        
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
            // For STU3 Consent, provision should be mapped to "except" 
            String targetPropertyName = ("provision".equals(propertyName) && "Consent".equals(resourceName)) ? "except" : propertyName;
            
            // Add to array property (most complex properties are arrays)
            addToArrayProperty(resource, targetPropertyName, complexObject);
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
                
            case "except":
                // Consent.except structure - handle complex nested structure
                return createExceptObject(nestedValues);
                
            default:
                // Generic complex object - add all nested values
                nestedValues.forEach(complexObject::add);
                break;
        }
        
        return complexObject.size() > 0 ? complexObject : null;
    }
    
    /**
     * Creates a Consent.except object from nested extension values
     * Handles the complex structure with actor, data, and nested provisions
     */
    private JsonObject createExceptObject(Map<String, JsonElement> nestedValues) {
        JsonObject except = new JsonObject();
        
        // Simple properties
        if (nestedValues.containsKey("type")) {
            except.add("type", nestedValues.get("type"));
        }
        if (nestedValues.containsKey("period")) {
            except.add("period", nestedValues.get("period"));
        }
        if (nestedValues.containsKey("action")) {
            except.add("action", nestedValues.get("action"));
        }
        if (nestedValues.containsKey("securityLabel")) {
            except.add("securityLabel", nestedValues.get("securityLabel"));
        }
        if (nestedValues.containsKey("purpose")) {
            except.add("purpose", nestedValues.get("purpose"));
        }
        if (nestedValues.containsKey("class")) {
            except.add("class", nestedValues.get("class"));
        }
        if (nestedValues.containsKey("code")) {
            except.add("code", nestedValues.get("code"));
        }
        if (nestedValues.containsKey("dataPeriod")) {
            except.add("dataPeriod", nestedValues.get("dataPeriod"));
        }
        
        logger.debug("Created except object with {} simple properties", except.size());
        return except.size() > 0 ? except : new JsonObject();
    }
    
    /**
     * Processes Consent.except extension with deeply nested structure
     */
    private void processExceptExtension(JsonObject resource, JsonObject extension, String propertyPath) {
        if (!extension.has("extension")) {
            logger.warn("Except extension has no nested extensions");
            return;
        }
        
        JsonArray nestedExtensions = extension.getAsJsonArray("extension");
        JsonObject except = new JsonObject();
        
        for (JsonElement nested : nestedExtensions) {
            JsonObject nestedExt = nested.getAsJsonObject();
            if (!nestedExt.has("url")) continue;
            
            String nestedUrl = nestedExt.get("url").getAsString();
            logger.debug("Processing except sub-extension: {}", nestedUrl);
            
            switch (nestedUrl) {
                case "type":
                case "period":
                case "action":
                case "securityLabel":
                case "purpose":
                case "class":
                case "code":
                case "dataPeriod":
                    // Simple value extensions
                    JsonElement value = extractExtensionValue(nestedExt);
                    if (value != null) {
                        except.add(nestedUrl, value);
                        logger.debug("Added except.{} = {}", nestedUrl, value);
                    }
                    break;
                    
                case "actor":
                    // Complex actor extension - these can have multiple instances
                    if (nestedExt.has("extension")) {
                        JsonObject actor = processActorSubExtension(nestedExt);
                        if (actor != null) {
                            addToArrayProperty(except, "actor", actor);
                            logger.debug("Added except.actor with {} properties", actor.size());
                        }
                    }
                    break;
                    
                case "data":
                    // Complex data extension - these can have multiple instances
                    if (nestedExt.has("extension")) {
                        JsonObject data = processDataSubExtension(nestedExt);
                        if (data != null) {
                            addToArrayProperty(except, "data", data);
                            logger.debug("Added except.data with {} properties", data.size());
                        }
                    }
                    break;
                    
                default:
                    // Handle nested except recursively (when URL matches except pattern)
                    if (nestedUrl.equals("http://fhir.conversion/cross-version/Consent.except")) {
                        JsonObject nestedExcept = processNestedExcept(nestedExt);
                        if (nestedExcept != null) {
                            addToArrayProperty(except, "except", nestedExcept);
                            logger.debug("Added nested except");
                        }
                    } else {
                        logger.debug("Unhandled except sub-extension: {}", nestedUrl);
                    }
                    break;
            }
        }
        
        if (except.size() > 0) {
            // For STU3 Consent, we want to create "except" property (array)
            addToArrayProperty(resource, "except", except);
            logger.info("✅ Applied complex extension: Consent.except with {} properties", except.size());
        } else {
            logger.warn("No except properties were processed");
        }
    }
    
    /**
     * Processes an actor sub-extension
     */
    private JsonObject processActorSubExtension(JsonObject actorExt) {
        if (!actorExt.has("extension")) return null;
        
        JsonObject actor = new JsonObject();
        JsonArray subExtensions = actorExt.getAsJsonArray("extension");
        
        for (JsonElement sub : subExtensions) {
            JsonObject subExt = sub.getAsJsonObject();
            if (subExt.has("url")) {
                String url = subExt.get("url").getAsString();
                JsonElement value = extractExtensionValue(subExt);
                if (value != null) {
                    actor.add(url, value);
                }
            }
        }
        
        return actor.size() > 0 ? actor : null;
    }
    
    /**
     * Processes a data sub-extension
     */
    private JsonObject processDataSubExtension(JsonObject dataExt) {
        if (!dataExt.has("extension")) return null;
        
        JsonObject data = new JsonObject();
        JsonArray subExtensions = dataExt.getAsJsonArray("extension");
        
        for (JsonElement sub : subExtensions) {
            JsonObject subExt = sub.getAsJsonObject();
            if (subExt.has("url")) {
                String url = subExt.get("url").getAsString();
                JsonElement value = extractExtensionValue(subExt);
                if (value != null) {
                    data.add(url, value);
                }
            }
        }
        
        return data.size() > 0 ? data : null;
    }
    
    /**
     * Processes a nested except recursively
     */
    private JsonObject processNestedExcept(JsonObject exceptExt) {
        JsonObject nestedExcept = new JsonObject();
        // Recursively process the nested except structure
        // This would follow the same pattern as processExceptExtension
        // For now, return a placeholder - the full implementation would be recursive
        return nestedExcept;
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
        
        // Try different value property names including new FHIR value types
        String[] valueProps = {"value", "valueBoolean", "valueString", "valueReference", 
                              "valueCode", "valueInteger", "valueDecimal", "valueCodeableConcept",
                              "valueCoding", "valuePeriod", "valueDateTime", "valueUri"};
        
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
