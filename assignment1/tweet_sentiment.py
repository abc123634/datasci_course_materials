# author: Lee Meng(b98705001@gmail.com)
# This python program parse "tweets" from Twitter which are included in a file in json.
# We therefore get sentiment values of each tweets by the aggregation of the 
# sentiment of indivudal term, which determined by the AFINN-111.txt

# Usage: python term_sentiment.py [sentiment_file.txt] [tweet_file.json] 
import sys
import json

def build_sentiment_dict(sentiment_file_name):
    # build a dictionary where (key, vaule) = (term, corresponding sentiment score)
    # where the terms and their scores are delimited by tab in sentiment file

    sentiment_dict = {}
    sentiment_file = open(sentiment_file_name)

    for line in sentiment_file:
        term, score = line.split("\t")
        sentiment_dict[term] = int(score)

    sentiment_file.close()

    return sentiment_dict

def build_tweets_dict(tweet_file_name):
    # build a dictionary where the (key, value) = (tweet_line_id, corredsponding tweet).
    # the tweet_line_id is decided by the line where the tweets locate at the tweet_file 
    # and will start from 1

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
    # a generator function which traverse all the way for a json obj which in essence represented 
    # by a nested dictionary to grape all useful text/content for sentiment analysis by searching 
    # the specific key(e.g. 'text') 

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

def compute_sentiment(tweets_dict, sentiment_dict):
    # compute the tweets' sentiment by aggrgate the total sentiment of terms
    # and return a dictionary where (key, value) = (tweet_id, sentiment score)
    sentiment_score = {}

    for id, tweet in tweets_dict.items():
        tweet_content = ""
        score = 0
        for text in get_text(tweet, 'text'):
            tweet_content += text
        terms = tweet_content.lower().split(' ')
        for term in terms:
            if term in sentiment_dict:
                score += sentiment_dict[term]
        sentiment_score[id] = score

    return sentiment_score

def main():
    sentiment_file_name = sys.argv[1]
    tweet_file_name = sys.argv[2]
    
    sentiment_dict = build_sentiment_dict(sentiment_file_name) #(k,v) = (term, sentiment score)
    tweets_dict = build_tweets_dict(tweet_file_name) #(k,v) = (tweet id, tweet)
    
    sentiment_score = compute_sentiment(tweets_dict, sentiment_dict) #(k,v) = (tweet id, sentiment score)

    for score in sentiment_score.values():
        print score

if __name__ == '__main__':
    main()
