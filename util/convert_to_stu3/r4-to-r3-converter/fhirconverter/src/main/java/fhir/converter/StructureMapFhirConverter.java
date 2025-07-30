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

/**
 * A FHIR converter that uses HAPI FHIR StructureMapUtilities for R4 to STU3 conversion.
 */
public class StructureMapFhirConverter {

    private static final Logger logger = LoggerFactory.getLogger(StructureMapFhirConverter.class);

    private final SimpleWorkerContext context;
    private final StructureMapUtilities smu;
    private final FhirContext r4Context = FhirContext.forR4();
    private final FhirContext dstu3Context = FhirContext.forDstu3();
    private final Map<String, StructureMap> structureMaps = new HashMap<>();

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
            
            for (Path mapFile : mapFiles) {
                try {
                    logger.debug("Parsing .map file: {}", mapFile.getFileName());
                    String mapContent = Files.readString(mapFile);
                    
                    // Try to parse using StructureMapUtilities
                    StructureMap structureMap = smu.parse(mapContent, mapFile.toString());
                    
                    if (structureMap != null && structureMap.getUrl() != null) {
                        structureMaps.put(structureMap.getUrl(), structureMap);
                        context.cacheResource(structureMap);
                        logger.debug("Successfully parsed .map file: {}", structureMap.getUrl());
                    }
                    
                } catch (Exception e) {
                    logger.debug("Could not parse .map file {}: {} (this is expected for some files)", 
                               mapFile.getFileName(), e.getMessage());
                }
            }
        }
    }

    public <T extends IBaseResource> org.hl7.fhir.dstu3.model.Resource convert(T sourceResource, String mapUrl) {
        logger.info("Converting with StructureMap: {}", mapUrl);
        
        try {
            // Get the resource type to find appropriate map
            String resourceType = getResourceType(sourceResource);
            String actualMapUrl = findAppropriateMap(resourceType, mapUrl);
            
            StructureMap map = structureMaps.get(actualMapUrl);
            if (map == null) {
                logger.warn("StructureMap not found: {}. Available maps: {}", 
                          actualMapUrl, structureMaps.keySet());
                return performBasicConversion(sourceResource);
            }

            // Convert HAPI resource to HL7 FHIR R4 resource
            IParser r4Parser = r4Context.newJsonParser();
            String resourceJson = r4Parser.encodeResourceToString(sourceResource);
            
            // Parse as HL7 FHIR R4 resource
            org.hl7.fhir.r4.model.Resource r4Resource = 
                (org.hl7.fhir.r4.model.Resource) r4Context.newJsonParser().parseResource(resourceJson);

            // Create target resource as R4 first, then convert to STU3
            org.hl7.fhir.r4.model.Resource r4TargetResource = createR4TargetResource(resourceType);

            // Perform transformation using StructureMapUtilities
            // The transform method expects Base types
            org.hl7.fhir.r4.model.Base sourceBase = (org.hl7.fhir.r4.model.Base) r4Resource;
            org.hl7.fhir.r4.model.Base targetBase = (org.hl7.fhir.r4.model.Base) r4TargetResource;
            smu.transform(null, sourceBase, map, targetBase);

            // Convert the R4 result to STU3
            IParser r4Parser2 = r4Context.newJsonParser();
            String resultJson = r4Parser2.encodeResourceToString(r4TargetResource);
            
            IParser dstu3Parser = dstu3Context.newJsonParser();
            org.hl7.fhir.dstu3.model.Resource finalResult = 
                (org.hl7.fhir.dstu3.model.Resource) dstu3Parser.parseResource(resultJson);

            logger.info("Successfully converted using StructureMap: {}", actualMapUrl);
            return finalResult;

        } catch (Exception e) {
            logger.error("StructureMap conversion failed: {}", e.getMessage());
            logger.info("Falling back to basic conversion");
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
                return new org.hl7.fhir.r4.model.ImplementationGuide();
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
                return new org.hl7.fhir.dstu3.model.ImplementationGuide();
            default:
                logger.warn("Unknown resource type: {}. Using generic resource.", resourceType);
                return new org.hl7.fhir.dstu3.model.Basic(); // Fallback
        }
    }

    private org.hl7.fhir.dstu3.model.Resource performBasicConversion(IBaseResource sourceResource) {
        logger.info("Performing basic conversion (fallback)");
        
        try {
            // Fall back to basic conversion approach
            IParser r4Parser = r4Context.newJsonParser();
            String resourceJson = r4Parser.encodeResourceToString(sourceResource);
            
            IParser dstu3Parser = dstu3Context.newJsonParser();
            IBaseResource dstu3Resource = dstu3Parser.parseResource(resourceJson);
            
            return (org.hl7.fhir.dstu3.model.Resource) dstu3Resource;
            
        } catch (Exception e) {
            logger.error("Basic conversion also failed", e);
            throw new RuntimeException("All conversion methods failed", e);
        }
    }

    public FhirContext getR4Context() {
        return r4Context;
    }

    public FhirContext getDstu3Context() {
        return dstu3Context;
    }

    public void printLoadedMaps() {
        logger.info("Loaded StructureMaps ({}):", structureMaps.size());
        for (String url : structureMaps.keySet()) {
            logger.info("  - {}", url);
        }
    }
}
