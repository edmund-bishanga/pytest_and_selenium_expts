#!/usr/bin/python

import log_gardening

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner
from test_classes.ParkRun import ParkRun
from pprint import pprint

def main():
    print('this is the main program... Ta!')
    # Space = Park("Eynesbury", temperature=15, precipitation=2, surface="mixed", inclination=2)
    # print('Park: Venue: {}'.format(Space.venue))
    # print('Park: Temp: {}'.format(Space.temperature))

    # Runner = ParkRunner("Edmund M Bishanga", age=36, height=1.75, weight=67, resilience=2, consistency=2, restHR=45, maxHR=200)
    # print("{}: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    # print("{}: BMI: {}".format(Runner.name, Runner.get_bmi()))

    # Race = ParkRun(park=Space, runner=Runner, distance_km=10, time_min=40)
    # print("{}: 5km_time_min: {}".format(Runner.name, Race.get_t_parkrun_min()))
    # print("{}: V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    # normalised_effort = 100 * round((Race.get_vo2max_current() / Runner.get_vo2max_potential()), 2)
    # print("{}: Normalised Effort: {}%".format(Runner.name, normalised_effort))

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

if __name__ == '__main__':
    main()