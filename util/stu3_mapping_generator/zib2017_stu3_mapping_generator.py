#!/usr/bin/env python3
"""
Comprehensive ZIB2017 to STU3 FHIR Mapping Generator

This script:
1. Extracts ZIB concept mappings from STU3 profile files
2. Extracts zib2017 and zib2020 concepts from the dataset JSON
3. Cross-references zib2017 concepts with zib2020 concepts (not R4 mappings)
4. Generates comprehensive mapping outputs with proper cross-referencing
5. Creates the final markdown table in STU3/input/includes/

Author: AI Assistant
Date: August 8, 2025
"""

import json
import re
import os
from pathlib import Path
import yaml

def find_concepts_recursively(data, depth=0):
    """
    Recursively finds all 'concept' objects within a given data structure.
    """
    concepts = []
    if isinstance(data, dict):
        for key, value in data.items():
            # Skip conceptList which contains value sets/terminology
            if key == 'conceptList':
                continue

            if key == 'concept' and isinstance(value, list):
                for concept in value:
                    concepts.append((concept, depth))
                    # Recurse into children
                    concepts.extend(find_concepts_recursively(concept, depth + 1))
            elif isinstance(value, (dict, list)):
                concepts.extend(find_concepts_recursively(value, depth))
    elif isinstance(data, list):
        for item in data:
            concepts.extend(find_concepts_recursively(item, depth))
    return concepts

