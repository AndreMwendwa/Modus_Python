# -*- coding: iso-8859-15 -*-
"""
Contains helper functions for the work with comma separated value (CSV) files
"""

import csv
from numpy.core.records import array


def readCSV(fileName, numpyRec=False, delimiter=","):
    """Reads a CSV file into a list
    10/20/07 updated for Python 2.5
    12/15/08 updated for numpy


    Read in a comma separated value text file into a list.
    The separator can be specified as well, which is useful for
    net files (semicolon separated).  Usually the first row of a csv
    file is the column names, but this is not required.  Each row is
    actually read in as a string, so the user might need to cast the
    values after this function call.  Optional argument numpyRec
    will return a numpy.records version (spreadsheet-like object),
    which requires the first row to be column names

    fileName - string - file name of csv file
    numpyRec - boolean - true or false to return numpy.records version, default false
    delimiter - string - delimiter, default is ",", but ";" is useful for net files

    return - list(list) - row lists

    A numpy.core.records array is returned instead, if numpy is imported before importing VisumPy.csvHelpers

    inFile = readCSV("c:/ids.csv")
    inFile = readCSV("c:/nodes.net", ";")
    """

    #Create file and csv reader
    f = open(fileName, "rt")

    #Change delimiter if required
    reader = csv.reader(f, delimiter=delimiter)

    #Read in rows and append to list
    y = []
    for x in reader:
        if x != []:
            y.append(x)

    #Return result as numarary.records if applicable
    if (numpyRec):
        y = array(y[1:len(y)], names=y[0])

    return y


def writeCSV(rowList, fileName, delimiter=","):
    """Writes a list of lists to a csv file
    10/20/07 updated for Python 2.5

    Writes a comma separated value text file from the list.
    The separator can be specified as well, which is useful for
    net files (semicolon separated).  Usually the first row of a csv
    file is the column names, but this is not required.

    rowList - list(list) - list of list of rows of table
    fileName - string - file name of csv file
    delimiter - string - delimiter, default is ",", but ";" is useful for net files

    return - null - null

    inFile = readCSV("c:/ids.csv")
    writeCSV(inFile, "c:/idsOut.csv")
    """

    #Create file and csv reader
    f = open(fileName, "wt")

    #Change delimiter if required
    writer = csv.writer(f, delimiter=delimiter)

    #Write rows and close
    writer.writerows(rowList)
    f.close()
