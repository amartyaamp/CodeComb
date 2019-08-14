import pickle
import pandas as pd
import sys
import os
from nltk.corpus import stopwords
import re
from gensim.models.word2vec import Word2Vec
from time import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

## Inputs assumed
## Dataframe which is the original dataset
## W2V MODEL
## Document Embeddings
## Each of above has to be provided separately

DATA_PATH = "C:\\Users\\amchau\\Desktop\\CodeComb_Outputs" ## FIXME should come from an environment var
DF_FILE = "df_outlook2" ## FIXME should come from env var

DOC_EMB_NAME = os.path.join(DATA_PATH, "doc_emb") + "_" + DF_FILE
W2V_MODEL_NAME = os.path.join(DATA_PATH, "w2v_model") + "_" + DF_FILE

f = lambda x : re.sub(r'[^a-zA-Z]+', ' ', x)
g = lambda x : x.strip()

def processInput(text):
    
    ## remove non alphas, strip then remove uppercases
    text = g(f(text))
    stop_words = stopwords.words('english')
    text = " ".join([t for t in text.split() if t not in stop_words])
    text = " ".join([t.lower() for t in text.split() ])
    return text

def handle_camel_case(text, keepOriginal=False):

    if keepOriginal:
        
        text_underscored_camelcase = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'_\1', text) # Camelcase split

        text_result = []
        for t in text_underscored_camelcase.split():

            if "_" in t:
                camelcases = t.split("_")
                text_result.append("".join(camelcases))
                text_result.append("".join(camelcases))
            else:
                text_result.append(t)
    
        res_text = " ".join(text_result)
    else:
        res_text = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', text) # Camelcase split
    
    return res_text


def process_text(text):
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    text = handle_camel_case(text, DF_FILE != "df_outlook") # Camelcase split
    text = processInput(text)
    text = " ".join([s.lower()  for s in text.split() if len(s) > 2 and s.isalpha()])
    
    return text.strip()

def make_doc_vec(text, model):
    
    text = process_text(text)
    n_terms = 0

    if len(text) > 0:
        text_terms = text.split()
        text_embedding = np.zeros(model[text_terms[0]].shape)
        for term in text_terms:
            try:
                #print (term)
                emb = model[term]
                text_embedding += emb
                n_terms += 1
            except KeyError:
                pass
    
    if n_terms > 0 :
        print ("total terms - "+str(n_terms))
        text_embedding /= n_terms
    
    return text_embedding
    
def get_query_results(query,topn):
    
    w2v_model = Word2Vec.load(W2V_MODEL_NAME)
    
    with open(DOC_EMB_NAME, "rb") as fp:
        doc_emb = pickle.load(fp)
    
    print ("Doc embedding shape - {}".format(doc_emb.shape))
    
    query_emb = make_doc_vec(query, w2v_model)
    scores = cosine_similarity(doc_emb, query_emb.reshape(1,-1))
    scores = scores.flatten()
    topn = 20
    
    ## Sort by scores and indices
    sorted_indices = scores.argsort()
    indices = sorted_indices[-topn:][::-1]
    min_indices = sorted_indices[:topn]
    
    print (50*"="+ "MAX AND MIN INDICES AND SCORES" + 50*"=")
    print (indices, min_indices)
    print (scores[indices], scores[min_indices] )
    print (50*"="+ "MAX AND MIN INDICES AND SCORES" + 50*"=")
    
    ## From indices above fetch the original document content
    with open(os.path.join(DATA_PATH, DF_FILE), "rb") as fp:
        df_corpus = pickle.load(fp)

    results_df = df_corpus.iloc[indices]
    
    print(results_df.describe())

    return results_df.to_json(orient="records")


if __name__ == "__main__":
	get_query_results('test', 20)


