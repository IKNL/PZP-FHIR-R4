import fhir.converter.StructureMapFhirConverter;
import fhir.converter.CrossVersionPostProcessor;
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
        public final String conversionMethod;
        public final boolean wasExcluded;
        
        public ConversionResult(org.hl7.fhir.dstu3.model.Resource resource, String capturedOutput) {
            this.resource = resource;
            this.capturedOutput = capturedOutput;
            this.detectedErrors = new ArrayList<>();
            
            // Analyze captured output for error patterns and conversion method
            if (capturedOutput != null && !capturedOutput.trim().isEmpty()) {
                analyzeOutput(capturedOutput);
            }
            
            this.hasStructureMapErrors = !detectedErrors.isEmpty();
            this.conversionMethod = determineConversionMethod(capturedOutput);
            this.wasExcluded = resource == null && capturedOutput != null && capturedOutput.contains("EXCLUDED:");
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
        
        private String determineConversionMethod(String output) {
            if (output == null || output.trim().isEmpty()) {
                return "UNKNOWN";
            }
            
            if (output.contains("EXCLUDED:")) {
                return "EXCLUDED";
            }
            
            if (output.contains("STRUCTUREMAP SUCCESS:") || output.contains("STRUCTUREMAP CONVERSION:")) {
                return "STRUCTUREMAP";
            }
            
            if (output.contains("BASIC SUCCESS:") || output.contains("BASIC CONVERSION:")) {
                return "BASIC";
            }
            
            if (output.contains("STRUCTUREMAP FAILED:") || output.contains("BASIC FAILED:")) {
                return "FAILED";
            }
            
            return "UNKNOWN";
        }
    }
    
    /**
     * Performs conversion with output capture and error detection
     */
    private static ConversionResult performConversionWithCapture(
            StructureMapFhirConverter converter, 
            IBaseResource r4Resource, 
            String mapUrl,
            String fileName) {
        
        // Capture both stdout and stderr during conversion
        ByteArrayOutputStream capturedOutput = new ByteArrayOutputStream();
        PrintStream captureStream = new PrintStream(capturedOutput);
        PrintStream originalOut = System.out;
        PrintStream originalErr = System.err;
        
        org.hl7.fhir.dstu3.model.Resource result = null;
        Exception conversionException = null;
        
        try {
            // Redirect output streams
            System.setOut(captureStream);
            System.setErr(captureStream);
            
            // Add debug output to captured stream
            captureStream.println("=== CONVERSION START ===");
            captureStream.println("File: " + fileName);
            captureStream.println("Resource Type: " + r4Resource.fhirType());
            captureStream.println("Map URL: " + mapUrl);
            captureStream.println("=========================");
            
            // Enable verbose logging by redirecting logger output
            // This is a hack to capture SLF4J logger output
            java.util.logging.Logger rootLogger = java.util.logging.Logger.getLogger("");
            java.util.logging.Handler[] handlers = rootLogger.getHandlers();
            java.util.logging.StreamHandler streamHandler = new java.util.logging.StreamHandler(captureStream, new java.util.logging.SimpleFormatter());
            streamHandler.setLevel(java.util.logging.Level.ALL);
            rootLogger.addHandler(streamHandler);
            rootLogger.setLevel(java.util.logging.Level.ALL);
            
            try {
                // Perform the conversion
                result = converter.convert(r4Resource, mapUrl);
                
                // Check if result is null - this indicates conversion failure
                if (result == null) {
                    captureStream.println("CONVERSION ERROR: converter.convert() returned null");
                    captureStream.println("This indicates all conversion methods failed");
                }
                
            } catch (Exception e) {
                // Capture any exception thrown during conversion
                conversionException = e;
                captureStream.println("CONVERSION EXCEPTION: " + e.getClass().getSimpleName());
                captureStream.println("EXCEPTION MESSAGE: " + e.getMessage());
                captureStream.println("STACK TRACE:");
                e.printStackTrace(captureStream);
            }
            
            // Remove the custom handler
            rootLogger.removeHandler(streamHandler);
            
            // Add debug output after conversion
            captureStream.println("=== CONVERSION END ===");
            captureStream.println("Result: " + (result != null ? "SUCCESS" : "NULL"));
            if (result != null) {
                captureStream.println("Result Type: " + result.getClass().getSimpleName());
                captureStream.println("Result Resource Type: " + result.fhirType());
            }
            if (conversionException != null) {
                captureStream.println("Exception during conversion: " + conversionException.getMessage());
            }
            captureStream.println("=====================");
            
        } finally {
            // Always restore original streams
            System.setOut(originalOut);
            System.setErr(originalErr);
        }
        
        // Get captured output
        String captured = capturedOutput.toString();
        
        // Save captured output to file for debugging
        saveDebugLog(fileName, mapUrl, captured, r4Resource, result);
        
        // If there was an exception and no result, re-throw the exception
        if (result == null && conversionException != null) {
            throw new RuntimeException("Conversion failed with exception: " + conversionException.getMessage(), conversionException);
        }
        
        return new ConversionResult(result, captured);
    }
    
    /**
     * Saves the complete StructureMap logging output to a debug file
     */
    private static void saveDebugLog(String fileName, String mapUrl, String capturedOutput, 
                                   IBaseResource sourceResource, org.hl7.fhir.dstu3.model.Resource resultResource) {
        try {
            // Create debug logs directory
            File debugDir = new File("debug-logs");
            if (!debugDir.exists()) {
                debugDir.mkdirs();
            }
            
            // Create debug file name based on source file and resource type
            String resourceType = extractResourceTypeFromMapUrl(mapUrl);
            String debugFileName = fileName.replace(".json", "") + "-" + resourceType + "-debug.txt";
            File debugFile = new File(debugDir, debugFileName);
            
            // Prepare debug content
            StringBuilder debugContent = new StringBuilder();
            debugContent.append("=".repeat(80)).append("\n");
            debugContent.append("STRUCTUREMAP DEBUG LOG\n");
            debugContent.append("=".repeat(80)).append("\n");
            debugContent.append("Source File: ").append(fileName).append("\n");
            debugContent.append("Map URL: ").append(mapUrl).append("\n");
            debugContent.append("Resource Type: ").append(resourceType).append("\n");
            debugContent.append("Timestamp: ").append(new java.util.Date()).append("\n");
            
            // Add source resource info
            if (sourceResource != null) {
                debugContent.append("Source Resource Type: ").append(sourceResource.fhirType()).append("\n");
                debugContent.append("Source Resource Class: ").append(sourceResource.getClass().getSimpleName()).append("\n");
            }
            
            // Add result resource info
            if (resultResource != null) {
                debugContent.append("Result Resource Type: ").append(resultResource.fhirType()).append("\n");
                debugContent.append("Result Resource Class: ").append(resultResource.getClass().getSimpleName()).append("\n");
                debugContent.append("Conversion Status: SUCCESS\n");
            } else {
                debugContent.append("Conversion Status: FAILED (null result)\n");
            }
            
            debugContent.append("=".repeat(80)).append("\n\n");
            
            if (capturedOutput != null && !capturedOutput.trim().isEmpty()) {
                debugContent.append("CAPTURED OUTPUT:\n");
                debugContent.append("-".repeat(40)).append("\n");
                debugContent.append(capturedOutput);
                debugContent.append("\n").append("-".repeat(40)).append("\n");
            } else {
                debugContent.append("NO OUTPUT CAPTURED\n");
                debugContent.append("-".repeat(40)).append("\n");
                debugContent.append("This could indicate:\n");
                debugContent.append("1. StructureMap execution is silent\n");
                debugContent.append("2. Conversion is using basic fallback\n");
                debugContent.append("3. Logging level is not verbose enough\n");
                debugContent.append("4. Output is going to a different stream\n");
                debugContent.append("-".repeat(40)).append("\n");
            }
            
            // Add analysis of what might be happening
            if (resultResource != null && (capturedOutput == null || capturedOutput.trim().isEmpty())) {
                debugContent.append("\n📊 ANALYSIS:\n");
                debugContent.append("Conversion succeeded but no StructureMap output was captured.\n");
                debugContent.append("This suggests the conversion may be using basic fallback instead of StructureMap.\n");
                debugContent.append("Check if the StructureMap file exists and is being loaded correctly.\n");
                
                if ("StructureDefinition".equals(resourceType)) {
                    debugContent.append("\n🔍 STRUCTUREDEFINITION SPECIFIC:\n");
                    debugContent.append("For StructureDefinition transformations, check:\n");
                    debugContent.append("- Is StructureDefinition.map loaded?\n");
                    debugContent.append("- Are the baseDefinition mappings being applied?\n");
                    debugContent.append("- Is fhirVersion being set to '3.0.2'?\n");
                }
            }
            
            debugContent.append("\nEND OF DEBUG LOG\n");
            debugContent.append("=".repeat(80)).append("\n");
            
            // Write to file
            Files.write(debugFile.toPath(), debugContent.toString().getBytes());
            
        } catch (Exception e) {
            // Don't let debug logging failure break the main process
            System.err.println("Warning: Failed to save debug log for " + fileName + ": " + e.getMessage());
        }
    }
    
    /**
     * Extracts resource type from map URL
     */
    private static String extractResourceTypeFromMapUrl(String mapUrl) {
        if (mapUrl != null && mapUrl.contains("/")) {
            String[] parts = mapUrl.split("/");
            String lastPart = parts[parts.length - 1];
            if (lastPart.contains("4to3")) {
                return lastPart.replace("4to3", "");
            }
            return lastPart;
        }
        return "Unknown";
    }
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== FHIR R4 to STU3 Batch Converter ===");
        System.out.println("Comprehensive FHIR resource conversion with error analysis");
        System.out.println("=" + "=".repeat(60));
        
        String mapsDir = "../maps/r4";
        String sourceDir = "../../../R4/fsh-generated/resources/";
        String outputDir = "../../../STU3/input/resources/";
        
        // Files to exclude from conversion (too difficult to transform)
        Set<String> excludedFiles = Set.of(
            "StructureDefinition-ACP-TreatmentDirective.json",
            "StructureDefinition-ACP-AdvanceDirective.json", 
            "ImplementationGuide-iknl.fhir.r4.pzp.json"
        );
        
        System.out.println("🚫 Files excluded from conversion:");
        excludedFiles.forEach(file -> System.out.println("  • " + file + " (will be handled manually)"));
        System.out.println("");
        
        // Create output directory if it doesn't exist
        File outputDirectory = new File(outputDir);
        if (!outputDirectory.exists()) {
            outputDirectory.mkdirs();
            System.out.println("✓ Created output directory: " + outputDir);
        }
        
        // Initialize converter
        System.out.println("🔧 Initializing StructureMap converter...");
        StructureMapFhirConverter converter = new StructureMapFhirConverter(mapsDir);
        
        // Debug: Check what StructureMaps are loaded
        System.out.println("🔍 Checking loaded StructureMaps...");
        try {
            // Use reflection to access the structureMaps field
            java.lang.reflect.Field structureMapsField = converter.getClass().getDeclaredField("structureMaps");
            structureMapsField.setAccessible(true);
            @SuppressWarnings("unchecked")
            java.util.Map<String, Object> loadedMaps = (java.util.Map<String, Object>) structureMapsField.get(converter);
            
            System.out.println("📋 Loaded " + loadedMaps.size() + " StructureMaps:");
            for (String mapUrl : loadedMaps.keySet()) {
                System.out.println("  • " + mapUrl);
            }
            
            // Check specifically for StructureDefinition map
            String structureDefMapUrl = "http://hl7.org/fhir/StructureMap/StructureDefinition4to3";
            if (loadedMaps.containsKey(structureDefMapUrl)) {
                System.out.println("✅ StructureDefinition4to3 map is loaded");
            } else {
                System.out.println("❌ StructureDefinition4to3 map is NOT loaded");
                System.out.println("🔍 This explains why StructureDefinition conversions use basic fallback");
            }
            
        } catch (Exception e) {
            System.out.println("⚠️  Could not inspect loaded StructureMaps: " + e.getMessage());
        }
        
        // Get FHIR contexts for parsing
        FhirContext r4Context = converter.getR4Context();
        FhirContext dstu3Context = converter.getDstu3Context();
        IParser r4Parser = r4Context.newJsonParser().setPrettyPrint(true);
        IParser dstu3Parser = dstu3Context.newJsonParser().setPrettyPrint(true);
        
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
        int structureMapCount = 0;  // Track StructureMap conversions
        int basicCount = 0;         // Track Basic conversions
        int excludedCount = 0;      // Track excluded files
        
        // Track conversion statistics
        Map<String, Integer> resourceTypeStats = new HashMap<>();
        Map<String, List<String>> errorsByResourceType = new HashMap<>();
        Map<String, Integer> errorPatternCounts = new HashMap<>();
        List<String> successfulFiles = new ArrayList<>();
        List<String> failedFiles = new ArrayList<>();
        List<String> structureMapIssues = new ArrayList<>(); // Track StructureMap-specific issues
        
        System.out.println("📁 Processing " + totalFiles + " JSON files...");
        System.out.println("🔍 Debug logs will be saved to: debug-logs/ directory");
        System.out.println("=" + "=".repeat(80));
        
        for (File file : jsonFiles) {
            String fileName = file.getName();
            String resourceType = "Unknown";
            
            // Check if this file should be excluded from conversion
            if (excludedFiles.contains(fileName)) {
                System.out.println("⏭️  Skipping excluded file: " + fileName);
                excludedCount++;
                continue;
            }
            
            try {
                // Read and parse the file to get resource type
                String inputJson = new String(Files.readAllBytes(file.toPath()));
                IBaseResource r4Resource = r4Parser.parseResource(inputJson);
                resourceType = r4Resource.fhirType();
                
                // Track resource type statistics
                resourceTypeStats.merge(resourceType, 1, Integer::sum);
                
                // Determine the appropriate map URL
                String mapUrl = "http://hl7.org/fhir/StructureMap/" + resourceType + "4to3";
                
                // Attempt conversion with output capture
                ConversionResult conversionResult = performConversionWithCapture(converter, r4Resource, mapUrl, fileName);
                
                if (conversionResult.wasExcluded) {
                    excludedCount++;
                    // Don't count as success or failure, just skip
                    continue;
                }
                
                if (conversionResult.resource != null) {
                    // Convert to JSON and save
                    String outputJson = dstu3Parser.encodeResourceToString(conversionResult.resource);
                    
                    // Apply post-processing for StructureDefinition resources
                    if ("StructureDefinition".equals(resourceType)) {
                        try {
                            CrossVersionPostProcessor postProcessor = new CrossVersionPostProcessor();
                            outputJson = postProcessor.processSTU3Resource(outputJson, resourceType);
                            System.out.println("✅ Applied post-processing to " + fileName);
                        } catch (Exception e) {
                            System.out.println("⚠️  Post-processing failed for " + fileName + ": " + e.getMessage());
                            // Continue with original output if post-processing fails
                        }
                    }
                    
                    // Prefix converted files with 'converted-'
                    String baseFileName = fileName.replace(".json", "");
                    String outputFileName = "converted-" + baseFileName + "-STU3.json";
                    String outputPath = outputDir + outputFileName;
                    
                    Files.write(Paths.get(outputPath), outputJson.getBytes());
                    
                    // Track conversion method and any issues
                    if (conversionResult.hasStructureMapErrors) {
                        for (String error : conversionResult.detectedErrors) {
                            structureMapIssues.add(fileName + ": " + error);
                        }
                    }
                    
                    // Track conversion method
                    if ("STRUCTUREMAP".equals(conversionResult.conversionMethod)) {
                        structureMapCount++;
                    } else if ("BASIC".equals(conversionResult.conversionMethod)) {
                        basicCount++;
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
        System.out.println("    🗺️  StructureMap conversions: " + structureMapCount);
        System.out.println("    📋 Basic conversions: " + basicCount);
        System.out.println("  ❌ Failed conversions: " + errorCount);
        if (excludedCount > 0) {
            System.out.println("  ⏭️  Excluded files: " + excludedCount);
            System.out.println("    💡 These files should be manually converted and placed with 'manual-' prefix");
        }
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
            System.out.println("  🗺️  StructureMap conversions: " + structureMapCount);
            System.out.println("  📋 Basic conversions: " + basicCount);
        }
        
        if (!structureMapIssues.isEmpty()) {
            System.out.println("\n🚨 STRUCTUREMAP ISSUES DETECTED (" + structureMapIssues.size() + "):");
            System.out.println("These files converted successfully but had StructureMap execution problems:");
            
            // Group issues by filename and extract meaningful error messages
            Map<String, Set<String>> issuesByFile = new HashMap<>();
            
            for (String issue : structureMapIssues) {
                String[] parts = issue.split(": ", 2);
                if (parts.length > 1) {
                    String fileName = parts[0];
                    String errorMessage = parts[1];
                    
                    // Extract only meaningful error messages, filter out stack traces and redundant info
                    String meaningfulError = extractMeaningfulError(errorMessage);
                    if (meaningfulError != null && !meaningfulError.trim().isEmpty()) {
                        issuesByFile.computeIfAbsent(fileName, k -> new LinkedHashSet<>()).add(meaningfulError);
                    }
                }
            }
            
            // Display grouped issues by filename
            for (Map.Entry<String, Set<String>> entry : issuesByFile.entrySet()) {
                String fileName = entry.getKey();
                Set<String> errors = entry.getValue();
                
                for (String error : errors) {
                    System.out.println("  ⚠️  [" + fileName + "] " + error);
                }
            }
            
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
        
        if (excludedCount > 0) {
            System.out.println("\n📋 MANUAL CONVERSION REQUIRED:");
            System.out.println("The following files were excluded from automatic conversion:");
            excludedFiles.forEach(file -> System.out.println("  • " + file));
            System.out.println("\n💡 TODO: Manually convert these files and save them with 'manual-' prefix:");
            excludedFiles.forEach(file -> {
                String baseName = file.replace(".json", "");
                String manualName = "manual-" + baseName + "-STU3.json";
                System.out.println("  • " + file + " → " + manualName);
            });
            System.out.println("\n   Place these manual files in: " + new File(outputDir).getAbsolutePath());
            System.out.println("   The IgXmlUpdater will automatically include them in the ImplementationGuide");
        }
        
        System.out.println("\n📁 Output files saved to: " + new File(outputDir).getAbsolutePath());
        System.out.println("🔍 Debug logs saved to: " + new File("debug-logs").getAbsolutePath());
        System.out.println("💡 Check debug logs to analyze StructureMap execution details");
        
        // Update STU3 ImplementationGuide XML with converted resources
        if (successCount > 0) {
            System.out.println();
            System.out.println("🔄 Updating ImplementationGuide XML...");
            System.out.println("   📋 Will include all resources in STU3/input/resources/:");
            System.out.println("   🔄 Converted files (prefixed with 'converted-')");
            System.out.println("   ✋ Manual files (prefixed with 'manual-')");
            IgXmlUpdater.updateIgXml();
        }
        
        System.out.println("=" + "=".repeat(80));
    }
    
    /**
     * Extracts meaningful error messages from StructureMap issue logs,
     * filtering out stack traces and redundant information
     */
    private static String extractMeaningfulError(String errorMessage) {
        if (errorMessage == null || errorMessage.trim().isEmpty()) {
            return null;
        }
        
        // Skip stack trace indicators and redundant messages
        if (errorMessage.contains("Full stack trace:") ||
            errorMessage.contains("Error type:") ||
            errorMessage.contains("❌ STRUCTUREMAP FAILED:") ||
            errorMessage.trim().equals("Falling back to basic conversion")) {
            return null;
        }
        
        // Extract meaningful error messages
        if (errorMessage.startsWith("StructureMapFhirConverter ERROR: Error message: ")) {
            return "StructureMapFhirConverter ERROR: " + errorMessage.substring("StructureMapFhirConverter ERROR: Error message: ".length());
        }
        
        if (errorMessage.startsWith("StructureMapFhirConverter ERROR: ")) {
            String remainder = errorMessage.substring("StructureMapFhirConverter ERROR: ".length());
            // Skip the intermediate error type and failed messages
            if (remainder.startsWith("❌") || remainder.startsWith("Error type:")) {
                return null;
            }
            return "StructureMapFhirConverter ERROR: " + remainder;
        }
        
        if (errorMessage.startsWith("StructureMap issue: ")) {
            String remainder = errorMessage.substring("StructureMap issue: ".length());
            if (!remainder.trim().equals("Falling back to basic conversion")) {
                return "StructureMap issue: " + remainder;
            }
            return null;
        }
        
        if (errorMessage.startsWith("General error: ")) {
            return errorMessage; // Keep general errors as-is
        }
        
        // For any other meaningful error messages that don't match patterns above
        if (!errorMessage.contains("stack trace") && 
            !errorMessage.contains("Error type:") &&
            !errorMessage.trim().isEmpty()) {
            return errorMessage;
        }
        
        return null;
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
