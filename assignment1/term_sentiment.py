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


def get_tweet_score(tweet_json, sentiment_score_dict, tweet_index, non_sentiment_index):
    """
    Sum the score for each term contains in the tweet (text value)
    :param non_sentiment_index: default dict contains the result of tweet index regarding of non-sentiment world
    :param tweet_index: tweet line number regarding of the input file
    :param tweet_json:
    :param sentiment_score_dict:
    :return:
    """
    sum_ = 0
    word_list = []
    try:
        text = tweet_json.get("text", "")
        word_list = re.split("\s+", text, re.UNICODE)
        for w in word_list:
            try:
                current_score = sentiment_score_dict[w.lower()]
            except KeyError:
                current_score = 0
                if re.match("^[a-z]+$", w, re.IGNORECASE):
                    non_sentiment_index[w.lower()].append(tweet_index)
            sum_ += current_score
    except :
        pass

    return sum_, len(word_list)


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
            print(*result)


def compute_results_non_sentiment(results_tweet_score, non_sentiment_index):
    """
    Compute sentiment value for a non sentiment word
    :param results_tweet_score: computed score by tweet. tweet are inserted with the same encountered index
    :param non_sentiment_index: defaultdict(list) key (non sentiment word), value list of tweet where the word has been
    encountered.
    :return: sorted iterable (key, value) key an estimated sentiment word and value it's float value
    """
    results = {}
    for w in non_sentiment_index:
        tot_avg = 0
        for tweet_index in non_sentiment_index[w]:
            tot_avg += float(results_tweet_score[tweet_index][0]) / results_tweet_score[tweet_index][1]
        word_avg = float(tot_avg) / len(non_sentiment_index[w])
        results[w] = round(word_avg, 3)

    return sorted(results.iteritems(), key=lambda x: x[0])


def main():
    """
    Main
    :return:
    """
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    results = []
    results_non_sentiment = dict()
    non_sentiment_index = defaultdict(list)

    assert os.path.isfile(sent_file), usage()
    assert os.path.isfile(tweet_file), usage()

    sentiment_score_dict = get_sentiment_score(sent_file)

    with open(tweet_file) as tweet_file_fh:
        for line_i, tweet_json_str in enumerate(tweet_file_fh):
            current_score = 0
            n_words = 0
            try:
                tweet_json = json.loads(tweet_json_str)
                current_score, n_words = get_tweet_score(
                    tweet_json, sentiment_score_dict, line_i, non_sentiment_index)
            except:
                pass
            results.append((current_score, n_words))

    scored_non_sentiment_world = compute_results_non_sentiment(results, non_sentiment_index)
    write_list(scored_non_sentiment_world)


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

