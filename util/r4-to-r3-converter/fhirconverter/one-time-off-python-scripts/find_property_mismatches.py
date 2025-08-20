#!/usr/bin/env python3
"""
FHIR R4 to STU3 Property Mismatch Finder

This script analyzes FHIR StructureMap files to find property name mismatches
between R4 source and STU3 target properties, and generates extension-based
transformation rules following the "Extension-Based Cross-Version Bridge" pattern.

Author: AI Assistant
Date: August 4, 2025
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

@dataclass
class PropertyMismatch:
    """Represents a property name mismatch between R4 and STU3"""
    file_path: str
    line_number: int
    original_line: str
    source_property: str
    target_property: str
    resource_type: str
    transformation_type: str  # e.g., "CodeableConcept", "Reference", "string"
    
class FhirPropertyMismatchFinder:
    """Finds and analyzes property mismatches in FHIR StructureMap files"""
    
    def __init__(self, maps_directory: str):
        self.maps_directory = Path(maps_directory)
        self.mismatches: List[PropertyMismatch] = []
        
        # Pattern to match StructureMap transformation rules
        # Examples:
        # src.reasonCode as vs -> tgt.indication as vt then CodeableConcept(vs, vt)
        # src.performer as vs -> tgt.consentingParty as vt then Reference(vs, vt)
        # src.encounter -> tgt.context;
        self.transformation_pattern = re.compile(
            r'src\.(\w+)(?:\s+as\s+\w+)?\s*->\s*tgt\.(\w+)(?:\s+as\s+\w+)?(?:\s+then\s+(\w+)\([^)]+\))?'
        )
        
        # Pattern to extract resource type from map file
        self.resource_type_pattern = re.compile(
            r'group\s+(\w+)\s*\('
        )
        
        # Known property mappings that are intentional and should be skipped
        self.known_intentional_mappings = {
            # These are legitimate cross-version property name changes
            'instantiatesCanonical': {'definition'},  # Communication.instantiatesCanonical -> definition
            'encounter': {'context'},  # encounter -> context is a common R4->STU3 change
            'reasonCode': {'indication'},  # reasonCode -> indication is legitimate
            'performer': {'consentingParty'},  # performer -> consentingParty is legitimate
        }
        
    def find_all_mismatches(self) -> List[PropertyMismatch]:
        """Find all property mismatches in .map files"""
        
        map_files = list(self.maps_directory.glob("*.map"))
        print(f"🔍 Analyzing {len(map_files)} .map files in {self.maps_directory}")
        
        for map_file in map_files:
            self._analyze_map_file(map_file)
            
        print(f"📊 Found {len(self.mismatches)} property mismatches")
        return self.mismatches
    
    def _analyze_map_file(self, map_file: Path) -> None:
        """Analyze a single .map file for property mismatches"""
        
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            resource_type = self._extract_resource_type(content)
            
            if not resource_type:
                print(f"⚠️  Could not determine resource type for {map_file.name}")
                return
                
            print(f"🔍 Analyzing {map_file.name} (Resource: {resource_type})")
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('//') or line.startswith('/*'):
                    continue
                    
                mismatch = self._check_line_for_mismatch(
                    line, map_file, line_num, resource_type
                )
                if mismatch:
                    self.mismatches.append(mismatch)
                    
        except Exception as e:
            print(f"❌ Error analyzing {map_file}: {e}")
    
    def _extract_resource_type(self, content: str) -> str:
        """Extract the resource type from the map file"""
        
        match = self.resource_type_pattern.search(content)
        if match:
            return match.group(1)
        return ""
    
    def _check_line_for_mismatch(self, line: str, map_file: Path, line_num: int, resource_type: str) -> PropertyMismatch:
        """Check if a line contains a property mismatch"""
        
        match = self.transformation_pattern.search(line)
        if not match:
            return None
            
        source_prop = match.group(1)
        target_prop = match.group(2)
        transformation_type = match.group(3) or "unknown"
        
        # Skip if properties are the same (no mismatch)
        if source_prop == target_prop:
            return None
            
        # Skip known intentional mappings
        if source_prop in self.known_intentional_mappings:
            if target_prop in self.known_intentional_mappings[source_prop]:
                return None
        
        return PropertyMismatch(
            file_path=str(map_file),
            line_number=line_num,
            original_line=line.strip(),
            source_property=source_prop,
            target_property=target_prop,
            resource_type=resource_type,
            transformation_type=transformation_type
        )
    
    def generate_extension_transformations(self) -> Dict[str, List[str]]:
        """Generate extension-based transformation rules for each resource type"""
        
        transformations_by_resource = {}
        
        for mismatch in self.mismatches:
            resource_type = mismatch.resource_type
            if resource_type not in transformations_by_resource:
                transformations_by_resource[resource_type] = []
            
            # Generate the extension transformation rule
            extension_url = f"http://fhir.conversion/cross-version/{resource_type}.{mismatch.target_property}"
            
            # Generate the StructureMap rule
            rule_name = f"{mismatch.target_property}-extension-rule"
            
            transformation_rule = f"""  // Cross-version property mapping: {mismatch.source_property} -> {mismatch.target_property}
  src.{mismatch.source_property} as vs -> tgt.extension as ext then create{mismatch.target_property.capitalize()}Extension(vs, ext) "{rule_name}";"""
            
            transformations_by_resource[resource_type].append(transformation_rule)
        
        return transformations_by_resource
    
    def generate_extension_groups(self) -> Dict[str, List[str]]:
        """Generate extension creation group functions for each resource type"""
        
        groups_by_resource = {}
        
        for mismatch in self.mismatches:
            resource_type = mismatch.resource_type
            if resource_type not in groups_by_resource:
                groups_by_resource[resource_type] = []
            
            extension_url = f"http://fhir.conversion/cross-version/{resource_type}.{mismatch.target_property}"
            group_name = f"create{mismatch.target_property.capitalize()}Extension"
            
            # Determine the value assignment based on transformation type
            if mismatch.transformation_type in ["CodeableConcept", "Reference", "Identifier"]:
                value_assignment = f"src -> ext.value = src \"{mismatch.target_property}-value\";"
            elif mismatch.transformation_type == "string":
                value_assignment = f"src -> ext.value = src \"{mismatch.target_property}-value\";"
            else:
                value_assignment = f"src -> ext.value = src \"{mismatch.target_property}-value\";"
            
            group_function = f"""group {group_name}(source src, target ext) {{
  src -> ext.url = '{extension_url}' "{mismatch.target_property}-url";
  {value_assignment}
}}"""
            
            groups_by_resource[resource_type].append(group_function)
        
        return groups_by_resource
    
    def print_report(self) -> None:
        """Print a detailed report of all property mismatches"""
        
        print("\n" + "="*80)
        print("🔍 FHIR R4 TO STU3 PROPERTY MISMATCH ANALYSIS")
        print("="*80)
        
        if not self.mismatches:
            print("✅ No property mismatches found!")
            return
        
        # Group by resource type
        by_resource = {}
        for mismatch in self.mismatches:
            if mismatch.resource_type not in by_resource:
                by_resource[mismatch.resource_type] = []
            by_resource[mismatch.resource_type].append(mismatch)
        
        for resource_type, mismatches in by_resource.items():
            print(f"\n📋 {resource_type} ({len(mismatches)} mismatches)")
            print("-" * 40)
            
            for mismatch in mismatches:
                print(f"  🔄 {mismatch.source_property} → {mismatch.target_property}")
                print(f"     File: {Path(mismatch.file_path).name}:{mismatch.line_number}")
                print(f"     Type: {mismatch.transformation_type}")
                print(f"     Line: {mismatch.original_line}")
                print()
    
    def save_results(self, output_file: str) -> None:
        """Save results to a JSON file for further processing"""
        
        results = {
            "analysis_date": "2025-08-04",
            "total_mismatches": len(self.mismatches),
            "mismatches_by_resource": {},
            "suggested_transformations": self.generate_extension_transformations(),
            "suggested_extension_groups": self.generate_extension_groups()
        }
        
        # Group mismatches by resource type for JSON output
        for mismatch in self.mismatches:
            resource_type = mismatch.resource_type
            if resource_type not in results["mismatches_by_resource"]:
                results["mismatches_by_resource"][resource_type] = []
            
            results["mismatches_by_resource"][resource_type].append({
                "source_property": mismatch.source_property,
                "target_property": mismatch.target_property,
                "transformation_type": mismatch.transformation_type,
                "file": Path(mismatch.file_path).name,
                "line_number": mismatch.line_number,
                "original_line": mismatch.original_line
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")

def main():
    """Main function to run the property mismatch analysis"""
    
    # Configure paths
    script_dir = Path(__file__).parent
    maps_dir = script_dir.parent / "maps" / "r4"
    output_file = script_dir / "property_mismatch_analysis.json"
    
    print("🚀 FHIR R4 to STU3 Property Mismatch Finder")
    print(f"📁 Maps directory: {maps_dir}")
    print(f"💾 Output file: {output_file}")
    
    # Create the analyzer
    analyzer = FhirPropertyMismatchFinder(str(maps_dir))
    
    # Find all mismatches
    mismatches = analyzer.find_all_mismatches()
    
    # Print report
    analyzer.print_report()
    
    # Save results
    analyzer.save_results(str(output_file))
    
    # Print suggested next steps
    print("\n🛠️  SUGGESTED NEXT STEPS:")
    print("1. Review the property_mismatch_analysis.json file")
    print("2. Apply the suggested extension transformations to .map files")
    print("3. Add the suggested extension groups to each .map file")
    print("4. Update the Java CrossVersionExtensionProcessor to handle new extensions")
    print("5. Test the transformations")
    
    return len(mismatches)

if __name__ == "__main__":
    exit_code = main()
    exit(0 if exit_code >= 0 else 1)
