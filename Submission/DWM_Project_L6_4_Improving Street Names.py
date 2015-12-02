"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


OSMFILE = "sample_seattle_washington_15103014.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

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


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                #print tag.attrib['k'], "; ", tag.attrib['v']  ### can audit on these fields if needed
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    
    name_split = name.split()
    in_expected = False
    for i in name_split:
        #print i
        if i in mapping.keys():
            #print i
            name_split[name_split.index(i)] = mapping[i]
            in_expected = True
        elif i in expected:
            in_expected = True
    
    if not in_expected:
        name_split.append("Street")
    
    name = ' '.join(name_split)
    return name



def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))
    print "st_types:: " #, st_types
    pprint.pprint(dict(st_types))
    print "LENGTH st_types:: ", len(st_types)

    for st_type, ways in st_types.iteritems():
        for name in ways:
            print "st_type: ", st_type   # used in getting each street type, to check for invalid types and then add to mapping.
            better_name = update_name(name, mapping)
            print name, "===>", better_name
    
    
    #print "NEW st_types:: " #, st_types
    #pprint.pprint(dict(st_types))


if __name__ == '__main__':
    test()