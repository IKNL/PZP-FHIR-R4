import os
import json

# --- Configuration ---
# Set the path to the directory containing your FSH-generated JSON files.
# For example, SUSHI's default output directory is often 'fsh-generated'.
INPUT_DIRECTORY = './fsh-generated/resources/'

# --- Script ---
def extract_fhir_data(directory: str) -> tuple[set, set]:
    """
    Finds all unique 'url' and 'baseDefinition' values from JSON files
    in a specified directory.

    Args:
        directory: The path to the directory to search.

    Returns:
        A tuple containing two sets: (unique_urls, unique_base_definitions).
    """
    unique_urls = set()
    unique_base_definitions = set()
    print(f"🔍 Searching for JSON files in: {os.path.abspath(directory)}")

    if not os.path.isdir(directory):
        print(f"❌ Error: Directory not found at '{directory}'")
        return unique_urls, unique_base_definitions

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Check for the 'url' key at the top level
                        if 'url' in data:
                            unique_urls.add(data['url'])
                        # Check for the 'baseDefinition' key (often in StructureDefinition)
                        if 'baseDefinition' in data:
                            unique_base_definitions.add(data['baseDefinition'])
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"⚠️  Could not parse {file_path}: {e}")

    return unique_urls, unique_base_definitions

if __name__ == "__main__":
    urls, base_definitions = extract_fhir_data(INPUT_DIRECTORY)

    # --- Print URL Results ---
    if urls:
        print(f"\n✅ Found {len(urls)} unique URLs:")
        for url in sorted(list(urls)):
            print(f"- {url}")
    else:
        print("\n🤷 No 'url' values found.")

    print("\n" + "="*50 + "\n") # Separator

    # --- Print baseDefinition Results ---
    if base_definitions:
        print(f"✅ Found {len(base_definitions)} unique baseDefinitions:")
        for base_def in sorted(list(base_definitions)):
            print(f"- {base_def}")
    else:
        print("🤷 No 'baseDefinition' values found.")