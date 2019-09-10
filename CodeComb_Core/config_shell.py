import os
from pyfiglet import figlet_format
import cutie
import configparser

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


## Set the format config
def set_format():

	format_opts = {"C++":"cpp", "Python":"py"}
	print(colored('Choose filetype (use up/down keys):', 'yellow'))
	format_keys = list(format_opts.keys())
	answers = cutie.select_multiple(format_keys)

	## Store the config file
	config = configparser.ConfigParser()

	home = os.path.expanduser("~")
	config_file = os.path.join(home, "codecomb_config.ini")
	config.read(config_file)

	config['FORMAT'] = dict((format_keys[ans], format_opts[format_keys[ans]]) \
		 for ans in answers)
	

	with open(config_file, "w") as fmtFile:
		config.write(fmtFile)
		


## Set the Editor

def set_editor():

	editor_opts = {"Vim":"vim ", "VSCode":"start code "}
	print(colored('Choose editor (use up/down keys):', 'yellow'))
	editor_keys = list(editor_opts.keys())
	answer = cutie.select(editor_keys, selected_index=0)

	## Store the config file
	config = configparser.ConfigParser()
	home = os.path.expanduser("~")
	config_file = os.path.join(home, "codecomb_config.ini")
	config.read(config_file)

	config['EDITOR'] = {"startcmd": editor_opts[editor_keys[answer]]}

	with open(config_file, "w") as fmtFile:
		config.write(fmtFile)

def config_shell():

	#os.system("cls")
	#os.system("clear")

	set_format()
	set_editor()

if __name__ == "__main__":

	config_shell()