#!/usr/bin/python
import argparse
import sys
from argparse import RawTextHelpFormatter

from libs.db_sqlite import SqliteDatabase

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-q', '--query', nargs='?')
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        sys.exit(0)

    db = SqliteDatabase()

    row = db.executeOne(args.query)
    if row:
        print(row)
