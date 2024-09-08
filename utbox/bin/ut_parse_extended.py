import sys
import csv
import logging

import ut_log
import ut_parse_lib
from six.moves import zip

########
# MAIN #
########
try:
    logger = ut_log.setup_logger()
except:
    logger = logging.getLogger(__name__)
    logger.warning("Failed to instantiate logger, falling back to default logger")

header = [
    'url',
    'list',
    'ut_scheme',
    'ut_netloc',
    'ut_path',
    'ut_params',
    'ut_query',
    'ut_fragment',
    'ut_domain',
    'ut_tld',
    'ut_domain_without_tld',
    'ut_subdomain',
    'ut_port',
    'ut_subdomain_parts',
    'ut_subdomain_count',
]

csv_in = csv.DictReader(
    sys.stdin)  # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header, header))))  # write header

TLDList = None

for row in csv_in:
    try:
        url = row['url'].strip()
    except Exception as e:
        logger.error("Did not find url field in row, continuing with next row")
        continue

    if TLDList == None:
        try:
            l = "pouet"
            if 'list' in row:
                l = row['list'].strip().lower()
            TLDList = ut_parse_lib.loadTLDFile(l)
        except Exception as e:
            logger.error("Failed to load TLD list with error: %s" % str(e))

    try:
        res = ut_parse_lib.parse_extended(url, TLDList)
        row.update(res)
    except Exception as e:
        logger.error("Got error %s on with url %s" % (str(e), url))

    # return row to Splunk
    csv_out.writerow(row)
