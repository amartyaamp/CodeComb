import pickle
import pandas as pd
import sys
import os
from nltk.corpus import stopwords
import re
from gensim.models.word2vec import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from termcolor import colored

from CodeComb_Core.env import *

from CodeComb_Core.utils import *
from CodeComb_Core.embeddings import *

## Inputs assumed
## Dataframe which is the original dataset
## W2V MODEL
## Document Embeddings
## Each of above has to be provided separately

	

def get_query_results(query='test',topn=10, debug=False):
	
	## Set debug mode
	if debug:
		logging.basicConfig(level=logging.INFO)
		logging.info("Debug mode on")

	w2v_model = Word2Vec.load(W2V_MODEL_PATH)
	
	try:
		with open(DOC_EMB_PATH, "rb") as fp:
			doc_emb = pickle.load(fp)
	except FileNotFoundError:
		logging.error(colored("Not found - {}. Did you run codecomb init before searching ?".format(DOC_EMB_PATH), 'red'))
		return "{}" ## return empty dictionary
	
	logging.info ("Doc embedding shape - {}".format(doc_emb.shape))
	
	query = process_text(query)
	query_emb = make_doc_vec(query, w2v_model)
	
	## If it is out of vocabs, report to user
	if query_emb.shape[0] <= 0 :
		return "error"
	
	scores = cosine_similarity(doc_emb, query_emb.reshape(1,-1))
	scores = scores.flatten()
	
	## Sort by scores and indices
	sorted_indices = scores.argsort()
	indices = sorted_indices[-topn:][::-1]
	min_indices = sorted_indices[:topn]
	
	print (50*"="+ "MAX AND MIN INDICES AND SCORES" + 50*"=")
	print (indices, min_indices)
	print (scores[indices], scores[min_indices] )
	print (50*"="+ "MAX AND MIN INDICES AND SCORES" + 50*"=")
	
	## From indices above fetch the original document content
	try:
		with open(os.path.join(DATA_PATH, DF_FILE+".pkl"), "rb") as fp:
			df_corpus = pickle.load(fp)
	except FileNotFoundError:
		logging.error(colored("Not found - {}. Did you run codecomb init before searching ?".format(DOC_EMB_PATH), 'red'))
		return "{}" ## return empty dictionary

	results_df = df_corpus.iloc[indices]
	logging.info (df_corpus.columns)
	
	logging.info(results_df.describe())

	return results_df.to_json(orient="records")


if __name__ == "__main__":

	logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)