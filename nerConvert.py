# Conevert the NER data to the spacy format of the NER model

import os
from bs4 import BeautifulSoup
from spacy.tokens import Doc, Span, DocBin
from spacy.vocab import Vocab

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_DIR = os.path.join(ROOT_DIR, 'Corpus')
NER_DIR = os.path.join(CORPUS_DIR, "SrpELTeC-gold")

ouputName = "SrpELTeC-gold"

outputFIlenameTrain = os.path.join(CORPUS_DIR, ouputName + "-train.spacy")
outputFIlenameDev = os.path.join(CORPUS_DIR, ouputName + "-dev.spacy")

def spacyDocfromFile(name):
    """
    Text example
    <div type="chapter" xml:id="SRP18881_C1">
    <p><s>Užurbala se cela kuća.</s></p>
    <p><s>Jest, do duše, u rod će se, i to u rod, kao u svoju rođenu kuću.</s><s>Ali na selo!</s><s> Pa ostati na selu nekoliko nedelja, kao što namerava gospođa Nata, to je, kao što opet ropta njena kćerka, gospođica</s></p>
    <p><s>Darinka, kad je u varoši „velika beseda“ rad prenosa kostiju Branka Radičevića, „toliko gladnih Misirskih godina“.</s></p>
    <p><s>Pa onda ne može gospođa Nata, da ne ponese štogod sestrinoj deci.</s><s> To će da bude radost od dece, kad im tetka iz varoši razda poklone!</s></p>
    <p><s>– Bože moj, seko. – reći će, do duše, kao i do sad, Kata Nati, – zar to mora biti?</s></p>

    """
    
    textFilename = os.path.join(NER_DIR, name + ".txt")
    
    """
    Annotation example
    T1	ROLE 229 236	gospođa
    T2	PERS 237 241	Nata
    T3	ROLE 283 292	gospođica
    T4	PERS 309 316	Darinka
    """
    annFilename = os.path.join(NER_DIR, name + ".ann")

    vocab = Vocab()
    entities = []

    #open files and read lines
    # Parse the XML file and extract the text
    with open(textFilename, "r", encoding='utf-8') as textFile:
        xml = textFile.read()
        soup = BeautifulSoup(xml, 'html.parser')
        text = soup.get_text()
    words = text.split()
    spaces = [True] * len(words)
    doc = Doc(vocab, words=words, spaces=spaces)

    # Loop over lines of the annotation file
    with open(annFilename, "r", encoding='utf-8') as annFile:
        annLines = annFile.readlines()
        for line in annLines:
            if line.startswith("T"):
                parts = line.strip().split("\t")
                label, start, end = parts[1].split()
                start = int(start)
                end = int(end)
                entity_text = text[start:end]
                entity_span = Span(doc, start, end, label=label)
                entities.append(entity_span)

    doc.ents = entities
    return doc

def spacyDocfromFileTest(name):
    """This function test the spacyDocfromFile function
    it creates Doc and then cheslk if the text is the same as the original text
    and text in ann file matches entities in the doc
    """
    doc = spacyDocfromFile(name)
    
    # Parse the XML file and extract the text
    textFilename = os.path.join(NER_DIR, name + ".txt")
    with open(textFilename, "r", encoding='utf-8') as textFile:
        xml = textFile.read()
        soup = BeautifulSoup(xml, 'html.parser')
        text = soup.get_text()

    # Loop over lines of the annotation file
    annFilename = os.path.join(NER_DIR, name + ".ann")
    with open(annFilename, "r", encoding='utf-8') as annFile:
        annLines = annFile.readlines()
        for line in annLines:
            if line.startswith("T"):
                parts = line.strip().split("\t")
                label, start, end = parts[1].split()
                start = int(start)
                end = int(end)
                entity_text = text[start:end]
                entity_span = Span(doc, start, end, label=label)
                assert entity_text == entity_span.text
                assert entity_span.text == doc[start:end].text


def folder2Spacy(folder):
    """
    folder - folder with text and annotation files
    """
    docs = DocBin()
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            print(os.path.join(folder, filename))
            #check if there ann file
            if os.path.isfile(os.path.join(folder, filename[:-4] + ".ann")):
                docs.add(spacyDocfromFile(filename[:-4]))

def testall():
    """Test all files in NER_DIR, to se if they work with spacyDocfromFile"""
    for filename in os.listdir(NER_DIR):
        if filename.endswith(".txt"):
            print(filename)
        try:
            spacyDocfromFileTest(filename[:-4])
            print("ok")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
def main():
    testall()
if __name__ == "__main__":
    main()