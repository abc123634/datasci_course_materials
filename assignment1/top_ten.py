"""Author: Lee Meng(b98705001@gmail.com)
This python program computes the ten most frequently occurring hashtags from some Twitter tweets

Usage: python top_ten.py <tweet_file>
"""

import sys
import json
import re

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

def pretty_print(json_obj):
    # display json in a json-style way, making it easier to identify structure
    print json.dumps(json_obj, indent=4, separators=(',',':'))

def get_content_by_key(tweet, key_specified):
    """a generator function which traverse all the way for a json obj which in essence represented 
    by a nested dictionary to grape all useful text/content for sentiment analysis by searching 
    the specific key(e.g. 'text') """

    if key_specified in tweet:
        yield tweet[key_specified]
    for value in tweet.values():
        if isinstance(value, dict):
            for value2 in value.values():
                if isinstance(value2, dict):
                    for text in get_content_by_key(value2, key_specified):
                    	if isinstance(text, list):
                    		yield text                        	

def get_terms_from_tweet(tweet, key_specified):
    # a helper function to extract all terms from tweet and return a term list
    tweet_content = ""
    for text in get_content_by_key(tweet, key_specified):
    	for dic in text:
    		tweet_content += ' ' 
    		tweet_content += dic['text']

    # tweet_content = tweet_content.lower().strip().replace('@', ' ').replace('-', ' ').replace("\"", " ").replace('?', ' ').replace('!', ' ')
    # tweet_content = tweet_content.replace('$', ' ').replace('%', ' ').replace('#', ' ').replace('/', ' ').replace('_', ' ').replace('.', ' ')

    # terms = re.split(r',|;|:|\s|\n|\t|4|of', tweet_content)
    terms = re.split(r',|\s', tweet_content)

    return terms


def main():
	tweet_file_name = sys.argv[1]
	tweets_dict     = build_tweets_dict(tweet_file_name) #(k,v) = (tweet id, tweet)

	tag_freq_dic = {} #(k, v) = (tag name, freq)
	for id, tweet in tweets_dict.items():
		hashtags = get_terms_from_tweet(tweet, 'hashtags')
		for hashtag in hashtags:
			if hashtag == '':
				pass
			elif not tag_freq_dic.has_key(hashtag):
				tag_freq_dic[hashtag] = 1
			else:
				tag_freq_dic[hashtag] += 1

	# for tag in tag_freq_dic:
	# 	print tag, tag_freq_dic[tag

	a = list(tag_freq_dic.items())
	a.sort(key=lambda x: x[0])
	a.sort(key=lambda x: x[1])

	print len(a)
	i = 0
	while True:
		print a[i][0], a[i][1]
		i += 1
		if len(a) <= i or i > 10:
			break

		# hashtags, description, name

if __name__ == '__main__':
	main()