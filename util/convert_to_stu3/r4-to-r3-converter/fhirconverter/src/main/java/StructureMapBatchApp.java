package fhir.converter;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class StructureMapBatchApp {
    public static void main(String[] args) {
        String sourceDir = "../source";
        String outputDir = "../output-structuremap-fixed";
        
        // Create output directory if it doesn't exist
        File outputDirFile = new File(outputDir);
        if (!outputDirFile.exists()) {
            outputDirFile.mkdirs();
        }
        
        // Initialize the StructureMap converter
        StructureMapFhirConverter converter = new StructureMapFhirConverter();
        
        // Process all JSON files in source directory
        File sourceDirFile = new File(sourceDir);
        File[] jsonFiles = sourceDirFile.listFiles((dir, name) -> name.toLowerCase().endsWith(".json"));
        
        if (jsonFiles == null) {
            System.err.println("No JSON files found in " + sourceDir);
            return;
        }
        
        int totalFiles = jsonFiles.length;
        int successCount = 0;
        int errorCount = 0;
        
        System.out.println("Processing " + totalFiles + " files with StructureMap converter...");
        
        for (File file : jsonFiles) {
            try {
                String fileName = file.getName();
                String baseName = fileName.substring(0, fileName.lastIndexOf('.'));
                String outputFileName = baseName + "-StructureMapFixed-STU3.json";
                String outputPath = outputDir + "/" + outputFileName;
                
                System.out.print("Converting " + fileName + "... ");
                
                // Read input file
                String inputJson = new String(Files.readAllBytes(file.toPath()));
                
                // Convert using StructureMap
                String outputJson = converter.convertToStu3(inputJson);
                
                // Write output file
                Files.write(Paths.get(outputPath), outputJson.getBytes());
                
                successCount++;
                System.out.println("SUCCESS");
                
            } catch (Exception e) {
                errorCount++;
                System.out.println("ERROR: " + e.getMessage());
                e.printStackTrace();
            }
        }
        
        System.out.println("\n=== CONVERSION SUMMARY ===");
        System.out.println("Total files: " + totalFiles);
        System.out.println("Successful: " + successCount);
        System.out.println("Errors: " + errorCount);
    }
}
