import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;
import org.hl7.fhir.instance.model.api.IBaseResource;
import fhir.converter.StructureMapFhirConverter;

public class SingleFileTest {
    public static void main(String[] args) {
        String sourceDir = "../source";
        String outputDir = "../output-single-test";
        String mapsDir = "../maps/r4";
        String testFile = "ValueSet-ACP-EuthanasiaStatement.json"; // Test with one ValueSet
        
        // Create output directory if it doesn't exist
        File outputDirFile = new File(outputDir);
        if (!outputDirFile.exists()) {
            outputDirFile.mkdirs();
        }
        
        try {
            // Initialize the StructureMap converter with maps directory
            StructureMapFhirConverter converter = new StructureMapFhirConverter(mapsDir);
            
            // Get FHIR contexts for parsing
            FhirContext r4Context = converter.getR4Context();
            FhirContext dstu3Context = converter.getDstu3Context();
            IParser r4Parser = r4Context.newJsonParser();
            IParser dstu3Parser = dstu3Context.newJsonParser();
            
            // Process single test file
            File file = new File(sourceDir + "/" + testFile);
            
            try {
                String fileName = file.getName();
                String baseName = fileName.substring(0, fileName.lastIndexOf('.'));
                String outputFileName = baseName + "-SingleTest-STU3.json";
                String outputPath = outputDir + "/" + outputFileName;
                
                System.out.print("Converting " + fileName + "... ");
                
                // Read input file
                String inputJson = new String(Files.readAllBytes(file.toPath()));
                
                // Parse R4 resource
                IBaseResource r4Resource = r4Parser.parseResource(inputJson);
                
                // Determine the appropriate map URL based on resource type
                String resourceType = r4Resource.fhirType();
                String mapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
                
                System.out.println("Using map: " + mapUrl);
                
                // Convert using StructureMap
                org.hl7.fhir.dstu3.model.Resource dstu3Resource = converter.convert(r4Resource, mapUrl);
                
                // Convert to JSON
                String outputJson = dstu3Parser.encodeResourceToString(dstu3Resource);
                
                // Write output file
                Files.write(Paths.get(outputPath), outputJson.getBytes());
                
                System.out.println("SUCCESS - written to " + outputPath);
                
            } catch (Exception e) {
                System.out.println("ERROR: " + e.getMessage());
                e.printStackTrace();
            }
            
        } catch (IOException e) {
            System.err.println("Failed to initialize StructureMapFhirConverter: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
