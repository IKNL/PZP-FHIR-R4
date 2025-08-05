package fhir.converter;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.hl7.fhir.instance.model.api.IBaseResource;
import org.hl7.fhir.r4.context.SimpleWorkerContext;
import org.hl7.fhir.r4.model.StructureMap;
import org.hl7.fhir.r4.utils.StructureMapUtilities;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * A FHIR converter that uses HAPI FHIR StructureMapUtilities for R4 to STU3 conversion.
 * 
 * EXCLUDED RESOURCES:
 * - ImplementationGuide: Not converted as these resources are not used/needed in our context
 */
public class StructureMapFhirConverter {

    private static final Logger logger = LoggerFactory.getLogger(StructureMapFhirConverter.class);

    private final SimpleWorkerContext context;
    private final StructureMapUtilities smu;
    private final FhirContext r4Context = FhirContext.forR4();
    private final FhirContext dstu3Context = FhirContext.forDstu3();
    private final Map<String, StructureMap> structureMaps = new HashMap<>();
    private final CrossVersionExtensionProcessor crossVersionProcessor = new CrossVersionExtensionProcessor();

    public StructureMapFhirConverter(String mapsDirectory) throws IOException {
        logger.info("Initializing StructureMap-based FhirConverter...");
        
        try {
            // Initialize SimpleWorkerContext
            this.context = new SimpleWorkerContext();
            
            // Initialize StructureMapUtilities
            this.smu = new StructureMapUtilities(context);
            
            // Load StructureMaps
            loadStructureMaps(mapsDirectory);
            
            logger.info("StructureMap-based FhirConverter initialized with {} maps", structureMaps.size());
            
        } catch (Exception e) {
            logger.error("Failed to initialize StructureMap-based converter", e);
            throw new IOException("Converter initialization failed", e);
        }
    }

    private void loadStructureMaps(String mapsDirectory) throws IOException {
        Path mapsPath = Paths.get(mapsDirectory);
        if (!Files.exists(mapsPath)) {
            throw new IOException("Maps directory does not exist: " + mapsDirectory);
        }

        // Load JSON StructureMap files first
        loadJsonStructureMaps(mapsPath);
        
        // Try to parse .map files as well
        loadMapFiles(mapsPath);
    }

    private void loadJsonStructureMaps(Path mapsPath) throws IOException {
        try (Stream<Path> paths = Files.walk(mapsPath)) {
            List<Path> jsonFiles = paths.filter(Files::isRegularFile)
                                       .filter(path -> path.toString().endsWith(".json"))
                                       .filter(path -> path.getFileName().toString().startsWith("StructureMap-"))
                                       .collect(Collectors.toList());
            
            logger.info("Found {} JSON StructureMap files", jsonFiles.size());
            
            for (Path jsonFile : jsonFiles) {
                try {
                    logger.debug("Loading JSON StructureMap: {}", jsonFile.getFileName());
                    String jsonContent = Files.readString(jsonFile);
                    
                    // Parse using HAPI FHIR
                    IParser parser = r4Context.newJsonParser();
                    StructureMap structureMap = parser.parseResource(StructureMap.class, jsonContent);
                    
                    // Store the map
                    structureMaps.put(structureMap.getUrl(), structureMap);
                    
                    // Also add to context
                    context.cacheResource(structureMap);
                    
                    logger.debug("Successfully loaded JSON StructureMap: {}", structureMap.getUrl());
                    
                } catch (Exception e) {
                    logger.error("Failed to load JSON StructureMap from {}: {}", jsonFile, e.getMessage());
                }
            }
        }
    }

