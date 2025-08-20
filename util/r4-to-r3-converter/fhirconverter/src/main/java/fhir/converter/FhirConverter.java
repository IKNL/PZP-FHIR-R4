package fhir.converter;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.hl7.fhir.instance.model.api.IBaseResource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;

/**
 * A reusable service for converting FHIR resources from R4 to STU3.
 * This implementation provides basic structure conversion without complex mapping.
 */
public class FhirConverter {

    private static final Logger logger = LoggerFactory.getLogger(FhirConverter.class);

    private final FhirContext r4Context = FhirContext.forR4();
    private final FhirContext dstu3Context = FhirContext.forDstu3();

    /**
     * Initializes the converter.
     *
     * @param mapsDirectory The path to the directory containing the .map files (currently unused).
     * @throws IOException If initialization fails.
     */
    public FhirConverter(String mapsDirectory) throws IOException {
        logger.info("Initializing FhirConverter...");
        
        // Log available map files for informational purposes
        logger.info("Scanning for StructureMaps in '{}'...", mapsDirectory);
        try (Stream<Path> paths = Files.walk(Paths.get(mapsDirectory))) {
            List<Path> mapFiles = paths.filter(Files::isRegularFile)
                                       .filter(path -> path.toString().endsWith(".map"))
                                       .collect(Collectors.toList());
            
            logger.info("Found {} .map files (currently not loaded):", mapFiles.size());
            for (Path path : mapFiles) {
                logger.info("  - {}", path.toString());
            }
        }
        
        logger.info("FhirConverter initialized successfully.");
        logger.warn("Note: This converter provides basic structure conversion. Full StructureMap-based conversion is not implemented.");
    }

    /**
     * Converts an R4 resource to STU3 by parsing it as STU3.
     * This is a basic conversion that works for resources with compatible structures.
     *
     * @param <T> The type of the source R4 resource.
     * @param sourceResource The R4 resource to convert.
     * @param mapUrl The canonical URL of the StructureMap (currently unused).
     * @return The converted STU3 resource.
     */
    public <T extends IBaseResource> org.hl7.fhir.dstu3.model.Resource convert(T sourceResource, String mapUrl) {
        logger.info("Converting R4 resource to STU3 (ignoring mapUrl: {})", mapUrl);
        
        try {
            // Parse the HAPI FHIR resource to JSON string using R4 context
            IParser r4Parser = r4Context.newJsonParser();
            String resourceJson = r4Parser.encodeResourceToString(sourceResource);
            
            logger.debug("R4 Resource JSON: {}", resourceJson);
            
            // Parse the same JSON as a STU3 resource
            // This works for resources that have compatible structures between R4 and STU3
            IParser dstu3Parser = dstu3Context.newJsonParser();
            IBaseResource dstu3Resource = dstu3Parser.parseResource(resourceJson);
            
            logger.info("Successfully converted resource to STU3");
            return (org.hl7.fhir.dstu3.model.Resource) dstu3Resource;
            
        } catch (Exception e) {
            logger.error("Error during R4 to STU3 conversion", e);
            throw new RuntimeException("Conversion failed: " + e.getMessage(), e);
        }
    }

    /**
     * @return The HAPI FHIR Context for R4.
     */
    public FhirContext getR4Context() {
        return r4Context;
    }

    /**
     * @return The HAPI FHIR Context for STU3.
     */
    public FhirContext getDstu3Context() {
        return dstu3Context;
    }
}