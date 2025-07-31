import fhir.converter.StructureMapFhirConverter;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;
import org.hl7.fhir.instance.model.api.IBaseResource;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class FhirBatchConverter {
    public static void main(String[] args) throws Exception {
        System.out.println("=== FHIR R4 to STU3 Batch Converter ===");
        System.out.println("Comprehensive FHIR resource conversion with error analysis");
        System.out.println("=" + "=".repeat(60));
        
        String mapsDir = "../maps/r4";
        String sourceDir = "../source/";
        String outputDir = "../output/";
        
        // Create output directory if it doesn't exist
        File outputDirectory = new File(outputDir);
        if (!outputDirectory.exists()) {
            outputDirectory.mkdirs();
            System.out.println("✓ Created output directory: " + outputDir);
        }
        
        // Initialize converter
        System.out.println("🔧 Initializing StructureMap converter...");
        StructureMapFhirConverter converter = new StructureMapFhirConverter(mapsDir);
        
        // Get FHIR contexts for parsing
        FhirContext r4Context = converter.getR4Context();
        FhirContext dstu3Context = converter.getDstu3Context();
        IParser r4Parser = r4Context.newJsonParser();
        IParser dstu3Parser = dstu3Context.newJsonParser();
        
        // Get all JSON files from source directory
        File sourceDirFile = new File(sourceDir);
        File[] jsonFiles = sourceDirFile.listFiles((dir, name) -> 
            name.toLowerCase().endsWith(".json"));
        
        if (jsonFiles == null || jsonFiles.length == 0) {
            System.err.println("❌ No JSON files found in " + sourceDir);
            return;
        }
        
        // Sort files by name for consistent processing
        Arrays.sort(jsonFiles, Comparator.comparing(File::getName));
        
        int totalFiles = jsonFiles.length;
        int successCount = 0;
        int errorCount = 0;
        
        // Track conversion statistics
        Map<String, Integer> resourceTypeStats = new HashMap<>();
        Map<String, List<String>> errorsByResourceType = new HashMap<>();
        Map<String, Integer> errorPatternCounts = new HashMap<>();
        List<String> successfulFiles = new ArrayList<>();
        List<String> failedFiles = new ArrayList<>();
        
        System.out.println("📁 Processing " + totalFiles + " JSON files...");
        System.out.println("=" + "=".repeat(80));
        
        for (File file : jsonFiles) {
            String fileName = file.getName();
            String resourceType = "Unknown";
            
            try {
                // Read and parse the file to get resource type
                String inputJson = new String(Files.readAllBytes(file.toPath()));
                IBaseResource r4Resource = r4Parser.parseResource(inputJson);
                resourceType = r4Resource.fhirType();
                
                // Track resource type statistics
                resourceTypeStats.merge(resourceType, 1, Integer::sum);
                
                // Determine the appropriate map URL
                String mapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
                
                System.out.print(String.format("%-50s [%s] ", fileName, resourceType));
                
                // Attempt conversion
                org.hl7.fhir.dstu3.model.Resource dstu3Resource = converter.convert(r4Resource, mapUrl);
                
                if (dstu3Resource != null) {
                    // Convert to JSON and save
                    String outputJson = dstu3Parser.encodeResourceToString(dstu3Resource);
                    String outputFileName = fileName.replace(".json", "-STU3.json");
                    String outputPath = outputDir + outputFileName;
                    
                    Files.write(Paths.get(outputPath), outputJson.getBytes());
                    
                    System.out.println("✓ SUCCESS → " + outputFileName);
                    successCount++;
                    successfulFiles.add(fileName + " → " + outputFileName);
                    
                } else {
                    // Failed but no exception thrown
                    System.out.println("✗ FAILED (conversion returned null)");
                    errorCount++;
                    failedFiles.add(fileName + " (conversion returned null)");
                    errorsByResourceType.computeIfAbsent(resourceType, k -> new ArrayList<>())
                        .add(fileName + ": Conversion returned null");
                    errorPatternCounts.merge("Conversion returned null", 1, Integer::sum);
                }
                
            } catch (Exception e) {
                // Exception during conversion
                String errorMessage = e.getMessage();
                if (errorMessage == null) {
                    errorMessage = e.getClass().getSimpleName();
                }
                
                System.out.println("✗ ERROR: " + errorMessage);
                errorCount++;
                failedFiles.add(fileName + " (" + errorMessage + ")");
                
                errorsByResourceType.computeIfAbsent(resourceType, k -> new ArrayList<>())
                    .add(fileName + ": " + errorMessage);
                
                // Extract error patterns for analysis
                String errorPattern = extractErrorPattern(errorMessage);
                errorPatternCounts.merge(errorPattern, 1, Integer::sum);
            }
        }
        
        // Print comprehensive analysis
        System.out.println("\n" + "=".repeat(80));
        System.out.println("=== CONVERSION SUMMARY ===");
        System.out.println("=" + "=".repeat(80));
        
        System.out.println("\n📊 OVERALL STATISTICS:");
        System.out.println("  📂 Source directory: " + sourceDir);
        System.out.println("  📤 Output directory: " + outputDir);
        System.out.println("  📋 Total files processed: " + totalFiles);
        System.out.println("  ✅ Successful conversions: " + successCount);
        System.out.println("  ❌ Failed conversions: " + errorCount);
        System.out.println("  📈 Success rate: " + String.format("%.1f%%", (successCount * 100.0 / totalFiles)));
        
        System.out.println("\n📈 RESOURCE TYPE STATISTICS:");
        resourceTypeStats.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .forEach(entry -> {
                int total = entry.getValue();
                int errors = errorsByResourceType.getOrDefault(entry.getKey(), Collections.emptyList()).size();
                int successes = total - errors;
                double successRate = (successes * 100.0 / total);
                System.out.println(String.format("  %-20s: %2d files (%2d ✓, %2d ✗) %.1f%%", 
                    entry.getKey(), total, successes, errors, successRate));
            });
        
        if (successCount > 0) {
            System.out.println("\n✅ SUCCESSFUL CONVERSIONS (" + successCount + "):");
            successfulFiles.forEach(file -> System.out.println("  ✓ " + file));
        }
        
        if (errorCount > 0) {
            System.out.println("\n❌ FAILED CONVERSIONS (" + errorCount + "):");
            failedFiles.forEach(file -> System.out.println("  ✗ " + file));
            
            System.out.println("\n🔍 ERROR PATTERNS (by frequency):");
            errorPatternCounts.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .forEach(entry -> 
                    System.out.println("  " + entry.getValue() + "x: " + entry.getKey()));
            
            System.out.println("\n📋 DETAILED ERRORS BY RESOURCE TYPE:");
            errorsByResourceType.entrySet().stream()
                .sorted(Map.Entry.comparingByKey())
                .forEach(entry -> {
                    System.out.println("\n  📂 " + entry.getKey() + " (" + entry.getValue().size() + " errors):");
                    for (String error : entry.getValue()) {
                        System.out.println("    • " + error);
                    }
                });
            
            System.out.println("\n🛠️  TROUBLESHOOTING RECOMMENDATIONS:");
            System.out.println("  1. Review StructureMap files in: " + mapsDir);
            System.out.println("  2. Focus on most common error patterns first");
            System.out.println("  3. Check specific .map files for failing resource types:");
            
            Set<String> problemResourceTypes = errorsByResourceType.keySet();
            for (String resourceType : problemResourceTypes) {
                if (!"Unknown".equals(resourceType)) {
                    System.out.println("     • " + resourceType + ".map");
                }
            }
        }
        
        System.out.println("\n🎯 CONVERSION COMPLETED");
        if (errorCount == 0) {
            System.out.println("🎉 All files converted successfully!");
        } else {
            System.out.println("⚠️  " + errorCount + " files failed conversion - check errors above");
        }
        
        System.out.println("\n📁 Output files saved to: " + new File(outputDir).getAbsolutePath());
        System.out.println("=" + "=".repeat(80));
    }
    
    private static String extractErrorPattern(String errorMessage) {
        if (errorMessage == null) return "Unknown error";
        
        // Common error pattern extraction for better categorization
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
        } else if (errorMessage.contains("NullPointerException")) {
            return "Null pointer exception";
        } else if (errorMessage.contains("parsing")) {
            return "Parsing error";
        } else {
            // Return first 50 characters of error for pattern recognition
            return errorMessage.length() > 50 ? 
                errorMessage.substring(0, 50) + "..." : errorMessage;
        }
    }
}
