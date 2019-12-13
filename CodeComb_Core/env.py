import os

 ## FIXME  most of the path variables should come from env vars
PWD = os.getcwd()
OUTPUT_PATH= os.path.join(PWD, "CodeComb_Outputs")
#FORMATS = ['.cpp']
DATA_PATH = os.path.join(PWD, "CodeComb_Data")
DF_FILE = "df_corpus"

DOC_EMB_PATH = os.path.join(OUTPUT_PATH, "doc_emb_" + DF_FILE)
ANN_INDEX_PATH = os.path.join(OUTPUT_PATH, "annoy_" + DF_FILE)
W2V_MODEL_PATH = os.path.join(OUTPUT_PATH, "w2v_model_" + DF_FILE)
DF_PATH = os.path.join(DATA_PATH, DF_FILE)

def ensure_dir(file_path):

	print ("Checking path = {}".format(file_path))
	if not os.path.exists(file_path):
		os.makedirs(file_path)



def init_path():

	ensure_dir(OUTPUT_PATH)
	ensure_dir(DATA_PATH)

