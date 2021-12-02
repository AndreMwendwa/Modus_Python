# -*- coding: iso-8859-15 -*-
"""
Contains helper functions for the work with matrix
"""
import numpy as numpackage
numpackage.seterr(invalid ='ignore')

import VisumPy.helpers
import struct
import zlib
import os, os.path
from heapq import nsmallest

def rowSums(mat):
    """Returns the row sums of the matrix


    mat - numpy.array - matrix

    return - numpy.array - vector of row sums
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    x = numpy.array([1,2,3,4],shape=[2,2])
    rowSums(x)
    """
    return numpackage.sum(mat, 1)

def colSums(mat):
    """Returns the column sums of the matrix

    mat - numpy.array - matrix

    return - numpy.array - vector of column sums
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    x = numpy.array([1,2,3,4],shape=[2,2])
    colSums(x)
    """
    return numpackage.sum(mat, 0)


def calcIntrazonal(mat, factor = 0.5, numNeighbors = 1):
  """Set diagonal of matrix as factor * average of nearest numNeighbors zones.
     The diagonal value for zone i is calculated from the numNeighbors smallest
     elements both in row i and column i.

  mat - numpy.array - matrix
  factor - float - scaling factor for value of nearest zones
  numNeighbors - integer - number of neighbors used (1 <= numNeighbors < number of zones)

  return - numpy.array - adjusted matrix
  A numpy array is returned, if numpy is imported before importing VisumPy.matrices

  x = numpy.array([1,2,3,4],shape=[2,2])
  x = calcIntrazonal(x, 0.5)
  x = calcIntrazonal(x, numNeighbors=3)
  """

  def avg(seq):
    return sum(seq) / len(seq)

  #Copy matrix
  mat = mat.copy()

  #Check k
  if type(numNeighbors) != type(1):
      raise Exception("Parameter numNeighbors must be integer.")
  numNeighbors = max(numNeighbors, 1) #minimum one neigbour

  #Set intrazonal
  if numNeighbors == 1:
      for i in range(0, len(mat[0])):
        mat[i, i] = 0
        if max(mat[i]) > 0:
          byrow = min(mat[i][mat[i] > 0]) * factor
        else:
          byrow = 0
        if max(mat[:, i]) > 0:
          bycol = min(mat[:, i][mat[:, i] > 0]) * factor
        else:
          bycol = 0
        mat[i, i] = min(byrow, bycol)
      return mat
  else:
      for i in range(0, len(mat[0])):
        mat[i, i] = 0
        if max(mat[i]) > 0:
          byrow = avg(nsmallest(numNeighbors, mat[i][mat[i] > 0])) * factor
        else:
          byrow = 0
        if max(mat[:, i]) > 0:
          bycol = avg(nsmallest(numNeighbors, mat[:, i][mat[:, i] > 0])) * factor
        else:
          bycol = 0
        mat[i, i] = min(byrow, bycol)
      return mat


def addVector(mat, vector, byrow = True):
    """Add vector by row or by column to matrix

    mat - numpy.array - matrix
    vector - numpy.array - row or column vector (array) to add to matrix
    byrow - bool - replicate by row or by column, default is byrow=True

    return - numpy.array - adjusted matrix
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    x = numpy.array([1,2,3,4],shape=[2,2])
    y = numpy.array([1,2])
    z = addVector(x, y)
    """

    #Copy matrix
    mat = mat.copy()

    #Add vector
    if byrow:
        mat = numpackage.add(mat, vector)
    else:
        mat = numpackage.transpose(numpackage.add(numpackage.transpose(mat), vector))
    return mat


def unique(vector):
    """Unique items in a vector

    vector - numpy.array - array of items

    return - numpy.array - unique items array
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    unique(numpy.array([1,2,2,3,4,5,5]))
    """
    return numpackage.array(list(set(vector)))



