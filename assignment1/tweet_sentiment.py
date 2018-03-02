from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import json
import sys

import os
import logging
import re
import codecs

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
    print("%s SENTIMENT_FILE STREAM_API_RESULT", file=sys.stderr)


def get_tweet_score(tweet_json, sentiment_score_dict):
    """
    Sum the score for each term contains in the tweet (text value)
    :param tweet_json:
    :param sentiment_score_dict:
    :return:
    """
    sum_ = 0
    try:
        text = tweet_json.get("text", "")
        word_list = re.split("\s+", text, re.UNICODE)

        for w in word_list:
            current_score = sentiment_score_dict.get(w.lower(), 0)
            sum_ += current_score
    except :
        pass

    return sum_


def write_list(result_list, fout=""):
    """
    write result list to file or stdout
    :param result_list:
    :param fout:
    :return:
    """
    if fout:
        with open(fout, mode="wb") as fout_fh:
            for result in result_list:
                fout_fh.write(str(result) + "\n")
    else:
        for result in result_list:
            print(result)


def main():
    """
    Main
    :return:
    """
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    results = []

    assert os.path.isfile(sent_file), usage()
    assert os.path.isfile(tweet_file), usage()

    sentiment_score_dict = get_sentiment_score(sent_file)

    with open(tweet_file) as tweet_file_fh:
        for line_i, tweet_json_str in enumerate(tweet_file_fh):
            current_score = 0
            try:
                tweet_json = json.loads(tweet_json_str)
                current_score = get_tweet_score(tweet_json, sentiment_score_dict)
            except:
                pass
            results.append(current_score)

    write_list(results)


def get_sentiment_score(s_file):
    """
    From a sentiment file returns dict of sentiment
    :param s_file:
    :return (dict): key the sentiment, value the score
    """
    dict_result = {}
    with codecs.open(s_file, encoding="utf-8") as f_sentiment:

        for line in f_sentiment:
            try:
                term, score = line.split('\t', 2)
                dict_result[term] = int(score.strip())
            except ValueError:
                pass
    return dict_result


if __name__ == '__main__':
    config_log()
    main()
