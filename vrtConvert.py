import os
import json
import argparse
from spacy.tokens import Doc, DocBin
from spacy.vocab import Vocab

def convert_to_spacy_format(file_path: str, output_file_path: str) -> None:
    """Converts a VRT file into a binary .spacy file compatible with SpaCy"""
    with open(file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()

    vocab = Vocab()
    doc_bin = DocBin()
    sentence = []
    pos_tags = []
    ud_tags = []
    lemmas = []
    header = lines[0].strip()  # Store the header

    # Inside your loop over the lines of the file
    for line in lines[1:]:  # Skip the header
        line = line.strip()
        if line and line != header:  # If the line is not empty and not a header
            parts = line.split("\t")
            token, ud, pos, lemma = parts[:4]  # Select only the first four values
            if pos == 'SENT':  # If the current token is a sentence delimiter
                # Add the current sentence to the DocBin (if it's not empty)
                if sentence:
                    doc = Doc(vocab, words=sentence, pos=ud_tags, tags=ud_tags, lemmas=lemmas)
                    doc_bin.add(doc)
                # Start a new sentence
                sentence = []
                pos_tags = []
                ud_tags = []
                lemmas = []
            else:
                sentence.append(token)
                pos_tags.append(pos)
                ud_tags.append(ud)
                lemmas.append(lemma)

    # Handle the last sentence if the file doesn't end with a sentence delimiter
    if sentence:
        doc = Doc(vocab, words=sentence, tags=pos_tags, lemmas=lemmas)
        doc_bin.add(doc)


    # Handle the last sentence if the file doesn't end with a sentence delimiter
    if sentence:
        doc = Doc(vocab, words=sentence, tags=ud_tags, lemmas=lemmas)
        doc_bin.add(doc)

    doc_bin.to_disk(output_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a VRT file to a binary .spacy file for SpaCy training.')
    parser.add_argument('vrt_file_path', type=str, help='The path to the input VRT file.')
    parser.add_argument('spacy_file_path', type=str, help='The path to the output .spacy file.')
    args = parser.parse_args()

    convert_to_spacy_format(args.vrt_file_path, args.spacy_file_path)


