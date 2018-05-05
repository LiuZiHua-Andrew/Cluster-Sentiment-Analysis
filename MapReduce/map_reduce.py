import couchdb,sys
from couchdb.design import ViewDefinition

couchServer=couchdb.Server('http://localhost:5984/')
database='geocoded_tweets'
designDocument='newDesignDocument'
viewName='polarity'
map_fun='''function(doc) { emit(doc.suburb, doc.polarity);};}'''
reduce_fun='''function(keys, values) { return sum(values)/values.length }'''

def map_reduce(couchServer,database,designDocument,viewName,map_fun,reduce_fun):
    couch=couchServer
    print(couch)

    db=couch[database]
    print(db)

    designDocument=designDocument
    viewName=viewName
    map_fun=map_fun
    reduce_fun=reduce_fun
    view=ViewDefinition(design=designDocument,name=viewName,
                        map_fun=map_fun,
                        reduce_fun=reduce_fun)
    view.sync(db)
    print('complete!')
map_reduce(couchServer,database,designDocument,viewName,map_fun,reduce_fun)