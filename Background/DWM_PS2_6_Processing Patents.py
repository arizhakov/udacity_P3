#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.
   
    with open(filename, 'r') as r:

        n = 0
        try:            
            for i, line in enumerate(r):
                if (line.startswith("<?xml")) and (n==0):
                    w = open("{}-{}".format(filename, n), 'w')
                    w.write(line)
                    n += 1
                elif (line.startswith("<?xml")) and (n>0):
                    w.close()
                    w = open("{}-{}".format(filename, n), 'w')
                    w.write(line)
                    n += 1
                else:
                    w.write(line)
        finally:
                w.close()
    pass


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()

'''
##http://code.activestate.com/recipes/578045-split-up-text-file-by-line-count/
with open(filepath, 'r') as r:
        name, ext = os.path.splitext(filename)
        try:
            w = open(os.path.join(path, '{}_{}{}'.format(name, 0, ext)), 'w')
            for i, line in enumerate(r):
                if not i % lpf:
                    #possible enhancement: don't check modulo lpf on each pass
                    #keep a counter variable, and reset on each checkpoint lpf.
                    w.close()
                    filename = os.path.join(path,
                                            '{}_{}{}'.format(name, i, ext))
                    w = open(filename, 'w')
                w.write(line)
        finally:
            w.close()
            
            
'''
'''
    
    #n=0
    f = open(filename, "r")
    
    for line in f:
        print line
    
    if f.readline().startswith("<?xml")
    
    f.close()
    
    for n in range(4):
        pass
    if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            
    
    
'''