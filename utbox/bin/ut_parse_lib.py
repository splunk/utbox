import os
import re
import sys
import csv
import json
import codecs

import ut_log

try:
	from urllib.parse import urlparse
except ImportError:
	from urllib.parse import urlparse

preg_rfc1808 = re.compile("://")
preg_ipv4 = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

#############
# FUNCTIONS #
#############
logger = ut_log.setup_logger()

# IANA : http://data.iana.org/TLD/tlds-alpha-by-domain.txt
# Mozilla: https://publicsuffix.org/list/public_suffix_list.dat


def _loadIANAList(filename="suffix_list_iana.dat"):
    TLDFILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           filename)  #"suffix_list_iana.dat")

    TLD = {'regulars': [], 'wildcards': [], 'exceptions': []}

    try:
        f = codecs.open(TLDFILE, "r", "utf-8")
    except Exception as e:
        raise e

    line = f.readline()
    while line:
        # skip comment or empty line
        if re.search('^\s*(#|$)', line):
            line = f.readline()
            continue

        line = line.strip().lower()
        TLD['regulars'].append(line)  # com
        line = f.readline()
    
    f.close()

    return TLD


def _loadMozillaList():
    """
	Load the Mozilla Suffix List and pre-process the TLDs.

	Ex: 'com' for '.com' or xn-<value>
	Ex: http://xn--3et6hy9whxi095c.xn--fiqz9s/
	
	*.ck
	!www.ck
	"""
    TLDFILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "suffix_list_mozilla.dat")

    TLD = {'regulars': [], 'wildcards': [], 'exceptions': []}

    try:
        f = codecs.open(TLDFILE, "r", "utf-8")
    except Exception as e:
        raise e

    line = f.readline()
    while line:
        # skip comment or empty line
        if re.search('^(\s*$|//)', line):
            line = f.readline()
            continue

        # stop at the first whitespace as stated on https://publicsuffix.org/list/
        line = line.lower()
        ret = re.search('^\s*([^\s]+)', line)
        if ret:
            tld_raw = ret.group(1)
            #tld_pun = tld_raw.encode('idna')

            c = tld_raw[0]
            if c == '*':
                TLD['wildcards'].append(tld_raw[2:])  # *.ck => ck
            elif c == '!':
                TLD['exceptions'].append(tld_raw[1:])  # !www.ck => www.ck
            else:
                TLD['regulars'].append(tld_raw)  # ro.com
        line = f.readline()

    f.close()

    return TLD


def loadTLDFile(tldlist="iana"):

    if tldlist == "mozilla":
        return _loadMozillaList()
    elif tldlist == "custom":
        return _loadIANAList(
            "suffix_list_custom.dat")  #dirty hack, but works ;)
    elif tldlist == "*":
        # load all lists
        Moz = _loadMozillaList()
        Cus = _loadIANAList("suffix_list_custom.dat")
        Ian = _loadIANAList()

        TLD = {
            'regulars':
            list(set(Moz['regulars'] + Cus['regulars'] + Ian['regulars'])),
            'wildcards':
            list(set(Moz['wildcards'] + Cus['wildcards'] + Ian['wildcards'])),
            'exceptions':
            list(set(Moz['exceptions'] + Cus['exceptions'] +
                     Ian['exceptions']))
        }

        return TLD

    return _loadIANAList()


