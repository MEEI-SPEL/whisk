#! /usr/bin/env python
"""
load_whiskers.py

Whisk data extractor.  Returns traces for each whisker stored in a binary file created when Whisk.exe runs.

Usage:
    load_whiskers.py -h | --help
    load_whiskers.py --version
    load_whiskers.py (-i <input_file> | --input <input_file>) -o <output_file>

Options:
    -h --help                   Show this screen and exit.
    --version                   Display the version and exit.
    -i --input=<input_file>     Specify the file to process.
    -o=<output_file>            Specify the file to create.
"""

from docopt import docopt
import sys
from trace import Load_Whiskers
import numpy as np


def main(inputargs):
    from collections import namedtuple
    import pandas as pd

    args = docopt(__doc__, argv=inputargs)
    filepath = args['--input']  # """C:\\Users\\VoyseyG\\Downloads\\movie.whiskers"""
    timedata = namedtuple("timedata", "frameid,mean_degrees,num_whiskers,stderr")
    res = Load_Whiskers(filepath)

    retval = []
    for frame, segments in res.iteritems():
        degrees = []
        for segind, seg in segments.iteritems():
            thisx = seg.x
            thisy = seg.y
            degrees.append(compute_vector_angle(thisx, thisy))
        mean_degrees = np.mean(np.abs(degrees))
        stderr = np.std(degrees) / np.sqrt(len(degrees))
        retval.append(timedata(frameid=int(frame),
                               mean_degrees=mean_degrees,
                               num_whiskers=len(degrees),
                               stderr=stderr))
    retval = pd.DataFrame(retval).sort_values('frameid')
    retval = retval.set_index('frameid')
    retval['mean_degrees'] = retval['mean_degrees'].replace(np.nan, 0, regex=True)
    retval.to_csv(args['-o'])

    return 0



def compute_vector_angle(x, y):
    """
    Estimate the vector angle given by the parametric vectors x and y relative to the euclidian axis.
    :param x:
    :param y:
    :return:
    """
    # normalize
    x_end = x[-1] - x[0]
    y_end = y[-1] - y[0]
    try:
        retval = np.arctan(y_end / x_end)
        return np.degrees(retval)
    except ZeroDivisionError:
        return np.nan


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] if len(sys.argv) > 1 else ""))