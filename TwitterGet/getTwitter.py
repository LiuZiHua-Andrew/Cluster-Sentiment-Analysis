import requests

def get_geocoded_tweets(include_docs='true',reduce='false',skip='0',limit=None,auth=('readonly','ween7ighai9gahR6')):
    url="http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/geoindex"

    if limit==None:
        payload = {'include_docs': include_docs, 'reduce': reduce, 'skip': skip}  # without limit
    else:
        payload = {'include_docs': include_docs, 'reduce': reduce, 'skip': skip,'limit':limit}  # without limit

    auth=auth
    r=requests.get(url=url,params=payload,auth=auth)

    return r.json()

geocoded_tweets=get_geocoded_tweets(limit='2',auth=('readonly','ween7ighai9gahR6'))
print(geocoded_tweets)