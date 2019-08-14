## Making the code corpus
## This involves
## Hit every directory and read every .cpp files
## Form a corpus of words without special symbols
## Tokenize Camel case and Hungarian to split out new words
## Any word below 3 letter is not Allowed

import re
import os
import pandas as pd
import sys
import pickle

OUTPUT_PATH= "C:\\Users\\amchau\\Desktop\\CodeComb_Outputs"

def handle_camel_case(text):

	text_underscored_camelcase = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'_\1', text) # Camelcase split
	
	text_result = []
	for t in text_underscored_camelcase.split():

		if "_" in t:
			camelcases = t.split("_")
			text_result.append("".join(camelcases))
			text_result.append("".join(camelcases))
		else:
			text_result.append(t)
	
	return " ".join(text_result)

	

def prepare_file(filename, location):

	with open(os.path.join(location,filename), "r", encoding = 'latin-1') as fp:
		file_data = fp.read()
	
	file_data = re.sub(r'[^a-zA-Z]+', ' ', file_data)
	file_data = handle_camel_case(file_data) # Camelcase split
	file_data = " ".join([s  for s in file_data.split() if len(s) > 2 and s.isalpha()])

	file_info = dict()
	file_info["body"] = file_data
	file_info["name"] = filename
	file_info["location"] = " ".join(location.split("/"))

	return file_info


def read_all_cpp_files(file_metas):

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

def test_read_all_cpp_files():
	path = "."

	print ("TEST READ ALL CPP FILES")
	files = get_cpp_files_name_location(path)
	file_contents = read_all_cpp_files(files)
	print (file_contents)



def test_prepare_file():

	location = "."
	filename = "sample_cpp.cpp"

	file_info = prepare_file(filename, location)
	print ("TEST PREPARE FILE")
	print (file_info)

	return

def get_cpp_files_name_location(path):

	files = []

	# r=root, d=directories, f = files
	for r, _, f in os.walk(path):
		for file in f:
			if '.cpp' in file:
				info = {}
				info['name'] = file
				info['location'] = r
				files.append(info)
	
	return files

def test_get_cpp_files_name_location():

	print ("TEST GET CPP FILES NAME LOCATION")
	path = "."
	file_infos = get_cpp_files_name_location(path)
	print (file_infos)
	print (len(file_infos))


def get_all_files_currentdir(pickle_file):
	PATH = "."

	files = get_cpp_files_name_location(PATH)
	file_contents = read_all_cpp_files(files)
	df_corpus = pd.DataFrame(file_contents)

	print (df_corpus[['body', 'location']].head())
	print (df_corpus.columns)
	print (df_corpus.describe())

	with open(os.path.join(OUTPUT_PATH, pickle_file),"wb") as fp:
		pickle.dump(df_corpus, fp)



def test_all_files_currentdir():
	print ("TEST ALL FILES CURRENTDIR")
	get_all_files_currentdir("tmp.pkl")


def run():

	if (len(sys.argv) < 2):
		print ("Usage : python make_code_corpus.py df_file")
		sys.exit(2)
	
	df_file = sys.argv[1]
	get_all_files_currentdir(df_file)
	

if __name__ == "__main__":

	## Uncomment below to test
	# test_prepare_file()
	# test_get_cpp_files_name_location()
	# test_read_all_cpp_files()
	# test_all_files_currentdir()
	run()
