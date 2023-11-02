import json
import os

# Constant metadata
AUTHOR = ""
EMAIL = "your.email@example.com"
LICENSE = "CC BY-SA 4.0"  # Example Creative Commons license

# Variable metadata (these can be modified or passed as arguments)
model_name = "MySpacyModel"
description = "An NLP model for processing text."
version = "1.0.0"

# Construct the metadata dictionary
meta = {
    "name": model_name,
    "version": version,
    "description": description,
    "author": AUTHOR,
    "email": EMAIL,
    "license": LICENSE,
}

# Specify the path for the meta.json file

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
meta_dir = os.path.join(ROOT_DIR, 'Meta')
if not os.path.exists(meta_dir):
    os.mkdir(meta_dir)

output_dir = os.path.join(meta_dir, model_name)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    
meta_path = os.path.join(output_dir, "meta.json")

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Write the metadata to the meta.json file
with open(meta_path, "w", encoding="utf-8") as meta_file:
    json.dump(meta, meta_file, indent=2)

print(f"meta.json file has been created at {meta_path}")


