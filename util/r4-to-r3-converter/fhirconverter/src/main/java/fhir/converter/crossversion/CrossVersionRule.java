package fhir.converter.crossversion;

/**
 * Represents a cross-version transformation rule that processes FHIR extensions
 * added during StructureMap transformation to handle version-specific properties.
 */
public class CrossVersionRule {
    private final String extensionUrl;
    private final String targetProperty;
    private final String description;
    private final CrossVersionProcessor processor;
    
    public CrossVersionRule(String extensionUrl, String targetProperty, String description, CrossVersionProcessor processor) {
        this.extensionUrl = extensionUrl;
        this.targetProperty = targetProperty;
        this.description = description;
        this.processor = processor;
    }
    
    public String getExtensionUrl() {
        return extensionUrl;
    }
    
    public String getTargetProperty() {
        return targetProperty;
    }
    
    public String getDescription() {
        return description;
    }
    
    public CrossVersionProcessor getProcessor() {
        return processor;
    }
    
    @FunctionalInterface
    public interface CrossVersionProcessor {
        /**
         * Processes the extension value and applies it to the target JSON
         * @param extensionValue The value from the R4 extension
         * @param targetJson The STU3 JSON being built
         * @param originalSource The original R4 source resource for context
         * @return Modified STU3 JSON
         */
        String process(Object extensionValue, String targetJson, Object originalSource);
    }
}
