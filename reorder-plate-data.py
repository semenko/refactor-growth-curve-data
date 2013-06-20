#!/usr/bin/env python

"""
Reformat 96<->384 plate reader data for processing.

Input: .csv files from OD measurements of 384-well plates **containing 96-wells of data** (each .csv is one timepoint)
    That is, robotically sample 96-well plates onto 384-well plates (skipping every other row) for volume/OD reasons.

Output: Re-ordered data with one well per row, and one timepoint per column.


Example: ./reorder-plate-data.py time_0.csv time_1.csv time_2.csv
Results: STDOUT prints space-separated data.
"""

import csv
import string
import sys

try:
    assert(len(sys.argv[1:]))
except AssertionError:
    print("ERROR: List input .csv files on the command line.")
    sys.exit()


# Store plate data
stored_plates = {}
# Loop over input filenames
for (plate_number, filename) in enumerate(sys.argv[1:]):
    with open(filename, 'U') as csvfile:
        reader = csv.reader(csvfile)
        for (row_number, row) in enumerate(reader):
            if row[0] == '':
                # We must be on the header row
                assert(len(row) == 26)
                stored_plates[plate_number] = {}
            else:
                stored_plates[plate_number][row_number] = row[1:]


COL_MAX = 12  # We ignore the last 12 columns on the 384-well plate.
ROW_MAX = 16
PLATE_MAX = len(stored_plates)

# Loop over
for row in range(1, ROW_MAX + 1)[::2]:
    for col in range(0, COL_MAX):
        print(string.uppercase[row//2] + str(col + 1)),
        for plate in range(PLATE_MAX - 1):
            print(stored_plates[plate][row][col]),
        print ""
