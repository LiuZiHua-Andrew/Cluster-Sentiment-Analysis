"""
Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583,
"""

import requests
import couchdb
import json
import sys
import getopt
import re
from SentimentAnalysis.SentimentAnalysis import sentiment_polarity


def put_data_into_couchdb(db_json,grid_json,data_json):

    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    couch_user = db_info['user']
    couch_password = db_info['password']
    couch_host = db_info['host']
    couch_port = db_info['port']
    db_name = db_info['processed_database']
    raw_db_name = db_info['raw_database']
    # source_url = db_info['tweet_source']
    host_and_port = "http://" +couch_user+":"+couch_password+"@"+couch_host + ":" + str(couch_port)

    couch = couchdb.Server(host_and_port)
    try:
        db = couch.create(db_name)  # create db
    except:
        db = couch[db_name]  # existing

    try:
        raw_db = couch[raw_db_name]  # existing
    except:
        raw_db = couch.create(raw_db_name)  # create db

    with open(grid_json) as f:
        grids_str = f.read()
    suburbs = json.loads(grids_str)

    f = open(data_json,encoding='utf-8')
    f.readline()
    count = 0
    while True:
        print (count)
        process_data = []
        raw_data = []
        for i in range(500):
            line = f.readline().strip("\n").strip()
            if line[-1] == ",":
                line = line[:-1]
            try:
                tweet = json.loads(line)
            except:
                raw_db.update(raw_data)
                db.update(process_data)
                print (count)
                print ("Done.")
                exit()
            twitter = tweet['doc']
            twitter.pop('_rev')
            raw_data.append(twitter)
            info = sentiment_polarity(twitter, suburbs)
            if info != None:
                process_data.append(info)
            count += 1
        raw_db.update(raw_data)
        db.update(process_data)

def main(argv):
    db_json = 'db.json'
    grid_json = 'vic.json'
    data_json = 'richard.json'
    try:
        opts, args = getopt.getopt(argv, "hd:g:t:", ['database=',"grid=",'tweet='])
    except getopt.GetoptError:
        print ("""-d <database_json>
                  -g <grid.json>
                  -t <tweet.json>""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("""-d <database_json>
                      -g <grid.json>
                      -t <tweet.json>""")
            sys.exit()

        elif opt in ("-d", "--database"):
            db_json = arg
        elif opt in ("-g", "--grid"):
            grid_json = arg
        elif opt in ("-t", "--tweet"):
            data_json = arg


    put_data_into_couchdb(db_json, grid_json, data_json)


if __name__ == "__main__":
   main(sys.argv[1:])
