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

public class App {

    public static void main(String[] args) throws IOException {
        
        // --- Configuration ---
        final String MAPS_DIRECTORY = "../maps/r4/"; 
        final String SOURCE_DIRECTORY = "../../../R4/fsh-generated/resources/";
        final String OUTPUT_DIRECTORY = "../../../STU3/input/resources/";
        final String MAP_URL = "http://hl7.org/fhir/StructureMap/StructureDefinition4to3";

        System.out.println("=======================================");
        System.out.println("Starting FHIR R4 to STU3 conversion job...");
        
        // Create output directory if it doesn't exist
        Path outputPath = Paths.get(OUTPUT_DIRECTORY);
        if (!Files.exists(outputPath)) {
            Files.createDirectories(outputPath);
            System.out.println("Created output directory: " + OUTPUT_DIRECTORY);
        }
        
        // 1. Initialize the converter. This is a one-time setup.
        FhirConverter converter = new FhirConverter(MAPS_DIRECTORY);

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
        
        int successCount = 0;
        int errorCount = 0;
        
        // 3. Process each source file
        for (Path sourceFile : sourceFiles) {
            String fileName = sourceFile.getFileName().toString();
            String outputFileName = fileName.replace(".json", "-STU3.json");
            String outputFilePath = OUTPUT_DIRECTORY + outputFileName;
            
            try {
                System.out.println("Processing: " + fileName);
                
                // Load the source R4 resource from the file
                IBaseResource sourceResource;
                try (InputStream stream = new FileInputStream(sourceFile.toString())) {
                    IParser parser = converter.getR4Context().newJsonParser();
                    sourceResource = parser.parseResource(stream);
                }

                // Perform the conversion
                Resource targetDstu3 = converter.convert(sourceResource, MAP_URL);

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
                errorCount++;
            }
        }

        System.out.println("=======================================");
        System.out.println("CONVERSION SUMMARY:");
        System.out.println("  Successfully converted: " + successCount + " files");
        System.out.println("  Failed conversions: " + errorCount + " files");
        System.out.println("  Output directory: " + OUTPUT_DIRECTORY);
        
        // Insert STU3 mappings from integration.json
        System.out.println("=======================================");
        System.out.println("Inserting STU3 mappings from integration.json...");
        try {
            final String INTEGRATION_JSON_PATH = "../../stu3_mapping_generator/integration.json";
            Stu3MappingInserter mappingInserter = new Stu3MappingInserter();
            mappingInserter.insertMappingsIntoStu3Profiles(OUTPUT_DIRECTORY, INTEGRATION_JSON_PATH);
            System.out.println("STU3 mappings insertion completed successfully!");
        } catch (Exception e) {
            System.err.println("Failed to insert STU3 mappings: " + e.getMessage());
            e.printStackTrace();
        }
        
        if (errorCount == 0) {
            System.out.println("SUCCESS: All conversions completed!");
        } else {
            System.out.println("COMPLETED: Some conversions failed - check error messages above");
        }
    }
}