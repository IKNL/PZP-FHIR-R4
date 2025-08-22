package fhir.converter;

import com.google.gson.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

/**
 * Inserts STU3 mappings from integration.json into converted STU3 StructureDefinition files.
 * 
 * This class reads the integration.json file containing dataset mappings and adds:
 * 1. Mapping declaration to StructureDefinition.mapping
 * 2. Element mappings to appropriate differential elements
 */
public class Stu3MappingInserter {
    
    private static final Logger logger = LoggerFactory.getLogger(Stu3MappingInserter.class);
    private final Gson prettyGson;
    
    // Mapping constants
    private static final String MAPPING_IDENTITY = "pall-izppz-zib2017v2025-03-11";
    private static final String MAPPING_URI = "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/";
    private static final String MAPPING_NAME = "PZP zib2017 dataset";
    
    public Stu3MappingInserter() {
        this.prettyGson = new GsonBuilder().setPrettyPrinting().create();
    }
    
    /**
     * Process all STU3 StructureDefinition files and insert mappings from integration.json
     */
    public void insertMappingsIntoStu3Profiles(String stu3ResourcesDir, String integrationJsonPath) throws IOException {
        logger.info("Starting STU3 mapping insertion...");
        logger.info("STU3 resources directory: {}", stu3ResourcesDir);
        logger.info("Integration JSON path: {}", integrationJsonPath);
        
        // Load integration mappings
        Map<String, List<IntegrationMapping>> profileMappings = loadIntegrationMappings(integrationJsonPath);
        
        // Process all STU3 StructureDefinition files
        Path resourcesPath = Paths.get(stu3ResourcesDir);
        if (!Files.exists(resourcesPath)) {
            logger.warn("STU3 resources directory does not exist: {}", stu3ResourcesDir);
            return;
        }
        
        Files.walk(resourcesPath)
            .filter(Files::isRegularFile)
            .filter(path -> {
                String filename = path.getFileName().toString();
                // Remove converted- or manual- prefix if present
                if (filename.startsWith("converted-")) {
                    filename = filename.substring("converted-".length());
                } else if (filename.startsWith("manual-")) {
                    filename = filename.substring("manual-".length());
                }
                // Accept any StructureDefinition-*.json file (with or without -STU3)
                return filename.startsWith("StructureDefinition-") && filename.endsWith(".json");
            })
            .forEach(file -> {
                try {
                    processStructureDefinitionFile(file, profileMappings);
                } catch (Exception e) {
                    logger.error("Failed to process file: {}", file, e);
                }
            });
        
        logger.info("STU3 mapping insertion completed");
    }
    
    /**
     * Load integration mappings from integration.json
     */
    private Map<String, List<IntegrationMapping>> loadIntegrationMappings(String integrationJsonPath) throws IOException {
        logger.info("Loading integration mappings from: {}", integrationJsonPath);
        
        Map<String, List<IntegrationMapping>> profileMappings = new HashMap<>();
        
        try (FileReader reader = new FileReader(integrationJsonPath)) {
            JsonArray integrationArray = JsonParser.parseReader(reader).getAsJsonArray();
            
            for (JsonElement element : integrationArray) {
                JsonObject record = element.getAsJsonObject();
                
                if (record.has("stu3_mappings")) {
                    JsonArray stu3Mappings = record.getAsJsonArray("stu3_mappings");
                    
                    for (JsonElement mappingElement : stu3Mappings) {
                        JsonObject mapping = mappingElement.getAsJsonObject();
                        
                        String profileId = getStringValue(mapping, "profile_id");
                        String datasetId = getStringValue(record, "dataset_id");
                        String datasetName = getStringValue(record, "name");
                        String elementPath = getStringValue(mapping, "element_path");
                        String elementId = getStringValue(mapping, "element_id");
                        
                        if (profileId != null && datasetId != null && elementPath != null) {
                            IntegrationMapping integrationMapping = new IntegrationMapping(
                                datasetId, datasetName, elementPath, elementId
                            );
                            
                            profileMappings.computeIfAbsent(profileId, k -> new ArrayList<>())
                                          .add(integrationMapping);
                        }
                    }
                }
            }
        }
        
        logger.info("Loaded mappings for {} profiles", profileMappings.size());
        for (String profileId : profileMappings.keySet()) {
            logger.debug("Profile {}: {} mappings", profileId, profileMappings.get(profileId).size());
        }
        
        return profileMappings;
    }
    
