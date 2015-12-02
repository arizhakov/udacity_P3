#!/usr/bin/env python
"""
FINAL PROJECT

"""

#from datetime import datetime
    
def make_query():
    #query = {"type":{"$exists": True}}
    query = {"type": "way"}
    return query


def make_pipeline():
    '''
    pipeline = [{"$group": {"_id":"$type","count":{"$sum":1}}},
                {"$sort":{"count":-1}}]
    '''
    pipeline = [{"$group": {"_id":"$type","count":{"$sum":1}}},
                {"$sort":{"count":-1}}]
    return pipeline


def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.PROJECT
    return db


if __name__ == "__main__":
    db = get_db()
    print "====="
    #print "db: ", db
    #print "-----"   
    query = make_query()
    #test = db.date151030.find()[10]
    for i in range(0,5):
        print db.date151030.find(query)[i] 
        print "-"
    #test1 = db.date151030.find(query)[20]    
    
    pipeline = make_pipeline()
    #test2 = make_aggregate(db, pipeline)[0]   '
    test2 = db.date151030.aggregate(pipeline) 
    #test2 = test2[0]
    
    '''
    for doc in db.date151030.aggregate(pipeline):
        print(doc)    
    '''
    
    print "test1:", test1
    print "-----"
    #print "test2:", test2
    print "-----"
    print "====="



'''
def make_aggregate(db, pipeline):
    result = db.tweets.aggregate(pipeline)
    return result
'''