import json
import couchdb
import sys,getopt
from couchdb.design import ViewDefinition
# reduce_fun = "function(keys, values) { return sum(values)/values.length }"
# view_tuples = \
#     [("surbub_polarity","function(doc) { emit(doc.suburb, doc.polarity);}",reduce_fun),
#      ("surbub_day_polarity","function(doc) { emit([doc.suburb,doc.created_at], doc.polarity);}",reduce_fun),
#      ("surbub_drunk","function(doc) { emit(doc.suburb, doc.drunk);}",reduce_fun),
#      ("surbub_day_drunk","function(doc) { emit([doc.suburb, doc.created_at], doc.drunk);}",reduce_fun),
#      ("surbub_hash","function (doc) {if(doc.hashtags.length>0){for(var i=0; i < doc.hashtags.length;i++){sub_hash = [doc.suburb, doc.hashtags[i]];emit(sub_hash, 1);}}}","function(keys, values) { return sum(values)}")
#      ]

def create_view(db, view_tuples):
    for vt in view_tuples:
        try:
            view = ViewDefinition(vt[0], vt[1], vt[2], vt[3])
            view.sync(db)
        except:
            pass


def main(argv):
    view_json = 'views.json'
    db_json = 'db.json'

    try:
        opts, args = getopt.getopt(argv, "v:d:", ['database=','view='])
    except getopt.GetoptError:
        print ("""-view <view_json>
                  -d <database_json>""")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("""-view <view_json>
                      -d <database_json>""")
            sys.exit()
        elif opt in ("-v", "--view"):
            view_json = arg
        elif opt in ("-d", "--database"):
            db_json = arg

    with open(view_json) as f:
        views = json.loads(f.read())
    view_tuples = [(v['doc'], v['view_name'], v['map_fun'], v['reduce_fun']) for v in views]

    with open(db_json) as f:
        db_info = f.read()
    db_info = json.loads(db_info)

    couch_user = db_info['user']
    couch_password = db_info['password']
    couch_host = db_info['host']
    couch_port = db_info['port']
    db_name = db_info['processed_database']
    host_and_port = "http://" + couch_user + ":" + couch_password + "@" + couch_host + ":" + str(couch_port)

    couch = couchdb.Server(host_and_port)
    try:
        db = couch.create(db_name)  # create db
    except:
        db = couch[db_name]  # existing
    create_view(db,view_tuples)

if __name__ == "__main__":
   main(sys.argv[1:])
