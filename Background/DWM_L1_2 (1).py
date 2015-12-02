#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    
    data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
    }
    
    #print sheet_data[1][1]
    
    data['maxvalue'] = sheet_data[1][1]
    data['maxtime'] = xlrd.xldate_as_tuple(sheet_data[1][0], 0)
    data['minvalue'] = sheet_data[1][1]
    data['mintime'] = xlrd.xldate_as_tuple(sheet_data[1][0], 0)
    data['avgcoast'] += data['avgcoast'] + sheet_data[1][1] 
    
    #print data['avgcoast']
    
    #print sheet.nrows-1
    
    for i in (range(2,sheet.nrows)):
        if (sheet_data[i][1]>data['maxvalue']):
            data['maxvalue'] = sheet_data[i][1]
            data['maxtime'] = xlrd.xldate_as_tuple(sheet_data[i][0], 0)
        if (sheet_data[i][1]<data['minvalue']):
            data['minvalue'] = sheet_data[i][1]
            data['mintime'] = xlrd.xldate_as_tuple(sheet_data[i][0], 0)
        data['avgcoast'] += sheet_data[i][1]
        #print data['avgcoast']
    data['avgcoast'] = data['avgcoast']/(sheet.nrows-1)
    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()

 ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:", 
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):", 
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):", 
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)

    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):", 
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)