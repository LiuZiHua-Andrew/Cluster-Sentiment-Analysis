import tweepy
import couchdb
import json
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self,f_name='twitter.json',output2couch=True,couch_host='localhost',couch_port=5984,db_name='test',api=None):
        tweepy.StreamListener(api)
        self.f_name=f_name
        self.output2couch=output2couch
        self.couch_host=couch_host
        self.couch_port=couch_port
        self.db_name=db_name

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            if self.output2couch:
                self.output2couchdb(data)
                return True
            else:
                with open(self.f_name, 'a') as f:
                    f.write(data)
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print("Error"+status)
        return True

    def output2couchdb(self,data):
        self.couch_host+":"+str(self.couch_port)
        couch = couchdb.Server()
        try:
            db = couch.create(self.db_name) # create db
        except:
            db = couch[self.db_name] # existing
        db.save(json.loads(data.encode('gbk')))