def extract_stu3_profile_mappings(profiles_directory):
    """
    Extracts ZIB concept mappings from STU3 FHIR profile JSON files.
    Returns dict mapping ZIB concept IDs to profile mapping info.
    """
    zib_mappings = {}
    
    if not os.path.exists(profiles_directory):
        print(f"Warning: STU3 profiles directory not found: {profiles_directory}")
        return zib_mappings
    
    profile_files = [f for f in os.listdir(profiles_directory) if f.endswith('.json')]
    print(f"Processing {len(profile_files)} STU3 profile files...")
    
    for filename in profile_files:
        filepath = os.path.join(profiles_directory, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
            continue
        
        # Skip if not a StructureDefinition
        if profile_data.get('resourceType') != 'StructureDefinition':
            continue
        
        profile_id = profile_data.get('id', filename.replace('.json', ''))
        profile_url = profile_data.get('url', '')
        resource_type = profile_data.get('type', '')
        
        # Extract element mappings from differential
        if 'differential' in profile_data and 'element' in profile_data['differential']:
            for element in profile_data['differential']['element']:
                element_path = element.get('path', '')
                element_id = element.get('id', '')
                
                # Look for mappings in this element
                if 'mapping' in element:
                    for mapping in element['mapping']:
                        mapping_identity = mapping.get('identity', '')
                        mapping_map = mapping.get('map', '')
                        
                        # Normalize mapping identifier to handle both 'NL-CM-xx' and 'NL-CM:xx'
                        norm_map = normalize_zib_concept_id(mapping_map)
                        # Look for HCIM/ZIB mappings
                        if norm_map and ('NL-CM:' in norm_map or 'hcim-' in mapping_identity.lower()):
                            # Extract the ZIB concept ID (e.g., "NL-CM:7.15.1")
                            zib_concept_match = re.search(r'NL-CM:[\d.]+', norm_map)
                            if zib_concept_match:
                                zib_concept_id = zib_concept_match.group(0)
                                
                                # Store the mapping information
                                if zib_concept_id not in zib_mappings:
                                    zib_mappings[zib_concept_id] = []
                                
                                zib_mappings[zib_concept_id].append({
                                    'profile_id': profile_id,
                                    'profile_url': profile_url,
                                    'resource_type': resource_type,
                                    'element_path': element_path,
                                    'element_id': element_id,
                                    'mapping_comment': mapping.get('comment', ''),
                                    'mapping_identity': mapping_identity,
                                    'zib_concept_id': zib_concept_id
                                })
    
    print(f"Extracted mappings for {len(zib_mappings)} ZIB concepts from STU3 profiles")
    return zib_mappings

def extract_dataset_concepts(json_file_path):
    """
    Extracts concepts from the dataset JSON file for both ZIBS2017 and ZIBS2020 groups.
    Returns two dicts mapping dataset IDs to concept info.
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Identify the two groups by shortName
    group2017 = None
    group2020 = None
    for grp in data.get('concept', []):
        if grp.get('shortName') == 'informatiestandaard_obv_zibs2017':
            group2017 = grp
        elif grp.get('shortName') == 'informatiestandaard_obv_zibs2020':
            group2020 = grp
    
    def parse_group(group):
        results = {}
        if not group:
            return results
        def recurse(concepts, depth=0):
            for c in concepts:
                full_id = c.get('id', '')
                dataset_id = full_id.split('.')[-1]
                name = None
                for n in c.get('name', []):
                    if n.get('language') == 'nl-NL':
                        name = n.get('#text')
                rels = []
                # capture ZIB references from relationship and inherit lists
                for rel in c.get('relationship', []):
                    rd = rel.get('refDisplay') or rel.get('refdisplay')
                    if rd:
                        # normalize dash vs colon in concept IDs
                        rels.append(normalize_zib_concept_id(rd))
                for inh in c.get('inherit', []):
                    rd = inh.get('refDisplay') or inh.get('refdisplay')
                    if rd:
                        # normalize dash vs colon in concept IDs
                        rels.append(normalize_zib_concept_id(rd))
                results[dataset_id] = {
                    'dataset_id': dataset_id,
                    'shortName': c.get('shortName'),
                    'name': name or c.get('shortName'),
                    'depth': depth,
                    'zib_refs': rels
                }
                recurse(c.get('concept', []), depth+1)
        recurse(group.get('concept', []))
        return results

    zib2017 = parse_group(group2017)
    zib2020 = parse_group(group2020)
    print(f"Loaded {len(zib2017)} ZIB2017 concepts and {len(zib2020)} ZIB2020 concepts from dataset")
    return zib2017, zib2020

def normalize_zib_concept_id(concept_id):
    """
    Normalizes ZIB concept IDs for comparison.
    """
    if not concept_id:
        return ""
    
    normalized = concept_id.strip()
    if normalized.startswith('NL-CM-'):
        normalized = normalized.replace('NL-CM-', 'NL-CM:', 1)
    elif normalized.startswith('NL-CM '):
        normalized = normalized.replace('NL-CM ', 'NL-CM:', 1)
    
    return normalized

def find_zib2017_to_zib2020_cross_references(zib2017_concepts, zib2020_concepts):
    """
    Find cross-references between zib2017 and zib2020 concepts based on name similarity.
    Only cross-references concepts that are different (avoids self-referencing).
    """
    cross_references = {}
    
    for zib2017_id, zib2017_concept in zib2017_concepts.items():
        zib2017_name = zib2017_concept['name'].lower()
        
        best_match = None
        best_score = 0
        
        for zib2020_id, zib2020_concept in zib2020_concepts.items():
            # Skip if same dataset ID (avoid self-referencing)
            if zib2017_id == zib2020_id:
                continue
                
            zib2020_name = zib2020_concept['name'].lower()
            
            # Calculate similarity score
            if zib2017_name == zib2020_name:
                score = 100  # Exact match
            elif zib2017_name in zib2020_name or zib2020_name in zib2017_name:
                score = 80   # Partial match
            elif any(word in zib2020_name for word in zib2017_name.split() if len(word) > 3):
                score = 60   # Word-level match
            else:
                score = 0
            
            if score > best_score:
                best_score = score
                best_match = {
                    'zib2020_dataset_id': zib2020_id,
                    'zib2020_name': zib2020_concept['name'],
                    'zib2020_depth': zib2020_concept['depth'],
                    'similarity_score': score
                }
        
        if best_match and best_score >= 60:  # Only include good matches
            cross_references[zib2017_id] = best_match
    
    print(f"Found {len(cross_references)} cross-references between zib2017 and zib2020 concepts")
    return cross_references

def generate_comprehensive_mappings(zib2017_concepts, stu3_mappings, cross_references):
    """
    Generate comprehensive mappings combining zib2017 concepts, STU3 mappings, and cross-references.
    """
    comprehensive_mappings = []
    
    # Process all zib2017 concepts
    for dataset_id, concept in zib2017_concepts.items():
        concept_name = concept['name']
        depth = concept['depth']
        
        # Find STU3 mappings for this concept (by searching for ZIB concept relationships)
        matching_stu3_mappings = []
        
        # For now, we'll need to match by name or other heuristics since we don't have direct ZIB concept IDs
        # This is where you might need to enhance the matching logic based on your specific requirements
        
        # Check if we have cross-reference to zib2020
        zib2020_cross_ref = cross_references.get(dataset_id)
        
        # Create mapping entry
        if matching_stu3_mappings:
            # Has STU3 mappings
            for stu3_mapping in matching_stu3_mappings:
                mapping_entry = {
                    'dataset_id': dataset_id,
                    'concept_name': concept_name,
                    'depth': depth,
                    'zib_concept_id': stu3_mapping['zib_concept_id'],
                    'resource_type': stu3_mapping['resource_type'],
                    'profile_id': stu3_mapping['profile_id'],
                    'profile_url': stu3_mapping['profile_url'],
                    'element_path': stu3_mapping['element_path'],
                    'element_id': stu3_mapping['element_id'],
                    'mapping_status': 'mapped_stu3',
                    'zib2020_cross_reference': zib2020_cross_ref
                }
                comprehensive_mappings.append(mapping_entry)
        else:
            # No STU3 mappings - create placeholder
            mapping_entry = {
                'dataset_id': dataset_id,
                'concept_name': concept_name,
                'depth': depth,
                'zib_concept_id': '',
                'resource_type': None,
                'profile_id': None,
                'profile_url': None,
                'element_path': None,
                'element_id': None,
                'mapping_status': 'needs_manual_mapping',
                'zib2020_cross_reference': zib2020_cross_ref
            }
            comprehensive_mappings.append(mapping_entry)
    
    # For demonstration, let's also add some example STU3 mappings from our profile analysis
    # You would need to implement the actual matching logic here
    
    print(f"Generated {len(comprehensive_mappings)} comprehensive mapping entries")
    return comprehensive_mappings

def save_json_output(mappings, output_file):
    """
    Save mappings to JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)
    
    print(f"JSON mappings saved to: {output_file}")