def rmse(arrayOne, arrayTwo):
    """Root Mean Square Error

    arrayOne - numpy.array or numpy.array - array one
    arrayTwo - numpy.array or numpy.array - array two

    return - float - Root Mean Square Error between the two arrays

    x = numpy.array([1,2,2,3,4,5,5])
    y = numpy.array([10,5,3,6,2,5,5])
    rmse(x,y)
    """
    rmse = (numpackage.sum((arrayOne.ravel() - arrayTwo.ravel()) ** 2) / (len(arrayTwo.ravel()) - 1)) ** 0.5
    return rmse


def prmse(arrayOne, arrayTwo):
    """Percent Root Mean Square Error

    arrayOne - numpy.array  or numpy.array- array one
    arrayTwo - numpy.array  or numpy.array- array two

    return - float - Percent Root Mean Square Error between the two arrays

    x = numpy.array([1,2,2,3,4,5,5])
    y = numpy.array([10,5,3,6,2,5,5])
    prmse(x,y)
    """

    calcRmse = rmse(arrayOne, arrayTwo)
    prmse = calcRmse * len(arrayOne.ravel()) / numpackage.sum(arrayTwo.ravel())
    return prmse


def aggregateMatrix(mat, mainZones, function = sum):
    """Aggregates a matrix by mainZones by the input function

    mat - numpy.array - matrix
    mainZones - numpy.array - for each matrix row, a corresponding main zone code
    function - function - Python function such as min, max, sum, len, default is sum

    return - numpy.array - mainZone matrix
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    x = numpy.array([1,2,3.,4,6,7,8,9,10],shape=[3,3])
    y = [1,2,2] #main zone for each zone
    aggregateMatrix(x,y,sum)
    aggregateMatrix(x,y,min)
    """
    if (numpackage.all(numpackage.array(len(mainZones)) == numpackage.array(mat.shape))):

        #Get unique district codes and create outMat
        mainZones = numpackage.array(mainZones)
        umainZones = unique(mainZones)
        umainZones.sort()

        noZoneIndexArray = numpackage.where(umainZones == 0.0)
        umainZones = numpackage.delete(umainZones, noZoneIndexArray)

        outMat = numpackage.zeros([len(umainZones), len(umainZones)], dtype = numpackage.float64)
        rowMat = numpackage.zeros([len(mainZones), len(umainZones)], dtype = numpackage.float64)

        #Collapse rows
        for i in range(0, len(mat[0])):
            for j in range(0, len(umainZones)):
                rowMat[i, j] = function(mat[i][mainZones == umainZones[j]])

        #Collapse columns
        for i in range(0, len(umainZones)):
            for j in range(0, len(umainZones)):
                outMat[j, i] = function(rowMat[:, i][mainZones == umainZones[j]])

        return outMat

    else:
        return None

