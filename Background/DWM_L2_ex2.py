#!/usr/bin/env python
# Your task here is to extract data from xml on authors of an article
# and add it to a list, one item for an author.
# See the provided data structure for the expected format.
# The tags for first name, surname and email should map directly
# to the dictionary keys, but you have to extract the attributes from the "insr" tag
# and add them to the list for the dictionary key "insr"

'''
One way of solving the exercise is listed below. There are couple of things to note about this solution:

since the names and email for authors are unique for each author, we use "find". The text method can be used to get the value of the tag.
since "insr" can contain several values, we use "findall" and iterate the returned list.
we access the attributes of a tag by method "attrib" and using the attribute name "iid"
'''

import xml.etree.ElementTree as ET

article_file = "exampleResearchArticle.xml"


def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def get_authors(root):
    authors = []
    for author in root.findall('./fm/bibl/aug/au'):
        data = {
                "fnm": None,
                "snm": None,
                "email": None,
                "insr": []
                }

                
        data["fnm"] = author.find('fnm').text
        data["snm"] = author.find('snm').text
        data["email"] = author.find('email').text
        #data["insr"] = author.find('insr').text
        ID = author.findall('insr')
        for i in ID:
            data["insr"].append(i.attrib["iid"])
               
        authors.append(data)

    return authors


def test():
    solution = [{'insr': ['I1'], 'fnm': 'Omer', 'snm': 'Mei-Dan', 'email': 'omer@extremegate.com'},
                {'insr': ['I2'], 'fnm': 'Mike', 'snm': 'Carmont', 'email': 'mcarmont@hotmail.com'},
                {'insr': ['I3', 'I4'], 'fnm': 'Lior', 'snm': 'Laver', 'email': 'laver17@gmail.com'},
                {'insr': ['I3'], 'fnm': 'Meir', 'snm': 'Nyska', 'email': 'nyska@internet-zahav.net'},
                {'insr': ['I8'], 'fnm': 'Hagay', 'snm': 'Kammar', 'email': 'kammarh@gmail.com'},
                {'insr': ['I3', 'I5'], 'fnm': 'Gideon', 'snm': 'Mann', 'email': 'gideon.mann.md@gmail.com'},
                {'insr': ['I6'], 'fnm': 'Barnaby', 'snm': 'Clarck', 'email': 'barns.nz@gmail.com'},
                {'insr': ['I7'], 'fnm': 'Eugene', 'snm': 'Kots', 'email': 'eukots@gmail.com'}]

    root = get_root(article_file)
    data = get_authors(root)

    assert data[0] == solution[0]
    assert data[1]["insr"] == solution[1]["insr"]


test()