def generate_markdown_table(mappings, zib2017_concepts, output_file):
    """
    Generate markdown table in the same style as R4 mappings.
    """
    # Group mappings by dataset_id
    concept_groups = {}
    for mapping in mappings:
        dataset_id = mapping['dataset_id']
        if dataset_id not in concept_groups:
            concept_groups[dataset_id] = []
        concept_groups[dataset_id].append(mapping)
    
    # Sort by dataset_id numerically
    sorted_dataset_ids = sorted(concept_groups.keys(), key=lambda x: int(x))
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#### Mappings by dataset ID\n\n")
        f.write("This table provides an overview of all dataset elements from the zib2017 dataset ")
        f.write("that are mapped to STU3 FHIR profiles based on ZIB concept relationships.\n\n")
        
        # Table header
        f.write("| ID | Dataset name | Resource | FHIR element |\n")
        f.write("|---|---|---|---|\n")
        
        # Generate table rows
        rows_written = 0
        unmapped_concepts = []
        
        for dataset_id in sorted_dataset_ids:
            concept_mappings = concept_groups[dataset_id]
            
            # Get concept info
            concept_info = zib2017_concepts.get(dataset_id, {})
            concept_name = concept_info.get('name', concept_mappings[0]['concept_name'])
            depth = concept_info.get('depth', 0)
            
            # Create indentation
            indentation = "&emsp;" * depth if depth > 0 else ""
            dataset_name = indentation + concept_name
            
            # Check for actual mappings
            actual_mappings = [m for m in concept_mappings if m['resource_type'] is not None]
            
            if actual_mappings:
                # Write row for each mapping
                for mapping in actual_mappings:
                    resource_type = mapping['resource_type']
                    profile_id = mapping['profile_id']
                    element_path = mapping['element_path']
                    
                    # Combine resource type and profile
                    resource_display = f'{resource_type} (<a href="StructureDefinition-{profile_id}.html">{profile_id}</a>)'
                    f.write(f"| {dataset_id} | {dataset_name} | {resource_display} | `{element_path}` |\n")
                    rows_written += 1
            else:
                # Track unmapped concept
                unmapped_concepts.append({
                    'dataset_id': dataset_id,
                    'name': concept_name,
                    'zib2020_cross_ref': concept_mappings[0].get('zib2020_cross_reference')
                })
        
        if rows_written == 0:
            f.write("| | No mappings were found. Check STU3 profile mappings. | | |\n")
        
        # Unmapped elements section
        if unmapped_concepts:
            f.write("\n\n##### Overview of Unmapped Elements\n\n")
            f.write("These elements need manual mapping to STU3 profiles:\n\n")
            f.write("| ID | Name | ZIB2020 Cross-Reference |\n")
            f.write("|---|---|---|\n")
            
            for concept in unmapped_concepts:
                dataset_id = concept['dataset_id']
                name = concept['name']
                zib2020_ref = concept['zib2020_cross_ref']
                
                if zib2020_ref:
                    cross_ref_info = f"{zib2020_ref['zib2020_name']} (ID: {zib2020_ref['zib2020_dataset_id']}, Score: {zib2020_ref['similarity_score']})"
                else:
                    cross_ref_info = "No similar zib2020 concept found"
                
                f.write(f"| {dataset_id} | {name} | {cross_ref_info} |\n")
        
        # Summary statistics
        total_concepts = len(zib2017_concepts)
        mapped_concepts = len([c for c in concept_groups.values() if any(m['resource_type'] is not None for m in c)])
        
        f.write(f"\n\n##### Summary\n\n")
        f.write(f"- **Total zib2017 concepts**: {total_concepts}\n")
        f.write(f"- **Mapped to STU3**: {mapped_concepts}\n")
        f.write(f"- **Coverage**: {mapped_concepts/total_concepts*100:.1f}%\n")
        f.write(f"- **Need manual mapping**: {len(unmapped_concepts)}\n")
    
    print(f"Markdown table saved to: {output_file}")