def balanceMatrix(mat, rowTargets, colTargets, iterations = 25, closePctDiff = 0.0001):
    """Balance a matrix to row and column totals
    10/20/07 allows rows and columns of the seed matrix to sum to 0
    12/17/07 allows rows and columns of the seed matrix to sum to 0 corrected
    6/10/09 row /column targets may be zero

    This procedure is also known as IPF (iterative proportional fitting) and Furness
    See balanceMatrixFromZoneAttributes for an easy-to-use wrapper of this function

    mat - numpy.array - matrix
    rowTargets - numpy.array - vector of row targets
    colTargets - numpy.array - vector of column targets
    iterations - int - number of iterations, default 25
    closePctDiff - float - percent difference allowed for closure, default 0.0001

    return - numpy.array - (un)balanced matrix
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    mat = numpy.array([0,80.,120,200,60,0,100,140,110,40,0,50,80,270,250,0],shape=(4,4))
    r = numpy.array([500,450,250,800])
    c = numpy.array([300,500,600,600])
    balanceMatrix(mat,r,c)
    """

    #Copy matrix
    mat = mat.copy()

    #Check feasibility
    if abs(rowTargets.sum() - colTargets.sum()) > closePctDiff :
        raise ValueError, "0" #"Sum of row targets does not equal sum of col targets --> infeasible!"
    rowSums = numpackage.sum(mat, 1)
    if not numpackage.all(rowSums[rowTargets > 0] > 0):
        raise ValueError, "1" #"Some rows with non-zero targets are all zero --> infeasible!"
    colSums = numpackage.sum(mat, 0)
    if not numpackage.all(colSums[colTargets > 0] > 0):
        raise ValueError, "2" #"Some columns with non-zero targets are all zero --> infeasible!"

    #Balancing Loop
    k = 0
    notClosed = True
    while (k < iterations and notClosed):

        coeff = []

        #Calculate and apply row scaling factor
        rowSums = numpackage.sum(mat, 1)
        rowCoeff = rowTargets / rowSums
        rowCoeff[rowSums == 0] = 0
        coeff.extend(rowCoeff[rowSums > 0])

        mat = numpackage.transpose(numpackage.transpose(mat) * rowCoeff)

        #Calculate and apply col scaling factor
        colSums = numpackage.sum(mat, 0)
        colCoeff = colTargets / colSums
        colCoeff[colSums == 0] = 0
        coeff.extend(colCoeff[colSums > 0])

        mat = mat * colCoeff


        if numpackage.all(abs(1 - numpackage.array(coeff)) < closePctDiff):
            notClosed = False

        #Iterate loop
        k = k + 1

    #Return (un)balanced matrix
    return mat


def balance3DMatrix(mat, rowTargets, colTargets, depTargets, iterations = 25, closePctDiff = 0.0001):
    """Balance a 3D matrix (array) to 3 dimensions (rows, columns, and a 3rd dimension totals)
    10/20/07 allows dimension sums of the seed matrix to sum to 0
    12/17/077 allows rows and columns of the seed matrix to sum to 0 corrected

    This procedure is also known as IPF (iterative proportional fitting) and Furness

    mat - numpy.array - 3D matrix (array)
    rowTargets - numpy.array - vector of row targets
    colTargets - numpy.array - vector of column targets
    depTargets - numpy.array - vector of 3rd dimension targets
    iterations - int - number of iterations, default 25
    closePctDiff - float - percent difference allowed for closure, default 0.0001

    return - numpy.array - (un)balanced 3D matrix
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    mat = numpy.array([0.0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],shape=(4,3,2))
    r = numpy.array([40,120,180,260])
    c = numpy.array([160,200,240])
    d = numpy.array([280,320])
    balance3DMatrix(mat,r,c,d,25,0.05)
    """

    #Copy matrix
    mat = mat.copy()

    #Balancing Loop
    k = 0
    notClosed = True
    while (k < iterations and notClosed):

        #Calculate and apply row scaling factor
        rowSums = numpackage.sum(numpackage.sum(mat, 2), 1)
        rowSums[rowSums == 0] = 0.0001
        rowCoeff = rowTargets / rowSums

        for i in range(0, len(rowTargets)):
            mat[i, :, :] = mat[i, :, :] * rowCoeff[i]

        #Calculate and apply col scaling factor
        colSums = numpackage.sum(numpackage.sum(mat, 2), 0)
        colSums[colSums == 0] = 0.0001
        colCoeff = colTargets / colSums

        for i in range(0, len(colTargets)):
            mat[:, i, :] = mat[:, i, :] * colCoeff[i]

        #Calculate and apply dep scaling factor
        depSums = numpackage.sum(numpackage.sum(mat, 0), 0)
        depSums[depSums == 0] = 0.0001
        depCoeff = depTargets / depSums

        for i in range(0, len(depTargets)):
            mat[:, :, i] = mat[:, :, i] * depCoeff[i]

        #Check closure
        coeff = []
        coeff.extend(rowCoeff)
        coeff.extend(colCoeff)
        coeff.extend(depCoeff)
        if numpackage.all(abs(1 - numpackage.array(coeff)) < closePctDiff):
            notClosed = False

        #Iterate loop
        k = k + 1

    #Return (un)balanced matrix

    return mat


