package fhir.converter.crossversion;

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
 * Generic processor for handling cross-version transformations using temporary FHIR extensions.
 * 
 * This implements the "Extension-Based Cross-Version Bridge" pattern:
 * 1. StructureMaps add temporary extensions for STU3-specific properties
 * 2. This processor finds and converts those extensions to native STU3 properties
 * 3. Extensions are removed from the final STU3 resource
 * 
 * ARCHITECTURE NOTE:
 * HAPI FHIR StructureMapUtilities is version-specific (R4 only), so we cannot
 * directly transform R4 → STU3. We use R4 → R4 (with extensions) → STU3 pattern.
 */
public class CrossVersionExtensionProcessor {
    
    private static final Logger logger = LoggerFactory.getLogger(CrossVersionExtensionProcessor.class);
    
    // Extension URL prefix for cross-version transformation hints
    private static final String CROSS_VERSION_EXTENSION_PREFIX = "http://fhir.conversion/cross-version/";
    
    private final Map<String, List<CrossVersionRule>> rulesByResourceType = new HashMap<>();
    private final JsonParser jsonParser = new JsonParser();
    
    public CrossVersionExtensionProcessor() {
        initializeStandardRules();
    }
    
    /**
     * Initialize standard cross-version transformation rules
     */
    private void initializeStandardRules() {
        // Communication.notDone rule
        addRule("Communication", new CrossVersionRule(
            CROSS_VERSION_EXTENSION_PREFIX + "Communication.notDone",
            "notDone",
            "R4 'not-done' status → STU3 notDone boolean",
            this::processBooleanExtension
        ));
        
        // Procedure.notDone rule
        addRule("Procedure", new CrossVersionRule(
            CROSS_VERSION_EXTENSION_PREFIX + "Procedure.notDone", 
            "notDone",
            "R4 'not-done' status → STU3 notDone boolean",
            this::processBooleanExtension
        ));
        
        // Procedure.notDoneReason rule
        addRule("Procedure", new CrossVersionRule(
            CROSS_VERSION_EXTENSION_PREFIX + "Procedure.notDoneReason",
            "notDoneReason", 
            "R4 statusReason → STU3 notDoneReason when status='not-done'",
            this::processCodeableConceptExtension
        ));
        
        // Add more rules as needed for other resources...
    }
    
    /**
     * Add a cross-version transformation rule for a specific resource type
     */
    public void addRule(String resourceType, CrossVersionRule rule) {
        rulesByResourceType.computeIfAbsent(resourceType, k -> new ArrayList<>()).add(rule);
        logger.debug("Added cross-version rule for {}: {} → {}", 
                    resourceType, rule.getExtensionUrl(), rule.getTargetProperty());
    }
    
    /**
     * Process R4 JSON with cross-version extensions and convert to STU3 JSON
     */
    public String processR4ToSTU3(String r4Json, String resourceType) {
        try {
            JsonObject jsonObject = jsonParser.parse(r4Json).getAsJsonObject();
            
            // Get rules for this resource type
            List<CrossVersionRule> rules = rulesByResourceType.get(resourceType);
            if (rules == null || rules.isEmpty()) {
                logger.debug("No cross-version rules for resource type: {}", resourceType);
                return r4Json; // No transformation needed
            }
            
            // Check if resource has extensions
            JsonArray extensions = jsonObject.getAsJsonArray("extension");
            if (extensions == null) {
                logger.debug("No extensions found in {} resource", resourceType);
                return r4Json; // No extensions to process
            }
            
            boolean hasTransformations = false;
            List<JsonElement> extensionsToRemove = new ArrayList<>();
            
            // Process each extension against our rules
            for (JsonElement extensionElement : extensions) {
                JsonObject extension = extensionElement.getAsJsonObject();
                String url = extension.get("url").getAsString();
                
                // Find matching rule
                CrossVersionRule matchingRule = rules.stream()
                    .filter(rule -> rule.getExtensionUrl().equals(url))
                    .findFirst()
                    .orElse(null);
                    
                if (matchingRule != null) {
                    logger.debug("Processing cross-version extension: {} → {}", url, matchingRule.getTargetProperty());
                    
                    // Extract extension value
                    Object extensionValue = extractExtensionValue(extension);
                    
                    // Apply transformation
                    String transformedJson = matchingRule.getProcessor().process(
                        extensionValue, jsonObject.toString(), null);
                    
                    // Update our JSON object
                    jsonObject = jsonParser.parse(transformedJson).getAsJsonObject();
                    
                    // Mark extension for removal
                    extensionsToRemove.add(extensionElement);
                    hasTransformations = true;
                }
            }
            
            // Remove processed extensions
            if (hasTransformations) {
                JsonArray newExtensions = new JsonArray();
                for (JsonElement extensionElement : extensions) {
                    if (!extensionsToRemove.contains(extensionElement)) {
                        newExtensions.add(extensionElement);
                    }
                }
                
                // Update extensions array (or remove if empty)
                if (newExtensions.size() > 0) {
                    jsonObject.add("extension", newExtensions);
                } else {
                    jsonObject.remove("extension");
                }
                
                logger.info("✅ Applied {} cross-version transformations to {}", 
                           extensionsToRemove.size(), resourceType);
            }
            
            return jsonObject.toString();
            
        } catch (Exception e) {
            logger.error("Failed to process cross-version extensions for {}: {}", resourceType, e.getMessage());
            return r4Json; // Return original on error
        }
    }
    
    /**
     * Extract value from extension based on type
     */
    private Object extractExtensionValue(JsonObject extension) {
        // Check for different value types (valueBoolean, valueString, valueCodeableConcept, etc.)
        for (String key : extension.keySet()) {
            if (key.startsWith("value")) {
                return extension.get(key);
            }
        }
        return null;
    }
    
    /**
     * Process boolean extension (e.g., notDone)
     */
    private String processBooleanExtension(Object extensionValue, String targetJson, Object originalSource) {
        if (extensionValue instanceof JsonElement) {
            JsonElement valueElement = (JsonElement) extensionValue;
            boolean boolValue = valueElement.getAsBoolean();
            
            // Parse target JSON and add boolean property
            JsonObject jsonObject = jsonParser.parse(targetJson).getAsJsonObject();
            jsonObject.addProperty("notDone", boolValue);
            
            return jsonObject.toString();
        }
        return targetJson;
    }
    
    /**
     * Process CodeableConcept extension (e.g., notDoneReason)
     */
    private String processCodeableConceptExtension(Object extensionValue, String targetJson, Object originalSource) {
        if (extensionValue instanceof JsonElement) {
            JsonElement valueElement = (JsonElement) extensionValue;
            
            // Parse target JSON and add CodeableConcept property  
            JsonObject jsonObject = jsonParser.parse(targetJson).getAsJsonObject();
            jsonObject.add("notDoneReason", valueElement);
            
            return jsonObject.toString();
        }
        return targetJson;
    }
    
    /**
     * Get all registered rules for debugging
     */
    public Map<String, List<CrossVersionRule>> getAllRules() {
        return new HashMap<>(rulesByResourceType);
    }
}
