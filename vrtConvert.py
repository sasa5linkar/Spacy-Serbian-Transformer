import os
import argparse
from spacy.tokens import Doc, DocBin
from spacy.vocab import Vocab

# Define the path to the corpus directory
CORPUS_PATH = os.path.join("", "Corpus")

# Function to convert a VRT file to a binary .spacy file for SpaCy training
def convert_to_spacy_format(file_path: str, output_file_path: str = None) -> None:
    """
    Function to convert a VRT file to a binary .spacy file for SpaCy training.

    Args:
        file_path (str): The path to the input VRT file. This path is relative to the "Corpus" directory.
        output_file_path (str, optional): The path to the output .spacy file. This path is relative to the "Corpus" directory.
            If not provided, the output file will have the same base name as the input file with the extension replaced by ".spacy".
    """
    # Join the corpus path with the file path
    file_path = os.path.join(CORPUS_PATH, file_path)
    
    # If output file path is not provided, use the same base name as the input file
    if output_file_path is None:
        base_name = os.path.splitext(file_path)[0]
        output_file_path = base_name + ".spacy"
    else:
        output_file_path = os.path.join(CORPUS_PATH, output_file_path)

    # Open the file and read the lines
    with open(file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()

    # Initialize vocab and DocBin
    vocab = Vocab()
    doc_bin = DocBin()

    # Initialize lists to store sentences, pos tags, ud tags and lemmas

    pos_tags = []
    ud_tags = []
    lemmas = []
    sentence = []
    lemma = []

    # Get the header from the first line
    header = lines[0].strip() if lines else None
    
    # Initialize sentence counter
    sentence_counter = 0

    # Loop through the lines
    for line in lines[1:]:
        line = line.strip()
        if line and line != header:  # If the line is not empty and not a header
            parts = line.split("\t")
            token, ud, pos, lemma = parts[:4]  # Select only the first four values
            if pos == 'SENT':  # If the current token is a sentence delimiter
                # Add the current sentence to the DocBin (if it's not empty)
                if sentence:
                    sent_starts = [True] + [False] * (len(sentence) - 1)
                    doc = Doc(vocab, words=sentence, pos=ud_tags, tags=ud_tags, lemmas=lemmas, sent_starts=sent_starts)
                    doc_bin.add(doc)
                sentence = []
                pos_tags = []
                ud_tags = []
                lemmas = []
            else:
                sentence.append(token)
                pos_tags.append(pos)
                ud_tags.append(ud)
                lemmas.append(lemma)

    # # Handle the last sentence if the file doesn't end with a sentence delimiter
    # if sentence:
    #     doc = Doc(vocab, words=sentence, tags=pos_tags, lemmas=lemmas)
    #     doc_bin.add(doc)


    # Handle the last sentence if the file doesn't end with a sentence delimiter
    if sentence:
        sent_starts = [True] + [False] * (len(sentence) - 1)
        doc = Doc(vocab, words=sentence, pos=ud_tags, tags=ud_tags, lemmas=lemmas, sent_starts=sent_starts)
        doc_bin.add(doc)


    # Initialize a new DocBin to hold the concatenated documents
    new_doc_bin = DocBin()

    # Initialize an empty list to hold the group of documents
    group = []

    # Initialize a counter to keep track of the number of documents
    counter = 0

    # Iterate over the documents in the DocBin
    for doc in doc_bin.get_docs(vocab):
        # Add the document to the group
        group.append(doc)
        
        # Increment the counter
        counter += 1
        
        # If the counter reaches 10, concatenate the documents and add to the new DocBin
        if counter == 10:
            # Concatenate the documents in the group
            concatenated = Doc.from_docs(group)
            
            # Add the concatenated document to the new DocBin
            new_doc_bin.add(concatenated)
            
            # Reset the group and counter
            group = []
            counter = 0

    # Handle any remaining documents
    if counter > 0:
        # Concatenate the remaining documents in the group
        concatenated = Doc.from_docs(group)
        
        # Add the concatenated document to the new DocBin
        new_doc_bin.add(concatenated)

    # Save the new DocBin to disk
    new_doc_bin.to_disk(output_file_path)

# Main function to parse command line arguments and call the conversion function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a VRT file to a binary .spacy file for SpaCy training.')
    parser.add_argument('vrt_file_path', type=str, help='The path to the input VRT file. This path is relative to the "Corpus" directory.')
    parser.add_argument('spacy_file_path', type=str, nargs='?', default=None, help='The path to the output .spacy file. This path is relative to the "Corpus" directory. If not provided, the output file will have the same base name as the input file with the extension replaced by ".spacy".')
    args = parser.parse_args()


    convert_to_spacy_format(args.vrt_file_path, args.spacy_file_path)