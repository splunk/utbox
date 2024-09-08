import os
import re
import sys
import csv
from io import open
from six.moves import range
from six.moves import zip

def ngramsplit(word, length):
    """
	ngramsplit("google", 2) => {'go':1, 'oo':1, 'og':1, 'gl':1, 'le':1}
	"""
    grams = {}

    for i in range(0, len(word) - length + 1):
        g = word[i:i + length]

        if not g in grams:
            grams[g] = 0
        grams[g] += 1
    return grams


def loadFile(f_name, gram_size=2):
    f_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f_name)

    LIST = {}
    entries = 0

    f_in = open(f_path, "r")
    line = f_in.readline()
    while line:
        line = line.lower().strip()
        grams = ngramsplit(line, gram_size)
        entries += 1

        for g in grams:
            if not g in LIST:
                LIST[g] = 0

            LIST[g] += grams[g]

        line = f_in.readline()
    f_in.close()

    return (entries, LIST)


def bayescore(word, n_good, set_good, n_bad, set_bad, gram_size=2):
    """
	Compute the naive bayesian score - Probability that the domain is a bad one knowing it's ngrams.
	Actually limited to 2-grams for now
	"""

    score = 0.0
    P_Total = 1.0
    P_TotalInv = 1.0

    grams = ngramsplit(word, gram_size)
    for g in grams:

        if not g in set_bad or not g in set_good:
            continue

        # probability that the gram X appears in bad domains
        P_G_B = (100.0 / n_bad) * set_bad[g]

        # probability that the gram X appears in good domains
        P_G_G = (100.0 / n_good) * set_good[g]

        # probability that a domain is a bad one, knowing that the gram X is in it;
        P = P_G_B / (P_G_B + P_G_G)

        P_Total *= P
        P_TotalInv *= (1 - P)

    return (P_Total / (P_Total + P_TotalInv))


########
# MAIN #
########
(n_good, set_good) = loadFile("bayesian_good.dic")
(n_bad, set_bad) = loadFile("bayesian_bad.dic")

header = ['word', 'ut_bayesian']

csv_in = csv.DictReader(
    sys.stdin)  # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header, header))))  # write header

for row in csv_in:
    word = row['word'].lower().strip()

    row['ut_bayesian'] = bayescore(word, n_good, set_good, n_bad, set_bad)

    # return row to Splunk
    csv_out.writerow(row)
