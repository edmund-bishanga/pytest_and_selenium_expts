#!/usr/bin/python

"""
log gardening module:
Often SysTest Experiments generate logs
These need to be post-processed and analysed
This module aims to have re-usable methods for doing just that...
"""

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=use-dict-literal
# pylint: disable=use-list-literal

# primary APIs
# + read_chunks
# + read_lines
# + readlog_tail
# + readlog_head
# + search_printlines
# + search_countlines
# + logsize_numlines
# + logsize_numbytes
# + logdate_created
# + logdate_lastmodified

import subprocess
from pprint import pprint


MEM_LIMIT = 10000
DEF_LOGFILE = "./logs/sample_service_log.txt"
DEF_ENCODING = 'UTF-8'


class LogGardening():
    """ For Reading and Analysing Log Files """

    def __init__(self, logfile_path=None):
        self.logfile_path = logfile_path

    def get_logfile_path(self):
        if not self.logfile_path:
            self.logfile_path = DEF_LOGFILE
        return self.logfile_path

    def set_logfile_path(self, new_log_file):
        self.logfile_path = new_log_file
        return self.logfile_path

    def readlog_chunks(self, chunksize=1024):
        with open(self.logfile_path, 'r', encoding=DEF_ENCODING) as f:
            while True:
                # read in memory-efficient chunks
                chunk = f.read(chunksize)
                if not chunk:
                    break
                yield chunk

    def printlog_lines(self):
        assert isinstance(self.logfile_path, str)
        with open(self.logfile_path, 'r', encoding=DEF_ENCODING) as logfile:
            file_generator = (line.strip() for line in logfile)
            for line in file_generator:
                if line and line[0].isalnum():
                    print(line)

    def printlog_lines_head(self, num_lines=10):
        assert isinstance(self.logfile_path, str)
        with open(self.logfile_path, 'r', encoding=DEF_ENCODING) as logfile:
            file_generator = (line.strip() for line in logfile)
            line_num = 0
            for line in file_generator:
                line_num += 1
                print(f'{line_num}: {line}')
                if line_num == num_lines:
                    break

    def readlog_tail(self, numbytes=100):
        help_txt = "numbytes: expects: +ve integer"
        assert isinstance(numbytes, int) and numbytes > 0, help_txt
        with open(self.logfile_path, 'rb') as f:
            tail = f.read(f.seek(-numbytes, 2))
        return tail

    def readlog_head(self, numbytes=100):
        help_txt = "numbytes: expects: +ve int"
        assert isinstance(numbytes, int) and numbytes > 0, help_txt
        head = ''
        try:
            with open(self.logfile_path, 'rb') as f:
                # head = f.read(numbytes) if numbytes < MEM_LIMIT else None
                head = f.read(numbytes)
        except FileNotFoundError as io_err:
            print(io_err)
        except MemoryError as mem_err:
            pprint(mem_err)
            err_details = f'numbytes: {numbytes} >> mem_limit: {MEM_LIMIT}'
            print('MemoryError: ', err_details)
        else:
            if head is None:
                print('Error: empty output, probably a MemoryError')
        return head

    def readlog_offsetchunk(self, offset=0, numbytes=100):
        assert isinstance(offset, int) and isinstance(numbytes, int)
        assert numbytes > 0, "numbytes: expects: +ve int"
        with open(self.logfile_path, 'rb') as f:
            f.seek(offset)
            chunk = f.read(f.seek(numbytes, 1))
        return chunk

    @staticmethod
    def run_shell_cmd(cmd):
        """ Return exit_code and stdout or raise exception. """
        if isinstance(cmd, str):
            cmd = cmd.split(' ')
        proc = dict()
        try:
            proc = subprocess.run(
                cmd, capture_output=True,
                shell=True, check=True, text=True
            )
            # proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            # output = proc.stdout.read()
        except subprocess.CalledProcessError as Err:
            print('\nDEBUG: Err')
            pprint(Err)
            raise
        finally:
            print('\nDEBUG: proc')
            pprint(proc)
            if proc and proc.returncode != 0:
                print(f'\nDEBUG: stderr: {proc.stderr}')
        return proc.stdout if proc else ''

    # grep for specific sub-string & print first 10 lines showing that
    def grep_lines_with_sub_string(self, sub_string, num_lines=10, logfile=None):
        log = logfile if logfile else self.logfile_path
        n_grepped_lines = list()
        # grep for substring in specified log, get lines
        util = 'grep'
        params = '-iIn'
        cmd = f'{util} {params} {sub_string} {log}'
        print(f'cmd: {cmd}')
        output = self.run_shell_cmd(cmd)
        # only return first N lines
        output_lines = str(output).strip('b').strip("'").strip().split('\n')
        for i in range(num_lines):
            if i < len(output_lines):
                n_grepped_lines.append(output_lines[i])
        return n_grepped_lines
