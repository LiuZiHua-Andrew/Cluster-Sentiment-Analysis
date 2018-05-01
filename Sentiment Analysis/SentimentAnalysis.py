from textblob import TextBlob
import couchdb
import json
from geojson_utils import point_in_polygon


def sentiment_polarity(db,suburbs):
    suburb_tweets_count = dict()
    for suburb in suburbs:
        suburb_tweets_count[suburb['properties']['Suburb_Name']] = 0
    polarities = []
    for id in db:
        twitter = db[id]
        text = twitter['text']
        blob = TextBlob(text)
        if not twitter['coordinates'] == None:
            for suburb in suburbs:
                if point_in_polygon(twitter['coordinates'], suburb['geometry']):
                    suburb_tweets_count[suburb['properties']['Suburb_Name']] += 1
                    break

        if not twitter['lang'] == 'en':  # If the language is not English, translate it.
            try:
                blob = blob.translate(from_lang=twitter['lang'], to="en")
            except:
                pass

        # blob = blob.correct()
        # print(blob.tags)

        for sentence in blob.sentences:
            polarities.append((sentence, sentence.sentiment.polarity))
    a = sorted(suburb_tweets_count.items(), key=lambda x: x[1], reverse=True)

    return polarities


def hashtag_ranking(db):
    hts = dict()
    for id in db:
        twitter = db[id]
        ht = twitter['entities']['hashtags']
        for h in ht:
            hts[h['text']] = hts.get(h['text'], 0) + 1
    return (sorted(hts.items(), key=lambda x: x[1], reverse=True))


with open("vic.json") as f:
    grids_str =f.read()

suburbs = json.loads(grids_str)

couch_host = "localhost"
couch_port = 5984
db_name = "test_au"

host_and_port = "http://"+couch_host+":"+str(couch_port)
couch = couchdb.Server(host_and_port)

try:
    db = couch[db_name]
except:
    exit(-1)

sentiment_polarity(db,suburbs)

