# -*- coding: iso-8859-15 -*-
"""
Contains helper functions for the calculation of the node orientation
"""

from VisumPy.helpers import GetMulti
import numpy
import VisumPy.csvHelpers


def turnValueByOrientation(Visum, attribute):
    """Create table of turn attribute by orientation for each active node

    This function creates a table of turn attributes by orientation (SBL, SBT, SBR, etc)
    The result is for each node a row with the node number and a column for each
    turn at that node.  It is limited to up to four legs.  The results of this
    function can be written to Excel with writeTableToExcelFile()

    Visum - visum object - visum object
    attribute - string - turn attribute name

    return - list(numarray.array, list) - column array and columns names list
    A numpy array is returned, if numpy is imported before importing VisumPy.reports

    turnVols = turnValueByOrientation(Visum, "VolVehPrT(AP)")
    """

    #Setup list structure of results - note 4 legs max at each node
    numTurnsPerNode = 4 * 4
    result = []

    #Build node turn data
    nodeIter = Visum.Net.Nodes.Iterator
    while nodeIter.Valid:

        #Get node and check if active
        node = nodeIter.Item
        if node.Active:

            #Get turns
            turns = node.ViaNodeTurns
            numTurns = len(turns.GetMultiAttValues("ViaNodeNo"))

            resultRow = numpy.repeat([0.0],numTurnsPerNode + 2) #node no and 4leg check extra

            if numTurns > 0:

                #Get orientation field
                if int(Visum.VersionNumber[0:2]) >= 11:
                    orientation = numpy.array(GetMulti(turns,"OrientationHBS"))
                else:
                    orientation = numpy.array(GetMulti(turns,"Orientation"))

                orientation = orientation.astype(numpy.int)

                #Get attribute value
                attributeValue = numpy.array(GetMulti(turns,attribute))

                #Set row of values
                resultRow[orientation + 1] = attributeValue
                resultRow[0] = node.AttValue("No")
                resultRow[1] = numTurns

            result.append(resultRow)

        #Next node
        nodeIter.Next()

    #List of attribute names
    attributesList = ["No","NumTurns","EBU","EBL","EBT","EBR","NBU","NBL","NBT","NBR","WBU","WBL","WBT","WBR","SBU","SBL","SBT","SBR"]

    #Return result
    return [numpy.transpose(result),attributesList]


def networkObjectAttributeList(networkObjectCollection, attributesList):
    """Create a list of columns of attributes for a network object

    The results of this function can be written to Excel with writeTableToExcelFile()

    networkObjectCollection - object - network object collection such as Nodes or Zones
    attributesList - list(String) - columns names list

    return - list(list, list) - column lists and columns names list

    attributes = ["Name","VehHourTravPrT(AP)","VehMiTravPrT(AP)","PassMiTrav(AP)","PassHourTrav(AP)"]
    result = networkObjectAttributeList(Visum.Net.Territories, attributes)
    writeTableToExcelFile(result[0], result[1], "c:/territoryIndicators.xls")
    """

    #Get attributes
    values = list()
    for i in range(0, len(attributesList)):

        attributeValues = GetMulti(networkObjectCollection,attributesList[i])
        values.append(attributeValues)

    #Return list
    return [values,attributesList]


def readTurnValueByOrientationFromCSV(Visum, fileName, targetAttribute):
    """read a numeric turn attribute from csv file based on node orientation
    works for up to 4 leg intersections based on turn ORIENTATION field
    A csv file should like the following, with "No" equal to node number:

    No,EBU,EBL,EBT,EBR,NBU,NBL,NBT,NBR,WBU,WBL,WBT,WBR,SBU,SBL,SBT,SBR
    10200,0,0,503.112,0,0,0,0,0,0,0,616.258,0,0,0,0,0
    10202,0,0,462.941,62.537,0,0.958,0,36.502,0,360.703,252.087,0,0,0,0,0
    10203,0,183.951,243.254,5.147,0,5.737,681.442,221.088,0,0,240.8,6.627,0,55.067,660.363,0
    12329,0,0,0,0,0,152.507,183.032,0,0,182.756,1120.336,296.722,0,0,410.495,16.527

    Visum - COM object - Visum object
    fileName - string - filename of csv file
    targetAttribute - string - a numeric turn attribute to put data in
    """

    #function to map turn orientation to turn orientation enum
    def swap(item):
        orientValues = dict()
        orientValues[0] = "NA"
        orientValues[1] = "EBU"
        orientValues[2] = "EBL"
        orientValues[3] = "EBT"
        orientValues[4] = "EBR"
        orientValues[5] = "NBU"
        orientValues[6] = "NBL"
        orientValues[7] = "NBT"
        orientValues[8] = "NBR"
        orientValues[9] = "WBU"
        orientValues[10] = "WBL"
        orientValues[11] = "WBT"
        orientValues[12] = "WBR"
        orientValues[13] = "SBU"
        orientValues[14] = "SBL"
        orientValues[15] = "SBT"
        orientValues[16] = "SBR"
        return (orientValues[int(item[1])],item[0])

    #read csv file
    csvData = VisumPy.csvHelpers.readCSV(fileName)

    #reset filter
    Visum.InitAllFilter()

    #for each node build a dict of each turn movement
    for i in range(1, len(csvData)):

        #need to flip tuples and change to strings
        turnsAtNode = Visum.Net.Nodes.ItemByKey(int(csvData[i][0])).ViaNodeTurns
        if int(Visum.VersionNumber[0:2]) >= 11:
            keyvaluepairs = turnsAtNode.GetMultiAttValues("ORIENTATIONHBS")
        else:
            keyvaluepairs = turnsAtNode.GetMultiAttValues("ORIENTATION")

        if len(keyvaluepairs) > 0:
            orientations = dict(map(swap, keyvaluepairs))
            targetAttributeData = map(list,turnsAtNode.GetMultiAttValues(targetAttribute))

            #loop through each turn
            for j in range(1,len(csvData[i])):
                if orientations.has_key(csvData[0][j]):
                    targetAttributeData[orientations[csvData[0][j]] - 1][1] = float(csvData[i][j])
            turnsAtNode.SetMultiAttValues(targetAttribute, targetAttributeData)
