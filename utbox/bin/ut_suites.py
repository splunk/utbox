import sys
import csv
import json

import ut_presets
import ut_log
from six.moves import zip

########
# MAIN #
########
logger = ut_log.setup_logger()

header = ['word', 'set', 'ut_suites']

csv_in = csv.DictReader(
    sys.stdin)  # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header, header))))  # write header

for row in csv_in:

    try:
        word = row['word'].strip()
        wordset = row['set'].strip()

        counts = ut_presets.suites(word, wordset)

        #row['ut_suites'] = json.dumps({'ut_suites':counts})
        row['ut_suites'] = json.dumps(counts)

    except Exception as e:
        logger.info(str(e))

    # return row to Splunk
    csv_out.writerow(row)
