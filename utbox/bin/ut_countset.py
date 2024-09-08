import sys
import csv
import json
from six.moves import zip
"""
# a-z
set_az = set(chr(c) for c in range(0x61, 0x7b))
set_AZ = set(chr(c) for c in range(0x41, 0x5B))
set_aZ = set_az ^ set_AZ
set_09 = set(chr(c) for c in range(0x30, 0x40))
set_printable = set(chr(c) for c in range(0x20, 0x7F))

# pouet    : all lowercase
# pouet_up : all uppercase
# pouet_all: lower and uppercase

PRESETS = {
 '@punct@'       : list(set_printable - set_aZ - set_09),
 '@typo@'        : ['&', '*', '@', '\\',  '^',  '#',  '%',  '~',  '_',  '|'],
 '@digits@'      : list(set_09),

 '@alpha@'       : list(set_az),
 '@alpha_up@'    : list(set_AZ),
 '@alpha_all@'   : list(set_aZ),

 '@alphanum@'    : list(set_az ^ set_09),
 '@alphanum_up@' : list(set_AZ ^ set_09),
 '@alphanum_all@': list(set_aZ ^ set_09),

 '@hexa@'        : list(set_09 ^ set('abcdef')),
 '@hexa_up@'     : list(set_09 ^ set('ABCDEF')),
 '@hexa_all@'    : list(set_09 ^ set('ABCDEFabcdef')),

 '@noalpha@'     : list(set_printable - set_aZ),
 '@base64@'      : list(set_aZ ^ set_09 ^ set('+/=')),

 '@vowels@'      : list(set('aeiouy')),
 '@vowels_up@'   : list(set('AEIOUY')),
 '@vowels_all@'  : list(set('aeiouyAEIOUY')),

 '@consonants@'    : list(set_az - set('aeiouy')),   
 '@consonants_up@' : list(set_az - set('AEIOUY')),   
 '@consonants_all@': list(set_az - set('aeiouyAEIOUY')),   
}


def countset(word, wordset):
	# @word@  is a special set which means that only the letters composing the submitted word are counted.

	if wordset == "@word@" : 
		s = list(set(word))
	else:
		try:
			s = PRESETS[ wordset ]
		except:
			s = list(set(wordset))

	counts = {'sum':0}
	for c in s:
		x = word.count(c)
		counts[ '%X' % ord(c) ] = x 
		counts[ 'sum' ] += x

	return counts

"""
import ut_presets

########
# MAIN #
########
header = ['word', 'set', 'ut_countset']

csv_in = csv.DictReader(
    sys.stdin)  # automatically use the first line as header
csv_out = csv.DictWriter(sys.stdout, header)
csv_out.writerow(dict(list(zip(header, header))))  # write header

for row in csv_in:
    word = row['word'].strip()
    wordset = row['set'].strip()

    counts = ut_presets.countset(word, wordset)

    row['ut_countset'] = json.dumps({'ut_countset': counts})

    # return row to Splunk
    csv_out.writerow(row)