    private void loadMapFiles(Path mapsPath) throws IOException {
        try (Stream<Path> paths = Files.walk(mapsPath)) {
            List<Path> mapFiles = paths.filter(Files::isRegularFile)
                                       .filter(path -> path.toString().endsWith(".map"))
                                       .collect(Collectors.toList());
            
            logger.info("Found {} .map files", mapFiles.size());
            
            int successfullyParsed = 0;
            int failedToParse = 0;
            
            // Track failed files for detailed reporting
            Map<String, String> failedFiles = new HashMap<>();
            
            for (Path mapFile : mapFiles) {
                try {
                    String fileName = mapFile.getFileName().toString();
                    logger.debug("🔄 Parsing .map file: {}", fileName);
                    String mapContent = Files.readString(mapFile);
                    
                    // Special handling for StructureDefinition.map to get detailed error info
                    boolean isStructureDefinitionMap = fileName.equals("StructureDefinition.map");
                    
                    if (isStructureDefinitionMap) {
                        logger.info("=== PARSING STRUCTUREDEFINITION.MAP ===");
                        logger.info("File path: {}", mapFile.toAbsolutePath());
                        logger.info("File size: {} characters", mapContent.length());
                        logger.info("First 200 characters: {}", 
                                  mapContent.length() > 200 ? mapContent.substring(0, 200) + "..." : mapContent);
                    }
                    
                    // Try to parse using StructureMapUtilities
                    StructureMap structureMap = smu.parse(mapContent, mapFile.toString());
                    
                    if (structureMap != null && structureMap.getUrl() != null) {
                        structureMaps.put(structureMap.getUrl(), structureMap);
                        context.cacheResource(structureMap);
                        successfullyParsed++;
                        logger.debug("✅ Successfully parsed .map file: {} -> {}", fileName, structureMap.getUrl());
                        
                        if (isStructureDefinitionMap) {
                            logger.info("✅ StructureDefinition.map SUCCESSFULLY PARSED!");
                            logger.info("Map URL: {}", structureMap.getUrl());
                            logger.info("Map Name: {}", structureMap.getName());
                            logger.info("Number of groups: {}", structureMap.getGroup().size());
                        }
                    } else {
                        failedToParse++;
                        String reason = "Parsed but result is null or has no URL";
                        failedFiles.put(fileName, reason);
                        
                        if (isStructureDefinitionMap) {
                            logger.error("❌ StructureDefinition.map parsed but result is null or has no URL");
                            logger.error("StructureMap object: {}", structureMap);
                            if (structureMap != null) {
                                logger.error("StructureMap URL: {}", structureMap.getUrl());
                                logger.error("StructureMap Name: {}", structureMap.getName());
                            }
                        } else {
                            logger.warn("❌ Failed to parse {}: {}", fileName, reason);
                        }
                    }
                    
                } catch (Exception e) {
                    failedToParse++;
                    String fileName = mapFile.getFileName().toString();
                    String reason = e.getClass().getSimpleName() + ": " + e.getMessage();
                    failedFiles.put(fileName, reason);
                    
                    boolean isStructureDefinitionMap = fileName.equals("StructureDefinition.map");
                    
                    if (isStructureDefinitionMap) {
                        logger.error("❌ FAILED TO PARSE STRUCTUREDEFINITION.MAP!");
                        logger.error("File: {}", mapFile.toAbsolutePath());
                        logger.error("Error type: {}", e.getClass().getSimpleName());
                        logger.error("Error message: {}", e.getMessage());
                        logger.error("Full stack trace:", e);
                        
                        // Try to show where the parsing failed
                        try {
                            String mapContent = Files.readString(mapFile);
                            String[] lines = mapContent.split("\n");
                            logger.error("Map file has {} lines", lines.length);
                            
                            // Show first few lines for context
                            for (int i = 0; i < Math.min(10, lines.length); i++) {
                                logger.error("Line {}: {}", i + 1, lines[i]);
                            }
                        } catch (Exception readError) {
                            logger.error("Could not even read the map file content: {}", readError.getMessage());
                        }
                    } else {
                        logger.warn("❌ Failed to parse {}: {}", fileName, reason);
                    }
                }
            }
            
            // Comprehensive summary report
            logger.info("📊 === MAP FILE PARSING SUMMARY ===");
            logger.info("📁 Total .map files found: {}", mapFiles.size());
            logger.info("✅ Successfully parsed: {}", successfullyParsed);
            logger.info("❌ Failed to parse: {}", failedToParse);
            
            if (failedToParse > 0) {
                logger.warn("🚨 === DETAILED FAILURE REPORT ===");
                logger.warn("The following {} .map files could not be parsed:", failedToParse);
                
                for (Map.Entry<String, String> failed : failedFiles.entrySet()) {
                    logger.warn("❌ {}: {}", failed.getKey(), failed.getValue());
                }
                
                logger.warn("💡 TROUBLESHOOTING TIPS:");
                logger.warn("   • Check FHIR Mapping Language syntax in failed files");
                logger.warn("   • Verify map declarations have valid URLs and names");
                logger.warn("   • Ensure 'uses' statements reference valid StructureDefinitions");
                logger.warn("   • Check for syntax errors in group definitions and rules");
                logger.warn("   • Validate that all referenced concepts exist in the FHIR version");
                logger.warn("   • Consider using FHIR validator or mapping tools for syntax checking");
            }
        }
    }

