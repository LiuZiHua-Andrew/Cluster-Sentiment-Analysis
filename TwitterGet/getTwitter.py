import requests
import couchdb
auth=('readonly','ween7ighai9gahR6')

def get_geocoded_tweets(include_docs='true',reduce='false',skip='0',limit=None,auth=('readonly','ween7ighai9gahR6')):
    url="http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/geoindex"

    if limit==None:
        payload = {'include_docs': include_docs, 'reduce': reduce, 'skip': skip}  # without limit
    else:
        payload = {'include_docs': include_docs, 'reduce': reduce, 'skip': skip,'limit':limit}  # without limit

    auth=auth
    r=requests.get(url=url,params=payload,auth=auth)

    return r.json()


def get_geo_json(reduce='false',start_key='\[\"r1r0\",2014,1,1\]',end_key='\[\"r1r1\",2017,12,31\]',skip='0',limit=None,auth=('readonly','ween7ighai9gahR6')):
    url="http://45.113.232.90/couchdbro/twitter/_design/twitter/_list/geojson/geoindex"

    if limit==None:
        payload = {'reduce': reduce, 'start_key':start_key,'end_key':end_key,'skip': skip}  # without limit
    else:
        payload = {'reduce': reduce, 'start_key':start_key,'end_key':end_key,'skip': skip,'limit':limit}  # without limit

    auth=auth
    r=requests.get(url=url,params=payload,auth=auth)
    return r
    # return r.json()

def get_aggregated_tweets_by_city(include_docs='false',reduce='true',group_level='1',skip='0',limit=None,auth=('readonly','ween7ighai9gahR6')):
    url="http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary"
    if limit==None:
        payload = {'include_docs': include_docs,'reduce': reduce,'group_level':group_level, 'skip': skip}  # without limit
    else:
        payload = {'include_docs': include_docs,'reduce': reduce,'group_level':group_level, 'skip': skip,'limit':limit}  # without limit

    auth=auth
    r=requests.get(url=url,params=payload,auth=auth)

    return r.json()

# geocoded_tweets=get_geocoded_tweets(skip='1',limit='1',auth=auth)
# print(geocoded_tweets)

geo_json=get_geo_json(limit='2',auth=auth)
print(geo_json)
#
# aggregated_tweets_by_city=get_aggregated_tweets_by_city(limit='20',auth=auth)
# print(aggregated_tweets_by_city)

#########################################################################################################################################
def put_data_into_couchdb():
    couch_host = "localhost"
    couch_port = 5984
    db_name = "geocoded_tweets"
    total_rows=3629417

    host_and_port = "http://" + couch_host + ":" + str(couch_port)
    couch = couchdb.Server(host_and_port)
    try:
        db = couch.create(db_name)  # create db
    except:
        db = couch[db_name]  # existing

    for i in range(total_rows):
        skip=str(i)
        geocoded_tweets = get_geocoded_tweets(skip=skip, limit='1', auth=auth)


        db.save(geocoded_tweets)

# put_data_into_couchdb()