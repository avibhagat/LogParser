import os
import glob
import argparse
import warnings
from sqlalchemy import exc as sa_exc
from lib.log_parser import LogParser


def lookup_files():
    return glob.glob(os.path.abspath("{0}/../resources/*.log".format(os.path.dirname(__file__))))

# Parse arguments
def get_args():
    parser = argparse.ArgumentParser(description='Parse arguments')
    parser.add_argument('-f', '--file', dest='file', metavar="file", type=str, help='log "file" to parse')
    parser.add_argument('-l', '--list-files', dest='list_available_files', action='store_true', help='show list of files available to parse')

    try:
        args = parser.parse_args()
        if args.list_available_files:
            print("\nPlease choose 1 log file from this list:\n\n{0}\n".format("\n".join(sorted(lookup_files()))))
            parser.exit(0)
        else:
            return args
    except ValueError as e:
        print(e)
        parser.print_help()
        parser.exit(1)

# Start point of code
if __name__ == '__main__':
    args = get_args()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        LogParser.parse_log(args.file)
