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

 -Model2: is trained in SrpKor4Tagging corpus using basic token to vector, tagger, lemmatizer.

Besides being useful, it will be comparation, to languge modeal traied using LLM

The next pipeline uses transformer-based models to provide tokenization, part-of-speech tagging, and lemmatization. Specifically:

- Model 3: `bert-base-multilingual-uncased` is a transformer-based model that is pre-trained on a large corpus of text in multiple languages. It is part of the BERT family of models and is designed to handle text in multiple languages without the need for language-specific models. 

- Model 4: `Classla Bertic` is a transformer-based model that is trained on Serbian, Croatian, and other similar languages. It is part of the `classla` library, which provides a suite of natural language processing tools for Slavic languages. 

- Model 5: `Berticovo` is a transformer-based model that is specifically trained on Serbian. It is part of the `bertic` library, which provides a suite of natural language processing tools for Serbian. 

Note that due to space constraints, only models 2 and 3 are uploaded on Git, but both the base configuration and configuration files are set for training. If anyone wants the files, they can contact me over Git and I will be happy to share them.

The next step in the pipeline is to add named entity recognition (NER) to the pipeline, but this is still a work in progress.