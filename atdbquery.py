# ATDBquery: query ATDB for survey status (ARTS or imaging)
# V.A. Moss 16/01/2019 (vmoss.astro@gmail.com)

__author__ = "V.A. Moss"
__date__ = "$16-jan-2019 17:00:00$"
__version__ = "0.1"

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from modules.functions import *
import time

# Function version
def atdbquery(obs_mode,failures,transient):
	"""
    The main program to be run.
    :return:
    """

    # Time the total process length
	start = time.time()

	# Send the query
	obs_list = query_database(obs_mode,failures,transient)
	print('Total number of results returned for %s: %s' % (obs_mode.upper(),len(obs_list)))

	# End timing
	end = time.time()
	total = end-start
	print('Total time to run query: %.2f sec' % (total))

	return obs_list


# System call version
if __name__ == '__main__':

	# Parse the relevant arguments
	parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
	parser.add_argument('-m', '--mode',
			default='imaging',
			help='Specify whether mode is imaging/sc1/sc4 (default: %(default)s)')
	parser.add_argument('-f', '--failures',
			default=False,
			action='store_true',
			help='Specify whether to include failures as well (default: %(default)s)')
	parser.add_argument('-t', '--transient',
			default=False,
			action='store_true',
			help='Specify whether to check only for current valid observations which have not been ingested (default: %(default)s)')

	# Parse the arguments above
	args = parser.parse_args()

	# Send the query
	obs_list = atdbquery(args.mode,args.failures,args.transient)
	print(obs_list)