    /**
     * Process a single StructureDefinition file and insert mappings
     */
    private void processStructureDefinitionFile(Path file, Map<String, List<IntegrationMapping>> profileMappings) throws IOException {
        logger.debug("Processing file: {}", file);
        
        // Extract profile ID from filename
        String filename = file.getFileName().toString();
        String profileId = extractProfileIdFromFilename(filename);
        
        if (profileId == null) {
            logger.warn("Could not extract profile ID from filename: {}", filename);
            return;
        }
        
        List<IntegrationMapping> mappings = profileMappings.get(profileId);
        if (mappings == null || mappings.isEmpty()) {
            logger.debug("No mappings found for profile: {}", profileId);
            return;
        }
        
        logger.info("Processing profile {} with {} mappings", profileId, mappings.size());
        
        // Load and modify the JSON
        JsonObject structureDefinition;
        try (FileReader reader = new FileReader(file.toFile())) {
            structureDefinition = JsonParser.parseReader(reader).getAsJsonObject();
        }
        
        // Add mapping declaration
        addMappingDeclaration(structureDefinition);
        
        // Add element mappings
        addElementMappings(structureDefinition, mappings);
        
        // Save the modified JSON
        try (FileWriter writer = new FileWriter(file.toFile())) {
            prettyGson.toJson(structureDefinition, writer);
        }
        
        logger.info("Updated profile: {}", profileId);
    }
    
    /**
     * Extract profile ID from filename (e.g., "converted-StructureDefinition-ACP-Patient-STU3.json" -> "ACP-Patient")
     */
    private String extractProfileIdFromFilename(String filename) {
        // Remove converted- or manual- prefix if present
        String cleanFilename = filename;
        if (filename.startsWith("converted-")) {
            cleanFilename = filename.substring("converted-".length());
        } else if (filename.startsWith("manual-")) {
            cleanFilename = filename.substring("manual-".length());
        }

        // Accept both with and without -STU3 suffix
        if (cleanFilename.startsWith("StructureDefinition-") && cleanFilename.endsWith(".json")) {
            String base = cleanFilename.substring("StructureDefinition-".length(), cleanFilename.length() - ".json".length());
            if (base.endsWith("-STU3")) {
                base = base.substring(0, base.length() - 6);
            }
            return base;
        }
        return null;
    }
    
    /**
     * Add mapping declaration to StructureDefinition.mapping
     */
    private void addMappingDeclaration(JsonObject structureDefinition) {
        JsonArray mappingArray = structureDefinition.getAsJsonArray("mapping");
        
        if (mappingArray == null) {
            mappingArray = new JsonArray();
            structureDefinition.add("mapping", mappingArray);
        }
        
        // Check if mapping already exists
        for (JsonElement element : mappingArray) {
            JsonObject mapping = element.getAsJsonObject();
            if (MAPPING_IDENTITY.equals(getStringValue(mapping, "identity"))) {
                logger.debug("Mapping declaration already exists");
                return;
            }
        }
        
        // Add new mapping declaration
        JsonObject mappingDeclaration = new JsonObject();
        mappingDeclaration.addProperty("identity", MAPPING_IDENTITY);
        mappingDeclaration.addProperty("uri", MAPPING_URI);
        mappingDeclaration.addProperty("name", MAPPING_NAME);
        
        mappingArray.add(mappingDeclaration);
        logger.debug("Added mapping declaration");
    }
    
