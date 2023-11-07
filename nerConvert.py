# Conevert the BRAT NER data to the spacy bin format of the NER model

import os
import re
import spacy
from spacy.tokens import DocBin, Doc
from sklearn.model_selection import train_test_split
from spacy.language import Language



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(ROOT_DIR, 'Corpus')
NER_DIR = os.path.join(CORPUS_DIR, "SrpELTeC-gold")


# Define a function to clean XML tags from the text
def clean_xml_tags(text):
    """
    Remove XML tags from the given text.
    """
    clean_text = re.sub(r'<[^>]+>', '', text)  # Remove XML tags
    return clean_text.strip()

# Define the conversion function
def ordered_search_based_brat_to_spacy(txt_path, ann_path):
    """
    Convert BRAT format annotations to SpaCy format by matching order of entities in .ann files with their order in cleaned .txt file.
    """
    with open(txt_path, 'r', encoding="utf-8") as f:
        text = clean_xml_tags(f.read())
    annotations = []
    ann_entities = []
    with open(ann_path, 'r', encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if parts[0].startswith("T"):
                entity_text = ' '.join(parts[4:])
                label = parts[1]
                ann_entities.append((entity_text, label))
    last_found_end = -1
    for entity_text, label in ann_entities:
        start = text.find(entity_text, last_found_end + 1)
        if start != -1:
            end = start + len(entity_text)
            annotations.append((start, end, label))
            last_found_end = end
    return (text, {"entities": annotations})
from spacy.tokens import DocBin, Span

# Define a function to create a DocBin object from the converted data
def create_docbin(data, nlp):
    doc_bin = DocBin()
    for text, annotations in data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)
        doc.ents = ents

        # Split the doc into smaller docs based on punctuation
        split_points = [i for i, token in enumerate(doc) if token.text in {'.', '!', '?'} and doc[min(i + 1, len(doc) - 1)].text != '.']
        start = 0
        for end in split_points:
            block_span = doc[start:end + 1]
            block_doc = nlp.make_doc(block_span.text)
            block_doc.ents = [Span(block_doc, ent.start - start, ent.end - start, label=ent.label_) for ent in block_span.ents if ent.start >= start and ent.end <= end]
            doc_bin.add(block_doc)
            start = end + 1
        block_span = doc[start:]  # Add the last block
        block_doc = nlp.make_doc(block_span.text)
        block_doc.ents = [Span(block_doc, ent.start - start, ent.end - start, label=ent.label_) for ent in block_span.ents if ent.start >= start and ent.end <= len(doc)]
        doc_bin.add(block_doc)
    return doc_bin

@Language.component("set_sentence_boundaries")
def set_sentence_boundaries(doc):
    for token in doc:
        if token.i == 0:
            token.is_sent_start = True
        elif token.text in [".", "!", "?"]:
            if token.i + 1 < len(doc) and not doc[token.i + 1].is_punct:
                doc[token.i + 1].is_sent_start = True
    return doc
# Path to the directory containing BRAT annotated files
dir_path = NER_DIR

# List all .txt files in the directory
all_txt_files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]

# Convert the entire dataset using the order-based approach
all_ordered_converted_data = {}
for txt_file in all_txt_files:
    ann_file = txt_file.replace(".txt", ".ann")
    if ann_file in os.listdir(dir_path):
        converted_data = ordered_search_based_brat_to_spacy(os.path.join(dir_path, txt_file), os.path.join(dir_path, ann_file))
        all_ordered_converted_data[txt_file] = converted_data

# Split the data into training and validation sets
train_files, valid_files = train_test_split(list(all_ordered_converted_data.keys()), test_size=0.2, random_state=42)

train_data = [all_ordered_converted_data[file] for file in train_files]
valid_data = [all_ordered_converted_data[file] for file in valid_files]

# Create a blank Serbian model
nlp = spacy.blank("sr")

# Add the custom component to the pipeline that sets sentence boundaries
nlp.add_pipe("set_sentence_boundaries")

train_doc_bin = create_docbin(train_data, nlp)
valid_doc_bin = create_docbin(valid_data, nlp)

# Save the binary files

ouputName = "SrpELTeC-gold"

train_bin_path = os.path.join(CORPUS_DIR, ouputName + "-train.spacy")
valid_bin_path = os.path.join(CORPUS_DIR, ouputName + "-dev.spacy")

train_doc_bin.to_disk(train_bin_path)
valid_doc_bin.to_disk(valid_bin_path)

print(f"Training data saved to: {train_bin_path}")
print(f"Validation data saved to: {valid_bin_path}")


