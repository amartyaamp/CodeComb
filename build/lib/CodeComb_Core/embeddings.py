from gensim.models.word2vec import Word2Vec
from time import time
import logging 
import multiprocessing
import os
import numpy as np
import pickle
from CodeComb_Core.env import *
from CodeComb_Core.utils import *


# Given a corpus (= unsplitted docs) train word embedding model on it
def make_word_embedding(w2v_input):
	cores = multiprocessing.cpu_count() 
	w2v_input = [w2v_input_i.split() for w2v_input_i in w2v_input]

	w2v_model = Word2Vec(min_count=1, size=300, workers=cores-1,window=20)

	t = time()
	w2v_model.build_vocab(w2v_input, progress_per=10000)
	print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

	t = time()
	w2v_model.train(w2v_input, total_examples=w2v_model.corpus_count, epochs=100, report_delay=1)

	print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))
	w2v_model.save(W2V_MODEL_PATH)

	return w2v_model

def test_make_word_embedding():

	corpus = [
		"I am testing word embedding",
		"I don't know what other string to give",
		"So I am testing with whatever I am thinking"
	]

	corpus = [process_text(doc) for doc in corpus]

	emb = make_word_embedding(corpus)
	print (type(emb))
	print (emb['word'].shape)


# given a document - unsplitted, return its embedding after averaging all embeddings of the docs
# model parameter takes a trained word embedding model that acts on every word
# Assumption - text is processed
# Returns ndarray
def make_doc_vec(text, model):
	

	#text = process_text(text) # Process all doc by removing stop words, splitting camel case
	n_terms = 0

	text_embedding = np.array([])
	if len(text) > 0:
		text_terms = text.split()
		try:
			text_embedding = np.zeros(model[text_terms[0]].shape)
			for term in text_terms:
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

def test_make_doc_vec():

	corpus = [
		"I am testing word embedding",
		"I don't know what other string to give",
		"So I am testing with whatever I am thinking"
	]

	emb = Word2Vec.load(W2V_MODEL_PATH)
	doc_vecs = [make_doc_vec(doc, emb) for doc in corpus]

	print (len(doc_vecs))
	for vec in doc_vecs:
		print (len(vec))

# Given a corpus - list of unsplitted texts, and a trained word embedding model, 
# Vectorize all docs to form a corpus vector
# Returns - ndarray
def embed_corpus(corpus, model):
	t = time()
	doc_emb = np.array([make_doc_vec(doc, model) for doc in list(corpus) ])

	print ("Time taken - {}".format(time() -t ))
	with open(DOC_EMB_PATH, "wb") as fp:
		pickle.dump(doc_emb, fp)

	return doc_emb
	
def test_embed_corpus():

	model = Word2Vec.load(W2V_MODEL_PATH)
	corpus = [
		"I am testing word embedding",
		"I don't know what other string to give",
		"So I am testing with whatever I am thinking"
	]

	corpus_vector = embed_corpus(corpus, model)

	print (corpus_vector.shape)


if __name__ == "__main__":

	logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)
	init_path()

	## Uncomment below to test
	# test_make_word_embedding()
	# test_make_doc_vec()
	# test_embed_corpus()