import tweepy
import sys, getopt
from MyStreamListener import MyStreamListener

CONSUMER_KEY = 'M2oVoMxM2guNKG1GJFy9YvOWZ'
CONSUMER_SECRET = '0BrWO6r2qyFUmYoXp4jbUC4QP3FjwwQmkNsgcbfQl7kWoifjgo'
ACCESS_TOKEN = '986794857120202752-GW1GhWVRUl8ZSIEaHYf1nRprkGxBWnO'
ACCESS_TOKEN_SECRET = 'vLxYc5SrUhPvPNEXaXghadXXeKgM8LkEsJc8xoY1lKgxs'

def get_authorization():

    info = {"consumer_key": CONSUMER_KEY,
            "consumer_secret": CONSUMER_SECRET,
            "access_token": ACCESS_TOKEN,
            "access_secret": ACCESS_TOKEN_SECRET}

    auth = tweepy.OAuthHandler(info['consumer_key'], info['consumer_secret'])
    auth.set_access_token(info['access_token'], info['access_secret'])
    return auth

def get_tweets(n,query=None):
    _max_queries = 100  # arbitrarily chosen value
    api = tweepy.API(get_authorization(),wait_on_rate_limit=True)

    tweets = tweet_batch = api.search(geocode='-37.814,144.96332,500km', count=n)
    ct = 1
    while len(tweets) < n and ct < _max_queries:
        tweet_batch = api.search(geocode='-37.814,144.96332,500km',
                                 count=n - len(tweets),
                                 max_id=tweet_batch.max_id)
        tweets.extend(tweet_batch)
        ct += 1
    return tweets

def create_stream(locations,f_name='twitter.json'):
    listener = MyStreamListener(f_name=f_name)
    stream = tweepy.Stream(get_authorization(), listener)
    stream.filter(locations=locations)


def main(argv):
    # Melbourne Coordinates
    melb_locations = [144.7, -38.1, 145.45, -37.5]
    has_filename =False
    try:
        opts, args = getopt.getopt(argv, "hf:", ["f="])
    except getopt.GetoptError:
        print 'twitterHarverster.py -f <output_filename>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -f <output_filename>'
            sys.exit()
        elif opt in ("-f", "--ofile"):
            has_filename =True
            outputfile = arg
    if has_filename:
        create_stream(melb_locations,f_name=outputfile)
    else:
        create_stream(melb_locations)

if __name__ == "__main__":
   main(sys.argv[1:])