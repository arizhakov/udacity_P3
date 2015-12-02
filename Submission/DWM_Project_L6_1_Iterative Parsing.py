#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Use iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.

count_tags function returns a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.
"""
import xml.etree.cElementTree as ET
#import pprint

def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        #print elem.tag
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    
    return tags

#'''
def test():

    tags = count_tags('sample_seattle_washington_15103014.osm')
    #pprint.pprint(tags)
    print "tags: ", tags

if __name__ == "__main__":
    test()
#'''

#print "tags: ", count_tags('sample_seattle_washington_15103014.osm')


