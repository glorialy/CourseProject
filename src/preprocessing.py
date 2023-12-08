import os
import sys

# import argparse
import contractions
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import numpy as np
import pandas as pd
import re
import string

filename = "Womens Clothing E-Commerce Reviews.csv"

# Function to preprocess the text
def preprocessText(text, token = False):
    # expand contractions, to avoid key words like "im" later
    text = contractions.fix(text)
    # Lowercasing
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    if token:
        return tokens # return tokens directly

    # Re-create text from tokens
    text = ' '.join(tokens)
    return text

def readAndProcess(saveFile = False, token = False):
    # read in data
    df = pd.read_csv(filename)
    df.drop(columns=df.columns[0], axis=1, inplace=True)

    # preprocessing
    df['processed_data'] = (df['Review Text'].fillna('') + ' ' + df["Title"].fillna('')).apply(lambda x: preprocessText(x,token))

    # optional: save data
    if saveFile:
        df.to_csv("Processed_reviews.csv")

    return df

if __name__ == "__main__":
    readAndProcess(True)