def parse_r4_mappings(md_file_path):
    """
    Parses the R4 mappings markdown to dict of dataset_id -> list of resource/path entries
    """
    mappings = {}
    pattern = re.compile(r"^\|\s*(\d+)\s*\|.*?\|\s*`([^`]*)`")
    with open(md_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line)
            if m:
                did, path = m.groups()
                # extract resource from line segments
                parts = line.split('|')
                resource = parts[2].strip()
                mappings.setdefault(did, []).append({'resource': resource, 'element_path': path})
    print(f"Parsed {sum(len(v) for v in mappings.values())} R4 mapping entries from {md_file_path}")
    return mappings

def generate_integration_json(zib2017, stu3_mappings, zib2020, r4_mappings, output_file):
    """
    Combines dataset concepts, STU3 profile mappings, and R4 mappings into an integration JSON.
    """
    # Initialize flat index for profile mappings
    flat_index = {}
    # Load flat profile mappings generated by extract_all_profile_mappings.py or extract_mappings_stu3.zib2017_package.py
    base = Path(__file__).parent
    candidates = [base / 'all_profile_mappings.json', base / 'all_nictiz_zib20217_profile_mappings.json']
    flat_file = next((f for f in candidates if f.exists()), None)
    if not flat_file:
        print(f"Flat profile mappings file not found in: {candidates}")
    else:
        try:
            flat_data = json.loads(flat_file.read_text(encoding='utf-8'))
            for entry in flat_data:
                eid = entry.get('id')
                path = entry.get('path')
                for m in entry.get('mapping', []):
                    cm = normalize_zib_concept_id(m.get('map',''))
                    if cm.startswith('NL-CM:'):
                        flat_index.setdefault(cm, []).append({
                            'element_id': eid,
                            'element_path': path,
                            'mapping_identity': m.get('identity'),
                            'mapping_comment': m.get('comment','')
                        })
        except Exception as e:
            print(f"Warning: failed to load flat mappings from {flat_file}: {e}")
    # end load flat mappings

    # load manual overrides
    overrides_file = Path(__file__).parent / 'manual_overrides.yaml'
    if overrides_file.exists():
        try:
            overrides = yaml.safe_load(overrides_file.read_text(encoding='utf-8')).get('overrides', {}) or {}
        except Exception as e:
            print(f"Warning loading overrides: {e}")
            overrides = {}
    else:
        print(f"No manual_overrides.yaml found, proceeding without overrides")
        overrides = {}
    # load IG profile definitions (STU3) to map each resource type to IG profile id
    ig_res_dir = Path(__file__).parent.parent.parent / 'STU3' / 'input' / 'resources'
    ig_profiles = {}
    if ig_res_dir.exists():
        for fn in os.listdir(ig_res_dir):
            if fn.endswith('.json'):
                try:
                    pdata = json.loads(Path(ig_res_dir / fn).read_text(encoding='utf-8'))
                    if pdata.get('resourceType') == 'StructureDefinition':
                        rtype = pdata.get('type')
                        pid = pdata.get('id')
                        # Only include profiles that start with 'ACP-' to avoid generic Nictiz profiles
                        if pid and pid.startswith('ACP-'):
                            ig_profiles.setdefault(rtype, []).append(pid)
                except:
                    continue
    # also load core Nictiz STU3 profiles for datatype mappings only
    core_res_dir = Path(__file__).parent / 'nictiz.fhir.nl.stu3.zib2017#2.2.20' / 'package'
    if core_res_dir.exists():
        for fn in os.listdir(core_res_dir):
            if fn.endswith('.json'):
                try:
                    pdata = json.loads(Path(core_res_dir / fn).read_text(encoding='utf-8'))
                    if pdata.get('resourceType') == 'StructureDefinition':
                        rtype = pdata.get('type')
                        pid = pdata.get('id')
                        # Only add datatype profiles (HumanName, Address, ContactPoint) from core package
                        if rtype in {'HumanName', 'Address', 'ContactPoint'}:
                            ig_profiles.setdefault(rtype, []).append(pid)
                except:
                    continue
    # in-scope resource types are those with IG profiles
    in_scope = set(ig_profiles.keys())
    records = []
    for did, info in zib2017.items():
        rec = {**info, 'stu3_mappings': [], 'r4_mappings': []}
        # STU3 mappings: manual overrides or auto
        if did in overrides:
            for ov in overrides.get(did, []) or []:
                if ov.get('resource') in in_scope:
                    rec['stu3_mappings'].append(ov)
        else:
            for ref in info['zib_refs']:
                norm = normalize_zib_concept_id(ref)
                # try both normalized and original keys
                for key in {norm, ref}:
                    for m in stu3_mappings.get(key, []):
                        rtype = m['resource_type']
                        if rtype in in_scope:
                            # pick first IG profile id for this resource
                            profile_ids = ig_profiles.get(rtype, [])
                            ig_pid = profile_ids[0] if profile_ids else None
                            rec['stu3_mappings'].append({
                                'zib_concept_id': norm,
                                'resource': rtype,
                                'profile_id': ig_pid,
                                'element_path': m['element_path'],
                                'element_id': m['element_id']
                            })
        # Deduplicate STU3 mappings and filter to in-scope resources
        unique = []
        seen = set()
        for m in rec['stu3_mappings']:
            if m.get('resource') not in in_scope:
                continue
            key = (m['zib_concept_id'], m['resource'], m.get('profile_id'), m['element_path'], m['element_id'])
            if key not in seen:
                seen.add(key)
                unique.append(m)
        rec['stu3_mappings'] = unique
        
        # Apply datatype context improvements to integration.json
        datatype_to_element = {'HumanName': '.name', 'Address': '.address', 'ContactPoint': '.telecom'}
        allowed_extra = {'HumanName', 'ContactPoint', 'Address'}
        
        # Build datatype context from existing mappings
        current_context = {}
        for m in rec['stu3_mappings']:
            resource = m.get('resource', '')
            path = m.get('element_path', '')
            if resource not in allowed_extra and path:
                for dtype, suffix in datatype_to_element.items():
                    if suffix in path:
                        current_context[dtype] = {'host_resource': resource, 'host_path': path}
        
        # Apply context overrides to integration.json mappings
        updated_mappings = []
        for m in rec['stu3_mappings']:
            resource = m.get('resource', '')
            path = m.get('element_path', '')
            
            if resource in allowed_extra:
                # Find appropriate host context
                host_info = None
                for dtype, suffix in datatype_to_element.items():
                    if dtype == resource and dtype in current_context:
                        host_info = current_context[dtype]
                        break
                
                if host_info:
                    host_resource = host_info['host_resource']
                    host_path = host_info['host_path']
                    
                    # Create updated mapping with host context
                    updated_mapping = m.copy()
                    if path == resource:  # root datatype
                        updated_mapping['resource'] = host_resource
                        updated_mapping['element_path'] = host_path
                        updated_mapping['element_id'] = host_path  # Update element_id to match path
                    else:  # child of datatype
                        updated_mapping['resource'] = host_resource
                        original_datatype = path.split('.')[0]
                        if path.startswith(original_datatype + '.'):
                            new_path = host_path + path[len(original_datatype):]
                            updated_mapping['element_path'] = new_path
                            updated_mapping['element_id'] = new_path  # Update element_id to match path
                    
                    # Update profile_id to match host resource
                    profile_ids = ig_profiles.get(host_resource, [])
                    if profile_ids:
                        updated_mapping['profile_id'] = profile_ids[0]
                    
                    updated_mappings.append(updated_mapping)
                else:
                    updated_mappings.append(m)
            else:
                updated_mappings.append(m)
        
        rec['stu3_mappings'] = updated_mappings
        
        # Final deduplication: remove standalone datatype mappings when host mappings exist
        deduplicated_mappings = []
        datatype_paths = set()
        host_paths = set()
        
        # First pass: collect all host resource paths
        for m in rec['stu3_mappings']:
            resource = m.get('resource', '')
            path = m.get('element_path', '')
            if resource not in allowed_extra:
                host_paths.add(path)
        
        # Second pass: add mappings, preferring host over datatype
        for m in rec['stu3_mappings']:
            resource = m.get('resource', '')
            path = m.get('element_path', '')
            
            if resource in allowed_extra:
                # This is a datatype mapping
                if path == resource:  # Root datatype (e.g., "HumanName")
                    # Check if there's a corresponding host mapping
                    has_host_equivalent = False
                    for dtype, suffix in datatype_to_element.items():
                        if dtype == resource:
                            # Look for host paths ending with this suffix
                            for host_path in host_paths:
                                if host_path.endswith(suffix):
                                    has_host_equivalent = True
                                    break
                            break
                    
                    if not has_host_equivalent:
                        deduplicated_mappings.append(m)
                else:
                    # Child datatype mapping - always keep these as they're unique
                    deduplicated_mappings.append(m)
            else:
                # Host resource mapping - always keep
                deduplicated_mappings.append(m)
        
        rec['stu3_mappings'] = deduplicated_mappings
        
        # Final exact duplicate removal: same dataset_id + resource + element_path
        final_mappings = []
        seen_mappings = set()
        for m in rec['stu3_mappings']:
            # Create a key from the dataset_id (which this record represents) + mapping details
            mapping_key = (
                rec.get('dataset_id', ''),
                m.get('resource', ''),
                m.get('profile_id', ''),
                m.get('element_path', ''),
                m.get('element_id', '')
            )
            if mapping_key not in seen_mappings:
                seen_mappings.add(mapping_key)
                final_mappings.append(m)
        
        rec['stu3_mappings'] = final_mappings
        # If no host-resource mappings found, try datatype profile propagation
        if not rec['stu3_mappings']:
            # fallback from selected datatype profiles only
            allowed_dtypes = {'HumanName', 'ContactPoint', 'Address'}
            for ref in info['zib_refs']:
                norm = normalize_zib_concept_id(ref)
                # look for datatype-level mappings by ZIB concept ID
                for m in stu3_mappings.get(norm, []):
                    dtype = m.get('resource_type')
                    datatype_profile_url = m.get('profile_url')
                    # only consider selected datatype profiles
                    if dtype in allowed_dtypes and datatype_profile_url:
                        # scan each host profile for elements typed with this datatype
                        for host_type, pids in ig_profiles.items():
                            for host_pid in pids:
                                host_file = ig_res_dir / f"StructureDefinition-{host_pid}.json"
                                try:
                                    hdata = json.loads(Path(host_file).read_text(encoding='utf-8'))
                                except Exception:
                                    continue
                                for el in hdata.get('differential', {}).get('element', []):
                                    path = el.get('path', '')
                                    # check if element type.profile matches the datatype
                                    for t in el.get('type', []):
                                        if t.get('profile') == datatype_profile_url:
                                            rec['stu3_mappings'].append({
                                                'zib_concept_id': norm,
                                                'resource': host_type,
                                                'profile_id': host_pid,
                                                'element_path': path,
                                                'element_id': el.get('id', '')
                                            })
            # dedupe propagated mappings
            seen = set()
            unique_dt = []
            for m in rec['stu3_mappings']:
                key = (m.get('zib_concept_id'), m.get('resource'), m.get('profile_id'), m.get('element_path'), m.get('element_id'))
                if key not in seen:
                    seen.add(key)
                    unique_dt.append(m)
            rec['stu3_mappings'] = unique_dt
        # final fallback: use flat profile mappings index
        if not rec['stu3_mappings']:
            for ref in info['zib_refs']:
                norm = normalize_zib_concept_id(ref)
                for fm in flat_index.get(norm, []):
                    path = fm['element_path']
                    resource = path.split('.', 1)[0]
                    if resource in in_scope:
                        profile_ids = ig_profiles.get(resource, [])
                        pid = profile_ids[0] if profile_ids else None
                        rec['stu3_mappings'].append({
                            'zib_concept_id': norm,
                            'resource': resource,
                            'profile_id': pid,
                            'element_path': path,
                            'element_id': fm.get('element_id'),
                            'mapping_identity': fm.get('mapping_identity'),
                            'mapping_comment': fm.get('mapping_comment')
                        })
            # dedupe final fallback mappings
            seen_ft = set()
            final_ft = []
            for m in rec['stu3_mappings']:
                key = (m['zib_concept_id'], m['resource'], m['profile_id'], m['element_path'], m['element_id'])
                if key not in seen_ft:
                    seen_ft.add(key)
                    final_ft.append(m)
            rec['stu3_mappings'] = final_ft
        # R4 mappings via name match in zib2020
        name_low = info['name'].lower()
        best_id, best_score = None, 0
        for did20, info20 in zib2020.items():
            n2 = info20['name'].lower()
            score = 100 if name_low==n2 else 80 if name_low in n2 else 0
            if score>best_score:
                best_score, best_id = score, did20
        if best_score >= 60 and best_id in r4_mappings:
            rec['r4_mappings'] = []
            for rm in r4_mappings[best_id]:
                # extract R4 profile id from HTML link if present
                res = rm.get('resource', '')
                prof_id = None
                m = re.search(r'<a[^>]*>([^<]+)</a>', res)
                if m:
                    prof_id = m.group(1)
                rec['r4_mappings'].append({
                    'resource': res,
                    'element_path': rm.get('element_path'),
                    'zib2020_dataset_id': best_id,
                    'zib2020_shortName': zib2020.get(best_id, {}).get('shortName'),
                    'r4_profile_id': prof_id
                })
        records.append(rec)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Integration JSON saved to: {output_file}")