    public <T extends IBaseResource> org.hl7.fhir.dstu3.model.Resource convert(T sourceResource, String mapUrl) {
        String resourceType = getResourceType(sourceResource);
        logger.info("🔄 Starting conversion for {} resource", resourceType);
        
        // Check if this resource type is excluded
        if ("ImplementationGuide".equals(resourceType)) {
            logger.info("❌ EXCLUDED: ImplementationGuide resources are not converted (not used in our context)");
            return null;
        }
        
        try {
            // Get the resource type to find appropriate map
            String actualMapUrl = findAppropriateMap(resourceType, mapUrl);
            
            logger.debug("Resource type: {}, Requested map: {}, Actual map URL: {}", resourceType, mapUrl, actualMapUrl);
            
            StructureMap map = structureMaps.get(actualMapUrl);
            if (map == null) {
                logger.warn("⚠️  StructureMap not found: {}. Available maps: {}", 
                          actualMapUrl, structureMaps.keySet());
                logger.info("📋 BASIC CONVERSION: Falling back to basic conversion for {} (missing StructureMap)", resourceType);
                return performBasicConversion(sourceResource);
            }

            logger.debug("Found StructureMap: {}", map.getUrl());
            logger.info("🗺️  STRUCTUREMAP CONVERSION: Using StructureMap for {} -> {}", resourceType, actualMapUrl);

            // Convert HAPI resource to HL7 FHIR R4 resource
            IParser r4Parser = r4Context.newJsonParser().setPrettyPrint(true);
            String resourceJson = r4Parser.encodeResourceToString(sourceResource);
            
            // Parse as HL7 FHIR R4 resource
            org.hl7.fhir.r4.model.Resource r4Resource = 
                (org.hl7.fhir.r4.model.Resource) r4Context.newJsonParser().parseResource(resourceJson);

            logger.debug("Converted to R4 resource: {}", r4Resource.getClass().getSimpleName());

            // Create target resource as R4 first, then convert to STU3
            org.hl7.fhir.r4.model.Resource r4TargetResource = createR4TargetResource(resourceType);

            logger.debug("Created target R4 resource: {}", r4TargetResource.getClass().getSimpleName());

            // Perform transformation using StructureMapUtilities
            logger.debug("Starting StructureMap transformation...");
            // The transform method expects Base types
            org.hl7.fhir.r4.model.Base sourceBase = (org.hl7.fhir.r4.model.Base) r4Resource;
            org.hl7.fhir.r4.model.Base targetBase = (org.hl7.fhir.r4.model.Base) r4TargetResource;
            smu.transform(null, sourceBase, map, targetBase);

            logger.debug("StructureMap transformation completed");

            // Convert the R4 result to STU3 using extension-based cross-version processing
            IParser r4Parser2 = r4Context.newJsonParser().setPrettyPrint(true);
            String resultJson = r4Parser2.encodeResourceToString(r4TargetResource);
            
            logger.debug("R4 result JSON length: {}", resultJson.length());
            
            // Apply cross-version extension processing (replaces manual handleCommunicationNotDone)
            String stu3Json = crossVersionProcessor.processR4ToSTU3(resultJson, resourceType);
            
            IParser dstu3Parser = dstu3Context.newJsonParser().setPrettyPrint(true);
            org.hl7.fhir.dstu3.model.Resource finalResult = 
                (org.hl7.fhir.dstu3.model.Resource) dstu3Parser.parseResource(stu3Json);

            logger.info("✅ STRUCTUREMAP SUCCESS: {} converted successfully using StructureMap: {}", resourceType, actualMapUrl);
            logger.debug("Final result type: {}", finalResult.fhirType());
            return finalResult;

        } catch (Exception e) {
            logger.error("❌ STRUCTUREMAP FAILED: Error in StructureMap conversion for {}", resourceType);
            logger.error("Error type: {}", e.getClass().getSimpleName());
            logger.error("Error message: {}", e.getMessage());
            logger.error("Full stack trace:", e);
            logger.info("📋 BASIC CONVERSION: Falling back to basic conversion for {} due to StructureMap error", resourceType);
            return performBasicConversion(sourceResource);
        }
    }

