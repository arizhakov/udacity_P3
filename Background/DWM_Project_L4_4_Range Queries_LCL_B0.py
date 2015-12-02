#!/usr/bin/env python
"""
FINAL PROJECT

"""

#from datetime import datetime
import pprint

    
def make_query():
    query = {"address":{"$exists": True}}
    #query = {"type": "way"}
    return query


def make_pipeline():

    
    
    pipeline = [{"$match":{"address.postcode":{"$exists":1}}}, 
                {"$group":{"_id":"$address.postcode", "count":{"$sum":1}}}, 
                {"$sort":{"count":-1}}
                ]
    ## works!
    
    
    pipeline = [{"$match":{"address.city":{"$exists":1}}}, 
                {"$group":{"_id":"$address.city", "count":{"$sum":1}}}, 
                {"$sort":{"count":-1}}
                ]
    ## works!
    
    
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, 
                {"$sort":{"count":-1}}, 
                {"$limit":1}
                ]
    ## works!
    
    
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, 
                {"$group":{"_id":"$count", "num_users":{"$sum":1}}},
                {"$sort":{"_id":1}}, 
                {"$limit":1}
                ]
    ## works!
                
    ### Exploring amenities!!!
    #
    pipeline = [{"$match":{"amenity":{"$exists":1}}}, 
                {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
                {"$sort":{"count":-1}}, 
                {"$limit":10}
                ]
    #works!
                
    pipeline = [{"$match":{"amenity":{"$exists":1},"amenity":"place_of_worship"}}, 
                {"$group":{"_id":"$religion", "count":{"$sum":1}}},
                {"$sort":{"count":-1}}, 
                {"$limit":10}
                ]
    #works!
                
    pipeline = [{"$match":{"amenity":{"$exists":1},"amenity":"restaurant"}}, 
                {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
                {"$sort":{"count":-1}}, 
                {"$limit":10}
                ]
    
    
    
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.date151120.aggregate(pipeline)]

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.PROJECT
    return db


if __name__ == "__main__":
    print "====="
    
    db = get_db()
    #print "db: ", db
    
    print "--- test0: db statistics ---"   
    ### db statistics:
    #   ---------------------------------
    #pprint.pprint(db.command("dbstats"))   ### db stats
    #pprint.pprint(db.command("collstats", "date151030"))   ### coll stats
    
    #test0 = db.date151120.find().count()
    
    #print "db.date151120.find().count() ::: ", db.date151120.find().count()
    #print "db.char.find({type:node}).count() ::: ", db.date151120.find({"type":"node"}).count()
    #print "db.char.find({type:way}).count() ::: ", db.date151120.find({"type":"way"}).count()
    #print "len(db.date151120.distinct(created.user)) ::: ", len(db.date151120.distinct("created.user"))
    
    
    #   ---------------------------------
    
    
    print "--- test 1: simple query ---"    
        
    query = make_query()
    test1 = db.date151120.find(query)[0]
    
    '''
    for i in range(0,5):
        print db.date151030.find(query)[i] 
        print "-"
    '''
    #test1 = db.date151030.find(query)[20]   
    
    #pprint.pprint(test1)
    
    
    print "--- test 2: pipeline aggregate ---" 
    
    pipeline = make_pipeline()
    #print pipeline
    #test2 = make_aggregate(db, pipeline)[0]   '
    test2 = aggregate(db, pipeline) 
    #test2 = test2[0]
    
    '''
    for doc in db.date151030.aggregate(pipeline):
        print(doc)    
    '''
    


    pprint.pprint(test2)
    
    
    
    
    print "====="





##### XXXXXXXXXXXXXXXXX


'''
def make_aggregate(db, pipeline):
    result = db.tweets.aggregate(pipeline)
    return result
'''

'''
ARCHIVE:

pipeline = [{"$group": {"_id":"$type","count":{"$sum":1}}},
            {"$sort":{"count":-1}}]
            
            
pipeline = [{"$unwind":"$isPartOf"},
            {"$project":{"region":"$isPartOf","city":"$name","pop":"$population", "country":"$country"}}, 
            {"$group": {"_id":{"country":"$country","region":"$region"},
                        "avg_ofRegion":{"$avg":"$pop"}}},
            { "$group" : {"_id" : "$_id.country", 
                          "avgRegionalPopulation":{"$avg":"$avg_ofRegion"}}}  
            ]
'''
    
    