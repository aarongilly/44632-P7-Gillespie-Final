# This script processes markdown files in a specified folder,
# extracts specified keys from their YAML frontmatter,
# and saves the extracted data to a CSV in the `data/` folder.

import os
import yaml
import csv

# --- Configuration ---
yaml_key_1 = "title"  
yaml_key_2 = "date"   
yaml_key_2_alt = "created"  
folder_path = "/Users/aaron/Desktop/content"  # intentionally not in the repo
output_csv_file = "data/Content.csv"
# --- End Configuration ---

def extract_frontmatter(file_path, key1, key2):
    """
    Extracts specified keys from the YAML frontmatter of a markdown file.

    Args:
        file_path (str): The path to the markdown file.
        key1 (str): The first YAML key to extract.
        key2 (str): The second YAML key to extract.

    Returns:
        tuple or None: A tuple containing the values of key1 and key2,
                       or None if frontmatter is not found or keys are missing.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) > 2 and lines[0].strip() == '---' and '---' in [line.strip() for line in lines[1:]]:
            frontmatter_end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == '---')
            frontmatter_str = "".join(lines[1:frontmatter_end])
            frontmatter = yaml.safe_load(frontmatter_str)
            value1 = frontmatter.get(key1)
            value2 = frontmatter.get(key2)
            if value2 is None:
                value2 = frontmatter.get(yaml_key_2_alt.lower())
            return (value1, value2)
        else:
            return None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def process_markdown_files(folder, key1, key2, output_file):
    """
    Processes all markdown files in a folder, extracts frontmatter data,
    and saves it to a CSV file.

    Args:
        folder (str): The path to the folder containing markdown files.
        key1 (str): The first YAML key to extract.
        key2 (str): The second YAML key to extract.
        output_file (str): The path to the output CSV file.
    """
    extracted_data = []
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            file_path = os.path.join(folder, filename)
            data = extract_frontmatter(file_path, key1, key2)
            if data:
                extracted_data.append((filename, data[0], data[1]))

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', key1, key2])  # Write header row
        csv_writer.writerows(extracted_data)

    print(f"Extracted data saved to {output_file}")

if __name__ == "__main__":
    process_markdown_files(folder_path, yaml_key_1, yaml_key_2, output_csv_file)