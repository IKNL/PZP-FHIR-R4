#!/usr/bin/env python3
"""
FHIR R4 to STU3 Extension Transformer

This script automatically transforms property mismatches in FHIR StructureMap files
by replacing direct property mappings with extension-based transformations following
the "Extension-Based Cross-Version Bridge" pattern.

Author: AI Assistant
Date: August 4, 2025
"""

import json
import re
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ExtensionTransformation:
    """Represents an extension-based transformation to apply"""
    source_property: str
    target_property: str
    resource_type: str
    extension_url: str
    original_line: str
    new_rule_line: str
    extension_group: str

class FhirExtensionTransformer:
    """Transforms FHIR StructureMap files to use extension-based cross-version mappings"""
    
    def __init__(self, analysis_file: str, maps_directory: str):
        self.analysis_file = Path(analysis_file)
        self.maps_directory = Path(maps_directory)
        
        # Load the analysis results
        with open(self.analysis_file, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        
        # Resources to skip (these need manual handling or are already handled)
        self.skip_resources = {
            'ImplementationGuide',  # Excluded from conversion
            'Reference',           # Complex type, needs manual handling
            'Money',               # Complex transformation logic
            'TriggerDefinition',   # Complex transformation logic
        }
        
        # Properties to skip (already handled or intentional)
        self.skip_properties = {
            'encounter': 'context',  # Already handled manually in Observation.map
        }
    
    def apply_all_transformations(self) -> None:
        """Apply extension-based transformations to all applicable map files"""
        
        print("🔧 FHIR Extension-Based Transformation Applier")
        print("=" * 60)
        
        for resource_type, mismatches in self.analysis["mismatches_by_resource"].items():
            
            if resource_type in self.skip_resources:
                print(f"⏭️  Skipping {resource_type} (manual handling required)")
                continue
            
            map_file = self.maps_directory / f"{resource_type}.map"
            if not map_file.exists():
                print(f"❌ Map file not found: {map_file}")
                continue
            
            print(f"🔧 Transforming {resource_type}.map ({len(mismatches)} mismatches)")
            self._transform_map_file(map_file, resource_type, mismatches)
    
    def _transform_map_file(self, map_file: Path, resource_type: str, mismatches: List[Dict]) -> None:
        """Transform a single map file"""
        
        try:
            # Read the current file
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            modified = False
            extension_groups = []
            
            for mismatch in mismatches:
                source_prop = mismatch["source_property"]
                target_prop = mismatch["target_property"]
                
                # Skip if this property mapping should be skipped
                if source_prop in self.skip_properties:
                    if self.skip_properties[source_prop] == target_prop:
                        print(f"  ⏭️  Skipping {source_prop} -> {target_prop} (already handled)")
                        continue
                
                # Generate the extension transformation
                transformation = self._generate_transformation(resource_type, mismatch)
                
                # Apply the transformation
                content, was_modified = self._apply_transformation(content, transformation)
                if was_modified:
                    modified = True
                    extension_groups.append(transformation.extension_group)
                    print(f"  ✅ Transformed: {source_prop} -> {target_prop}")
                else:
                    print(f"  ⚠️  Could not transform: {source_prop} -> {target_prop}")
            
            # Add extension groups to the end of the file
            if extension_groups:
                content = self._add_extension_groups(content, extension_groups)
                modified = True
            
            # Write the modified file
            if modified:
                # Create backup
                backup_file = map_file.with_suffix('.map.backup')
                map_file.rename(backup_file)
                print(f"  💾 Backup created: {backup_file.name}")
                
                # Write new content
                with open(map_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ Updated: {map_file.name}")
            else:
                print(f"  ℹ️  No changes needed for {map_file.name}")
                
        except Exception as e:
            print(f"  ❌ Error transforming {map_file}: {e}")
    
    def _generate_transformation(self, resource_type: str, mismatch: Dict) -> ExtensionTransformation:
        """Generate an extension transformation for a property mismatch"""
        
        source_prop = mismatch["source_property"]
        target_prop = mismatch["target_property"]
        transformation_type = mismatch["transformation_type"]
        original_line = mismatch["original_line"]
        
        # Generate extension URL
        extension_url = f"http://fhir.conversion/cross-version/{resource_type}.{target_prop}"
        
        # Generate rule name
        rule_name = f"{target_prop}-extension-rule"
        
        # Generate the new transformation rule
        new_rule_line = f"  // Cross-version property mapping: {source_prop} -> {target_prop}\n  src.{source_prop} as vs -> tgt.extension as ext then create{target_prop.capitalize()}Extension(vs, ext) \"{rule_name}\";"
        
        # Generate extension group function
        group_name = f"create{target_prop.capitalize()}Extension"
        
        # Determine value assignment based on transformation type
        if transformation_type in ["CodeableConcept", "Reference", "Identifier", "Period"]:
            value_assignment = f"src -> ext.value = src \"{target_prop}-value\";"
        elif transformation_type == "string":
            value_assignment = f"src -> ext.value = src \"{target_prop}-value\";"
        elif transformation_type == "unknown":
            value_assignment = f"src -> ext.value = src \"{target_prop}-value\";"
        else:
            value_assignment = f"src -> ext.value = src \"{target_prop}-value\";"
        
        extension_group = f"""group {group_name}(source src, target ext) {{
  src -> ext.url = '{extension_url}' "{target_prop}-url";
  {value_assignment}
}}"""
        
        return ExtensionTransformation(
            source_property=source_prop,
            target_property=target_prop,
            resource_type=resource_type,
            extension_url=extension_url,
            original_line=original_line,
            new_rule_line=new_rule_line,
            extension_group=extension_group
        )
    
    def _apply_transformation(self, content: str, transformation: ExtensionTransformation) -> tuple[str, bool]:
        """Apply a single transformation to the content"""
        
        # Find the original line and replace it
        original_line = transformation.original_line.strip()
        
        # Try to find and replace the exact line
        if original_line in content:
            content = content.replace(original_line, transformation.new_rule_line)
            return content, True
        
        # Try to find a pattern-based match if exact match fails
        source_prop = transformation.source_property
        target_prop = transformation.target_property
        
        # Pattern to match variations of the original line
        pattern = rf"src\.{re.escape(source_prop)}.*?tgt\.{re.escape(target_prop)}.*?;"
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(0), transformation.new_rule_line)
            return content, True
        
        return content, False
    
    def _add_extension_groups(self, content: str, extension_groups: List[str]) -> str:
        """Add extension group functions to the end of the file"""
        
        # Add extension groups before the final closing brace or at the end
        groups_text = "\n\n" + "\n\n".join(extension_groups)
        
        # Find the last closing brace of a group function and add after it
        # or just append to the end if no suitable location found
        content += groups_text
        
        return content

def main():
    """Main function to run the extension transformer"""
    
    # Configure paths
    script_dir = Path(__file__).parent
    analysis_file = script_dir / "property_mismatch_analysis.json"
    maps_dir = script_dir.parent / "maps" / "r4"
    
    print("🚀 FHIR Extension-Based Transformation Applier")
    print(f"📁 Analysis file: {analysis_file}")
    print(f"📁 Maps directory: {maps_dir}")
    
    if not analysis_file.exists():
        print(f"❌ Analysis file not found: {analysis_file}")
        print("   Run find_property_mismatches.py first!")
        return 1
    
    # Create the transformer
    transformer = FhirExtensionTransformer(str(analysis_file), str(maps_dir))
    
    # Apply transformations
    transformer.apply_all_transformations()
    
    print("\n✅ Transformation complete!")
    print("\n🛠️  NEXT STEPS:")
    print("1. Review the modified .map files")
    print("2. Update CrossVersionExtensionProcessor.java to handle new extensions")
    print("3. Test the transformations")
    print("4. Remove .backup files if everything works correctly")
    
    return 0

if __name__ == "__main__":
    exit(main())
