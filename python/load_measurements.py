"""
load_measurements.py

Whisk data extractor.  Returns traces for each whisker stored in a binary file created when Whisk.exe runs.

Usage:
    load_measurements.py -h | --help
    load_measurements.py --version
    load_measurements.py (-i <input_file> | --input <input_file>) -o <output_file>

Options:
    -h --help                   Show this screen and exit.
    --version                   Display the version and exit.
    -i --input=<input_file>     Specify the file to process.
    -o=<output_file>            Specify the file to create.
"""

import sys

from docopt import docopt
from traj import MeasurementsTable


def main(inputargs):
    from collections import namedtuple
    import pandas as pd

    args = docopt(__doc__, argv=inputargs)
    filepath = args['--input']
    #timedata = namedtuple("timedata", "frameid,mean_degrees,num_whiskers,stderr")
    table = MeasurementsTable(filepath)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] if len(sys.argv) > 1 else ""))
