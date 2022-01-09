#!/usr/bin/python
""" Experiments regarding miscellaneous linux cmds: run via python. """

# imports
import subprocess
from pprint import pprint

from log_modules.log_gardening import LogGardening

# helper functions
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
    cmd = 'grep -rnIi import .'
    output = run_subprocess_cmd(cmd)

    output = LogGardening.run_shell_cmd(cmd)
    print(f'\noutput: stdout\n: {output}')

if __name__ == "__main__":
    main()
