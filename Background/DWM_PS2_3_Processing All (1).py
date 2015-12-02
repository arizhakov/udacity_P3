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
    
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list 
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:
        soup = BeautifulSoup(html)
        doc1 = soup.find('table', {'class': 'dataTDRight'}).find_all('td')
        '''
        for i in soup.find('table', {'class': 'dataTDRight'}.find_all('td'):
            print i.index
            #if str(i.text)[0:3] != "All":
             #   data.append(i['value'])
        '''
        for i in range(len(doc1)):
            if i > 4:
                if i % 5 == 0:
                    info['year'] = str(doc1[i].text)
                if i % 5 == 1:
                    info['month'] = str(doc1[i].text)
                if i % 5 == 2:
                    info['flights'] = {}
                    info['flights']['domestic'] = str(doc1[i].text)
                if i % 5 == 3:
                    info['flights']['international'] = str(doc1[i].text)
                    data.append(info)
                    info = {}
                    info["courier"], info["airport"] = f[:6].split("-")
        
        
        for i in data:
            if i['month']=="TOTAL":
                data.remove(i)
       
        for i in data:
            i['month']=int(i['month'].replace(',',''))
            i['flights']['international']=int(i['flights']['international'].replace(',',''))
            i['flights']['domestic']=int(i['flights']['domestic'].replace(',',''))
            i['year']=int(i['year'].replace(',',''))

    return data


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
