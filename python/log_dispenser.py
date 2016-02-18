#!/usr/bin/python
import sys
from classes.LogFile import LogFile


def main():
    test = LogFile()

    if len(sys.argv) == 6:
        start = test.get_start()
        end = test.get_end(start)
        print test.create_file(start, end)
    elif len(sys.argv) == 4:
        print test.get_dates_zip()
    elif len(sys.argv) == 2:
        print test.get_simple_log()
    else:
        print "Something wrong with arguments passed in "
        sys.exit(-1)

if __name__ == '__main__':
    main()
