package fhir.converter;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.hl7.fhir.dstu3.model.Resource;
import org.hl7.fhir.instance.model.api.IBaseResource;

import ca.uhn.fhir.parser.IParser;

public class StructureMapApp {

    public static void main(String[] args) throws IOException {
        
        // --- Configuration ---
        final String MAPS_DIRECTORY = "../maps/r4/";
        final String SOURCE_DIRECTORY = "../source/";
        final String OUTPUT_DIRECTORY = "../output-structuremap-test/";
        final String MAP_URL = "http://hl7.org/fhir/StructureMap/StructureDefinition4to3";

        System.out.println("=======================================");
        System.out.println("Starting FHIR R4 to STU3 conversion with StructureMaps...");
        
        // Create output directory if it doesn't exist
        Path outputPath = Paths.get(OUTPUT_DIRECTORY);
        if (!Files.exists(outputPath)) {
            Files.createDirectories(outputPath);
            System.out.println("Created output directory: " + OUTPUT_DIRECTORY);
        }
        
        // 1. Initialize the StructureMap-based converter
        StructureMapFhirConverter converter = new StructureMapFhirConverter(MAPS_DIRECTORY);
        
        // Print loaded maps for debugging
        converter.printLoadedMaps();

        // 2. Find all JSON files in the source directory
        System.out.println("Scanning source directory: " + SOURCE_DIRECTORY);
        List<Path> sourceFiles;
        try (Stream<Path> paths = Files.walk(Paths.get(SOURCE_DIRECTORY))) {
            sourceFiles = paths.filter(Files::isRegularFile)
                               .filter(path -> path.toString().endsWith(".json"))
                               .filter(path -> !path.getFileName().toString().contains("-STU3"))
                               .collect(Collectors.toList());
        }
        
        System.out.println("Found " + sourceFiles.size() + " JSON files to convert");
        
        // Test with just the first file
        sourceFiles = sourceFiles.subList(0, Math.min(1, sourceFiles.size()));
        System.out.println("Testing with first " + sourceFiles.size() + " file(s)...");
        
        int successCount = 0;
        int errorCount = 0;
        
        // 3. Process each source file
        for (Path sourceFile : sourceFiles) {
            String fileName = sourceFile.getFileName().toString();
            String outputFileName = fileName.replace(".json", "-StructureMap-STU3.json");
            String outputFilePath = OUTPUT_DIRECTORY + outputFileName;
            
            try {
                System.out.println("Processing: " + fileName);
                
                // Load the source R4 resource from the file
                IBaseResource sourceResource;
                try (InputStream stream = new FileInputStream(sourceFile.toString())) {
                    IParser parser = converter.getR4Context().newJsonParser();
                    sourceResource = parser.parseResource(stream);
                }

                // Determine appropriate map URL based on resource type
                String resourceType = getResourceType(sourceResource);
                String actualMapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
                
                System.out.println("  Resource type: " + resourceType);
                System.out.println("  Using map: " + actualMapUrl);

                // Perform the conversion
                Resource targetDstu3 = converter.convert(sourceResource, actualMapUrl);

                // Save the converted STU3 resource to the output directory
                try (FileOutputStream stream = new FileOutputStream(outputFilePath)) {
                    IParser parser = converter.getDstu3Context().newJsonParser().setPrettyPrint(true);
                    String out = parser.encodeResourceToString(targetDstu3);
                    stream.write(out.getBytes());
                }
                
                System.out.println("  ✓ Converted to: " + outputFileName);
                successCount++;
                
            } catch (Exception e) {
                System.err.println("  ✗ Failed to convert " + fileName + ": " + e.getMessage());
                e.printStackTrace();
                errorCount++;
            }
        }

        System.out.println("=======================================");
        System.out.println("STRUCTUREMAP CONVERSION SUMMARY:");
        System.out.println("  Successfully converted: " + successCount + " files");
        System.out.println("  Failed conversions: " + errorCount + " files");
        System.out.println("  Output directory: " + OUTPUT_DIRECTORY);
        
        if (errorCount == 0) {
            System.out.println("SUCCESS: All conversions completed!");
        } else {
            System.out.println("COMPLETED: Some conversions failed - check error messages above");
        }
    }
    
    private static String getResourceType(IBaseResource resource) {
        // Extract resource type from the resource class name
        String className = resource.getClass().getSimpleName();
        // Remove any HAPI prefixes/suffixes like "R4" etc.
        return className.replaceAll("^.*\\.", "").replaceAll("R4$", "");
    }
}
