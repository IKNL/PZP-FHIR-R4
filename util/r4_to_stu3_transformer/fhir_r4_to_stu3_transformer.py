#!/usr/bin/env python3
"""
FHIR R4 to STU3 Transformer - Main Orchestrator

This is the main entry point for transforming FHIR resources from R4 to STU3.
It coordinates resource-specific transformers and handles batch processing.

Usage:
    python fhir_r4_to_stu3_transformer.py input_dir output_dir [--resources Consent,Encounter]

Author: AI Assistant
Date: August 26, 2025
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Union
from datetime import datetime
import importlib
import inspect

# Import the base transformer
from transformers.base_transformer import BaseTransformer


class FhirR4ToStu3Transformer:
    """Main orchestrator for FHIR R4 to STU3 transformations."""
    
    def __init__(self):
        """Initialize the transformer with automatically discovered resource transformers."""
        self.transformers = self._discover_transformers()
    
    def _discover_transformers(self) -> Dict[str, BaseTransformer]:
        """Automatically discover all transformer classes in the transformers package."""
        discovered_transformers = {}
        
        # Get the transformers directory path
        transformers_dir = Path(__file__).parent / 'transformers'
        
        # Look for all *_transformer.py files
        for transformer_file in transformers_dir.glob('*_transformer.py'):
            if transformer_file.name == 'base_transformer.py':
                continue
                
            try:
                # Import the module
                module_name = f"transformers.{transformer_file.stem}"
                module = importlib.import_module(module_name)
                
                # Look for classes that inherit from BaseTransformer
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(obj, BaseTransformer) and 
                        obj != BaseTransformer and 
                        not inspect.isabstract(obj)):
                        
                        # Create an instance of the transformer
                        transformer_instance = obj()
                        resource_type = transformer_instance.resource_type
                        discovered_transformers[resource_type] = transformer_instance
                        print(f"Discovered transformer: {resource_type} ({name})")
                        
            except Exception as e:
                print(f"Warning: Could not load transformer from {transformer_file.name}: {e}")
        
        return discovered_transformers
    
    def get_available_resources(self) -> List[str]:
        """Get list of supported resource types."""
        return list(self.transformers.keys())
    
    def transform_resource(self, resource_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Transform a single FHIR resource from R4 to STU3.
        
        Args:
            resource_data: R4 resource as dictionary
            
        Returns:
            STU3 resource as dictionary, or None if resource should be skipped
            
        Raises:
            ValueError: If resource type is not supported (except for skipped types)
        """
        resource_type = resource_data.get('resourceType')
        
        # Skip ValueSet, StructureDefinition, ImplementationGuide, Parameters, and SearchParameter resources - these are never converted
        if resource_type in ['ValueSet', 'StructureDefinition', 'ImplementationGuide', 'Parameters', 'SearchParameter']:
            return None
        
        if resource_type not in self.transformers:
            raise ValueError(f"Unsupported resource type: {resource_type}")
        
        transformer = self.transformers[resource_type]
        return transformer.transform_resource(resource_data)
    
    def transform_file(self, input_file: Path, output_file: Path) -> bool:
        """
        Transform a single FHIR resource file from R4 to STU3.
        
        Args:
            input_file: Path to R4 resource file
            output_file: Path for STU3 output file
            
        Returns:
            True if transformation succeeded, False otherwise, None if skipped
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                r4_resource = json.load(f)
            
            # Check if this is a resource type we should skip
            resource_type = r4_resource.get('resourceType')
            if resource_type in ['ValueSet', 'StructureDefinition', 'ImplementationGuide', 'Parameters', 'SearchParameter']:
                print(f"⏭ Skipping {input_file.name} (type: {resource_type} - not converted)")
                return None
            
            print(f"Transforming: {input_file.name} -> {output_file.name}")
            
            stu3_resource = self.transform_resource(r4_resource)
            
            # If transform_resource returns None, the resource was skipped
            if stu3_resource is None:
                print(f"⏭ Skipped {input_file.name} (resource type not converted)")
                return None
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stu3_resource, f, indent=2, ensure_ascii=False)
                
            print(f"✓ Successfully transformed {input_file.name}")
            return True
            
        except Exception as e:
            print(f"✗ Error transforming {input_file.name}: {e}")
            return False
    
    def transform_directory(self, input_dir: Path, output_dir: Path, 
                          pattern: str = "*.json", 
                          resource_types: Optional[Set[str]] = None) -> None:
        """
        Transform all matching FHIR resource files in a directory.
        
        Args:
            input_dir: Directory containing R4 resources
            output_dir: Directory for STU3 output
            pattern: File pattern to match (default: "*.json")
            resource_types: Set of resource types to transform (None = all supported)
        """
        input_files = list(input_dir.glob(pattern))
        
        if not input_files:
            print(f"No files found matching pattern '{pattern}' in {input_dir}")
            return
        
        print(f"Found {len(input_files)} files to process")
        
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        for input_file in input_files:
            try:
                # Quick check of resource type if filtering is requested
                if resource_types:
                    with open(input_file, 'r', encoding='utf-8') as f:
                        resource_data = json.load(f)
                    
                    resource_type = resource_data.get('resourceType')
                    if resource_type not in resource_types:
                        print(f"⏭ Skipping {input_file.name} (type: {resource_type})")
                        skipped_count += 1
                        continue
                
                # Generate output filename
                output_file = output_dir / f"converted-{input_file.name}"
                
                result = self.transform_file(input_file, output_file)
                if result is True:
                    success_count += 1
                elif result is False:
                    error_count += 1
                elif result is None:
                    skipped_count += 1
                    
            except Exception as e:
                print(f"✗ Failed to process {input_file.name}: {e}")
                error_count += 1
        
        print(f"\nTransformation complete:")
        print(f"  ✓ Success: {success_count}")
        print(f"  ✗ Errors: {error_count}")
        print(f"  ⏭ Skipped: {skipped_count}")


def main():
    """Main entry point."""
    transformer = FhirR4ToStu3Transformer()
    available_resources = transformer.get_available_resources()
    
    parser = argparse.ArgumentParser(
        description="Transform FHIR resources from R4 to STU3",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('input', help="Input file or directory path")
    parser.add_argument('output', help="Output file or directory path")
    parser.add_argument('--pattern', default="*.json", 
                       help="File pattern for directory processing (default: *.json)")
    parser.add_argument('--resources', 
                       help=f"Comma-separated list of resource types to transform.\n"
                            f"Available: {', '.join(available_resources)}\n"
                            f"Default: all supported types")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist")
        sys.exit(1)
    
    # Parse resource types filter
    resource_types = None
    if args.resources:
        resource_types = set(args.resources.split(','))
        # Validate resource types
        invalid_types = resource_types - set(available_resources)
        if invalid_types:
            print(f"Error: Unsupported resource types: {', '.join(invalid_types)}")
            print(f"Available types: {', '.join(available_resources)}")
            sys.exit(1)
    
    try:
        if input_path.is_file():
            if not transformer.transform_file(input_path, output_path):
                sys.exit(1)
        elif input_path.is_dir():
            transformer.transform_directory(input_path, output_path, args.pattern, resource_types)
        else:
            print(f"Error: '{input_path}' is neither a file nor directory")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTransformation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