# Add STU3 IG markdown generator
def generate_ig_markdown(integration_file, resources_dir, output_file):
    """
    Generates markdown table for STU3 IG based on integration.json and profiled resources.
    """
    # load integration records
    with open(integration_file, 'r', encoding='utf-8') as f:
        records = json.load(f)
    # determine dataset order from dataset JSON (group2017)
    dataset_file = Path(__file__).parent.parent / "DS_pzp_dataset_raadplegen_(download_2025-07-29T11_58_18).json"
    zib2017_concepts, _ = extract_dataset_concepts(str(dataset_file))
    dataset_order = list(zib2017_concepts.keys())
    # index records by dataset_id
    rec_map = {rec['dataset_id']: rec for rec in records}
    # determine in-scope resources based on available STU3 profile definitions
    in_scope = set()
    for fn in os.listdir(resources_dir):
        if fn.endswith('.json'):
            try:
                pdata = json.load(open(os.path.join(resources_dir, fn), 'r', encoding='utf-8'))
                if pdata.get('resourceType') == 'StructureDefinition':
                    pid = pdata.get('id', '')
                    # Only include ACP profiles, not generic Nictiz profiles
                    if pid.startswith('ACP-'):
                        in_scope.add(pdata.get('type'))
            except Exception:
                continue
    # also allow key datatypes
    allowed_extra = {'HumanName', 'ContactPoint', 'Address'}
    in_scope |= allowed_extra
    # build hierarchical context map to detect host resources for datatypes
    datatype_context_map = {}
    datatype_to_element = {'HumanName': '.name', 'Address': '.address', 'ContactPoint': '.telecom'}
    
    # first pass: build context map by analyzing element paths
    for did in dataset_order:
        rec = rec_map.get(did, {})
        mappings = rec.get('stu3_mappings', [])
        for m in mappings:
            resource = m.get('resource', '')
            path = m.get('element_path', '')
            if resource not in allowed_extra and path:
                # this is a host resource, check if any datatypes appear below it
                for dtype, suffix in datatype_to_element.items():
                    if suffix in path:
                        # found a datatype usage, store the host context
                        host_prefix = path.split(suffix)[0] + suffix
                        datatype_context_map[dtype] = {'host_resource': resource, 'host_prefix': host_prefix}
    
    # write markdown
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#### Mappings by dataset ID\n\n")
        f.write("This table lists all ZIB2017 dataset elements in original order, including unmapped ones, filtered to in-scope STU3 resources.\n\n")
        f.write("| ID | Dataset name | Resource | FHIR element |\n")
        f.write("|---|---|---|---|\n")
        
        current_context = {}  # track current datatype context
        active_datatype_context = None  # track which datatype context is currently active
        
        for did in dataset_order:
            rec = rec_map.get(did, {})
            indent = '&emsp;' * rec.get('depth', 0)
            dname = indent + rec.get('name', '')
            mappings = rec.get('stu3_mappings', [])
            current_depth = rec.get('depth', 0)
            
            # Apply same deduplication logic as in integration.json
            deduplicated_mappings = []
            datatype_paths = set()
            host_paths = set()
            
            # First pass: collect all host resource paths
            for m in mappings:
                resource = m.get('resource', '')
                path = m.get('element_path', '')
                if resource not in allowed_extra:
                    host_paths.add(path)
            
            # Second pass: add mappings, preferring host over datatype
            for m in mappings:
                resource = m.get('resource', '')
                path = m.get('element_path', '')
                
                if resource in allowed_extra:
                    # This is a datatype mapping
                    if path == resource:  # Root datatype (e.g., "HumanName")
                        # Check if there's a corresponding host mapping
                        has_host_equivalent = False
                        for dtype, suffix in datatype_to_element.items():
                            if dtype == resource:
                                # Look for host paths ending with this suffix
                                for host_path in host_paths:
                                    if host_path.endswith(suffix):
                                        has_host_equivalent = True
                                        break
                                break
                        
                        if not has_host_equivalent:
                            deduplicated_mappings.append(m)
                    else:
                        # Child datatype mapping - always keep these as they're unique
                        deduplicated_mappings.append(m)
                else:
                    # Host resource mapping - always keep
                    deduplicated_mappings.append(m)
            
            # Final exact duplicate removal for markdown: same dataset_id + resource + element_path
            final_mappings = []
            seen_mappings = set()
            for m in deduplicated_mappings:
                # Create a key from the dataset_id (which this record represents) + mapping details
                mapping_key = (
                    did,  # dataset_id for this record
                    m.get('resource', ''),
                    m.get('profile_id', ''),
                    m.get('element_path', ''),
                    m.get('element_id', '')
                )
                if mapping_key not in seen_mappings:
                    seen_mappings.add(mapping_key)
                    final_mappings.append(m)
            
            for m in final_mappings:
                resource = m.get('resource', '')
                path = m.get('element_path', '')
                # only include in-scope and allowed resources
                if resource not in in_scope:
                    continue
                
                # detect if we're entering a new host resource context (reset datatype context)
                if resource not in allowed_extra and path:
                    # this is a host resource, update context for datatypes
                    for dtype, suffix in datatype_to_element.items():
                        if suffix in path:
                            current_context[dtype] = {'host_resource': resource, 'host_path': path, 'depth': current_depth}
                            active_datatype_context = dtype
                            break
                    else:
                        # if no datatype suffix found, we might be exiting datatype context
                        if active_datatype_context and current_depth <= current_context.get(active_datatype_context, {}).get('depth', 999):
                            active_datatype_context = None
                
                # apply datatype context overrides
                if resource in allowed_extra:
                    # find the appropriate host context - try active context first
                    host_info = None
                    if active_datatype_context and active_datatype_context in current_context:
                        host_info = current_context[active_datatype_context]
                    else:
                        # fallback to finding any matching context
                        for dtype, suffix in datatype_to_element.items():
                            if dtype == resource and dtype in current_context:
                                host_info = current_context[dtype]
                                active_datatype_context = dtype
                                break
                    
                    if host_info:
                        host_resource = host_info['host_resource']
                        host_path = host_info['host_path']
                        
                        # override resource column and path
                        if path == resource:  # root datatype (e.g., "HumanName")
                            resource = host_resource  # Use host resource, not full path
                            path = host_path
                        else:  # child of datatype (e.g., "HumanName.given")
                            resource = host_resource
                            # replace datatype prefix with host prefix in path
                            original_datatype = path.split('.')[0]
                            if path.startswith(original_datatype + '.'):
                                path = host_path + path[len(original_datatype):]
                elif active_datatype_context and active_datatype_context in current_context:
                    # we're in a datatype context but this row doesn't have a datatype resource
                    # this might be a child element that should inherit the datatype context
                    host_info = current_context[active_datatype_context]
                    host_resource = host_info['host_resource']
                    host_path = host_info['host_path']
                    
                    # check if this path starts with the active datatype
                    datatype_name = active_datatype_context
                    if path.startswith(datatype_name + '.'):
                        resource = host_resource
                        path = host_path + path[len(datatype_name):]
                
                f.write(f"| {did} | {dname} | {resource} | `{path}` |\n")

