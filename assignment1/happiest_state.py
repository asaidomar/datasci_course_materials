from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import json
import sys

import os
import logging
import re
import codecs
from collections import defaultdict

logger = None  # logger proxy


STATE_CODE = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

STATE_CODE_REVERSED = dict([ (v, k) for k, v in STATE_CODE.iteritems()])

def config_log():
    global logger
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


def get_current_state(tweet_json):
    # coordonates = tweet_json.get("coordinates", {}).get("coordinates", {})

    place = tweet_json.get("place", {}).get("name", "")

    if place:
        return STATE_CODE_REVERSED.get(place, "")

    user_location = tweet_json.get("user", {}).get("location", "")
    if user_location:
        return user_location.split(",")[-1]


def get_tweet_score(tweet_json, sentiment_score_dict, result_states):
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
            current_state = get_current_state(tweet_json)
            if current_state:
                result_states[current_state] += current_score
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
    results_sorted = sorted(result_list.iteritems(), key=lambda x: x[1], reverse=True)[0]
    if fout:
        with open(fout, mode="wb") as fout_fh:
            for result in results_sorted:
                fout_fh.write(result + "\n")
    else:
        print(results_sorted[0])


def main():
    """
    Main
    :return:
    """
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    assert os.path.isfile(sent_file), usage()
    assert os.path.isfile(tweet_file), usage()

    sentiment_score_dict = get_sentiment_score(sent_file)
    result_state_score = defaultdict(int)

    with open(tweet_file) as tweet_file_fh:
        for line_i, tweet_json_str in enumerate(tweet_file_fh):
            current_score = 0
            try:
                tweet_json = json.loads(tweet_json_str)
                current_score = get_tweet_score(tweet_json, sentiment_score_dict, result_state_score)
            except:
                pass

    write_list(result_state_score)


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
