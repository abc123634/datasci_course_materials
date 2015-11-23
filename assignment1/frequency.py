"""author: Lee Meng(b98705001@gmail.com)
This program parse a Twitter tweet into list of terms and count their (relative) frequencies by the 
native equation: [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]
And write the result to the stdout.

Usage: python frequency.py <tweet_file>
"""

import sys
import json
import re
    
def get_text(tweet, key_specified):
    """a generator function which traverse all the way for a json obj which in essence represented 
    by a nested dictionary to grape all useful text/content for sentiment analysis by searching 
    the specific key(e.g. 'text') """

    if key_specified in tweet:
        yield tweet[key_specified].encode('utf8')
    for value in tweet.values():
        if isinstance(value, dict):
            for value2 in value.values():
                if isinstance(value2, dict):
                    for text in get_text(value2, key_specified):
                        yield text.encode('utf8')


def get_terms_from_tweet(tweet):
    # a helper function to extract all terms from tweet and return a term list
    tweet_content = ""
    for text in get_text(tweet, 'text'):
        tweet_content += ' '
        tweet_content += text

    # tweet_content = tweet_content.lower().strip().replace('@', ' ').replace('-', ' ').replace("\"", " ").replace('?', ' ').replace('!', ' ')
    # tweet_content = tweet_content.replace('$', ' ').replace('%', ' ').replace('#', ' ').replace('/', ' ').replace('_', ' ').replace('.', ' ')

    # terms = re.split(r',|;|:|\s|\n|\t|4|of', tweet_content)
    terms = re.split(r',|:|;|\s', tweet_content)

    return terms


def build_tweets_dict(tweet_file_name):
    """build a dictionary where the (key, value) = (tweet_line_id, corredsponding tweet).
    the tweet_line_id is decided by the line where the tweets locate at the tweet_file 
    and will start from 1"""

    tweets_dict = {}
    tweet_file = open(tweet_file_name)

    line_id = 1
    for line in tweet_file:
        tweet = json.loads(line)
        tweets_dict[line_id] = tweet
        line_id += 1
    
    tweet_file.close()

    return tweets_dict

def build_inverted_index_for_all_term(tweets_dict):
    # parse tweet content into term first by using get_term_for_tweet()
    # then build inverted index list for every individual term from all the tweets

    term_occur_in_tweet = {}
    for tweet_id, tweet in tweets_dict.items():
        terms = get_terms_from_tweet(tweet)
        for term in terms:
            if term == '':
                pass
            elif not term_occur_in_tweet.has_key(term):
                term_occur_in_tweet[term] = [tweet_id]
            else: 
                term_occur_in_tweet[term].append(tweet_id)
    return term_occur_in_tweet

def main():
    tweet_file_name = sys.argv[1]
    tweets_dict = build_tweets_dict(tweet_file_name) #(k,v) = (tweet id, tweet)

    inverted_index_list = build_inverted_index_for_all_term(tweets_dict) #(k, v) = (term, inverted index list)

    total_freq = 0.0
    for l in inverted_index_list.values():
        total_freq += len(l)

    for term, l in inverted_index_list.items():
        print term, str(len(l) / total_freq)

if __name__ == '__main__':
    main()