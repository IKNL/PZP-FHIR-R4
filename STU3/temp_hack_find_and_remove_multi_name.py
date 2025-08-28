import os
import json

# --- Configuration ---
# Directory containing your FHIR resource files.
# Based on your output, this is set to 'input/resources'.
search_directory = "input/resources"
# ---------------------

print(f"Searching for and updating files in: {search_directory}\n")
updated_files_count = 0
problem_files = []

# List all files in the directory
try:
    filenames = os.listdir(search_directory)
except FileNotFoundError:
    print(f"Error: The directory '{search_directory}' was not found.")
    print("Please check the 'search_directory' variable in the script.")
    exit()

for filename in filenames:
    if filename.endswith(".json"):
        filepath = os.path.join(search_directory, filename)
        try:
            # First, read the entire file
            with open(filepath, 'r', encoding='utf-8') as f:
                resource = json.load(f)

            # Check if the 'name' key exists, is a list, and has more than one item
            if 'name' in resource and isinstance(resource['name'], list) and len(resource['name']) > 1:
                
                original_name_count = len(resource['name'])
                
                # Modify the resource in memory to keep only the first name
                resource['name'] = resource['name'][:1]
                
                # Re-open the file in write mode to save the changes
                with open(filepath, 'w', encoding='utf-8') as f:
                    # Write the modified data back to the file with pretty printing
                    json.dump(resource, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Updated {filename}: Reduced name count from {original_name_count} to 1.")
                updated_files_count += 1

        except Exception as e:
            problem_files.append((filename, str(e)))

# --- Final Summary ---
print("\n--------------------")
print("Script finished.")

if updated_files_count > 0:
    print(f"\nSuccessfully updated {updated_files_count} files.")
else:
    print("\nNo files needed updating.")

if problem_files:
    print("\nCould not process the following files due to errors:")
    for f, err in problem_files:
        print(f"- {f}: {err}")
print("--------------------")