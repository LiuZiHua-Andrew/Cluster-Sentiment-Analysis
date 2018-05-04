import couchdb,sys
from couchdb.design import ViewDefinition

couch=couchdb.Server('http://localhost:5984/')

print(couch)

db=couch['geocoded_tweets']

print(db)

designDocument='newDesignDocument'
viewName='polarity'
map_fun='''function(doc) { emit(doc.suburb, doc.polarity);};}'''
reduce_fun='''function(keys, values) { return sum(values)/values.length }'''

view=ViewDefinition(design=designDocument,name=viewName,
                    map_fun=map_fun,
                    reduce_fun=reduce_fun)

view.sync(db)

print('complete!')