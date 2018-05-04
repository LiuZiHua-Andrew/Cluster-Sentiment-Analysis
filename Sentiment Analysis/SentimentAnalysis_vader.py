from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import couchdb
import json
from geojson_utils import point_in_polygon
from nltk.tokenize import TweetTokenizer
import sys
import getopt
def preprocess(text):
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text)

    for token in tokens[:]:
        if token[0] == u'@' or token[0] == u'#'  or (len(token) >= 7 and token.lower()[:7] == u'http://') or (len(token) >= 8 and token.lower()[:8] == u'https://'):
            tokens.remove(token)

    sent =''
    for token in tokens:
        sent += token + ' '
    return sent.strip()

def sentiment_polarity(db_json,suburbs):
    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    couch_host = db_info['host']
    couch_port = db_info['port']
    db_name = db_info['database']
    db_name2 = db_info['database2']

    host_and_port = "http://" + couch_host + ":" + str(couch_port)
    couch = couchdb.Server(host_and_port)

    try:
        db = couch[db_name]
    except:
        exit(-1)

    try:
        couch.delete(db_name2)
    except:
        pass

    db2 = couch.create(db_name2)

    processed_data = []
    for id in db:
        twitter = db[id]
        try:
            text = twitter['extended_tweet']['full_text']
        except:
            text = twitter['text']

        blob = TextBlob(text)
        if not twitter['lang'] == 'en':  # If the language is not English, translate it.
            try:
                blob = blob.translate(from_lang=twitter['lang'], to="en")
            except:
                continue

        blob = TextBlob(preprocess(blob.raw))

        s = None
        if not twitter['coordinates'] == None:
            for suburb in suburbs:
                if point_in_polygon(twitter['coordinates'], suburb['geometry']):
                    # suburb_tweets_count[suburb['properties']['Suburb_Name']] += 1
                    s = suburb['properties']['Suburb_Name']
                    break

            if s != None:
                analysis_data = dict()
                analysis_data['_id'] = twitter['id_str']
                analysis_data['suburb'] = s
                analysis_data['hashtags'] = [ht['text'] for ht in twitter['entities']['hashtags']]
                analysis_data['polarity'] = blob.sentiment.polarity
                processed_data.append(analysis_data)
                if len(processed_data) == 10:
                    db2.update(processed_data)
                    processed_data = []

    if len(processed_data) > 0:
        db2.update(processed_data)


def main(argv):
    db_json = 'db.json'
    try:
        opts, args = getopt.getopt(argv, "hd:", ['database='])
    except getopt.GetoptError:
        print ("""-d <database_json>""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("""-d <database_json>""")
            sys.exit()
        elif opt in ("-d", "--database"):
            db_json = arg


    with open("vic.json") as f:
        grids_str = f.read()
    suburbs = json.loads(grids_str)

    sentiment_polarity(db_json,suburbs)


if __name__ == "__main__":
   main(sys.argv[1:])