def findTLD(netloc, TLDList):
    """
	Require a TLDList initialized by readTLDFile(). 
	The netloc args _must_ be lower-ed before entering this function.

	COUAC  => None
	yo.COM => com
	com    => com
	pouet.ck => pouet.ck
	www.ck   => ck
	google.com     => com
	www.google.com => com
	www.google.co.uk => co.uk
	www.google.bl.uk => uk
	www.bl.ck => bl.ck
	bl.www.ck => ck
	yoyo.pouet.fujikawaguchiko.yamanashi.jp => fujikawaguchiko.yamanashi.jp
	city.pouet.kawasaki.jp => pouet.kawasaki.jp
	pouet.city.kawasaki.jp => kawasaki.jp
	"""
    wildcards = TLDList['wildcards']
    exceptions = TLDList['exceptions']
    regulars = TLDList['regulars']

    TLD = None
    parts = netloc.split('.')
    items = []
    is_wildcard = False

    i = len(parts)
    while (i > 0) and (TLD == None):
        i -= 1

        items.insert(0, parts[i])
        candidate = '.'.join(items)

        if candidate in regulars:
            continue

        # is it a wildcard?
        if candidate in wildcards:
            is_wildcard = True
            continue
        elif is_wildcard:
            if candidate in exceptions:
                items.pop(0)
                candidate = '.'.join(items)
            TLD = candidate
        else:
            items.pop(0)
            if len(items) > 0:
                TLD = '.'.join(items)

    if (TLD == None) and len(items) > 0:
        TLD = '.'.join(items)

    return TLD


def extended_split(netloc, TLDList):
    """
	Extensive split of the domain name with Mozilla Suffix List.
	"""

    ret = {
        'ut_domain': "None",
        'ut_tld': "None",
        'ut_domain_without_tld': "None",
        'ut_subdomain': "None",
        'ut_subdomain_parts': "None",
        'ut_subdomain_count': "0",
        'ut_port': "80"
    }

    # fix for base64
    host_without_port = netloc.lower()

    # extract the port from the netloc and remove it
    tmp = netloc.split(':')
    if len(tmp) > 1:
        ret['ut_port'] = tmp.pop()
        host_without_port = tmp[0].lower()
    netloc = ':'.join(tmp)

    # find the TLD
    t = findTLD(host_without_port, TLDList)
    if t == None:

        # if this is an IPv4 we just copy it
        if preg_ipv4.search(netloc):
            ret['ut_domain'] = netloc
            ret['ut_domain_without_tld'] = netloc

        return ret
    ret['ut_tld'] = t

    tld_len = len(ret['ut_tld'])
    net_len = len(netloc)

    if tld_len == net_len:
        return ret

    parts = netloc[0:(net_len - tld_len - 1)].split('.')

    ret['ut_domain_without_tld'] = parts.pop()

    ret['ut_domain'] = '.'.join([ret['ut_domain_without_tld'], ret['ut_tld']])

    number_of_subdomains = len(parts)
    if number_of_subdomains:
        ret['ut_subdomain_count'] = number_of_subdomains
        ret['ut_subdomain'] = '.'.join(parts)

        sp = {}
        i = number_of_subdomains
        for p in parts:
            label = 'ut_subdomain_level_%s' % i
            sp[label] = p
            i -= 1
        ret['ut_subdomain_parts'] = json.dumps(sp)

    return ret


def parse_simple(url):
    # Following the syntax specifications in RFC 1808, urlparse recognizes
    # a netlog only if it is properly introduced by '//'.
    if not preg_rfc1808.search(url):
        url = "//%s" % url

    try:
        o = urlparse(url)
    except Exception as e:
        raise e

    res = {}
    res['ut_scheme'] = "None"
    res['ut_netloc'] = "None"
    res['ut_path'] = "None"
    res['ut_params'] = "None"
    res['ut_query'] = "None"
    res['ut_fragment'] = "None"

    if o.scheme:
        res['ut_scheme'] = o.scheme
    if o.netloc:
        res['ut_netloc'] = o.netloc
    if o.path:
        res['ut_path'] = o.path
    if o.params:
        res['ut_params'] = o.params
    if o.query:
        res['ut_query'] = o.query
    if o.fragment:
        res['ut_fragment'] = o.fragment

    return res


def parse_extended(url, TLDList):

    res = parse_simple(url)
    r = extended_split(res['ut_netloc'], TLDList)
    res.update(r)

    return res