def main():
    """
    Main function to orchestrate the entire mapping process.
    """
    print("=== Comprehensive ZIB2017 to STU3 FHIR Mapping Generator ===")
    
    # Configuration
    BASE_DIR = Path(__file__).parent.parent
    
    # Input files and directories
    DATASET_FILE = BASE_DIR / "DS_pzp_dataset_raadplegen_(download_2025-07-29T11_58_18).json"
    STU3_PROFILES_DIR = Path(__file__).parent / "nictiz.fhir.nl.stu3.zib2017#2.2.20" / "package"
    
    # Output files
    OUTPUT_DIR = Path(__file__).parent
    JSON_OUTPUT = OUTPUT_DIR / "comprehensive_zib2017_stu3_mappings.json"
    MARKDOWN_OUTPUT = BASE_DIR.parent / "STU3" / "input" / "includes" / "zib2017_stu3_mappings.md"
    
    # Root concept ID
    ROOT_CONCEPT_ID = "2.16.840.1.113883.2.4.3.11.60.117.2.350"
    
    print(f"Dataset File: {DATASET_FILE}")
    print(f"STU3 Profiles Directory: {STU3_PROFILES_DIR}")
    print(f"JSON Output: {JSON_OUTPUT}")
    print(f"Markdown Output: {MARKDOWN_OUTPUT}")
    print()
    
    # Step 1: Extract STU3 profile mappings
    print("Step 1: Extracting STU3 profile mappings...")
    stu3_mappings = extract_stu3_profile_mappings(str(STU3_PROFILES_DIR))
    
    # Step 2: Extract zib2017 and zib2020 concepts from dataset
    print("\nStep 2: Extracting zib2017 and zib2020 concepts from dataset...")
    zib2017_concepts, zib2020_concepts = extract_dataset_concepts(str(DATASET_FILE))
    
    # Step 3: Parsing R4 mapping markdown for ZIB2020...
    print("\nStep 3: Parsing R4 mapping markdown for ZIB2020...")
    md_file = BASE_DIR.parent / "R4" / "input" / "includes" / "mappings.md"
    r4_mappings = parse_r4_mappings(str(md_file))

    # Step 4: Generating integration JSON...
    print("\nStep 4: Generating integration JSON...")
    integration_file = OUTPUT_DIR / "integration.json"
    generate_integration_json(zib2017_concepts, stu3_mappings, zib2020_concepts, r4_mappings, str(integration_file))

    # Integration complete
    print("\n=== Integration Generation Complete ===")
    print(f"- Integration file: {integration_file}")
    # Step 5: Generate STU3 IG markdown
    print("\nStep 5: Generating STU3 IG markdown table...")
    resources_dir = BASE_DIR.parent / "STU3" / "input" / "resources"
    ig_md = BASE_DIR.parent / "STU3" / "input" / "includes" / "zib2017_stu3_mappings.md"
    generate_ig_markdown(str(integration_file), str(resources_dir), str(ig_md))
    print(f"STU3 IG markdown saved to: {ig_md}")
    return

if __name__ == "__main__":
    main()