    /**
     * Add element mappings to differential elements
     */
    private void addElementMappings(JsonObject structureDefinition, List<IntegrationMapping> mappings) {
        JsonObject differential = structureDefinition.getAsJsonObject("differential");
        if (differential == null) {
            logger.warn("No differential found in StructureDefinition");
            return;
        }
        
        JsonArray elements = differential.getAsJsonArray("element");
        if (elements == null) {
            logger.warn("No elements found in differential");
            return;
        }
        
        // Create a map of element paths/IDs to mappings for easy lookup
        Map<String, List<IntegrationMapping>> elementMappings = new HashMap<>();
        for (IntegrationMapping mapping : mappings) {
            if (mapping.elementPath != null) {
                elementMappings.computeIfAbsent(mapping.elementPath, k -> new ArrayList<>()).add(mapping);
            }
            if (mapping.elementId != null && !mapping.elementId.equals(mapping.elementPath)) {
                elementMappings.computeIfAbsent(mapping.elementId, k -> new ArrayList<>()).add(mapping);
            }
        }
        
        // Process each element
        for (JsonElement elementElement : elements) {
            JsonObject element = elementElement.getAsJsonObject();
            String elementId = getStringValue(element, "id");
            String elementPath = getStringValue(element, "path");
            
            List<IntegrationMapping> elementMappingList = new ArrayList<>();
            
            // Find mappings by element ID or path
            if (elementId != null && elementMappings.containsKey(elementId)) {
                elementMappingList.addAll(elementMappings.get(elementId));
            }
            if (elementPath != null && elementMappings.containsKey(elementPath)) {
                elementMappingList.addAll(elementMappings.get(elementPath));
            }
            
            if (!elementMappingList.isEmpty()) {
                addMappingToElement(element, elementMappingList);
            }
        }
    }
    
    /**
     * Add mapping to a specific element
     */
    private void addMappingToElement(JsonObject element, List<IntegrationMapping> mappings) {
        JsonArray mappingArray = element.getAsJsonArray("mapping");
        
        if (mappingArray == null) {
            mappingArray = new JsonArray();
            element.add("mapping", mappingArray);
        }
        
        // Add mappings
        for (IntegrationMapping mapping : mappings) {
            // Check if mapping already exists
            boolean exists = false;
            for (JsonElement existingElement : mappingArray) {
                JsonObject existingMapping = existingElement.getAsJsonObject();
                if (MAPPING_IDENTITY.equals(getStringValue(existingMapping, "identity")) &&
                    mapping.datasetId.equals(getStringValue(existingMapping, "map"))) {
                    exists = true;
                    break;
                }
            }
            
            if (!exists) {
                JsonObject elementMapping = new JsonObject();
                elementMapping.addProperty("identity", MAPPING_IDENTITY);
                elementMapping.addProperty("map", mapping.datasetId);
                if (mapping.datasetName != null) {
                    elementMapping.addProperty("comment", mapping.datasetName);
                }
                
                mappingArray.add(elementMapping);
                logger.debug("Added mapping to element {}: {} -> {}", 
                           getStringValue(element, "path"), mapping.datasetId, mapping.datasetName);
            }
        }
    }
    
    /**
     * Safely get string value from JsonObject
     */
    private String getStringValue(JsonObject obj, String key) {
        JsonElement element = obj.get(key);
        return element != null && !element.isJsonNull() ? element.getAsString() : null;
    }
    
    /**
     * Data class to hold integration mapping information
     */
    private static class IntegrationMapping {
        final String datasetId;
        final String datasetName;
        final String elementPath;
        final String elementId;
        
        IntegrationMapping(String datasetId, String datasetName, String elementPath, String elementId) {
            this.datasetId = datasetId;
            this.datasetName = datasetName;
            this.elementPath = elementPath;
            this.elementId = elementId;
        }
    }
}
