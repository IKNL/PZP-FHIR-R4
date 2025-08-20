package fhir.converter;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Stream;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class IgXmlUpdater {
    
    private static final String STU3_RESOURCES_DIR = "../../../STU3/input/resources/";
    private static final String STU3_IG_XML_FILE = "../../../STU3/input/IKNL_PZP_IG.xml";
    
    public static void updateIgXml() {
        try {
            System.out.println("🔄 Updating STU3 ImplementationGuide XML with converted resources...");
            
            // 1. Scan converted STU3 resources
            Map<String, ResourceInfo> convertedResources = scanConvertedResources();
            System.out.println("   📊 Found " + convertedResources.size() + " converted resources");
            
            // 2. Load and parse the IG XML
            Document doc = loadIgXml();
            
            // 3. Update resource references
            updateResourceReferences(doc, convertedResources);
            
            // 4. Save the updated XML
            saveIgXml(doc);
            
            System.out.println("✅ Successfully updated STU3 ImplementationGuide XML");
            
        } catch (Exception e) {
            System.err.println("❌ Failed to update IG XML: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static Map<String, ResourceInfo> scanConvertedResources() throws IOException {
        Map<String, ResourceInfo> resources = new HashMap<>();
        Path resourcesDir = Paths.get(STU3_RESOURCES_DIR);
        
        if (!Files.exists(resourcesDir)) {
            System.out.println("   ⚠️  STU3 resources directory not found: " + resourcesDir.toAbsolutePath());
            return resources;
        }
        
        try (Stream<Path> paths = Files.walk(resourcesDir)) {
            paths.filter(Files::isRegularFile)
                  .filter(path -> path.toString().endsWith(".json"))
                  .forEach(path -> {
                      try {
                          ResourceInfo info = parseResourceInfo(path);
                          if (info != null) {
                              String key = info.resourceType + "/" + info.id;
                              resources.put(key, info);
                          }
                      } catch (Exception e) {
                          System.err.println("   ⚠️  Failed to parse " + path.getFileName() + ": " + e.getMessage());
                      }
                  });
        }
        
        return resources;
    }
    
    private static ResourceInfo parseResourceInfo(Path jsonFile) throws IOException {
        String content = Files.readString(jsonFile);
        JsonObject json = JsonParser.parseString(content).getAsJsonObject();
        
        if (!json.has("resourceType") || !json.has("id")) {
            return null;
        }
        
        ResourceInfo info = new ResourceInfo();
        info.resourceType = json.get("resourceType").getAsString();
        info.id = json.get("id").getAsString();
        info.fileName = jsonFile.getFileName().toString();
        
        // Try to get a description from the resource
        if (json.has("description")) {
            info.description = json.get("description").getAsString();
        } else if (json.has("title")) {
            info.description = json.get("title").getAsString();
        } else if (json.has("name")) {
            info.description = json.get("name").getAsString();
        } else {
            // Generate a default description
            info.description = generateDescription(info.resourceType, info.id);
        }
        
        return info;
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
    
    private static Document loadIgXml() throws Exception {
        File xmlFile = new File(STU3_IG_XML_FILE);
        if (!xmlFile.exists()) {
            throw new IOException("IG XML file not found: " + xmlFile.getAbsolutePath());
        }
        
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(xmlFile);
    }
    
    private static void updateResourceReferences(Document doc, Map<String, ResourceInfo> convertedResources) throws Exception {
        XPathFactory xPathFactory = XPathFactory.newInstance();
        XPath xpath = xPathFactory.newXPath();
        
        // Find the definition element
        Node definitionNode = (Node) xpath.compile("//definition").evaluate(doc, XPathConstants.NODE);
        if (definitionNode == null) {
            throw new Exception("Could not find <definition> element in IG XML");
        }
        
        // Remove all existing resource elements
        NodeList existingResources = (NodeList) xpath.compile(".//resource").evaluate(definitionNode, XPathConstants.NODESET);
        for (int i = existingResources.getLength() - 1; i >= 0; i--) {
            Node resourceNode = existingResources.item(i);
            resourceNode.getParentNode().removeChild(resourceNode);
        }
        
        // Add new resource elements based on converted resources
        List<ResourceInfo> sortedResources = new ArrayList<>(convertedResources.values());
        sortedResources.sort((a, b) -> {
            // Sort by resource type first, then by ID
            int typeCompare = a.resourceType.compareTo(b.resourceType);
            if (typeCompare != 0) return typeCompare;
            return a.id.compareTo(b.id);
        });
        
        for (ResourceInfo resource : sortedResources) {
            Element resourceElement = createResourceElement(doc, resource);
            definitionNode.appendChild(resourceElement);
            
            // Add some formatting (newline and indentation)
            definitionNode.appendChild(doc.createTextNode("\n    "));
        }
        
        System.out.println("   📝 Updated " + sortedResources.size() + " resource references");
    }
    
    private static Element createResourceElement(Document doc, ResourceInfo resource) {
        Element resourceElem = doc.createElement("resource");
        
        Element referenceElem = doc.createElement("reference");
        Element refElem = doc.createElement("reference");
        refElem.setAttribute("value", resource.resourceType + "/" + resource.id);
        referenceElem.appendChild(refElem);
        resourceElem.appendChild(referenceElem);
        
        Element descElem = doc.createElement("description");
        descElem.setAttribute("value", resource.description);
        resourceElem.appendChild(descElem);
        
        return resourceElem;
    }
    
    private static void saveIgXml(Document doc) throws Exception {
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        transformer.setOutputProperty("indent", "yes");
        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
        
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(new File(STU3_IG_XML_FILE));
        transformer.transform(source, result);
    }
    
    private static class ResourceInfo {
        String resourceType;
        String id;
        String description;
        String fileName;
    }
}
