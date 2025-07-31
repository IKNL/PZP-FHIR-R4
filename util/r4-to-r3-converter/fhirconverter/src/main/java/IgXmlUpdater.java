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
    
    public static void updateIgXml() {
        try {
            System.out.println("🔄 Updating STU3 ImplementationGuide XML with converted resources...");
            
            // Scan converted resources
            Map<String, ResourceInfo> resources = scanConvertedResources();
            
            if (resources.isEmpty()) {
                System.out.println("⚠️  No converted resources found in " + STU3_RESOURCES_DIR);
                return;
            }
            
            // Update the IG XML file
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
        
        for (File file : jsonFiles) {
            try {
                String content = Files.readString(file.toPath());
                ResourceInfo info = parseResourceInfo(content, file.getName());
                if (info != null) {
                    resources.put(info.id, info);
                }
            } catch (Exception e) {
                System.out.println("⚠️  Could not parse " + file.getName() + ": " + e.getMessage());
            }
        }
        
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
        File igXmlFile = new File(STU3_IG_XML_PATH);
        
        if (!igXmlFile.exists()) {
            System.out.println("⚠️  IG XML file does not exist: " + igXmlFile.getAbsolutePath());
            return;
        }
        
        // Parse the XML
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(igXmlFile);
        
        // Find the ImplementationGuide element
        XPath xpath = XPathFactory.newInstance().newXPath();
        Node igNode = (Node) xpath.evaluate("//ImplementationGuide", doc, XPathConstants.NODE);
        
        if (igNode == null) {
            System.out.println("⚠️  Could not find ImplementationGuide element in XML");
            return;
        }
        
        // Remove existing resource elements
        NodeList existingResources = (NodeList) xpath.evaluate(".//resource", igNode, XPathConstants.NODESET);
        for (int i = existingResources.getLength() - 1; i >= 0; i--) {
            Node resourceNode = existingResources.item(i);
            resourceNode.getParentNode().removeChild(resourceNode);
        }
        
        // Add new resource elements
        for (ResourceInfo resource : resources.values()) {
            Element resourceElement = doc.createElement("resource");
            
            // Add reference
            Element referenceElement = doc.createElement("reference");
            Element referenceRef = doc.createElement("reference");
            referenceRef.setAttribute("value", resource.resourceType + "/" + resource.id);
            referenceElement.appendChild(referenceRef);
            resourceElement.appendChild(referenceElement);
            
            // Add name if available
            if (resource.name != null && !resource.name.isEmpty()) {
                Element nameElement = doc.createElement("name");
                nameElement.setAttribute("value", resource.name);
                resourceElement.appendChild(nameElement);
            }
            
            // Add description (use title or name)
            String description = resource.title != null ? resource.title : resource.name;
            if (description != null && !description.isEmpty()) {
                Element descElement = doc.createElement("description");
                descElement.setAttribute("value", description);
                resourceElement.appendChild(descElement);
            }
            
            // Add exampleBoolean
            Element exampleElement = doc.createElement("exampleBoolean");
            boolean isExample = resource.resourceType.equals("Patient") || 
                              resource.resourceType.equals("Observation") ||
                              resource.resourceType.equals("Consent") ||
                              resource.id.toLowerCase().contains("example");
            exampleElement.setAttribute("value", String.valueOf(isExample));
            resourceElement.appendChild(exampleElement);
            
            igNode.appendChild(resourceElement);
        }
        
        // Write the updated XML back to file
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        transformer.setOutputProperty(javax.xml.transform.OutputKeys.INDENT, "yes");
        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
        
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(igXmlFile);
        transformer.transform(source, result);
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
