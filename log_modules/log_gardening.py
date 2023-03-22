#!/usr/bin/python

"""
A Module for Post-Processing of SysTest Logs.

Most SysTest Experiments generate logs
These need to be post-processed and analysed
This module aims to have re-usable methods for doing just that...

Primary APIs: Proposed
+ read_chunks
+ read_lines
+ readlog_tail
+ readlog_head
+ search_printlines
+ search_countlines
+ logsize_numlines
+ logsize_numbytes
+ logdate_created
+ logdate_lastmodified
"""

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=use-dict-literal
# pylint: disable=use-list-literal

import os
import subprocess
from pprint import pprint

MEM_LIMIT = 10000
DEF_LOGFILE = os.path.join(os.curdir, '..', 'logs', 'sample_service_log.txt')
DEF_ENCODING = 'UTF-8'

class LogGardening():
    """ For Reading and Post-Processing/Analysing Log Files """

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
        """Yields chunks of log file, in specified byte sizes.

        Args:
            chunksize (int, optional): size in bytes of chunk.
                                       Defaults to 1024.

        Yields:
            str: chunks of log, in specified byte size.
        """
        with open(self.logfile_path, 'r', encoding=DEF_ENCODING) as f:
            while True:
                # read in memory-efficient chunks
                chunk = f.read(chunksize)
                if not chunk:
                    break
                yield chunk

    def printlog_lines(self):
        """Output to stdout, entire log."""
        assert isinstance(self.logfile_path, str)
        with open(self.logfile_path, 'r', encoding=DEF_ENCODING) as logfile:
            file_generator = (line.strip() for line in logfile)
            for line in file_generator:
                if line and line[0].isalnum():
                    print(line)

    def printlog_lines_head(self, num_lines=10):
        """Prints to stdout, top n lines of self.logfile_path.

        Args:
            num_lines (int, optional): number of lines. Defaults to 10.
        """
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
        """Parse log file, output bottom n bytes.

        Args:
            numbytes (int, optional): n bytes. Defaults to 100.

        Returns:
            str: bottom n bytes of the log file.
        """
        help_txt = 'numbytes: expects: +ve integer'
        assert isinstance(numbytes, int) and numbytes > 0, help_txt
        with open(self.logfile_path, 'rb') as f:
            tail = f.read(f.seek(-numbytes, 2))
        return tail

    def readlog_head(self, numbytes=100):
        """Parses log and returns top selection.

        Args:
            numbytes (int, optional): number of bytes to output

        Returns:
            str: selection of log file, first n bytes.
        """
        help_txt = 'numbytes: expects: +ve int'
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
        """Parses log file, from an offset starting point, n bytes.

        Args:
            offset (int, optional): starting point, line number.
                                    Defaults to 0.
            numbytes (int, optional): number of bytes to output.
                                      Defaults to 100.

        Returns:
            str: selection of log file, described by the args above.
        """
        assert isinstance(offset, int) and isinstance(numbytes, int)
        assert numbytes > 0, 'numbytes: expects: +ve int'
        with open(self.logfile_path, 'rb') as f:
            f.seek(offset)
            chunk = f.read(numbytes)
        return chunk

    @staticmethod
    def run_shell_cmd(cmd):
        """Runs cmd in os.shell, returns stdout

        Args:
            cmd (str): shell command to run

        Returns:
            dict: result: containing stdout, stderr, returncode.
        
        Raises:
            CalledProcessError: cmd response failure details
        """
        # """ Return exit_code and stdout or raise exception. """
        if isinstance(cmd, str):
            cmd = cmd.split(' ')
        result = dict()
        try:
            result = subprocess.run(
                cmd, capture_output=True,
                shell=True, check=True, text=True
            )
            # result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            # output = result.stdout.read()
        except subprocess.CalledProcessError as Err:
            print('\nDEBUG: Err')
            pprint(Err)
            raise
        finally:
            print('\nDEBUG: result')
            pprint(result)
            if result and result.returncode != 0:
                print(f'\nDEBUG: stderr: {result.stderr}')
        return result

    def grep_lines_with_sub_string(self, sub_str, num_lines=10, logfile=None):
        """Searches for specified pattern, prints request number of instances.

        Args:
            sub_str (str): search pattern/string
            num_lines (int, optional): number of lines to output.
                                       Defaults to 10.
            logfile (str, optional): path to log file.
                                     Defaults to None.

        Returns:
            str: corresponding n lines with search string.
        """
        n_grepped_lines = list()
        log = logfile if logfile else self.logfile_path
        # grep for substring in specified log, get lines
        util = 'grep'
        params = '-iIn'
        cmd = f'{util} {params} {sub_str} {log}'
        print(f'cmd: {cmd}')
        output = str(self.run_shell_cmd(cmd).stdout)
        # only return first N lines
        if output:
            output_lines = output.strip('b').strip("'").strip().split('\n')
            for i in range(num_lines):
                if i < len(output_lines):
                    n_grepped_lines.append(output_lines[i])
        return n_grepped_lines

    def collect_n_log_chunks(self, n_chunks=3, chunk_bsize=100):
        """Gets a finite number of sized log chunks from self.logfile_path

        Args:
            n_chunks (int, optional): number of chunks to return.
                                      Defaults to 3.
            chunk_bsize (int, optional): size of each chunk: bytes.
                                         Defaults to 100.

        Returns:
            list: collection of n chunks of log text
        """
        logchunks = []
        i_chunks = 0
        chunk_bsize = 100
        while i_chunks < n_chunks:
            new_offset = i_chunks * chunk_bsize
            chunk = self.readlog_offsetchunk(
                offset=new_offset,
                numbytes=chunk_bsize
            )
            print(f'\nDEBUG: chunk: {list(chunk)}')
            logchunks.append(list(chunk))
            i_chunks += 1
        self.printlog_lines_head(num_lines=12)
        return logchunks

if __name__ == '__main__':
    logfile = os.path.join(os.curdir, '..', 'logs', 'geckodriver.log')
    log_file_analyser = LogGardening(logfile_path=logfile)
    log_chunks = log_file_analyser.collect_n_log_chunks(n_chunks=3)
    print(f'log_chunks: \n{log_chunks}')
