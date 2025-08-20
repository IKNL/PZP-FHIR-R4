import fhir.converter.StructureMapFhirConverter;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;
import org.hl7.fhir.instance.model.api.IBaseResource;
import java.io.File;
import java.nio.file.Files;
import java.util.*;

public class AllResourcesErrorTest {
    public static void main(String[] args) throws Exception {
        System.out.println("=== All Resources StructureMap Error Analysis ===");
        
        String mapsDir = "../maps/r4";
        String sourceDir = "../source/";
        String outputDir = "../output-error-analysis/";
        
        // Create output directory if it doesn't exist
        File outputDirectory = new File(outputDir);
        if (!outputDirectory.exists()) {
            outputDirectory.mkdirs();
            System.out.println("Created output directory: " + outputDir);
        }
        
        StructureMapFhirConverter converter = new StructureMapFhirConverter(mapsDir);
        
        // Get FHIR contexts for parsing
        FhirContext r4Context = converter.getR4Context();
        IParser r4Parser = r4Context.newJsonParser();
        
        // Get all JSON files from source directory
        File sourceDirFile = new File(sourceDir);
        File[] jsonFiles = sourceDirFile.listFiles((dir, name) -> 
            name.toLowerCase().endsWith(".json"));
        
        if (jsonFiles == null || jsonFiles.length == 0) {
            System.err.println("No JSON files found in " + sourceDir);
            return;
        }
        
        // Sort files by name for consistent processing
        Arrays.sort(jsonFiles, Comparator.comparing(File::getName));
        
        int totalFiles = jsonFiles.length;
        int successCount = 0;
        int errorCount = 0;
        
        // Track errors by resource type and error pattern
        Map<String, List<String>> errorsByResourceType = new HashMap<>();
        Map<String, Integer> errorPatternCounts = new HashMap<>();
        List<String> successfulResourceTypes = new ArrayList<>();
        
        System.out.println("Processing " + totalFiles + " JSON files for StructureMap errors...");
        System.out.println("=" + "=".repeat(80));
        
        for (File file : jsonFiles) {
            String fileName = file.getName();
            String resourceType = "Unknown";
            
            try {
                // Read and parse the file to get resource type
                String inputJson = new String(Files.readAllBytes(file.toPath()));
                IBaseResource r4Resource = r4Parser.parseResource(inputJson);
                resourceType = r4Resource.fhirType();
                
                // Determine the appropriate map URL
                String mapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
                
                System.out.print(String.format("%-50s [%s] ", fileName, resourceType));
                
                // Attempt conversion
                org.hl7.fhir.dstu3.model.Resource dstu3Resource = converter.convert(r4Resource, mapUrl);
                
                if (dstu3Resource != null) {
                    // Success
                    System.out.println("✓ SUCCESS");
                    successCount++;
                    if (!successfulResourceTypes.contains(resourceType)) {
                        successfulResourceTypes.add(resourceType);
                    }
                } else {
                    // Failed but no exception thrown
                    System.out.println("✗ FAILED (returned null)");
                    errorCount++;
                    errorsByResourceType.computeIfAbsent(resourceType, k -> new ArrayList<>())
                        .add(fileName + ": Conversion returned null");
                    errorPatternCounts.merge("Conversion returned null", 1, Integer::sum);
                }
                
            } catch (Exception e) {
                // Exception during conversion
                System.out.println("✗ ERROR: " + e.getMessage());
                errorCount++;
                
                String errorMessage = e.getMessage();
                if (errorMessage == null) {
                    errorMessage = e.getClass().getSimpleName();
                }
                
                errorsByResourceType.computeIfAbsent(resourceType, k -> new ArrayList<>())
                    .add(fileName + ": " + errorMessage);
                
                // Extract error patterns for analysis
                String errorPattern = extractErrorPattern(errorMessage);
                errorPatternCounts.merge(errorPattern, 1, Integer::sum);
            }
        }
        
        // Print comprehensive analysis
        System.out.println("\n" + "=".repeat(80));
        System.out.println("=== COMPREHENSIVE ERROR ANALYSIS ===");
        System.out.println("=" + "=".repeat(80));
        
        System.out.println("\n📊 OVERALL STATISTICS:");
        System.out.println("  Total files processed: " + totalFiles);
        System.out.println("  Successful conversions: " + successCount);
        System.out.println("  Failed conversions: " + errorCount);
        System.out.println("  Success rate: " + String.format("%.1f%%", (successCount * 100.0 / totalFiles)));
        
        System.out.println("\n✅ SUCCESSFUL RESOURCE TYPES:");
        Collections.sort(successfulResourceTypes);
        for (String resourceType : successfulResourceTypes) {
            System.out.println("  ✓ " + resourceType);
        }
        
        System.out.println("\n❌ ERROR PATTERNS (by frequency):");
        errorPatternCounts.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .forEach(entry -> 
                System.out.println("  " + entry.getValue() + "x: " + entry.getKey()));
        
        System.out.println("\n🔍 ERRORS BY RESOURCE TYPE:");
        errorsByResourceType.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .forEach(entry -> {
                System.out.println("\n  📂 " + entry.getKey() + " (" + entry.getValue().size() + " errors):");
                for (String error : entry.getValue()) {
                    System.out.println("    • " + error);
                }
            });
        
        System.out.println("\n🎯 RECOMMENDATIONS:");
        if (errorCount > 0) {
            System.out.println("  1. Focus on fixing StructureMap files for resource types with errors");
            System.out.println("  2. Most common error patterns should be prioritized");
            System.out.println("  3. Check the specific .map files in ../maps/r4/ directory");
            
            // Suggest specific map files to check
            Set<String> problemResourceTypes = errorsByResourceType.keySet();
            System.out.println("\n  📝 Map files to investigate:");
            for (String resourceType : problemResourceTypes) {
                if (!"Unknown".equals(resourceType)) {
                    System.out.println("    • " + resourceType + ".map");
                }
            }
        } else {
            System.out.println("  🎉 All conversions successful! No StructureMap fixes needed.");
        }
        
        System.out.println("\n" + "=".repeat(80));
    }
    
    private static String extractErrorPattern(String errorMessage) {
        if (errorMessage == null) return "Unknown error";
        
        // Common error pattern extraction
        if (errorMessage.contains("No matches found for rule")) {
            if (errorMessage.contains("ContactDetail to ContactDetail")) {
                return "ContactDetail transformation error";
            } else if (errorMessage.contains("ElementDefinition to ElementDefinition")) {
                return "ElementDefinition transformation error";
            } else {
                return "No matches found for rule";
            }
        } else if (errorMessage.contains("StructureMap conversion failed")) {
            return "StructureMap conversion failed";
        } else if (errorMessage.contains("infinite loop")) {
            return "Infinite loop in transformation";
        } else if (errorMessage.contains("Cannot resolve")) {
            return "Cannot resolve reference";
        } else if (errorMessage.contains("transformation")) {
            return "Transformation error";
        } else {
            // Return first 50 characters of error for pattern recognition
            return errorMessage.length() > 50 ? 
                errorMessage.substring(0, 50) + "..." : errorMessage;
        }
    }
}
