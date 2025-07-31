#!/usr/bin/env python3
"""
Safe cleanup script for unused StructureMap files.
This script moves potentially unused .map files to a backup directory.
"""

import os
import shutil
from pathlib import Path

def main():
    print("🧹 FHIR StructureMap Cleanup Tool")
    print("=" * 50)
    
    # Paths
    maps_dir = Path("r4-to-r3-converter/maps/r4")
    backup_dir = Path("r4-to-r3-converter/maps/unused_backup")
    
    # Files to keep (directly used + dependencies)
    keep_files = {
        # Directly used resource types
        'Communication.map', 'Consent.map', 'Device.map', 'DeviceUseStatement.map',
        'Encounter.map', 'Goal.map', 'ImplementationGuide.map', 'Observation.map',
        'Patient.map', 'Practitioner.map', 'PractitionerRole.map', 'Procedure.map',
        'RelatedPerson.map', 'SearchParameter.map', 'StructureDefinition.map', 'ValueSet.map',
        
        # Base types and dependencies (likely needed)
        'Address.map', 'Age.map', 'Annotation.map', 'Attachment.map', 'BackboneElement.map',
        'CodeableConcept.map', 'Coding.map', 'ContactDetail.map', 'ContactPoint.map',
        'Contributor.map', 'Count.map', 'DataRequirement.map', 'Distance.map',
        'DomainResource.map', 'Dosage.map', 'Duration.map', 'Element.map', 'Expression.map',
        'Extension.map', 'HumanName.map', 'Identifier.map', 'Meta.map', 'Money.map',
        'Narrative.map', 'ParameterDefinition.map', 'Period.map', 'Quantity.map',
        'Range.map', 'Ratio.map', 'Reference.map', 'RelatedArtifact.map', 'Resource.map',
        'SampledData.map', 'TriggerDefinition.map', 'UsageContext.map'
    }
    
    if not maps_dir.exists():
        print(f"❌ Maps directory not found: {maps_dir.absolute()}")
        return
    
    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created backup directory: {backup_dir.absolute()}")
    
    # Find all .map files
    all_map_files = list(maps_dir.glob("*.map"))
    files_to_move = [f for f in all_map_files if f.name not in keep_files]
    
    print(f"📊 Analysis:")
    print(f"   • Total .map files found: {len(all_map_files)}")
    print(f"   • Files to keep: {len(keep_files)}")
    print(f"   • Files to move to backup: {len(files_to_move)}")
    print()
    
    if not files_to_move:
        print("✅ No files to move - all appear to be needed!")
        return
    
    # Show what will be moved
    print("📦 Files to be moved to backup:")
    for i, file_path in enumerate(sorted(files_to_move), 1):
        if i <= 10:  # Show first 10
            print(f"   • {file_path.name}")
        elif i == 11:
            print(f"   • ... and {len(files_to_move) - 10} more files")
            break
    print()
    
    # Confirm action
    response = input("❓ Proceed with moving files to backup? (yes/no): ").lower().strip()
    
    if response not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        return
    
    # Move files
    moved_count = 0
    failed_count = 0
    
    print("🚀 Moving files...")
    for file_path in files_to_move:
        try:
            destination = backup_dir / file_path.name
            shutil.move(str(file_path), str(destination))
            moved_count += 1
            if moved_count <= 5:  # Show first few
                print(f"   ✅ Moved: {file_path.name}")
        except Exception as e:
            print(f"   ❌ Failed to move {file_path.name}: {e}")
            failed_count += 1
    
    if moved_count > 5:
        print(f"   ... and {moved_count - 5} more files moved successfully")
    
    print()
    print("📈 Results:")
    print(f"   • Files moved: {moved_count}")
    print(f"   • Files failed: {failed_count}")
    print(f"   • Backup location: {backup_dir.absolute()}")
    
    # Verification
    remaining_files = len(list(maps_dir.glob("*.map")))
    print(f"   • .map files remaining: {remaining_files}")
    
    print()
    print("🔄 NEXT STEPS:")
    print("1. Test your FHIR converter to ensure it still works correctly")
    print("2. If everything works fine, you can delete the backup directory")
    print("3. If there are issues, restore files from backup:")
    print(f"   mv {backup_dir}/*.map {maps_dir}/")
    print()
    print("✅ Cleanup complete!")

if __name__ == "__main__":
    main()
