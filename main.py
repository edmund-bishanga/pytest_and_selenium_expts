#!usr/bin/python

# python.exe fullpath: "& C:/Users/mebis/AppData/Local/Microsoft/WindowsApps/python.exe"

import log_gardening

from pprint import pprint

def main():
    print('this is the main program... Ta!')

    # testing log parsing/gardening module.
    logfile = "./sample_service_log.txt"
    # logchunks = []
    # limit = 3
    # while len(logchunks) < limit:
    #     chunk = log_gardening.readlog_chunks(logfile, chunksize=40)
    #     logchunks.append([line for line in chunk])
    # pprint(logchunks)

    # log_gardening.printlog_lines(logfile)

    chunkbytes = 200
    offstart = 50

    head = log_gardening.readlog_head(logfile, numbytes=chunkbytes)
    print('\nHEAD {} bytes of: {}'.format(chunkbytes, logfile))
    pprint(head)

    chunk = log_gardening.readlog_offsetchunk(logfile, offset=offstart, numbytes=chunkbytes)
    print('\nCHUNK {} bytes, offset from {} of {}'.format(
        chunkbytes, offstart, logfile
        )
    )
    pprint(chunk)

    tail = log_gardening.readlog_tail(logfile, numbytes=chunkbytes)
    print('\nTAIL {} bytes of: {}'.format(chunkbytes, logfile))
    pprint(tail)

    print('\n')

    invalid_numbytes = [-100, 100000000000, 0, -1, 0.01]
    for numbytes in invalid_numbytes:
        print('verify: input validation: numbytes: {}'.format(numbytes))
        output = log_gardening.readlog_head(logfile, numbytes)
        print('output: {}'.format(repr(output)))

if __name__ == '__main__':
    main()
