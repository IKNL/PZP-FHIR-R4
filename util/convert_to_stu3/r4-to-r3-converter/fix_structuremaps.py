#!/usr/bin/env python3
"""
Smart StructureMap Fixer

This script systematically fixes all StructureMap files to use proper 
primitive conversion functions instead of direct assignments.

Pattern to fix:
  src.field -> tgt.field;
Should become:
  src.field as vs -> tgt.field as vt then fieldType(vs, vt);

Where fieldType is determined by the FHIR specification.
"""

import os
import re
import glob
from typing import Dict, Set, List, Tuple

# Map of common FHIR field names to their primitive types
FIELD_TYPE_MAPPING = {
    # Primitive types
    'id': 'id',
    'versionId': 'id', 
    'lastUpdated': 'instant',
    'implicitRules': 'uri',
    'language': 'code',
    'version': 'string',
    'name': 'string',
    'title': 'string',
    'status': 'code',
    'experimental': 'boolean',
    'date': 'dateTime',
    'publisher': 'string',
    'description': 'markdown',
    'purpose': 'markdown',
    'copyright': 'markdown',
    'url': 'uri',
    'identifier': 'Identifier',
    'use': 'code',
    'family': 'string',
    'given': 'string',
    'prefix': 'string',
    'suffix': 'string',
    'text': 'Narrative',
    'contained': 'Resource',
    'extension': 'Extension',
    'modifierExtension': 'Extension',
    'profile': 'canonical',
    'security': 'Coding',
    'tag': 'Coding',
    'created': 'dateTime',
    'disposition': 'string',
    'active': 'boolean',
    'gender': 'code',
    'birthDate': 'date',
    'deceased': 'boolean',
    'telecom': 'ContactPoint',
    'address': 'Address',
    'maritalStatus': 'CodeableConcept',
    'multipleBirth': 'boolean',
    'photo': 'Attachment',
    'contact': 'BackboneElement',
    'communication': 'BackboneElement',
    'generalPractitioner': 'Reference',
    'managingOrganization': 'Reference',
    'link': 'BackboneElement',
    'start': 'dateTime',
    'end': 'dateTime',
    'code': 'CodeableConcept',
    'category': 'CodeableConcept',
    'subject': 'Reference',
    'context': 'Reference', 
    'encounter': 'Reference',
    'effective': 'dateTime',
    'issued': 'instant',
    'performer': 'Reference',
    'value': 'Quantity',
    'dataAbsentReason': 'CodeableConcept',
    'interpretation': 'CodeableConcept',
    'note': 'Annotation',
    'bodySite': 'CodeableConcept',
    'method': 'CodeableConcept',
    'specimen': 'Reference',
    'device': 'Reference',
    'referenceRange': 'BackboneElement',
    'related': 'BackboneElement',
    'component': 'BackboneElement'
}

# Available primitive conversion functions (from primitives.map)
PRIMITIVE_CONVERTERS = {
    'boolean', 'canonical', 'code', 'date', 'dateTime', 'decimal', 'id', 
    'instant', 'integer', 'markdown', 'oid', 'positiveInt', 'string', 
    'time', 'unsignedInt', 'uri', 'url', 'uuid', 'xhtml'
}

# Available complex type converters (need to be discovered)
COMPLEX_CONVERTERS = set()

def discover_complex_converters(maps_dir: str) -> Set[str]:
    """Discover available complex type converters from map files."""
    converters = set()
    
    for map_file in glob.glob(os.path.join(maps_dir, "*.map")):
        if 'primitives.map' in map_file:
            continue
            
        with open(map_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find group definitions for complex types
        group_pattern = r'group\s+([A-Z][a-zA-Z]+)\s*\('
        matches = re.findall(group_pattern, content)
        for match in matches:
            if match not in ['Resource', 'DomainResource', 'Element', 'BackboneElement']:
                converters.add(match)
    
    return converters

def get_field_type(field_name: str) -> str:
    """Get the type for a field, defaulting to string if unknown."""
    return FIELD_TYPE_MAPPING.get(field_name, 'string')

def should_convert_field(field_name: str, field_type: str) -> bool:
    """Determine if a field should be converted using explicit conversion."""
    # Always convert primitive types
    if field_type in PRIMITIVE_CONVERTERS:
        return True
    
    # Convert complex types if we have converters for them  
    if field_type in COMPLEX_CONVERTERS:
        return True
        
    # Don't convert unknown complex types or arrays
    return False

def fix_mapping_line(line: str, line_num: int, filename: str) -> str:
    """Fix a single mapping line if it needs conversion."""
    # Pattern: src.field -> tgt.field;
    pattern = r'^\s*src\.([a-zA-Z_][a-zA-Z0-9_]*)\s*->\s*tgt\.([a-zA-Z_][a-zA-Z0-9_]*)\s*;\s*$'
    match = re.match(pattern, line.strip())
    
    if not match:
        return line
        
    src_field, tgt_field = match.groups()
    
    # Skip if fields don't match (different field names)
    if src_field != tgt_field:
        return line
        
    field_type = get_field_type(src_field)
    
    if should_convert_field(src_field, field_type):
        # Convert to explicit conversion
        indent = len(line) - len(line.lstrip())
        new_line = f"{' ' * indent}src.{src_field} as vs -> tgt.{tgt_field} as vt then {field_type}(vs, vt);\n"
        print(f"  Fixed {filename}:{line_num}: {src_field} -> {field_type} conversion")
        return new_line
    
    return line

def fix_map_file(filepath: str) -> int:
    """Fix a single map file and return number of changes made."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    changes = 0
    new_lines = []
    
    for i, line in enumerate(lines, 1):
        new_line = fix_mapping_line(line, i, os.path.basename(filepath))
        if new_line != line:
            changes += 1
        new_lines.append(new_line)
    
    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return changes

def main():
    maps_dir = "maps/r4"
    
    print("🔧 Smart StructureMap Fixer")
    print("=" * 50)
    
    if not os.path.exists(maps_dir):
        print(f"❌ Maps directory not found: {maps_dir}")
        return
    
    # Discover available converters
    print("📋 Discovering available converters...")
    global COMPLEX_CONVERTERS
    COMPLEX_CONVERTERS = discover_complex_converters(maps_dir)
    
    print(f"✅ Found {len(PRIMITIVE_CONVERTERS)} primitive converters")
    print(f"✅ Found {len(COMPLEX_CONVERTERS)} complex converters")
    print(f"   Complex: {', '.join(sorted(COMPLEX_CONVERTERS))}")
    print()
    
    # Process all map files
    total_changes = 0
    files_changed = 0
    all_map_files = glob.glob(os.path.join(maps_dir, "*.map"))
    
    print(f"📁 Found {len(all_map_files)} map files")
    
    for map_file in sorted(all_map_files):
        if 'primitives.map' in map_file:
            continue  # Skip primitives file
            
        print(f"🔍 Processing {os.path.basename(map_file)}...")
        changes = fix_map_file(map_file)
        
        if changes > 0:
            files_changed += 1
            total_changes += changes
            print(f"  ✅ Made {changes} changes")
        else:
            print(f"  ➡️  No changes needed")
    
    print()
    print("📊 SUMMARY")
    print("=" * 50) 
    print(f"✅ Files processed: {len(all_map_files) - 1}")  # -1 for primitives
    print(f"✅ Files changed: {files_changed}")
    print(f"✅ Total changes: {total_changes}")
    print()
    print("🎉 StructureMap fix complete!")

if __name__ == "__main__":
    main()
