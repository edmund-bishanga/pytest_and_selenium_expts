#!/usr/bin/python
""" Experiments regarding miscellaneous linux cmds: run via python. """

# imports
import argparse as ap
import subprocess
from pprint import pprint

from log_modules.log_gardening import LogGardening

# helper functions
def get_inputs_from_args():
    args = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter)
    args.add_argument(
        '-s', "--search-string", default='Bible',
        help='str: grep search string'
    )
    inputs = args.parse_args()
    print(f'DEBUG: inputs: {inputs}')
    return inputs

def run_subprocess_cmd(cmd_str):
    cmd = cmd_str.split(' ')
    output = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
    print('output dict\n')
    pprint(output, width=30)
    print(f'\noutput: stdout\n: {output.stdout}')
    print(f'\noutput: return_code: {output.returncode}')
    return output


# main
def main():
    # cmd = 'find ~/src/pytest_and_selenium_expts/ -name "py_script*.py" -type f -print0'
    # cmd = ['grep', '-rnIi', 'import', '.']
    inputs = get_inputs_from_args()

    cmd = f'grep -rnIi {inputs.search_string} .'
    output = run_subprocess_cmd(cmd)
    print(f'\noutput: object\n: {output}')

    output = LogGardening.run_shell_cmd(cmd).stdout
    print(f'\noutput: stdout\n: {output}')

if __name__ == "__main__":
    main()
