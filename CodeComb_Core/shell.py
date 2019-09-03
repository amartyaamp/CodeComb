from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt as pt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion

from pyfiglet import figlet_format
import cutie
from tqdm import tqdm
import click
from CodeComb_Core.query import *
from CodeComb_Core.make_code_corpus import *


## Either colorama or termcolor
try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
	from termcolor import colored
except ImportError:
	colored = None


## Stylish text output
def log(string, color, font="slant", figlet=False):
	if colored:
		if not figlet:
			print(colored(string, color))
		else:
			print(colored(figlet_format(
				string, font=font), color))
	else:
		print(string)


def open_editor(name, location):

	path_to_file = os.path.join(location, name)
	print ("Path - {}".format(path_to_file))
	os.system('start code '+'"' + path_to_file + '"')


def get_list_selection(questions, captions=None, selected=None):

	answer = cutie.select(questions, caption_indices=captions, selected_index=0)
	return answer


def run_shell():

	os.system('cls')
	os.system('clear')
	## Title logo
	log ('CodeComb', 'green', 'slant', True)
	log ('Welcome to CodeComb!!', 'yellow')
	log ('Start searching below...', 'yellow')

	## 
	if cutie.prompt_yes_or_no(colored('Index Corpus ? ', 'yellow')):
		init_corpus()

	## Codecomb REPL
	user_input = ""
	while user_input != "exit":


		user_input = pt('CCmb>',
			history=FileHistory('history.txt'),
			auto_suggest=AutoSuggestFromHistory(),
			)

		click.echo_via_pager(user_input)
		#ask_question(questions, result_style)
		if user_input != "exit":
			results =  get_query_results(user_input, topn=10)
			results = eval(results)
			questions_list = [res['name'] + "\t" + res['location'] for res in results]
			questions_list.append('back')

			## Search results mode
			answer = get_list_selection(questions_list)
			while (answer != (len(questions_list)-1)):
				answer_row = results[answer]
				name, loc = answer_row['name'], answer_row['location']
				logging.info(answer)
				open_editor(name, loc)
				answer = get_list_selection(questions_list, selected=answer)
			#testTQDM()

		



if __name__ == "__main__":
	run_shell()