    private String getResourceType(IBaseResource resource) {
        // Extract resource type from the resource
        String className = resource.getClass().getSimpleName();
        // Remove any HAPI prefixes/suffixes
        return className.replaceAll("^.*\\.", "").replaceAll("R4$", "");
    }

    private String findAppropriateMap(String resourceType, String requestedMapUrl) {
        // Try to find a map for this resource type
        String resourceMapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
        
        if (structureMaps.containsKey(resourceMapUrl)) {
            return resourceMapUrl;
        }
        
        // Try the requested URL
        if (structureMaps.containsKey(requestedMapUrl)) {
            return requestedMapUrl;
        }
        
        // Try some common patterns
        String[] patterns = {
            "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3",
            "http://hl7.org/fhir/StructureMap/" + resourceType.toLowerCase() + "4to3",
            requestedMapUrl
        };
        
        for (String pattern : patterns) {
            if (structureMaps.containsKey(pattern)) {
                return pattern;
            }
        }
        
        return requestedMapUrl; // Return original even if not found
    }

    private org.hl7.fhir.r4.model.Resource createR4TargetResource(String resourceType) {
        // Create appropriate R4 resource based on type (will be transformed and then converted to STU3)
        // NOTE: ImplementationGuide is excluded and will never reach this method
        switch (resourceType) {
            case "Patient":
                return new org.hl7.fhir.r4.model.Patient();
            case "Observation":
                return new org.hl7.fhir.r4.model.Observation();
            case "Consent":
                return new org.hl7.fhir.r4.model.Consent();
            case "Communication":
                return new org.hl7.fhir.r4.model.Communication();
            case "Encounter":
                return new org.hl7.fhir.r4.model.Encounter();
            case "Goal":
                return new org.hl7.fhir.r4.model.Goal();
            case "Procedure":
                return new org.hl7.fhir.r4.model.Procedure();
            case "Device":
                return new org.hl7.fhir.r4.model.Device();
            case "DeviceUseStatement":
                return new org.hl7.fhir.r4.model.DeviceUseStatement();
            case "Practitioner":
                return new org.hl7.fhir.r4.model.Practitioner();
            case "PractitionerRole":
                return new org.hl7.fhir.r4.model.PractitionerRole();
            case "RelatedPerson":
                return new org.hl7.fhir.r4.model.RelatedPerson();
            case "StructureDefinition":
                return new org.hl7.fhir.r4.model.StructureDefinition();
            case "ValueSet":
                return new org.hl7.fhir.r4.model.ValueSet();
            case "SearchParameter":
                return new org.hl7.fhir.r4.model.SearchParameter();
            case "ImplementationGuide":
                // This should never be reached due to exclusion check, but included for completeness
                logger.warn("ImplementationGuide should be excluded - this indicates a bug in the exclusion logic");
                return null;
            default:
                logger.warn("Unknown resource type: {}. Using generic resource.", resourceType);
                return new org.hl7.fhir.r4.model.Basic(); // Fallback
        }
    }

