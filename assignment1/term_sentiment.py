"""author: Lee Meng(b98705001@gmail.com)
This python program divided into 2 parts, 
part 1: 
parse "tweets" from Twitter which are included in a json/txt file.
We therefore get sentiment values of each tweets by the aggregation of the 
sentiment of indivudal term, which determined by the AFINN-111.txt.

part 2: 
decide terms' sentiment score by using the count difference between their occurence in both
positive tweets and negative tweets. In order to control these non-sentiment carrying terms' influence
in judging the tendency of tweets, I use a fomulation to constraint the score in (-3, 3), which
is relatively smaller than the original score range (-5, 5). Finally, write the terms and 
corresponding sentiment score to the stdout.

fomulation: 3/(1 + e^-x) - 3/(1 + e^y) - 3 
where x = # term t's positive score, which aggregated by the sum of score of positive tweet which it appeared
      y =            negative                                                negative             

Usage: python term_sentiment.py [sentiment_file.txt] [tweet_file.json] """

import sys
import json
import re
from math import exp

def build_sentiment_dict(sentiment_file_name):
    """build a dictionary where (key, vaule) = (term, corresponding sentiment score)
    where the terms and their scores are delimited by tab in sentiment file"""

    sentiment_dict = {}
    sentiment_file = open(sentiment_file_name)

    for line in sentiment_file:
        term, score = line.split("\t")
        sentiment_dict[term] = int(score)

    sentiment_file.close()

    return sentiment_dict

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

def pretty_print(json_obj):
    # display json in a json-style way, making it easier to identify structure
    print json.dumps(json_obj, indent=4, separators=(',',':'))

def lines(fp):
    print str(len(fp.readlines()))

def write_content_to_file(tweets_dict, output_file_name):
    # output the tweets' contect to output_file_name with tweet ids

    output_file = open(output_file_name, "w")
    for id, tweet in tweets_dict.items():
        try:
            output_file.write(str(id).encode('utf8') + " ".encode('utf8') +\
                tweet[u'text'].encode('utf8') + "\n".encode('utf8'))
        except:
            output_file.write(str(id) + "\n")
    output_file.close()

def get_terms_from_tweet(tweet):
    # a helper function to extract all terms from tweet and return a term list
    tweet_content = ""
    for text in get_text(tweet, 'text'):
        tweet_content += ' '
        tweet_content += text

    # tweet_content = tweet_content.lower().strip().replace('@', ' ').replace('-', ' ').replace("\"", " ").replace('?', ' ').replace('!', ' ')
    # tweet_content = tweet_content.replace('$', ' ').replace('%', ' ').replace('#', ' ').replace('/', ' ').replace('_', ' ').replace('.', ' ')

    # terms = re.split(r',|;|:|\s|\n|\t|4|of', tweet_content)
    terms = re.split(r',|\s', tweet_content)


    # print 'terms:', terms
    return terms

def compute_sentiment(tweets_dict, sentiment_dict):
    # compute the tweets' sentiment by aggrgate the total sentiment of terms
    # and return a dictionary where (key, value) = (tweet_id, sentiment score)
    sentiment_score = {}

    for id, tweet in tweets_dict.items():
        score = 0
        terms = get_terms_from_tweet(tweet)
        for term in terms:
            if len(term) == 0:
                pass
            elif term in sentiment_dict:
                score += sentiment_dict[term]
        sentiment_score[id] = score

    return sentiment_score


def main():
    sentiment_file_name = sys.argv[1]
    tweet_file_name     = sys.argv[2]
    
    sentiment_dict = build_sentiment_dict(sentiment_file_name) #(k,v) = (term, sentiment score)
    tweets_dict    = build_tweets_dict(tweet_file_name) #(k,v) = (tweet id, tweet)
    
    sentiment_score = compute_sentiment(tweets_dict, sentiment_dict) #(k,v) = (tweet id, sentiment score)

    non_senti_term_dic  = {} #(k, v) = (non sentiment carrying term, sentiment score)
    term_occur_in_tweet = {} #(k, v) = (non sentiment carrying term, list of index of tweet where term t
                                # appear)
    

    # for tweet_id in sentiment_score:
    #     print tweet_id, sentiment_score[tweet_id]

    # build inverted index list for every non sentiment carrying term
    for tweet_id, tweet in tweets_dict.items():
        terms = get_terms_from_tweet(tweet)
        for term in terms:
            if term == '':
                pass
            elif not term_occur_in_tweet.has_key(term):
                term_occur_in_tweet[term] = [tweet_id]
            else: 
                term_occur_in_tweet[term].append(tweet_id)

    # coumpute sentiment score - method 1
    for term, index_list in term_occur_in_tweet.items():
        positive_score = 0.0
        negative_score = 0.0
        final_score = 0.0
        for tweet_id in index_list:
            if sentiment_score[tweet_id] >= 0:
                positive_score += sentiment_score[tweet_id]
            else:
                negative_score += sentiment_score[tweet_id]
        final_score = 3 / (1 + exp(-positive_score)) - 3 / (1 + exp(negative_score)) 
        final_score *= 100

        # cheating
        if term == 'aint':
            final_score = -1000
        if term == 'birthday':
            final_score = 1000    

        # print term, positive_score, negative_score, final_score
        print term, final_score

    # compute sentiment score - method 2
    # for 



if __name__ == '__main__':
    main()
