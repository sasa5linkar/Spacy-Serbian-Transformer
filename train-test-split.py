from spacy.tokens import DocBin
from spacy.vocab import Vocab
import random
import os

CORPUS_PATH = os.path.join("", "Corpus")

# Define the split_data function
def split_data(data, split_ratio=0.8):
    random.shuffle(data)
    split_point = int(len(data) * split_ratio)
    return data[:split_point], data[split_point:]

# Load the original data
name = "SrpKor4Tagging"
origin_path = os.path.join(CORPUS_PATH, f"{name}.spacy")
doc_bin = DocBin().from_disk(origin_path)
data = list(doc_bin.get_docs(Vocab()))

# Split the data into training and development sets
train_data, dev_data = split_data(data)
train_path = os.path.join(CORPUS_PATH, f"{name}-train.spacy")
dev_path = os.path.join(CORPUS_PATH, f"{name}-dev.spacy")
# Save the training and development data as separate .spacy files
DocBin(docs=train_data).to_disk(train_path)
DocBin(docs=dev_data).to_disk(dev_path)

# Load the .spacy files to verify that they were saved correctly
train_bin = DocBin().from_disk(train_path)
dev_bin = DocBin().from_disk(dev_path)

train_docs = list(train_bin.get_docs(Vocab()))
dev_docs = list(dev_bin.get_docs(Vocab()))

# Check the first few words of the first document in each set
train_preview = " ".join([token.text for token in train_docs[0]])
dev_preview = " ".join([token.text for token in dev_docs[0]])

train_preview, dev_preview


