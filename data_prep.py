import pandas as pd
import numpy as np
import matplotlib as plt
import plotly
import spacy
import nltk
import re
import string
import srbai
import json

import os,glob
import pandas as pd

from pathlib import Path
from typing import List
from srbai.Alati.Transliterator import transliterate_cir2lat

def load_data(path: Path) -> List[str]:
    texts = []

    for filename in glob.glob(os.path.join(path, "*.tt")):
        data = []
        
        with open(filename, 'r') as f:
            for line in f:
               
                if line.startswith('<s>') or line.startswith('</s>'):
                    continue
                
                columns = line.strip().split('\t')
                
                ## za menjanje pos ovde, ako vise pos onda ovo zakomentarisati, korstiti sintaksu ispod
                if len(columns) == 3 and columns[1] == 'NOUN': 
                # if len(columns) == 3 and columns[1] in ['NOUN', 'VERB']:
                    data.append(columns[2])
        
        text = ' '.join(data)
        
        texts.append(text)
    
    return texts

def get_stopwords(stopwords_path: List[str], stops_add_path: List[str], save_stopwords_path, transliterate_func=transliterate_cir2lat) -> List[str]:
    def convert_path_to_list(load_path):
        with open(load_path, 'r', encoding="utf-8") as f:
            words = f.read()
            return list(words.split('\n'))
    
    stopwords = convert_path_to_list(stopwords_path)
    stopwords_add = convert_path_to_list(stops_add_path)
    
    stopwords.extend(stopwords_add)
    
    if transliterate_func:
        stopwords = [transliterate_func(word) for word in stopwords]
    
    with open(save_stopwords_path, 'w', encoding="utf-8") as file:
        data_to_write = '\n'.join(stopwords)
        file.write(data_to_write)
    
    return stopwords

def clean_text(text, save_path): #stops
    cleaned_text = []
    for t in text:
        # removing extra whitespace and special characters
        t = t.replace("\n\n", " ").replace('\n', ' ').replace('—', '').replace('„', '').replace('“','').replace('«', '').replace('»', '').replace('@card@', '').replace('’', '').replace('–', '').replace('\"', '')
        t = t.translate(str.maketrans(" ", " ", string.punctuation)) # removing puntuation
        # t = re.sub(r'\b\w{1,2}\b', '', t)
        # t = " ".join([word for word in t.split() if word.lower() not in stops])
        t = t.strip() 
        t = re.sub(" +", " ", t) 
        if t:
    
          cleaned_text.append(t)
    
    return cleaned_text



def get_filenames(path):
    filenames = []

    for filepath in glob.glob(os.path.join(path, "*.tt")):
        filename = os.path.basename(filepath)
        
        name_part = filename.split('.xml-out.tt')[0]
        
        filenames.append(name_part)
    
    return filenames


def save_strings_as_jsonl(strings, folder_path):
  
    os.makedirs(folder_path, exist_ok=True)

    for i, text in enumerate(strings):
        data = {"text": text}
        
        file_name = f"file_{i}.jsonl"
        file_path = os.path.join(folder_path, file_name)
        
    
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def save_strings_as_jsonl(strings, folder_path, filenames):
    # Ensure the output folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Check if the number of strings matches the number of filenames
    if len(strings) != len(filenames):
        raise ValueError("The number of strings does not match the number of filenames.")

    for i, text in enumerate(strings):
        data = {"text": text}
        
        file_name = f"{filenames[i]}.jsonl"
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ in "__main__":
    data_path = "data_lema_pos"
    stopwords_path = "stopwordsSRB.txt"
    stops_add_path = "stops_extra.txt"
    save_path = "final_stopwords_lat.txt"
    cleaned_texts_path = "cleaned_texts/"

    texts = load_data(data_path)
    stopwords = get_stopwords(stopwords_path, stops_add_path, save_path)
    cleaned_texts = clean_text(texts, cleaned_texts_path)
    print(len(cleaned_texts))

    filenames = get_filenames(data_path)
    save_strings_as_jsonl(cleaned_texts, cleaned_texts_path, filenames)
