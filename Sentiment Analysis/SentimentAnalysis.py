from textblob import TextBlob
import couchdb

couch_host = "localhost"
couch_port = 5984
db_name = "test"

host_and_port = "http://"+couch_host+":"+str(couch_port)
couch = couchdb.Server(host_and_port)

try:
    db = couch[db_name]
except:
    exit(-1)

for id in db:
    twitter = db[id]
    text = twitter['text']
    blob = TextBlob(text)
    if not twitter['lang'] == 'en': # If the language is not English, translate it.
        blob = blob.translate(from_lang=twitter['lang'],to="en")
    # blob = blob.correct()
    # print(blob.tags)
    for sentence in blob.sentences:
        print(sentence)
        print(sentence.sentiment.polarity)

