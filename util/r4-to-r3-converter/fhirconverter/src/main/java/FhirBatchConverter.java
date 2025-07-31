import fhir.converter.StructureMapFhirConverter;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.parser.IParser;
import org.hl7.fhir.instance.model.api.IBaseResource;
import main.java.IgXmlUpdater;
import java.io.File;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class FhirBatchConverter {
    
    // Pattern to detect StructureMapFhirConverter ERROR messages
    private static final Pattern ERROR_PATTERN = Pattern.compile(
        "\\[FhirBatchConverter\\.main\\(\\)\\] ERROR fhir\\.converter\\.StructureMapFhirConverter - (.+)"
    );
    
    // Pattern to detect other common error indicators
    private static final Pattern STRUCTURE_MAP_ERROR_PATTERN = Pattern.compile(
        "(StructureMap conversion failed|No matches found for rule|Falling back to basic conversion)"
    );
    
    /**
     * Captures console output during conversion and analyzes it for error patterns
     */
    private static class ConversionResult {
        public final org.hl7.fhir.dstu3.model.Resource resource;
        public final String capturedOutput;
        public final List<String> detectedErrors;
        public final boolean hasStructureMapErrors;
        
        public ConversionResult(org.hl7.fhir.dstu3.model.Resource resource, String capturedOutput) {
            this.resource = resource;
            this.capturedOutput = capturedOutput;
            this.detectedErrors = new ArrayList<>();
            
            // Analyze captured output for error patterns
            if (capturedOutput != null && !capturedOutput.trim().isEmpty()) {
                analyzeOutput(capturedOutput);
            }
            
            this.hasStructureMapErrors = !detectedErrors.isEmpty();
        }
        
        private void analyzeOutput(String output) {
            String[] lines = output.split("\\n");
            
            for (String line : lines) {
                // Check for specific StructureMapFhirConverter ERROR messages
                Matcher errorMatcher = ERROR_PATTERN.matcher(line);
                if (errorMatcher.find()) {
                    detectedErrors.add("StructureMapFhirConverter ERROR: " + errorMatcher.group(1));
                    continue;
                }
                
                // Check for other StructureMap error patterns
                Matcher structureMapMatcher = STRUCTURE_MAP_ERROR_PATTERN.matcher(line);
                if (structureMapMatcher.find()) {
                    detectedErrors.add("StructureMap issue: " + structureMapMatcher.group(1));
                    continue;
                }
                
                // Check for any line containing "ERROR" related to FHIR conversion
                if (line.contains("ERROR") && 
                    (line.contains("fhir") || line.contains("StructureMap") || line.contains("conversion"))) {
                    detectedErrors.add("General error: " + line.trim());
                }
            }
        }
    }
    
    /**
     * Performs conversion with output capture and error detection
     */
    private static ConversionResult performConversionWithCapture(
            StructureMapFhirConverter converter, 
            IBaseResource r4Resource, 
            String mapUrl) {
        
        // Capture both stdout and stderr during conversion
        ByteArrayOutputStream capturedOutput = new ByteArrayOutputStream();
        PrintStream captureStream = new PrintStream(capturedOutput);
        PrintStream originalOut = System.out;
        PrintStream originalErr = System.err;
        
        org.hl7.fhir.dstu3.model.Resource result = null;
        
        try {
            // Redirect output streams
            System.setOut(captureStream);
            System.setErr(captureStream);
            
            // Perform the conversion
            result = converter.convert(r4Resource, mapUrl);
            
        } finally {
            // Always restore original streams
            System.setOut(originalOut);
            System.setErr(originalErr);
        }
        
        // Get captured output
        String captured = capturedOutput.toString();
        
        return new ConversionResult(result, captured);
    }
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== FHIR R4 to STU3 Batch Converter ===");
        System.out.println("Comprehensive FHIR resource conversion with error analysis");
        System.out.println("=" + "=".repeat(60));
        
        String mapsDir = "../maps/r4";
        String sourceDir = "../../../R4/fsh-generated/resources/";
        String outputDir = "../../../STU3/input/resources/";
        
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
        List<String> structureMapIssues = new ArrayList<>(); // Track StructureMap-specific issues
        
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
                
                // Attempt conversion with output capture
                ConversionResult conversionResult = performConversionWithCapture(converter, r4Resource, mapUrl);
                
                if (conversionResult.resource != null) {
                    // Convert to JSON and save
                    String outputJson = dstu3Parser.encodeResourceToString(conversionResult.resource);
                    String outputFileName = fileName.replace(".json", "-STU3.json");
                    String outputPath = outputDir + outputFileName;
                    
                    Files.write(Paths.get(outputPath), outputJson.getBytes());
                    
                    // Check for StructureMap issues even on successful conversion
                    if (conversionResult.hasStructureMapErrors) {
                        System.out.println("⚠️  SUCCESS (with issues) → " + outputFileName);
                        for (String error : conversionResult.detectedErrors) {
                            System.out.println("    🚨 " + error);
                            structureMapIssues.add(fileName + ": " + error);
                        }
                    } else {
                        System.out.println("✓ SUCCESS → " + outputFileName);
                    }
                    
                    successCount++;
                    successfulFiles.add(fileName + " → " + outputFileName);
                    
                } else {
                    // Failed conversion
                    String failureReason = "conversion returned null";
                    
                    // Check if we captured any error details
                    if (conversionResult.hasStructureMapErrors) {
                        failureReason = String.join("; ", conversionResult.detectedErrors);
                        for (String error : conversionResult.detectedErrors) {
                            structureMapIssues.add(fileName + ": " + error);
                        }
                    }
                    
                    System.out.println("✗ FAILED (" + failureReason + ")");
                    errorCount++;
                    failedFiles.add(fileName + " (" + failureReason + ")");
                    errorsByResourceType.computeIfAbsent(resourceType, k -> new ArrayList<>())
                        .add(fileName + ": " + failureReason);
                    errorPatternCounts.merge(failureReason, 1, Integer::sum);
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
        
        if (!structureMapIssues.isEmpty()) {
            System.out.println("\n🚨 STRUCTUREMAP ISSUES DETECTED (" + structureMapIssues.size() + "):");
            System.out.println("These files converted successfully but had StructureMap execution problems:");
            structureMapIssues.forEach(issue -> System.out.println("  ⚠️  " + issue));
            
            System.out.println("\n🔍 COMMON STRUCTUREMAP PATTERNS:");
            Map<String, Integer> structureMapPatterns = new HashMap<>();
            for (String issue : structureMapIssues) {
                String pattern = extractStructureMapPattern(issue);
                structureMapPatterns.merge(pattern, 1, Integer::sum);
            }
            structureMapPatterns.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .forEach(entry -> 
                    System.out.println("  " + entry.getValue() + "x: " + entry.getKey()));
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
        if (errorCount == 0 && structureMapIssues.isEmpty()) {
            System.out.println("🎉 All files converted successfully with no issues!");
        } else if (errorCount == 0) {
            System.out.println("✅ All files converted successfully, but " + structureMapIssues.size() + " had StructureMap issues");
            System.out.println("💡 Consider reviewing StructureMap files to resolve conversion warnings");
        } else {
            System.out.println("⚠️  " + errorCount + " files failed conversion - check errors above");
            if (!structureMapIssues.isEmpty()) {
                System.out.println("⚠️  " + structureMapIssues.size() + " additional files had StructureMap issues");
            }
        }
        
        System.out.println("\n📁 Output files saved to: " + new File(outputDir).getAbsolutePath());
        
        // Update STU3 ImplementationGuide XML with converted resources
        if (successCount > 0) {
            System.out.println();
            IgXmlUpdater.updateIgXml();
        }
        
        System.out.println("=" + "=".repeat(80));
    }
    
    private static String extractStructureMapPattern(String issue) {
        if (issue.contains("StructureMapFhirConverter ERROR")) {
            return "StructureMapFhirConverter ERROR";
        } else if (issue.contains("StructureMap conversion failed")) {
            return "StructureMap conversion failed";
        } else if (issue.contains("No matches found for rule")) {
            return "No matches found for rule";
        } else if (issue.contains("Falling back to basic conversion")) {
            return "Falling back to basic conversion";
        } else if (issue.contains("StructureMap issue")) {
            return "StructureMap execution issue";
        } else if (issue.contains("General error")) {
            return "General conversion error";
        } else {
            return "Other StructureMap issue";
        }
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
