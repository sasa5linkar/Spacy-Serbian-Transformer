import spacy
from spacy.tokens import DocBin
import os

# Define the directory paths and output name
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(ROOT_DIR, 'Corpus')
outputName = "SrpELTeC-gold"  # Replace with your output name

# Load a blank model (replace "en_core_web_sm" with your model if needed)
nlp = spacy.blank("sr")

# Load the DocBin from file
train_bin_path = os.path.join(CORPUS_DIR, outputName + "-train.spacy")
doc_bin = DocBin().from_disk(train_bin_path)

# Get a list of Doc objects
docs = list(doc_bin.get_docs(nlp.vocab))

# Print the text and entities of the first few docs
for doc in docs[:5]:  # Adjust the number as needed
    print("Text:", doc.text)
    for ent in doc.ents:
        print("Entity:", ent.text, ent.start_char, ent.end_char, ent.label_)
    print("\n")