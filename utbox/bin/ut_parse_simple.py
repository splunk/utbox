import re
import sys
import csv

import ut_log
import ut_parse_lib
from six.moves import zip

"""
ut_parse_simple is just a wrapper to python's urlparse so we don't
need to load the TLD lists.
"""

########
# MAIN #
########
logger = ut_log.setup_logger()

header  = ['url', 
	'ut_scheme', 'ut_netloc', 'ut_path', 'ut_params', 'ut_query', 'ut_fragment']

csv_in  = csv.DictReader(sys.stdin) # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header,header)))) # write header

for row in csv_in:
	url = row['url'].strip()

	try:
		res = ut_parse_lib.parse_simple(url)
		row.update( res )
	except Exception as e:
		logger.error("Got error %s on with url %s" % (str(e), url))

	# return row to Splunk
	csv_out.writerow(row)

