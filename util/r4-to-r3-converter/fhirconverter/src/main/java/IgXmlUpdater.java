package main.java;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * Updates the IKNL_PZP_IG.xml file with converted resource references
 */
public class IgXmlUpdater {
    
    private static final String STU3_RESOURCES_DIR = "../../../STU3/input/resources/";
    private static final String STU3_IG_XML_PATH = "../../../STU3/input/IKNL_PZP_IG.xml";
    private static final String R4_PAGECONTENT_DIR = "../../../R4/input/pagecontent/";
    private static final String STU3_PAGECONTENT_DIR = "../../../STU3/input/pagecontent/";
    private static final String R4_INCLUDES_DIR = "../../../R4/input/includes/";
    private static final String STU3_INCLUDES_DIR = "../../../STU3/input/includes/";
    
    public static void updateIgXml() {
        try {
            System.out.println("🔄 Updating STU3 ImplementationGuide XML with converted resources...");
            
            // 1. Copy markdown files from R4 to STU3
            copyMarkdownFiles();
            
            // 2. Scan converted resources
            Map<String, ResourceInfo> resources = scanConvertedResources();
            
            if (resources.isEmpty()) {
                System.out.println("⚠️  No converted resources found in " + STU3_RESOURCES_DIR);
                return;
            }
            
            // 3. Update the IG XML file
            updateResourceReferences(resources);
            
            System.out.println("✅ Updated IKNL_PZP_IG.xml with " + resources.size() + " resource references");
            
        } catch (Exception e) {
            System.err.println("❌ Error updating IG XML: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static Map<String, ResourceInfo> scanConvertedResources() throws Exception {
        Map<String, ResourceInfo> resources = new HashMap<>();
        File resourcesDir = new File(STU3_RESOURCES_DIR);
        
        if (!resourcesDir.exists()) {
            System.out.println("⚠️  Resources directory does not exist: " + resourcesDir.getAbsolutePath());
            return resources;
        }
        
        File[] jsonFiles = resourcesDir.listFiles((dir, name) -> name.endsWith(".json"));
        
        if (jsonFiles == null) {
            return resources;
        }
        
        // Set of allowed resource types for IG inclusion
        Set<String> allowedResourceTypes = Set.of("StructureDefinition", "ValueSet", "SearchParameter");
        
        int convertedCount = 0;
        int manualCount = 0;
        
        for (File file : jsonFiles) {
            try {
                String content = Files.readString(file.toPath());
                ResourceInfo info = parseResourceInfo(content, file.getName());
                if (info != null && allowedResourceTypes.contains(info.resourceType)) {
                    resources.put(info.id, info);
                    
                    // Track whether this is a converted or manual file
                    if (file.getName().startsWith("converted-")) {
                        convertedCount++;
                    } else if (file.getName().startsWith("manual-")) {
                        manualCount++;
                    }
                }
            } catch (Exception e) {
                System.out.println("⚠️  Could not parse " + file.getName() + ": " + e.getMessage());
            }
        }
        
        System.out.println("📋 Found " + resources.size() + " resources:");
        System.out.println("   🔄 Converted files: " + convertedCount);
        System.out.println("   ✋ Manual files: " + manualCount);
        System.out.println("   📝 Resource types: StructureDefinition, ValueSet, SearchParameter");
        
        return resources;
    }
    
    private static ResourceInfo parseResourceInfo(String jsonContent, String fileName) {
        try {
            JsonObject json = JsonParser.parseString(jsonContent).getAsJsonObject();
            
            String resourceType = json.has("resourceType") ? json.get("resourceType").getAsString() : null;
            String id = json.has("id") ? json.get("id").getAsString() : null;
            String name = json.has("name") ? json.get("name").getAsString() : null;
            String title = json.has("title") ? json.get("title").getAsString() : null;
            String url = json.has("url") ? json.get("url").getAsString() : null;
            
            if (resourceType != null && id != null) {
                return new ResourceInfo(resourceType, id, name, title, url, fileName);
            }
        } catch (Exception e) {
            // Ignore parsing errors for non-FHIR files
        }
        return null;
    }
    
    private static void updateResourceReferences(Map<String, ResourceInfo> resources) throws Exception {
        System.out.println("📝 Generating new IKNL_PZP_IG.xml file...");
        
        // Generate the complete XML content
        StringBuilder xmlContent = new StringBuilder();
        
        // Add XML header and fixed content
        xmlContent.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        xmlContent.append("<ImplementationGuide xmlns=\"http://hl7.org/fhir\"\n");
        xmlContent.append("  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n");
        xmlContent.append("  xsi:schemaLocation=\"http://hl7.org/fhir ../input-cache/schemas/R3/fhir-single.xsd\">\n");
        xmlContent.append("  <id value=\"iknl.fhir.stu3.pzp\" />\n");
        xmlContent.append("  <url value=\"https://fhir.iknl.nl/fhir/ImplementationGuide/iknl.fhir.stu3.pzp\" />\n");
        xmlContent.append("  <version value=\"0.1.0\" />\n");
        xmlContent.append("  <name value=\"PZP\" />\n");
        xmlContent.append("  <title value=\"IKNL PZP \" />\n");
        xmlContent.append("  <status value=\"draft\" />\n");
        xmlContent.append("  <experimental value=\"false\" />\n");
        xmlContent.append("  <publisher value=\"IKNL\" />\n");
        xmlContent.append("  <contact>\n");
        xmlContent.append("    <telecom>\n");
        xmlContent.append("      <system value=\"url\" />\n");
        xmlContent.append("      <value value=\"https://www.iknl.nl\" />\n");
        xmlContent.append("    </telecom>\n");
        xmlContent.append("  </contact>\n");
        xmlContent.append("  <description value=\"TODO\" />\n");
        xmlContent.append("  <jurisdiction>\n");
        xmlContent.append("    <coding>\n");
        xmlContent.append("      <system value=\"http://unstats.un.org/unsd/methods/m49/m49.htm\" />\n");
        xmlContent.append("      <code value=\"001\" />\n");
        xmlContent.append("    </coding>\n");
        xmlContent.append("  </jurisdiction>\n");
        xmlContent.append("  <packageId value=\"iknl.fhir.stu3.pzp\" />\n");
        xmlContent.append("  <license value=\"CC0-1.0\" />\n");
        xmlContent.append("  <fhirVersion value=\"3.0.2\" />\n");
        xmlContent.append("  <dependsOn>\n");
        xmlContent.append("    <uri value=\"https://simplifier.net/packages/nictiz.fhir.nl.stu3.zib2017/2.2.20\" />\n");
        xmlContent.append("    <packageId value=\"nictiz.fhir.nl.stu3.zib2017\" />\n");
        xmlContent.append("    <version value=\"2.2.20\" />\n");
        xmlContent.append("  </dependsOn>\n");
        xmlContent.append("  <definition>\n");
        
        // Add page blocks
        addPageBlocks(xmlContent);
        
        // Add resource blocks
        addResourceBlocks(xmlContent, resources);
        
        // Add fixed parameters
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"copyrightyear\" />\n");
        xmlContent.append("      <value value=\"2025+\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <!-- releaselabel should be the ballot status for HL7-published IGs. -->\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"releaselabel\" />\n");
        xmlContent.append("      <value value=\"CI Build\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"find-other-resources\" />\n");
        xmlContent.append("      <value value=\"true\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"path-liquid\" />\n");
        xmlContent.append("      <value value=\"templates\\liquid\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"shownav\" />\n");
        xmlContent.append("      <value value=\"true\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"showsource\" />\n");
        xmlContent.append("      <value value=\"true\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"i18n-default-lang\" />\n");
        xmlContent.append("      <value value=\"en\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("    <parameter>\n");
        xmlContent.append("      <code value=\"fcp-approved-specification\" />\n");
        xmlContent.append("      <value value=\"false\" />\n");
        xmlContent.append("    </parameter>\n");
        xmlContent.append("  </definition>\n");
        xmlContent.append("</ImplementationGuide>\n");
        
        // Write the complete XML to file
        File igXmlFile = new File(STU3_IG_XML_PATH);
        Files.writeString(igXmlFile.toPath(), xmlContent.toString());
        
        System.out.println("✅ Generated new IKNL_PZP_IG.xml with " + resources.size() + " resources");
    }
    
    private static void addPageBlocks(StringBuilder xmlContent) throws Exception {
        System.out.println("📄 Adding page blocks...");
        
        // Add the main page structure
        xmlContent.append("    <page>\n");
        xmlContent.append("      <!-- The root will always be toc.html - the template will force it if you don't do it -->\n");
        xmlContent.append("      <nameUrl value=\"toc.html\" />\n");
        xmlContent.append("      <title value=\"Table of Contents\" />\n");
        xmlContent.append("      <generation value=\"html\" />\n");
        xmlContent.append("      <page>\n");
        xmlContent.append("        <nameUrl value=\"index.html\" />\n");
        xmlContent.append("        <title value=\"PZP IG Home page\" />\n");
        xmlContent.append("        <generation value=\"html\" />\n");
        xmlContent.append("      </page>\n");
        
        // Add markdown pages
        File pageContentDir = new File(STU3_PAGECONTENT_DIR);
        if (pageContentDir.exists()) {
            File[] mdFiles = pageContentDir.listFiles((dir, name) -> name.toLowerCase().endsWith(".md"));
            if (mdFiles != null) {
                for (File mdFile : mdFiles) {
                    String fileName = mdFile.getName();
                    String baseName = fileName.substring(0, fileName.lastIndexOf('.'));
                    String htmlName = baseName + ".html";
                    String title = generatePageTitle(baseName);
                    
                    xmlContent.append("      <page>\n");
                    xmlContent.append("        <nameUrl value=\"").append(htmlName).append("\" />\n");
                    xmlContent.append("        <title value=\"").append(title).append("\" />\n");
                    xmlContent.append("        <generation value=\"markdown\" />\n");
                    xmlContent.append("      </page>\n");
                    
                    System.out.println("   📄 Added page: " + htmlName + " (" + title + ")");
                }
            }
        }
        
        xmlContent.append("    </page>\n");
    }
    
    private static void addResourceBlocks(StringBuilder xmlContent, Map<String, ResourceInfo> resources) {
        System.out.println("📋 Adding resource blocks...");
        
        // Sort resources by type and then by ID for consistent output
        List<ResourceInfo> sortedResources = new ArrayList<>(resources.values());
        sortedResources.sort((a, b) -> {
            int typeCompare = a.resourceType.compareTo(b.resourceType);
            if (typeCompare != 0) return typeCompare;
            return a.id.compareTo(b.id);
        });
        
        for (ResourceInfo resource : sortedResources) {
            String description = generateDescription(resource.resourceType, resource.id);
            
            xmlContent.append("    <resource>\n");
            xmlContent.append("      <reference>\n");
            xmlContent.append("        <reference value=\"").append(resource.resourceType).append("/").append(resource.id).append("\" />\n");
            xmlContent.append("      </reference>\n");
            xmlContent.append("      <description value=\"").append(description).append("\" />\n");
            xmlContent.append("    </resource>\n");
        }
        
        System.out.println("   📋 Added " + sortedResources.size() + " resource blocks");
    }
    
    private static String generateDescription(String resourceType, String id) {
        switch (resourceType) {
            case "StructureDefinition":
                return "Profile for " + id.replace("-", " ");
            case "ValueSet":
                return "ValueSet for " + id.replace("-", " ");
            case "SearchParameter":
                return "SearchParameter for " + id.replace("-", " ");
            case "ImplementationGuide":
                return "Implementation Guide: " + id;
            default:
                return resourceType + " " + id.replace("-", " ");
        }
    }
    
    private static String generatePageTitle(String baseName) {
        // Convert filename to readable title
        String title = baseName.replace("-", " ").replace("_", " ");
        
        // Capitalize first letter of each word
        String[] words = title.split(" ");
        StringBuilder titleBuilder = new StringBuilder();
        for (String word : words) {
            if (word.length() > 0) {
                titleBuilder.append(Character.toUpperCase(word.charAt(0)));
                if (word.length() > 1) {
                    titleBuilder.append(word.substring(1).toLowerCase());
                }
                titleBuilder.append(" ");
            }
        }
        
        return titleBuilder.toString().trim();
    }
    
    private static void copyMarkdownFiles() throws Exception {
        System.out.println("📋 Copying markdown files from R4 to STU3...");
        
        // Copy pagecontent files
        copyDirectoryContents(R4_PAGECONTENT_DIR, STU3_PAGECONTENT_DIR);
        
        // Copy includes files
        copyDirectoryContents(R4_INCLUDES_DIR, STU3_INCLUDES_DIR);
        
        System.out.println("✅ Markdown files copied successfully");
    }
    
    private static void copyDirectoryContents(String sourcePath, String targetPath) throws Exception {
        File sourceDir = new File(sourcePath);
        File targetDir = new File(targetPath);
        
        if (!sourceDir.exists()) {
            System.out.println("   ⚠️  Source directory not found: " + sourceDir.getAbsolutePath());
            return;
        }
        
        // Create target directory if it doesn't exist
        if (!targetDir.exists()) {
            targetDir.mkdirs();
        }
        
        // Copy all files from source to target
        File[] files = sourceDir.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    File targetFile = new File(targetDir, file.getName());
                    Files.copy(file.toPath(), targetFile.toPath(), java.nio.file.StandardCopyOption.REPLACE_EXISTING);
                    System.out.println("   📄 Copied: " + file.getName());
                }
            }
        }
    }
    
    private static class ResourceInfo {
        final String resourceType;
        final String id;
        final String name;
        final String title;
        final String url;
        final String fileName;
        
        ResourceInfo(String resourceType, String id, String name, String title, String url, String fileName) {
            this.resourceType = resourceType;
            this.id = id;
            this.name = name;
            this.title = title;
            this.url = url;
            this.fileName = fileName;
        }
    }
}
