#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
#import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

-> You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. 

1) You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
X you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    X attributes in the CREATED array should be added under a key "created"
    X attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
X if second level tag "k" value contains problematic characters, it should be ignored
X if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Highway", "Terrace", "Alley", "Bend", "Center", "Circle", "Close",
            "Crescent", "Plaza", "Way", "Loop", "Crest", "View", "Route", "Point"]

mapping = { "St": "Street",
            "ST": "Street",
            "St.": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "AVE": "Avenue",
            "Ave.": "Avenue",
            "avenue": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "N": "North",
            "NE": "Northeast",
            "E": "East",
            "SE": "Southeast",
            "S": "South",
            "S.": "South",
            "SW": "Southwest",
            "W": "West",
            "NW": "Northwest",
            "west": "West",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "boulevard": "Boulevard",
            "Ct": "Court",
            "Hwy": "Highway"
            }



def update_name(name, mapping):
    
    name_split = name.split()
    in_expected = False
    for i in name_split:
        if i in mapping.keys():
            name_split[name_split.index(i)] = mapping[i]
            in_expected = True
        elif i in expected:
            in_expected = True
    
    if not in_expected:
        name_split.append("Street")
    
    name = ' '.join(name_split)
    return name


def shape_element(element):
    node = {}
    node['created'] = {}
    node['pos'] = [0,0]

    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag
        for attr in element.attrib:
            if attr in CREATED:
                node['created'][attr] = element.attrib[attr]
            elif attr == 'lat':
                node['pos'][0] = float(element.attrib[attr])
            elif attr == 'lon':
                node['pos'][1] = float(element.attrib[attr])
            else:
                node[attr] = element.attrib[attr]
                
        for child in element:
            if child.tag == "tag":
                if 'address' not in node.keys():
                    node['address'] = {}
                if (problemchars.search(child.attrib['k']) == None):
                    if (child.attrib['k'][:5] == "addr:" and not (re.search(":", child.attrib['k'][5:]))):
                        if (child.attrib['k'][:11] == "addr:street"):
                            node['address'][child.attrib['k'][5:]] = update_name(child.attrib['v'], mapping)
                        else:
                            node['address'][child.attrib['k'][5:]] = child.attrib['v']
                    elif (child.attrib['k'][:5] != "addr:"):                 
                        node[child.attrib['k']] = child.attrib['v']
            if child.tag == "nd":
                if 'node_refs' not in node.keys():
                    node['node_refs'] = []
                node['node_refs'].append(child.attrib['ref'])       

        if ('address' in node.keys()):
            if node['address'] == {}:
                del node['address']

        return node
    else:
        return None

def process_map(file_in, pretty = False):
    '''
    Instructor Notes

    If you are using the process_map() procedure above on your own computer 
    to write to a JSON file, 
    make sure you call it with pretty = False parameter. 
    Otherwise, mongoimport might give you an error when you try to 
    import the JSON file to MongoDB.
    '''
    
    file_out = "{0}.json".format(file_in)
    data = []
    #count = 0
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            #count += 1
            #print "count: ", count
            #print element
            #print el
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    
    ##data = process_map('sample_seattle_washington_15103014.osm', False)
    #data = process_map('seattle_washington.osm', False) ### failed, due to memory. # check after restart.
    #data = process_map('sample_seattle_washington_15111515_every2.osm', False)
    data = process_map('sample_seattle_washington_15111609_every6.osm', False)
    #print data
    #pprint.pprint(data)


if __name__ == "__main__":
    test()