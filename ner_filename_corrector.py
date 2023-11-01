"""
I provider corpus, the .txt files are not named correctly. 
The some .ann files have the 'lat' prefix, but the some corresponding .txt files don't.
Those .txt files should have the 'lat' prefix, but they don't.n
This script renames the .txt files by adding the 'lat' prefix.


"""

import os




ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(ROOT_DIR, 'Corpus')
NER_DIR = os.path.join(CORPUS_DIR, "SrpELTeC-gold")

# All files in the directory
all_files = os.listdir(NER_DIR)

# Identify .txt files without the 'lat' prefix but having a corresponding .ann file with the 'lat' prefix
txt_files_to_rename = [f for f in all_files if not f.startswith("lat") and f.endswith(".txt") and f"lat{f}"[:-4]+".ann" in all_files]

# Rename the identified .txt files by adding the 'lat' prefix
for txt_file in txt_files_to_rename:
    old_path = os.path.join(NER_DIR, txt_file)
    new_path = os.path.join(NER_DIR, "lat" + txt_file)
    os.rename(old_path, new_path)

print("Renaming completed.")
