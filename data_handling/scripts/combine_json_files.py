# Combines Genre JSON Files so that they can be more easily added to tables
import json
import os

def concatenate_jsons(source_directory, output_file):
    combined_data = []
    file_count = 0  # Counter to track number of files processed

    # Iterate through each file in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(source_directory, filename)
            print(f"Processing {file_path}...")  # Debug: output current file path
            with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
                try:
                    data = json.load(file)
                    combined_data.append(data)  # Append the data from each JSON file to the list
                    file_count += 1
                except json.JSONDecodeError as e:
                    print(f"Error reading {filename}: {e}. File may be empty or not valid JSON.")
                except UnicodeDecodeError as e:
                    print(f"Unicode decode error in {filename}: {e}")

    print(f"Processed {file_count} files.")  # Debug: output number of files processed

    # Write the combined list of all data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:  # Use UTF-8 encoding for output file
        json.dump(combined_data, file, indent=4)

    print(f"All JSON files from {source_directory} have been concatenated into {output_file}")

# Example usage
source_dir = '../raw_data/Genres-JSON/'  # Directory containing the JSON files
output_json = '../raw_data/Genres-JSON/_genres.json'    # Name of the output file
concatenate_jsons(source_dir, output_json)
