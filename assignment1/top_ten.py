from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import json
import sys

import os
import logging
import re
import codecs
import math

from collections import defaultdict

TOP_N = 10


logger = None  # logger proxy


def config_log():
    global  logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    logger = logging.getLogger(__file__)

    return logger


def hw():
    print ('Hello, world!')


def lines(fp):
    print( len(fp.readlines()) )


def main_old():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)


def usage():
    return "%s STREAM_API_RESULT" % sys.argv[0]


def get_term_dispatch(tweet_json, result):
    """
    :param tweet_json:
    :return:
    """
    try:
        hash_tags = tweet_json.get("entities", {}).get("hashtags", [])
        for tag in hash_tags:
            result[tag.get("text")] += 1
    except:
        pass


def write_list(result_list, fout=""):
    """
    write result list to file or stdout
    :param result_list:
    :param fout:
    :return:
    """
    results_sorted = sorted(result_list.iteritems(), key=lambda x: x[1], reverse=True)[:TOP_N]
    if fout:
        with open(fout, mode="wb") as fout_fh:
            for result in results_sorted:
                fout_fh.write(result + "\n")
    else:
        for result, occ in results_sorted:
            print(result,  occ)


def main():
    """
    Main
    :return:
    """
    tweet_file = sys.argv[1]
    term_occurence = defaultdict(int)

    assert os.path.isfile(tweet_file), usage()
    with open(tweet_file) as tweet_file_fh:
        for line_i, tweet_json_str in enumerate(tweet_file_fh):
            tweet_json = json.loads(tweet_json_str)
            get_term_dispatch(tweet_json, term_occurence)

    write_list(term_occurence)


if __name__ == '__main__':
    config_log()
    main()
