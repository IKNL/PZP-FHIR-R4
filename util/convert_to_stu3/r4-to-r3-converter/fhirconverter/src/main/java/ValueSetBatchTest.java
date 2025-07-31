import fhir.converter.StructureMapFhirConverter;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;
import org.hl7.fhir.instance.model.api.IBaseResource;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

public class ValueSetBatchTest {
    public static void main(String[] args) throws Exception {
        System.out.println("=== ValueSet Batch Conversion Test ===");
        
        String mapsDir = "../maps/r4";
        StructureMapFhirConverter converter = new StructureMapFhirConverter(mapsDir);
        
        // Get FHIR contexts for parsing
        FhirContext r4Context = converter.getR4Context();
        FhirContext dstu3Context = converter.getDstu3Context();
        IParser r4Parser = r4Context.newJsonParser();
        IParser dstu3Parser = dstu3Context.newJsonParser();
        
        // List of all ValueSet files to test
        List<String> valueSetFiles = Arrays.asList(
            "ValueSet-ACP-YesNoUnknownVS.json",
            "ValueSet-ACP-PreferredPlaceOfDeath.json", 
            "ValueSet-ACP-MedicalPolicyGoal.json",
            "ValueSet-ACP-MedicalDeviceProductType-ICD.json",
            "ValueSet-ACP-EuthanasiaStatement.json"
        );
        
        String sourceDir = "../source/";
        String outputDir = "../output-valueset-batch/";
        
        // Create output directory if it doesn't exist
        File outputDirectory = new File(outputDir);
        if (!outputDirectory.exists()) {
            outputDirectory.mkdirs();
            System.out.println("Created output directory: " + outputDir);
        }
        
        int successCount = 0;
        int totalCount = valueSetFiles.size();
        
        for (String fileName : valueSetFiles) {
            try {
                System.out.println("\n--- Processing: " + fileName + " ---");
                
                String inputPath = sourceDir + fileName;
                String outputPath = outputDir + fileName.replace(".json", "-BatchTest-STU3.json");
                
                // Check if source file exists
                File sourceFile = new File(inputPath);
                if (!sourceFile.exists()) {
                    System.err.println("ERROR: Source file not found: " + inputPath);
                    continue;
                }
                
                // Read input file
                String inputJson = new String(Files.readAllBytes(sourceFile.toPath()));
                
                // Parse R4 resource
                IBaseResource r4Resource = r4Parser.parseResource(inputJson);
                
                // Determine the appropriate map URL
                String resourceType = r4Resource.fhirType();
                String mapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
                
                System.out.print("Using map: " + mapUrl + " ... ");
                
                // Convert using StructureMap
                org.hl7.fhir.dstu3.model.Resource dstu3Resource = converter.convert(r4Resource, mapUrl);
                
                if (dstu3Resource != null) {
                    // Convert to JSON and save
                    String outputJson = dstu3Parser.encodeResourceToString(dstu3Resource);
                    Files.write(Paths.get(outputPath), outputJson.getBytes());
                    
                    System.out.println("✓ Successfully converted and saved to: " + outputPath);
                    successCount++;
                    
                    // Print some basic info about the converted ValueSet
                    if (dstu3Resource instanceof org.hl7.fhir.dstu3.model.ValueSet) {
                        org.hl7.fhir.dstu3.model.ValueSet convertedValueSet = (org.hl7.fhir.dstu3.model.ValueSet) dstu3Resource;
                        System.out.println("  - ID: " + convertedValueSet.getId());
                        System.out.println("  - URL: " + convertedValueSet.getUrl());
                        System.out.println("  - Name: " + convertedValueSet.getName());
                        System.out.println("  - Status: " + convertedValueSet.getStatus());
                        
                        if (convertedValueSet.hasCompose() && convertedValueSet.getCompose().hasInclude()) {
                            int conceptCount = convertedValueSet.getCompose().getInclude().stream()
                                .mapToInt(include -> include.hasConcept() ? include.getConcept().size() : 0)
                                .sum();
                            System.out.println("  - Concepts: " + conceptCount);
                        }
                    }
                    
                } else {
                    System.err.println("✗ Conversion returned null for: " + fileName);
                }
                
            } catch (Exception e) {
                System.err.println("✗ ERROR converting " + fileName + ": " + e.getMessage());
                e.printStackTrace();
            }
        }
        
        System.out.println("\n=== Batch Conversion Summary ===");
        System.out.println("Total ValueSets processed: " + totalCount);
        System.out.println("Successful conversions: " + successCount);
        System.out.println("Failed conversions: " + (totalCount - successCount));
        System.out.println("Success rate: " + String.format("%.1f%%", (successCount * 100.0 / totalCount)));
        
        if (successCount == totalCount) {
            System.out.println("🎉 All ValueSets converted successfully!");
        } else {
            System.out.println("⚠️  Some ValueSets failed to convert. Check the errors above.");
        }
    }
}
