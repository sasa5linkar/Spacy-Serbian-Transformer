# Spacy-Serbian-Transformer

This project aims to train tagger for the Serbian language using SpaCwith the use of Large Language Model (LLM)es. The training data is sourced from the Jertehs Corpus.

The project workflow involves several stages, including data preparation, model training, and evaluation. This repository contains scripts and instructions for each of these steps.

## Data Preparation

SrpKor4Tagging Jertehs Corpus data is provided in Verticalized Text (VRT) format. VRT is an annotated text format that includes essential linguistic information about each word, such as its lemma, part of speech, and morphological attributes.

The `vrtConvert.py` script is used for converting the VRT files into a format compatible with SpaCy training. This script processes the VRT file and generates a binary `.spacy` file. The `.spacy` file comprises the words, lemmas, POS tags, and UD tags from the VRT file.

Here's how to use the script:

```bash
python vrtConvert.py path_to_your_vrt_file.vr```t output.spacy
```

## Baseline 

Model2- is trained in SrpKor4Tagging using basic token to vector, tagger, lemmatizer.

Besides being useful, it will be comaration, to languge modeal traied using LLM

