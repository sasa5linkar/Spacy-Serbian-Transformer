# Spacy-Serbian-Transformer

This project aims to train tagger for the Serbian language using SpaCwith the use of Large Language Model (LLM)es. The training data is sourced from the Jertehs Corpus.

The project workflow involves several stages, including data preparation, model training, and evaluation. This repository contains scripts and instructions for each of these steps.

## Data Preparation

SrpKor4Tagging Jerteh's Corpus data is provided in Verticalized Text (VRT) format. VRT is an annotated text format that includes essential linguistic information about each word, such as its lemma, part of speech, and morphological attributes.

There is two other corpuses in Coprus folder:
    UD_Serbian-SET (Universal Dependencies) from [here] (https://github.com/UniversalDependencies/UD_Serbian-SET)    
This is on conllu format, and and it was converted to VRT format using standard spacy convereter. 

The next is SrpELTeC-gold, also from Jerteh. It set of old Serbian novela, and in BRAT format. In in folder SrpELTeC-gold, there is script for converting BRAT to spacy. 

The `vrtConvert.py` script is used for converting the VRT files into a format compatible with SpaCy training. This script processes the VRT file and generates a binary `.spacy` file. The `.spacy` file comprises the words, lemmas, POS tags, and UD tags from the VRT file.



Here's how to use the script:

```bash
python vrtConvert.py path_to_your_vrt_file.vrt output.spacy
```

Note that root path for the VRT file is set in the script. It is Corpus folder in this git. 

The script will generate a `.spacy` file in the same directory as the VRT file. This file can be used for training the SpaCy model.

Next 

There is two other corpuses in Coprus folder:
    UD_Serbian-SET (Universal Dependencies) from [here] (https://github.com/UniversalDependencies/UD_Serbian-SET)    

There was problem with naming convention in SrpELTeC-gold corpus, so the script `ner_filename_corrector.py` was writtent o rename files.

The convesion to spacy format is done using `nerConvert.py` script. Note that scrptit uses spacy pipeline, since SrpELTeC-gold only has NER tags, and not others. If onl;y NER si tot betraing using blank is enough.

And finally script `train-test-split.py` is used to spearte spacy files in train, eval and test sets. 

Here is how to use it:

```bash
python train-test-split. name_of_your_spacy_file.spacy
```    
It assumed that file is in Corpus folder, and it will generate train, eval and test files in the same folder, adding -train -dev, -test, just before .spacy .


## Baseline 

 -Model2: is trained in SrpKor4Tagging corpus using basic token to vector, tagger, lemmatizer.

Besides being useful, it will be comparation, to languge modeal traied using LLM

The next pipeline uses transformer-based models to provide tokenization, part-of-speech tagging, and lemmatization. Specifically:

- Model 3: `bert-base-multilingual-uncased` is a transformer-based model that is pre-trained on a large corpus of text in multiple languages. It is part of the BERT family of models and is designed to handle text in multiple languages without the need for language-specific models. 

- Model 4: `Classla Bertic` is a transformer-based model that is trained on Serbian, Croatian, and other similar languages. It is part of the `classla` library, which provides a suite of natural language processing tools for Slavic languages. 

- Model 5: `Berticovo` is a transformer-based model that is specifically trained on Serbian. It is part of the `bertic` library, which provides a suite of natural language processing tools for Serbian. 

Model 6-

Note that due to space constraints, only models 2 and 3 are uploaded on Git, but both the base configuration and configuration files are set for training. If anyone wants the files, they can contact me over Git and I will be happy to share them.

The next step in the pipeline is to add named entity recognition (NER) to the pipeline, but this is still a work in progress.

Model 5 was converted to package and uploaded to Hugging Face model hub. It can be found [here](https://huggingface.co/Tanor/sr_Spacy_Serbian_Model_SrpKor4Tagging_BERTICOVO).

it can drecly intasteled using pip:

```bash
!pip install https://huggingface.co/Tanor/sr_Spacy_Serbian_Model_SrpKor4Tagging_BERTICOVO/resolve/main/sr_Spacy_Serbian_Model_SrpKor4Tagging_BERTICOVO-any-py3-none-any.whl

```
and it can be used in spacy pipeline:

```bash
# Using spacy.load().
import spacy
nlp = spacy.load("sr_Spacy_Serbian_Model_SrpKor4Tagging_BERTICOVO")

# Importing as module.
import sr_Spacy_Serbian_Model_SrpKor4Tagging_BERTICOVO
nlp = sr_Spacy_Serbian_Model_SrpKor4Tagging_BERTICOVO.load()

```

