#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Task: explore the data a bit more.
    1) find out how many unique users have contributed to the map in this particular area!
    2) The function process_map should return a set of unique user IDs ("uid")

"""


def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        
        ''' uncomment for specific getting users of a specific tag type
        if element.tag == "node":
            users.add(element.get('user'))
        '''
        users.add(element.get('user'))

    return users


def test():

    users = process_map('sample_seattle_washington_15103014.osm')
    #print users
    pprint.pprint(users)
    #print len(users)
    #assert len(users) == 6
    

if __name__ == "__main__":
    test()


