#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
# This is example of the datastructure you should return
# Each item in the list should be a dictionary containing all the relevant data
# Note - year, month, and the flight data should be integers
# You should skip the rows that contain the TOTAL data for a year
# data = [{"courier": "FL",
#         "airport": "ATL",
#         "year": 2012,
#         "month": 12,
#         "flights": {"domestic": 100,
#                     "international": 100}
#         },
#         {"courier": "..."}
# ]
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """This is example of the data structure you should return.
    Each item in the list should be a dictionary containing all the relevant data
    from each row in each file. Note - year, month, and the flight data should be 
    integers. You should skip the rows that contain the TOTAL data for a year
    data = [{"courier": "FL",
            "airport": "ATL",
            "year": 2012,
            "month": 12,
            "flights": {"domestic": 100,
                        "international": 100}
            },
            {"courier": "..."}
    ]
    """
    #print "file name is: ", f
    
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list 
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html)
        doc1 = soup.find('table', {'class': 'dataTDRight'}).find_all('td')
        #print len(data)
        '''
        for i in soup.find('table', {'class': 'dataTDRight'}.find_all('td'):
            print i.index
            #if str(i.text)[0:3] != "All":
             #   data.append(i['value'])
        '''
        #print data
        for i in range(len(doc1)):
            if i > 4:
                #print i, info
                
                #print i, info
                if i % 5 == 0:
                    info['year'] = str(doc1[i].text)
                    #print i, info
                if i % 5 == 1:
                    info['month'] = str(doc1[i].text)
                    #print i, info
                if i % 5 == 2:
                    info['flights'] = {}
                    info['flights']['domestic'] = str(doc1[i].text)
                    #print i, info
                if i % 5 == 3:
                    #print i, info
                    info['flights']['international'] = str(doc1[i].text)
                    #print i, info
                    data.append(info)
                    #print data
                    #clear 'info'
                    info = {}
                    info["courier"], info["airport"] = f[:6].split("-")
                    #info
                    #print i, info
        #'''
        for i in range(len(data)):
            #
            if data[i]['month']=="TOTAL":
                data.pop(i)
            #print info
            
            #print data[0:2]
         #'''           
        
            #print i, data[i]
        #print data[0:5]
        #print info
        #print str(data[len(data)-1].text)
        #print str(data[1*5+(5 % 5)].text)
        #print "\n"
        #print len(data)
        #print data

    return data

'''
>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup(unicodestring_containing_the_entire_htlm_doc)
>>> table = soup.find('table', {'class': 'details'})
>>> th = table.find('th', text='Issued on:')
>>> th
<th>Issued on:</th>
>>> td = th.findNext('td')
'''

def test():
    print "Running a simple test..."
    open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
        
    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == 'FL'
    assert data[0]["month"] == 10
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}
    
    print "... success!"
'''
if __name__ == "__main__":
    test()
'''

#Local processes
#process_file('data/FL-ATL.html')
a = process_file('FL-ATL.html')

''' 
>>>15092510 sandbox
print "\n"
print len(a)
print "old a: ", a 

#print "a[0]", a[3]['month']

for i in range(len(a)):
    #print i
    #print "a['month']", a['month']
    if a[i]['month']=="TOTAL":
        a.pop(i)

print "\n"
print len(a)
print "new a: ", a 
'''
