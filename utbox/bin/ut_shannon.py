import sys
import csv
import math
from six.moves import zip
"""
This lookup compute the shannon entropy.
http://en.wikipedia.org/wiki/Entropy_%28information_theory%29
"""


#############
# FUNCTIONS #
#############
def shannon(word):
    entropy = 0.0
    length = len(word)

    occ = {}
    for c in word:
        if not c in occ:
            occ[c] = 0
        occ[c] += 1

    for (k, v) in list(occ.items()):
        p = float(v) / float(length)
        entropy -= p * math.log(p, 2)  # Log base 2

    return entropy


########
# MAIN #
########
header = ['word', 'ut_shannon']

csv_in = csv.DictReader(
    sys.stdin)  # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header, header))))  # write header

for row in csv_in:
    word = row['word'].strip()

    row['ut_shannon'] = shannon(word)

    # return row to Splunk
    csv_out.writerow(row)
