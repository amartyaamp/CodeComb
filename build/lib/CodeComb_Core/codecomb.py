#!/usr/bin/env python3


import fire

from CodeComb_Core.make_code_corpus import *
from CodeComb_Core.query import *
from CodeComb_Core.shell import *


def run(debug=False):
    if debug:
        logging.basicConfig(level=logging.INFO)
        logging.info("Debug mode on")

    fire.Fire({ 'q': get_query_results, 'init': init_corpus, 'shell': run_shell })

if __name__ == "__main__":
    run()
    