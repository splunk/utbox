import os
import re
import sys
import csv
from io import open
from six.moves import range
from six.moves import zip
"""
Module that compute a ratio between the word length and the length of it's known composing words
Use the wordlist meaning.dic (one word per line). This list is loaded once per batch of 50,000
events (Splunk Internal behavior on custom search commands).

microsoft = micro + soft (2 words in meaning.dic) => ratio = 1
microxyze = micro + xyze (1 word in meaning.dic)  => ratio = 5/9 (len('micro')/len('microsoft'))

This is a very naive algorithm, this should be improved.
"""


def loadWordlist():
    f_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          "meaning.dic")

    f_in = open(f_path, "r")
    WORDLIST = {}

    line = f_in.readline()
    while line:
        line = line.lower().strip()
        le = len(line)

        # do we have a words of the same size already?
        if not le in WORDLIST:
            WORDLIST[le] = []

        # check required in case of duplicated words.
        if not line in WORDLIST[le]:
            WORDLIST[le].append(re.compile(line))

        line = f_in.readline()
    f_in.close()

    return WORDLIST


def meaning(WORDLIST, word):

    word = word.lower()
    wlen = len(word)
    s_len = 0

    for i in range(wlen, 0, -1):
        if not i in WORDLIST:
            continue

        for preg_t in WORDLIST[i]:

            if preg_t.search(word):
                word = preg_t.sub(".", word)
                s_len += i

    ratio = 0.0
    if s_len:
        ratio = float(s_len) / float(wlen)

    return ratio


########
# MAIN #
########
WORDLIST = loadWordlist()
header = ['word', 'ut_meaning_ratio']

csv_in = csv.DictReader(
    sys.stdin)  # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header, header))))  # write header

for row in csv_in:
    word = row['word'].strip()

    row['ut_meaning_ratio'] = meaning(WORDLIST, word)

    # return row to Splunk
    csv_out.writerow(row)
