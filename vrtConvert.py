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
    sentences = []
    pos_tags = []
    ud_tags = []
    lemmas = []
    sentence = []
    pos_tag = []
    ud_tag = []
    lemma = []

    # Get the header from the first line
    header = lines[0].strip() if lines else None
    
    # Initialize sentence counter
    sentence_counter = 0

    # Loop through the lines
    for line in lines[1:]:
        line = line.strip()
        if line and line != header:
            parts = line.split("\t")
            token, ud, pos, lemma = parts[:4]

            # If the pos tag is 'SENT', it indicates the end of a sentence
            if pos == 'SENT':
                sentences.append((sentence_counter, sentence, ud_tags, ud_tags, lemmas))
                sentence_counter += 1
                # If 10 sentences have been processed, create a Doc and add it to the DocBin
                if sentence_counter == 10:
                    doc = Doc(vocab, words=[word for _, sentence, _, _, _ in sentences for word in sentence],
                            pos=[pos for _, _, _, pos, _ in sentences for pos in pos],
                            tags=[tag for _, _, _, tag, _ in sentences for tag in tag],
                            lemmas=[lemma for _, _, _, _, lemma in sentences for lemma in lemma])
                    doc_bin.add(doc)
                    sentences = []
                    sentence_counter = 0
                sentence = []
                pos_tags = []
                ud_tags = []
                lemmas = []
            else:
                sentence.append(token)
                pos_tags.append(pos)
                ud_tags.append(ud)
                lemmas.append(lemma)

        # If there are any remaining sentences, create a Doc and add it to the DocBin
        if sentences:
            doc = Doc(vocab, words=[word for _, sentence, _, _, _ in sentences for word in sentence],
                    pos=[pos for _, _, _, pos, _ in sentences for pos in pos],
                    tags=[tag for _, _, _, tag, _ in sentences for tag in tag],
                    lemmas=[lemma for _, _, _, _, lemma in sentences for lemma in lemma])
            doc_bin.add(doc)

    # Save the DocBin to disk
    doc_bin.to_disk(output_file_path)

# Main function to parse command line arguments and call the conversion function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a VRT file to a binary .spacy file for SpaCy training.')
    parser.add_argument('vrt_file_path', type=str, help='The path to the input VRT file. This path is relative to the "Corpus" directory.')
    parser.add_argument('spacy_file_path', type=str, nargs='?', default=None, help='The path to the output .spacy file. This path is relative to the "Corpus" directory. If not provided, the output file will have the same base name as the input file with the extension replaced by ".spacy".')
    args = parser.parse_args()


    convert_to_spacy_format(args.vrt_file_path, args.spacy_file_path)