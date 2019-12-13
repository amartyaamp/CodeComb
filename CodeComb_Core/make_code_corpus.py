## Making the code corpus
## This involves
## Hit every directory and read every supported files
## Form a corpus of words without special symbols
## Tokenize Camel case and Hungarian to split out new words
## Any word below 3 letter is not Allowed

import os
import pandas as pd
import sys
import pickle
import configparser

from CodeComb_Core.embeddings import *
from CodeComb_Core.utils import *
from CodeComb_Core.env import *


## Read the file and pack it into file_info dict
def prepare_file(filename, location):

	with open(os.path.join(location,filename), "r", encoding = 'latin-1') as fp:
		file_data = fp.read()
	
	#file_data = process_text(file_data)

	file_info = dict()
	file_info["body"] = file_data
	file_info["name"] = filename
	file_info["location"] = location
	file_info["ext"] = filename[filename.rfind('.')+1:]

	return file_info


# From file metas  read all file content of supported formats
def read_all_supported_files(file_metas):

	print ("READING FILES")
	print ("Total files-{}".format(len(file_metas)))
	file_contents = []

	for i, info in enumerate(file_metas):
		path_to_file = info['location']
		file_name = info['name']

		if ((i % 100) == 0):
			print ("Processed {} files".format(i-1))

		content = prepare_file(file_name, path_to_file)
		file_contents.append(content)
	
	return file_contents

def test_read_all_supported_files():
	path = os.getcwd()

	print ("TEST READ ALL CPP FILES")
	files = get_supported_files_name_location(path)
	file_contents = read_all_supported_files(files)
	print (file_contents)



def test_prepare_file():

	location = os.getcwd()
	filename = "sample_cpp.cpp"

	file_info = prepare_file(filename, location)
	print ("TEST PREPARE FILE")
	print (file_info)

	return

## Load Formats from the config file

def load_format():
	config = configparser.ConfigParser()
	config.read(os.path.join(os.path.expanduser("~"), "codecomb_config.ini"))
	fmts = list(config['FORMAT'].values())

	formats_list = ["."+fmt  for fmt in fmts]
	return formats_list

# Get Metas
def get_supported_files_name_location(path):

	files = []

	# r=root, d=directories, f = files
	for r, _, f in os.walk(path):
		for file in f:
			formats = load_format()
			for fmt in formats:
				if file.endswith(fmt):
					info = {}
					info['name'] = file
					info['location'] = r
					files.append(info)
	
	return files

def test_get_supported_files_name_location():

	print ("TEST GET SUPPORTED FILES NAME LOCATION")
	path = "."
	file_infos = get_supported_files_name_location(path)
	print (file_infos)
	print (len(file_infos))

## Recursively reads all supported file names from current locations 
## And forms a DF
def get_all_files_currentdir(pickle_file):
	PATH = os.getcwd()

	files = get_supported_files_name_location(PATH)
	file_contents = read_all_supported_files(files)
	df_corpus = pd.DataFrame(file_contents)

	logging.info (df_corpus[['body', 'location']].head())
	logging.info (df_corpus.columns)
	logging.info (df_corpus.describe())

	with open(os.path.join(DATA_PATH, pickle_file),"wb") as fp:
		pickle.dump(df_corpus, fp)


def test_all_files_currentdir():
	print ("TEST ALL FILES CURRENTDIR")
	get_all_files_currentdir("tmp.pkl")


## Given a df file source, it makes word-embeddings and document vectors out of it
def embed_df_corpus(df_file):
	print (20*"=" + "Initializing Corpus embeddings" + 20*"=")

	with open(os.path.join(DATA_PATH, df_file), "rb") as dfPickled:
		dfCorpus = pickle.load(dfPickled)
	
	dfCorpus["corpus"] = dfCorpus["name"] + " " + dfCorpus["location"] + " " + dfCorpus["body"]
	X = dfCorpus["corpus"].tolist()
	X_cleaned = [process_text(X_i) for X_i in X]

	## Create word embedding
	emb = make_word_embedding(X_cleaned)

	## Create Document vectors of entire corpus
	#embed_corpus(X_cleaned, emb)
	make_annoy_index(X_cleaned, emb)

	print (20*"=" + "Corpus Embeddings done" + 20*"=")
	
def test_embed_df_corpus():

	df_file = "df_corpus.pkl"
	embed_df_corpus(df_file)


## Initializes / Indexes the corpus in two steps
## Gets all metas and body of the corpus
def init_corpus(df_file="df_corpus.pkl", debug=False):

	## Set debug mode
	if debug:
		logging.basicConfig(level=logging.INFO)
		logging.info("Debug mode on")

	## Ensure all output dirs in place
	init_path()


	print (20*"#" + "prepping the corpus" + 20*"#")
	t = time()
	get_all_files_currentdir(df_file)
	embed_df_corpus(df_file)
	print('Time taken to init: {} mins'.format(round((time() - t) / 60, 2)))
	

if __name__ == "__main__":

	## Uncomment below to test
	# test_prepare_file()
	# test_get_cpp_files_name_location()
	# test_read_all_cpp_files()
	# test_all_files_currentdir()
	#test_embed_df_corpus()

	logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

	init_corpus()
