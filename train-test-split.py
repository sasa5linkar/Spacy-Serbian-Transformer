from spacy.tokens import DocBin
from spacy.vocab import Vocab
import random
import os

CORPUS_PATH = os.path.join("", "Corpus")

def split_data(data, train_ratio=0.7, dev_ratio=0.15):
    """
    This function splits the data into training, development, and test sets.
    """
    random.shuffle(data)
    train_point = int(len(data) * train_ratio)
    dev_point = int(len(data) * (train_ratio + dev_ratio))
    return data[:train_point], data[train_point:dev_point], data[dev_point:]

def save_data(data, path):
    """
    This function saves the data to a .spacy file at the provided path.
    """
    DocBin(docs=data).to_disk(path)

def load_and_preview_data(path, vocab=Vocab()):
    """
    This function loads the data from a .spacy file and returns a preview of the first document.
    """
    doc_bin = DocBin().from_disk(path)
    docs = list(doc_bin.get_docs(vocab))
    preview = " ".join([token.text for token in docs[0]])
    return preview

def main(name):
    """
    This function loads the original data, splits it into training, development, and test sets,
    saves each set as a separate .spacy file, and prints a preview of the first document in each set.
    """
    # Load the original data
    origin_path = os.path.join(CORPUS_PATH, f"{name}.spacy")
    doc_bin = DocBin().from_disk(origin_path)
    # Create a Vocab instance
    vocab = Vocab()

    # Use the same Vocab instance to get docs
    data = list(doc_bin.get_docs(vocab))

    # Split the data into training, development, and test sets
    train_data, dev_data, test_data = split_data(data)

    # Save the training, development, and test data as separate .spacy files
    train_path = os.path.join(CORPUS_PATH, f"{name}-train.spacy")
    dev_path = os.path.join(CORPUS_PATH, f"{name}-dev.spacy")
    test_path = os.path.join(CORPUS_PATH, f"{name}-test.spacy")
    save_data(train_data, train_path)
    save_data(dev_data, dev_path)
    save_data(test_data, test_path)

    # Load the .spacy files and print a preview of the first document in each set
    train_preview = load_and_preview_data(train_path)
    dev_preview = load_and_preview_data(dev_path)
    test_preview = load_and_preview_data(test_path)
    print(f"Train preview: {train_preview}")
    print(f"Dev preview: {dev_preview}")
    print(f"Test preview: {test_preview}")

if __name__ == "__main__":
    main("SrpELTeC-gold")

