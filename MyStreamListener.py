import tweepy
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self,f_name='twitter.json',api=None):
        tweepy.StreamListener(api)
        self.f_name=f_name

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            with open(self.f_name, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print("Error"+status)
        return True