def setDiagonalFromZoneAttribute(Visum, mat, zoneAttr):
    """Sets the diagonal of a matrix from a zone attribute

    Visum - COM object - Visum object
    mat - numpy.array - matrix
    zoneAttr - zone attribute name - string
    return - numpy.array - matrix
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices

    import VisumPy.helpers
    x = setDiagonalFromZoneAttribute(Visum, VisumPy.helpers.GetSkimMatrix(Visum, 1), "ADDVAL1")
    VisumPy.helpers.SetSkimMatrix(Visum, 1, x)
    """

    #Copy matrix
    mat = mat.copy()

    #get attr and set diagonal
    attr = VisumPy.helpers.GetMulti(Visum.Net.Zones, zoneAttr)
    mat[numpackage.identity(mat.shape[0], dtype = numpackage.bool)] = attr

    return mat

def setZoneAttributeFromDiagonal(Visum, mat, zoneAttr):
    """Sets a zone attribute from the diagonal of a matrix

    Visum - COM object - Visum object
    mat - numpy.array - matrix
    zoneAttr - zone attribute name - string
    return - null - null

    import VisumPy.helpers
    x = VisumPy.helpers.GetODMatrix(Visum, 1)
    setZoneAttributeFromDiagonal(Visum, x, "ADDVAL1")
    """

    #get diagonal and set zone attribute
    diag = mat.diagonal()
    VisumPy.helpers.SetMulti(Visum.Net.Zones, zoneAttr, diag)

def balanceMatrixFromZoneAttributes(Visum, matNum, rowAttName, colAttName, iterations = 25, closePctDiff = 0.0001):
    """Balances a matrix from zone attributes for row and column totals
    This function modifies the matrix in VISUM so you probably want to make a copy first
    This function is a wrapper around the balanceMatrix function

    Visum - COM object - Visum object
    matNum - integer - OD matrix number in VISUM
    rowAttName - string - zone attribute for row target
    colAttName - string - zone attribute for column target
    iterations - int - number of iterations, default 25
    closePctDiff - float - percent difference allowed for closure, default 0.0001
    return - null - null

    balanceMatrixFromZoneAttributes(Visum, 1, "ADDVAL1", "ADDVAL2")
    """
    mat = VisumPy.helpers.GetODMatrix(Visum, matNum)
    r = VisumPy.helpers.GetMulti(Visum.Net.Zones, rowAttName)
    c = VisumPy.helpers.GetMulti(Visum.Net.Zones, colAttName)
    result = balanceMatrix(mat, numpackage.array(r), numpackage.array(c))

    VisumPy.helpers.SetODMatrix(Visum, matNum, result)

