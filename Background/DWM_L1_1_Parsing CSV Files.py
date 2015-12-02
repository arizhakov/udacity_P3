# Your task is to read the input DATAFILE line by line, and for the first 10 lines (not including the header)
# split each line on "," and then for each line, create a dictionary
# where the key is the header title of the field, and the value is the value of that field in the row.
# The function parse_file should return a list of dictionaries,
# each data line in the file being a single list entry.
# Field names and values should not contain extra whitespace, like spaces or newline characters.
# You can use the Python string method strip() to remove the extra whitespace.
# You have to parse only the first 10 data lines in this exercise,
# so the returned list should have 10 entries!
import os

DATADIR = ""
DATAFILE = "beatles-diskography.csv"


def parse_file(datafile):
    data = []
    count = 0
    TITLE = 0
    RELEASE = 0 
    LABEL = 0
    UK = 0
    US = 0
    BPI = 0
    RIAA = 0 
    with open(datafile, "r") as f:
        for line in f:
            dict1 = {}
            if (count == 0):
                TITLE,RELEASE,LABEL,UK,US,BPI,RIAA = line.strip().split(',')
                count += 1
            else:
                title,release,label,uk,us,bpi,riaa = line.strip().split(',')
                dict1[TITLE] = title
                dict1[RELEASE] = release
                dict1[LABEL] = label
                dict1[UK] = uk
                dict1[US] = us
                dict1[BPI] = bpi
                dict1[RIAA] = riaa                               
                
                data.append(dict1)
                count += 1
                        
            # first 10 lines
            if (count == 11):
                break
            
            

    return data


def test():
    # a simple test of your implemetation
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

    
test()