    private org.hl7.fhir.dstu3.model.Resource createTargetResource(String resourceType) {
        // Create appropriate STU3 resource based on type
        switch (resourceType) {
            case "Patient":
                return new org.hl7.fhir.dstu3.model.Patient();
            case "Observation":
                return new org.hl7.fhir.dstu3.model.Observation();
            case "Consent":
                return new org.hl7.fhir.dstu3.model.Consent();
            case "Communication":
                return new org.hl7.fhir.dstu3.model.Communication();
            case "Encounter":
                return new org.hl7.fhir.dstu3.model.Encounter();
            case "Goal":
                return new org.hl7.fhir.dstu3.model.Goal();
            case "Procedure":
                return new org.hl7.fhir.dstu3.model.Procedure();
            case "Device":
                return new org.hl7.fhir.dstu3.model.Device();
            case "DeviceUseStatement":
                return new org.hl7.fhir.dstu3.model.DeviceUseStatement();
            case "Practitioner":
                return new org.hl7.fhir.dstu3.model.Practitioner();
            case "PractitionerRole":
                return new org.hl7.fhir.dstu3.model.PractitionerRole();
            case "RelatedPerson":
                return new org.hl7.fhir.dstu3.model.RelatedPerson();
            case "StructureDefinition":
                return new org.hl7.fhir.dstu3.model.StructureDefinition();
            case "ValueSet":
                return new org.hl7.fhir.dstu3.model.ValueSet();
            case "SearchParameter":
                return new org.hl7.fhir.dstu3.model.SearchParameter();
            case "ImplementationGuide":
                // This should never be reached due to exclusion check, but included for completeness
                logger.warn("ImplementationGuide should be excluded - this indicates a bug in the exclusion logic");
                return null;
            default:
                logger.warn("Unknown resource type: {}. Using generic resource.", resourceType);
                return new org.hl7.fhir.dstu3.model.Basic(); // Fallback
        }
    }

    private org.hl7.fhir.dstu3.model.Resource performBasicConversion(IBaseResource sourceResource) {
        String resourceType = getResourceType(sourceResource);
        logger.info("📋 BASIC CONVERSION: Performing basic conversion (fallback) for {}", resourceType);
        
        try {
            // Fall back to basic conversion approach
            IParser r4Parser = r4Context.newJsonParser().setPrettyPrint(true);
            String resourceJson = r4Parser.encodeResourceToString(sourceResource);
            
            logger.debug("Basic conversion - R4 JSON length: {}", resourceJson.length());
            
            IParser dstu3Parser = dstu3Context.newJsonParser().setPrettyPrint(true);
            IBaseResource dstu3Resource = dstu3Parser.parseResource(resourceJson);
            
            logger.info("✅ BASIC SUCCESS: {} converted successfully using basic conversion", resourceType);
            logger.debug("Basic conversion result type: {}", dstu3Resource.fhirType());
            
            return (org.hl7.fhir.dstu3.model.Resource) dstu3Resource;
            
        } catch (Exception e) {
            logger.error("❌ BASIC FAILED: Basic conversion failed for {}", resourceType);
            logger.error("Basic conversion failed - Error type: {}", e.getClass().getSimpleName());
            logger.error("Basic conversion failed - Error message: {}", e.getMessage());
            logger.error("Basic conversion failed - Full stack trace:", e);
            throw new RuntimeException("Basic conversion methods failed: " + e.getMessage(), e);
        }
    }

    public FhirContext getR4Context() {
        return r4Context;
    }

    public FhirContext getDstu3Context() {
        return dstu3Context;
    }
    
    public CrossVersionExtensionProcessor getCrossVersionProcessor() {
        return crossVersionProcessor;
    }

    public void printLoadedMaps() {
        logger.info("Loaded StructureMaps ({}):", structureMaps.size());
        for (String url : structureMaps.keySet()) {
            logger.info("  - {}", url);
        }
        
        // Cross-version extension processor is ready
        logger.info("Cross-Version Extension Processor: Ready for R4→STU3 transformations");
    }
}