def readBIMatrixWithHeader(fileName):
    """Function to read in a BI packed matrix with header

    Internal function used by readBIMatrix

    fileName - string - fileName
    return - numpy matrix - matrix
    A numpy array is returned, if numpy is imported before importing VisumPy.matrices
    """
    def checkBinFlag(file, name):
        binFlag = file.read(1)
        if binFlag == '\x01':
            return 1
        elif binFlag == '\x00':
            return 0
        else:
            file.close()
            raise Exception("Flag of %s doesn't exist." % name)

    def skipColumnNames(file, idvalue, colNumber):
        if idvalue[2] >='K':
            # read row names and column names
            for i in range(0, colNumber):
                itemLenght = struct.unpack("l", file.read(4))[0]
                if itemLenght > 0:
                    itemValue = struct.unpack(str(itemLenght * 2) + "c", file.read(itemLenght * 2))
    #open matrix
    if not os.path.exists(fileName):
        raise Exception("File with name %s doesn't exist." % fileName)

    file = open(fileName, "rb")
    #read in header info
    idlength = file.read(2)
    idvalue = file.read(struct.unpack("h", idlength)[0])
    headerlength = file.read(2)
    headervalue = file.read(struct.unpack("h", headerlength)[0])
    transportvalue = struct.unpack("i", file.read(4))[0]
    starttime = struct.unpack("f", file.read(4))[0]
    endtime = struct.unpack("f", file.read(4))[0]
    factor = struct.unpack("f", file.read(4))[0]
    rows = struct.unpack("l", file.read(4))[0]
    numCols = rows
    datatype = struct.unpack("h", file.read(2))[0]
    roundproc = checkBinFlag(file, "round procedure")

    if idvalue == "$BI":
        zonenums = struct.unpack(str(rows) + "l", file.read(rows * 4))
    else:
        numCols = struct.unpack("l", file.read(4))[0]
        zonenums = struct.unpack(str(rows) + "l", file.read(rows * 4))
        zonenumsCol = struct.unpack(str(numCols) + "l", file.read(numCols * 4))
        skipColumnNames(file, idvalue, numCols + rows)

    #for whole matrix
    allnull = checkBinFlag(file, "all null")

    if allnull == 0:
        diagsum = struct.unpack("d", file.read(8))[0]

        #for each zone
        datavalues = []
        rowsum = []
        colsum = []
        for i in zonenums:
            compresslength = struct.unpack("l", file.read(4))[0]
            data = file.read(compresslength)
            recordList = list(struct.unpack(str(numCols) + "d", zlib.decompress(data)))
            datavalues.append(recordList)
            if idvalue[2] < 'L':
                rowsum.append(struct.unpack("d", file.read(8))[0])
                colsum.append(struct.unpack("d", file.read(8))[0])

        if idvalue[2] >= 'L':
            # for this format the row and colsums are written as a vector each
            data = file.read(8*rows)
            rowsum = list(struct.unpack(str(rows) + "d", data))
            # same for cols
            data = file.read(8*numCols)
            colsum = list(struct.unpack(str(numCols) + "d", data))
    else:
        diagsum = 0
        datavalues = numpackage.zeros([len(zonenums), len(zonenums)], dtype = numpackage.float64).tolist()
        rowsum = numpackage.zeros([len(zonenums)], dtype = numpackage.float64).tolist()
        colsum = numpackage.zeros([len(zonenums)], dtype = numpackage.float64).tolist()

    #End of file
    if file.read() == '':

        #Close connection and return data
        file.close()

        result = {} #dictionary object
        result['id'] = idvalue
        result['header'] = headervalue
        result['transport'] = transportvalue
        result['starttime'] = starttime
        result['endtime'] = endtime
        result['factor'] = factor
        result['rows'] = rows
        result['cols'] = numCols
        result['datatype'] = datatype
        result['roundproc'] = roundproc
        result['zonenums'] = zonenums
        result['allnull'] = allnull
        result['diagsum'] = diagsum
        result['datavalues'] = datavalues
        result['rowsum'] = rowsum
        result['colsum'] = colsum
        return result
    else:
        file.close()
        raise Exception("Read the binary matrix is failed." % fileName)

