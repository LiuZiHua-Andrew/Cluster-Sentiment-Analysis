import tweepy
import couchdb
import sys, getopt
import json
from MyStreamListener import MyStreamListener

def get_authorization(access_file):
    with open(access_file) as f:
        access_str = f.read()

    access = json.loads(access_str)

    info = {"consumer_key": access['CONSUMER_KEY'],
            "consumer_secret": access['CONSUMER_SECRET'],
            "access_token": access['ACCESS_TOKEN'],
            "access_secret": access['ACCESS_TOKEN_SECRET']}

    auth = tweepy.OAuthHandler(info['consumer_key'], info['consumer_secret'])
    auth.set_access_token(info['access_token'], info['access_secret'])
    return auth

def get_tweets(access):
    couch_host = "localhost"
    couch_port = 5984
    db_name = "test_old"

    host_and_port = "http://" + couch_host + ":" + str(couch_port)
    couch = couchdb.Server(host_and_port)
    try:
        db = couch.create(db_name)  # create db
    except:
        db = couch[db_name]  # existing

    api = tweepy.API(get_authorization(access),wait_on_rate_limit=True)
    for status in tweepy.Cursor(api.search,q='',geocode='-25.042217096750914,134.53221344885128,2000km').items():
        db.save(status._json)

def create_stream(locations, access_json ,db_json, grid_json, f_name=None):
    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    with open(grid_json) as f:
        grids_str = f.read()
    suburbs = json.loads(grids_str)

    listener = MyStreamListener(f_name=f_name, couch_host=db_info['host'], couch_port=db_info['port'], db_name=db_info['processed_database'],raw_db_name=db_info['raw_database'],suburbs=suburbs)
    stream = tweepy.Stream(get_authorization(access_json), listener)
    stream.filter(locations=locations)


def main(argv):
    # West Australia
    wa_location = [112.8,-35.33,129,-13.5]
    # Northern Territory
    nt_location = [129,-26,138,-10.75]
    # South Australia
    sa_location = [129,-38.1,141,-26]
    # Queensland, NSW, Victoria, Tasmania
    qnvt_location = [138,-26,141,-15.8, 141,-15.8,146,-10.5, 141,-43.8,154,-15.8]

    outputfile = 'twitter.json'
    access_token_json = 'access.json'
    db_json = 'db.json'
    grid_json ='vic.json'
    location = qnvt_location
    try:
        opts, args = getopt.getopt(argv, "ho:a:d:l:g:", ["outputfile=",'access=','database=','location=','grid='])
    except getopt.GetoptError:
        print ("""-o <output_filename>
                  -a <access_token_josn>
                  -d <database_json>
                  -l < West Australia: 1,
                       Northern Territory: 2,
                       South Australia: 3
                       Queensland, NSW, Victoria, Tasmania: 4>
                 """)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("""-o <output_filename>
                      -a <access_token_josn>
                      -d <database_json>
                      -l < West Australia: 1,
                           Northern Territory: 2,
                           South Australia: 3
                           Queensland, NSW, Victoria, Tasmania: 4""")
            sys.exit()
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-a", "--access"):
            access_token_json = arg
        elif opt in ("-d", "--database"):
            db_json = arg
        elif opt in ("-l", "--location"):
            if arg == '0':
                location = wa_location
            elif arg == '1':
                location = nt_location
            elif arg == '2':
                location = sa_location
            elif arg == '3':
                location = qnvt_location
            else:
                print ("""-l < West Australia: 0,
                               Northern Territory: 1,
                               South Australia: 2
                               Queensland, NSW, Victoria, Tasmania: 3""")
                sys.exit(2)
        elif opt in ("-g", "--grid"):
            grid_json = arg

    create_stream(location, access_token_json,db_json,grid_json,f_name=outputfile,)

    # get_tweets(access_token_json)

if __name__ == "__main__":
   main(sys.argv[1:])