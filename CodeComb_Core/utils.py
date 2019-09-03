import re
from nltk.corpus import stopwords
import logging

def processInput(text):
	
	## remove non alphas, strip then remove uppercases
	f = lambda x : re.sub(r'[^a-zA-Z]+', ' ', x)
	g = lambda x : x.strip()
	text = g(f(text))
	stop_words = stopwords.words('english')
	text = " ".join([t for t in text.split() if t not in stop_words])
	text = " ".join([s.lower()  for s in text.split() if len(s) > 2 and s.isalpha()])

	return text

def handle_camel_case(text, keepOriginal=False):

	logging.info ("camelcase input="+text)
	if keepOriginal:
		
		text_underscored_camelcase = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r'_\1', text) # Camelcase split

		text_result = []
		for t in text_underscored_camelcase.split():

			if "_" in t:
				camelcases = t.split("_")
				camelcases = " ".join(camelcases).split() ## Removes empty strings from above step - [" ", "abc"] --> ["abc"]
				text_result.append("".join(camelcases))

				if len(camelcases) > 1 :  ## Now that there are no empty strings, if len > 1 then we have multiple words
					text_result.append(" ".join(camelcases))
			else:
				text_result.append(t)
	
		res_text = " ".join(text_result)
	else:
		res_text = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', text) # Camelcase split
	
	logging.info ("Camel case removed -"+ res_text)
	return res_text


def process_text(text):
	f = lambda x : re.sub(r'[^a-zA-Z]+', ' ', x) # basic non alpha pruning, FIXME - should  this be removed?
	text = f(text)

	text = handle_camel_case(text, True) # Camelcase split
	text = processInput(text)

	logging.info ("Processed text - {}".format(text))
	
	return text.strip()