def writeBIMatrixWithHeader(input, fileName):
    """Function to write a BI packed matrix with header

    Internal function used by writeBIMatrix

    input - list - matrix data and header
    fileName - string - fileName
    return - null - null
    """

    #open matrix

    file = open(fileName, "wb")
    if len(input['rowsum']) != len(input['colsum']):
        file.close()
        msg = "The number of row %d is not equal with the number of columns %d. The matrix has to be symmetrical!"  %(len(input['rowsum']), len(input['colsum']))
        raise Exception(msg)

    #create header string
    header = "\nMuuli-Matrix im gepackten Binary format.\nBezirke: " + \
    str(input['rows']) + " \nVarTyp: 5 \nGesamtsumme: " + \
    str(sum(input['colsum'])) + " \nDiagonalsumme: " + \
    str(input['diagsum']) + " \nVMittel: " + str(input['transport']) + \
    " \nvon: " + str(input['starttime']) + " \nbis: " + \
    str(input['endtime']) + " \nFaktor: " + str(input['factor']) + " \n"
    headerlength = len(header)
    #write header info
    file.write(struct.pack("h", 3))
    file.write(struct.pack("3s", "$BI"))
    file.write(struct.pack("h", headerlength))
    file.write(struct.pack(str(headerlength) + "s", header))

    #write additional header info
    file.write(struct.pack("i", input['transport']))
    file.write(struct.pack("f", input['starttime']))
    file.write(struct.pack("f", input['endtime']))
    file.write(struct.pack("f", input['factor']))
    file.write(struct.pack("l", input['rows']))
    file.write(struct.pack("h", input['datatype']))

    if input['roundproc'] == 1:
        file.write("\x01")
    else:
        file.write("\x00")

    #for each row
    for i in range(0, len(input['zonenums'])):
        file.write(struct.pack("l", input['zonenums'][i]))

    #for whole matrix
    if input['allnull'] == 1:
        file.write("\x01")
    else:
        file.write("\x00")

    file.write(struct.pack("d", input['diagsum']))

    #for each zone
    import array
    for i in range(0, len(input['zonenums'])):
        dataArray = array.array('d', list(input['datavalues'][i]))
        data = zlib.compress(dataArray.tostring())
        file.write(struct.pack("l", len(data)))
        file.write(data)
        file.write(struct.pack("d", input['rowsum'][i]))
        file.write(struct.pack("d", input['colsum'][i]))
    #Close connection and return data
    file.close()


def toNumArray(matList):
    """Convert BI list to numpy array

    Internal function used by readBIMatrix

    matList - list - matrix and header
    return - numpy matrix - matrix
    """

    rowdim = matList['rows']
    coldim = matList['cols']
    newArray = numpackage.array(matList['datavalues'])
    newArray = numpackage.reshape(newArray, (rowdim, coldim))
    return newArray

def fromNumArray(nArray, zoneNums):
    """Convert numpy to BI list

    Internal function used by writeBIMatrix

    nArray - numpy matrix - matrix
    zoneNums - list - list of zone numbers
    return - list - matrix with header
    """
    result = {} #dictionary object
    result['id'] = '$BI'
    result['transport'] = 0
    result['starttime'] = 0
    result['endtime'] = 24
    result['factor'] = 1
    result['rows'] = len(nArray)
    result['datatype'] = 5
    result['roundproc'] = 1
    result['zonenums'] = zoneNums
    result['allnull'] = 0
    result['diagsum'] = nArray.diagonal().sum()
    result['datavalues'] = nArray.tolist()
    result['rowsum'] = numpackage.sum(nArray, 1)
    result['colsum'] = numpackage.sum(nArray, 0)
    return result

def readBIMatrix(fileName):
    """Simple reading of a BI Matrix to a numpy matrix

    fileName - string - fileName
    return - numpy matrix - matrix

    x = readBIMatrix("c:/test.mtx")
    writeBIMatrix(x,[1,2,3],"c:/testout.mtx")

    If you need info in the matrix header (such as zone nums), then
    you can use the read/write with header functions.
    """
    return toNumArray(readBIMatrixWithHeader(fileName))

def writeBIMatrix(nArray, zoneNums, fileName):
    """Simple writing of a BI Matrix from a numpy matrix

    nArray - numpy matrix - matrix
    zoneNums - list - list of zone numbers
    fileName - string - fileName
    return - null - null

    x = readBIMatrix("c:/test.mtx")
    writeBIMatrix(x,[1,2,3],"c:/testout.mtx")

    If you need info in the matrix header (such as zone nums), then
    you can use the read/write with header functions.
    """
    writeBIMatrixWithHeader(fromNumArray(nArray, zoneNums), fileName)
