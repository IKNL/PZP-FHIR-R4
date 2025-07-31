#!/usr/bin/env python3
"""
Script to identify unused StructureMap files in the R4-to-STU3 converter.
This script compares the available .map files with the resource types actually being converted.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def get_used_resource_types():
    """Extract resource types from source JSON files."""
    source_dir = Path("../../../../R4/fsh-generated/resources")
    used_types = set()
    
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir.absolute()}")
        return used_types
    
    for json_file in source_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'resourceType' in data:
                    used_types.add(data['resourceType'])
        except Exception as e:
            print(f"Error reading {json_file}: {e}")
    
    return used_types

def get_available_map_files():
    """Get all available .map files and their corresponding resource types."""
    maps_dir = Path("r4-to-r3-converter/maps/r4")
    available_maps = {}
    
    if not maps_dir.exists():
        print(f"Maps directory not found: {maps_dir.absolute()}")
        return available_maps
    
    for map_file in maps_dir.glob("*.map"):
        # Extract resource type from filename (e.g., "Patient.map" -> "Patient")
        resource_type = map_file.stem
        available_maps[resource_type] = map_file
    
    return available_maps

def analyze_dependencies():
    """Analyze .map files to find dependencies (imports)."""
    maps_dir = Path("r4-to-r3-converter/maps/r4")
    dependencies = defaultdict(set)
    
    if not maps_dir.exists():
        return dependencies
    
    for map_file in maps_dir.glob("*.map"):
        try:
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find import statements
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('imports '):
                        # Extract the imported map name
                        # e.g., 'imports "http://hl7.org/fhir/StructureMap/*4to3"'
                        if '*4to3' in line:
                            # This imports all 4to3 maps - mark as dependency on common maps
                            dependencies[map_file.stem].add('*4to3')
                        else:
                            # Extract specific map name from URL
                            import_line = line.replace('imports ', '').strip(' "')
                            if '/StructureMap/' in import_line:
                                map_name = import_line.split('/StructureMap/')[-1].replace('4to3', '')
                                if map_name and map_name != '*':
                                    dependencies[map_file.stem].add(map_name)
        except Exception as e:
            print(f"Error analyzing dependencies in {map_file}: {e}")
    
    return dependencies

def find_base_type_dependencies():
    """Identify maps that are likely base/common types used by others."""
    maps_dir = Path("r4-to-r3-converter/maps/r4")
    base_types = set()
    
    # Common FHIR base types that are likely dependencies
    common_base_types = {
        'Element', 'BackboneElement', 'DomainResource', 'Resource',
        'Extension', 'Narrative', 'Meta', 'Identifier', 'HumanName',
        'Address', 'ContactPoint', 'Coding', 'CodeableConcept',
        'Quantity', 'Range', 'Period', 'Ratio', 'SampledData',
        'Attachment', 'Reference', 'Annotation', 'ContactDetail',
        'Contributor', 'DataRequirement', 'Expression', 'ParameterDefinition',
        'RelatedArtifact', 'TriggerDefinition', 'UsageContext', 'Dosage',
        'Money', 'Count', 'Distance', 'Duration', 'Age', 'SimpleQuantity'
    }
    
    # Check which of these exist as map files
    for map_file in maps_dir.glob("*.map"):
        if map_file.stem in common_base_types:
            base_types.add(map_file.stem)
    
    return base_types

def main():
    print("🔍 Finding unused StructureMap files...")
    print("=" * 60)
    
    # Get data
    used_types = get_used_resource_types()
    available_maps = get_available_map_files()
    dependencies = analyze_dependencies()
    base_types = find_base_type_dependencies()
    
    print(f"📊 Analysis Results:")
    print(f"   • Used resource types: {len(used_types)}")
    print(f"   • Available .map files: {len(available_maps)}")
    print(f"   • Identified base types: {len(base_types)}")
    print()
    
    print("🎯 Used Resource Types:")
    for resource_type in sorted(used_types):
        status = "✅ Has map" if resource_type in available_maps else "❌ Missing map"
        print(f"   • {resource_type:<20} {status}")
    print()
    
    # Find unused maps (excluding base types and dependencies)
    directly_used = set(used_types)
    potentially_needed = set()
    
    # Add dependencies of directly used maps
    for used_type in directly_used:
        if used_type in dependencies:
            potentially_needed.update(dependencies[used_type])
    
    # Add base types (likely to be dependencies)
    potentially_needed.update(base_types)
    
    # Remove the '*4to3' placeholder
    potentially_needed.discard('*4to3')
    
    all_needed = directly_used | potentially_needed
    unused_maps = set(available_maps.keys()) - all_needed
    
    print("🗂️ Map File Categories:")
    print()
    
    print("✅ DIRECTLY USED (from source files):")
    for resource_type in sorted(directly_used):
        if resource_type in available_maps:
            print(f"   • {resource_type}.map")
    print()
    
    print("🔗 LIKELY DEPENDENCIES (base types + imports):")
    for resource_type in sorted(potentially_needed):
        if resource_type in available_maps:
            print(f"   • {resource_type}.map")
    print()
    
    print("❌ POTENTIALLY UNUSED:")
    unused_list = sorted(unused_maps)
    if unused_list:
        for resource_type in unused_list:
            print(f"   • {resource_type}.map")
        print(f"\n📈 Total potentially unused: {len(unused_list)} files")
    else:
        print("   • None found - all maps appear to be needed!")
    
    print()
    print("⚠️  IMPORTANT NOTES:")
    print("   • 'Potentially unused' files should be reviewed manually")
    print("   • Some maps may be dependencies not detected by this analysis")
    print("   • Base/common types (Element, Address, etc.) are likely needed")
    print("   • Test the converter after removing any files!")
    
    # Generate cleanup commands
    if unused_list:
        print()
        print("🧹 CLEANUP COMMANDS (review before running!):")
        print("   # Move potentially unused files to backup directory:")
        print("   mkdir -p r4-to-r3-converter/maps/unused_backup")
        for resource_type in unused_list:
            print(f"   mv r4-to-r3-converter/maps/r4/{resource_type}.map r4-to-r3-converter/maps/unused_backup/")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
