from prompt_toolkit.history import FileHistory
from prompt_toolkit import prompt as pt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings

from pyfiglet import figlet_format
import cutie
from tqdm import tqdm
import click
import configparser

from CodeComb_Core.query import *
from CodeComb_Core.make_code_corpus import *
from CodeComb_Core.config_shell import *

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


binding = KeyBindings()

@binding.add('c-d')
def _(event):

	log("Ctrl-D . Exiting CodeComb", 'yellow')
	event.app.exit()


def open_editor(name, location):

	path_to_file = os.path.join(location, name)
	log ("Path - {}".format(path_to_file), "yellow")

	config = configparser.ConfigParser()
	config.read(os.path.join(os.environ['HOME'], "codecomb_config.ini"))
	start_editor_cmd = str(config['EDITOR']['startcmd'])
	print (start_editor_cmd)

	## FIXME - adding quotes to allow spaces in path names, can we use subprocess
	os.system( start_editor_cmd + ' "' + path_to_file + '"') 


def get_list_selection(questions, captions=None, selected=None):

	answer = cutie.select(questions, caption_indices=captions, selected_index=0)
	return answer


def clrscr():

	os.system('cls') # Windows
	os.system('clear') # Linux

def run_shell(debug=False):


	## Set debug mode
	if debug:
		logging.basicConfig(level=logging.INFO)
		logging.info("Debug mode on")

	## If the config file not found
	if not os.path.exists(os.path.join(os.environ['HOME'], "codecomb_config.ini")):
		config_shell()


	## User may want to re-index 
	if cutie.prompt_yes_or_no(colored('Index Corpus ? (Use up/down keys) ', 'yellow')):
		#set_format()
		init_corpus()
		input(colored("Press Enter to continue...", "yellow"))

	## Codecomb REPL

	clrscr()
	## Title logo
	log ('CodeComb', 'green', 'slant', True)
	log ('Welcome to CodeComb!!', 'yellow')
	log ('Start searching below...', 'yellow')
	
	user_input = ""
	while user_input != "exit":


		user_input = pt('CCmb>',
			history=FileHistory('history.txt'),
			auto_suggest=AutoSuggestFromHistory(),
			)

		if len(user_input.strip()) > 0 and user_input != "exit":
			results =  get_query_results(user_input, topn=10)
			if results == "error":
				log("Keyword(s) not found!!", 'red')
			else:
				results = eval(results)
				questions_list = [res['name'] + "\t" + res['location'] for res in results]
				questions_list.append('back')
				questions_list = [colored(question, 'green') for question in questions_list]

				## Search results mode
				answer = get_list_selection(questions_list)
				while (answer != (len(questions_list)-1)):
					answer_row = results[answer]
					name, loc = answer_row['name'], answer_row['location']
					logging.info(answer)
					open_editor(name, loc)
					clrscr()
					answer = get_list_selection(questions_list, selected=answer)
		
	
	log("Exiting CodeComb ", "yellow")

	## run_shel END

		



if __name__ == "__main__":
	run_shell()