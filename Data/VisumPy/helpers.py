# -*- coding: iso-8859-15 -*-
"""
Contains the functions for getting and setting attributes for all network objects of one type
"""

from operator import itemgetter
import sys
import numpy
import os
import codecs
import numbers
import json
import win32com.client


def SetMulti(container, attribute, values, activeOnly=False):
    """Set the values of an attribute for all objects in a given network object collection

    container - COM object - the network object collection (e.g. Nodes, Links)
    attribute - string - attribute ID
    values - list - new values, as many as there are objects in the collection
    activeOnly - bool - True ==> set for active objects only
    return - none

    SetMulti(Visum.Net.Nodes, "ADDVAL1", [-1, -2, -3])
    """
    if activeOnly:
        raw = container.GetMultiAttValues(attribute, activeOnly) # a bit expensive, but the only way to get the indices
        indices = map(itemgetter(0), raw)
    else:
        indices = range(1, len(values) + 1)

    container.SetMultiAttValues(attribute, (zip(indices, values)))


def GetMulti(container, attribute, activeOnly = False):
    """Get the values of an attribute for all objects in a given network object collection

    container - COM object - the network object collection (e.g. Nodes, Links)
    attribute - string - attribute ID
    activeOnly - bool - True ==> get for active objects only

    return - list - new values, as many as there are objects in the collection

    values = GetMulti(Visum.Net.Nodes, "ADDVAL1")
    """
    # this is a hack, because Blocks and BlockItems have GetMultiAttValues without activeonly!
    try:
        raw = container.GetMultiAttValues(attribute, activeOnly)
    except:
        raw = container.GetMultiAttValues(attribute)
    values = map(itemgetter(1), raw)
    return values # todo: integer conversion

def GetMultiByFormula(container, formula, activeOnly=False):
    """Get the values of a formula evaluated on all objects in a given network object collection

    container - COM object - the network object collection (e.g. Nodes, Links)
    formula - string - formula to be evaluated (e.g. "10*[NO] + [TYPENO]")
    activeOnly - bool - True ==> get for active objects only

    return - list - new values, as many as there are objects in the collection

    values = GetMultiByFormula(Visum.Net.Nodes, "10*[NO] + [TYPENO]")
    """
    raw = container.GetMultiByFormula(formula, activeOnly)
    values = map(itemgetter(1), raw)
    return values

def GetAttShortName(container, attrID):
    """Reads the short name of an given net object attribute and returns it. If the installed VISUM-Version
    does not provide the needed COM-function 'GetShortName' the return value will be the passed attribute ID instead of raising
    an error or something similar

    container - COM object - the network object collection (e.g. Nodes, Links)
    attrID - string - the ID of the attribute thats short name will be read and returned.
    return - the shortName of the attribute with passed attrID

    GetAttShortName(Visum.Net.Nodes, "ADDVAL1")
    """
    try:
        attributes = container.Attributes
        shortName = attributes.GetShortName(attrID)
    except:
        shortName = attrID
    return shortName

def GetTableShortName(container, tableName):
    """Reads the short name of an given net object and returns it. If the installed VISUM-Version
    does not provide the needed COM-function 'GetTableShortName' the return value will be the passed tableName instead of raising
    an error or something similar

    container - COM object - the network object collection (e.g. Nodes, Links)
    tableName - string - the name of the net object whoose short name will be read and returned.
    return - the shortName of the passed passed tableName or the origin tableName if the COM-function is not available

    GetTableShortName(Visum.Net.Nodes)
    """
    try:
        attributes = container.Attributes #.GetTableShortName()
        shortName = attributes.GetTableShortName
    except Exception:
        shortName = tableName
    return shortName

# methods for getting and setting the contents of an OD matrix
# the matrix can be selected by passing either its number or the
# code of a demand segment.

def GetODMatrix(Visum, which):
    """Get an OD matrix as a numpy array.

    visum - COM object - the VISUM object
    which - string - demand segment code OR
          - number - matrix number

    return - numpy.array - matrix contents

    mat = GetODMatrix(Visum, 2)
    mat = GetODMatrix(Visum, "C")
    """
    matrix = __getODMatrix(Visum, which)
    return numpy.array(matrix.GetValues())

def SetODMatrix(Visum, which, values, additive=False):
    """Set an OD matrix from a two-dimensional sequence.

    visum - COM object - the VISUM object
    which - string - demand segment code OR
          - number - matrix number
    values - list(list) or numpy.array - matrix contents
    additive - bool - add to existing matrix instead of replace

    return - none

    SetODMatrix(Visum, 2, ((1,2,3),
                           (4,5,6),
                           (7,8,9)))

    SetODMatrix(Visum, "C", ((1,2,3),
                            (4,5,6),
                            (7,8,9)))
    """
    matrix = __getODMatrix(Visum, which)
    matrix.SetValues(values, additive)

# methods for getting and setting the contents of a skim matrix

def GetSkimMatrix(Visum, which, dseg=None):
    """Get a skim matrix as a numpy array.

    visum - COM object - the VISUM object
    which - number or code string - matrix number or matrix code string
    dseg - dseg string - string

    return - numpy.array - matrix contents

    mat = GetSkimMatrix(Visum, 3)

    mat = GetSkimMatrix(Visum, "TT0", "C")
    """
    #if which is an integer then use it, else lookup from string codes and dseg
    if __isNumberType(which):
        return numpy.array(Visum.Net.Matrices.ItemByKey(which).GetValues())
    else:
        return numpy.array(Visum.Net.Matrices.ItemByKey(skimLookup(Visum, which, dseg)).GetValues())

def SetSkimMatrix(Visum, which, values, additive=False):
    """Set a skim matrix from a two-dimensional sequence.

    visum - COM object - the VISUM object
    which - number - matrix number
    values - list(list) or numpy.array - matrix contents
    additive - bool - add to existing matrix instead of replace

    return - none

    SetSkimMatrix(Visum, 2, ((1,2,3),
                             (4,5,6),
                             (7,8,9)))
    or

    SetSkimMatrix(Visum, skimLookup(Visum, "TT0","C"),  ((1,2,3),
                                                  (4,5,6),
                                                  (7,8,9)))
    """
    matrix = Visum.Net.Matrices.ItemByKey(which)
    matrix.SetValues(values, additive)

def GetMatrix(Visum, which):
    """Get a matrix as a numpy array.

    visum - COM object - the VISUM object
    which - number - matrix number OR
          - string - matrix code OR
          - dict - matrix reference

    return - numpy.array - matrix contents

    mat = GetMatrix(Visum, 42)
    mat = GetMatrix(Visum, "C")
    mat = GetMatrix(Visum, {"CODE": "C"})
    """

    matrix = __getMatrix(Visum, which)
    return numpy.array(matrix.GetValues())

def SetMatrix(Visum, which, values, additive=False):
    """Set a matrix from a two-dimensional sequence.

    visum - COM object - the VISUM object
    which - number - matrix number OR
          - string - matrix code OR
          - dict - matrix reference
    values - list(list) or  2D array - matrix contents
    additive - bool - add to existing matrix instead of replace

    return - none

    SetMatrix(Visum, 2, ((1,2,3),
                         (4,5,6),
                         (7,8,9)))
    SetMatrix(Visum, "C", ((1,2,3),
                           (4,5,6),
                           (7,8,9)))
    SetMatrix(Visum, {"CODE": "C"}, ((1,2,3),
                                     (4,5,6),
                                     (7,8,9)))
    """
    matrix = __getMatrix(Visum, which)
    matrix.SetValues(values, additive)

def __IsInProcessVisum(Visum):
    if hasattr(Visum, '_in_process_instance_id_to_pid'):
        visum_pid = Visum._in_process_instance_id_to_pid.get(id(Visum))
        return visum_pid == os.getpid()
    return False

def __warn_about_slow_matrix_access(Visum):
    warning_msg = "Using slow generic matrix access because raw access is only available to scripts running in Visum."
    try:
        sys.stderr.write("Warning: " + warning_msg + "\n")
    except: # flushing stderr fails if executed inside Visum as visum is *not* a console application
        pass
    messagepriority_warning = 16384
    Visum.Log(messagepriority_warning, warning_msg)

def __GetVisumMatrixShape(VisumMat):
    return int(VisumMat.AttValue("NumRows")), int(VisumMat.AttValue("NumCols"))

def __GetRawAccessHiLo(NumpyMat):
    hi, lo = divmod(NumpyMat.ctypes.data, 1 << 31)
    if hi < 0 or hi >= 1 << 31:
        raise Exception("Memory address too large for raw data access. Please contact PTV Visum support.")
    return hi, lo

def __CopyToNumpy(Visum, VisumMat, NumpyMat=None):
    if __IsInProcessVisum(Visum):
        VisumMatShape = __GetVisumMatrixShape(VisumMat)
        if NumpyMat is None:
            NumpyMat = numpy.empty(VisumMatShape, order='C', dtype=numpy.float64)
        elif NumpyMat.shape != VisumMatShape:
            raise Exception("Cannot copy a Visum matrix of size %s into a NumPy matrix of size %s."% (VisumMatShape, NumpyMat.shape))
        elif NumpyMat.dtype != numpy.float64:
            raise Exception("Data type of NumPy matrix must be float64 in order to use raw copying.")
        hi, lo = __GetRawAccessHiLo(NumpyMat)
        VisumMat.GetValuesRaw(hi, lo)
    else:
        __warn_about_slow_matrix_access(Visum)
        if NumpyMat is not None:
            raise Exception("Cannot read directly into existing numpy matrix when called outside of Visum.")
        NumpyMat = numpy.array(VisumMat.GetValues())
    return NumpyMat

def __CopyFromNumpy(Visum, VisumMat, NumpyMat):
    if __IsInProcessVisum(Visum):
        VisumMatShape = __GetVisumMatrixShape(VisumMat)
        if NumpyMat.shape != VisumMatShape:
            raise Exception("Cannot copy a NumPy matrix of size %s into a Visum matrix of size %s."% (NumpyMat.shape, VisumMatShape))
        NumpyMat = NumpyMat.astype(numpy.float64, order='C', copy=False)
        if not NumpyMat.flags.owndata:
            NumpyMat = NumpyMat.copy()
        hi, lo = __GetRawAccessHiLo(NumpyMat)
        VisumMat.SetValuesRaw(hi, lo)
    else:
        __warn_about_slow_matrix_access(Visum)
        VisumMat.SetValues(NumpyMat)

def GetMatrixRaw(Visum, which, intoMat=None):
    """Get a matrix as a numpy array.

    Uses a much faster mechanism than GetMatrix when called from a script
    running inside Visum.

    visum - COM object - the VISUM object
    which - number - matrix number OR
          - string - matrix code OR
          - dict - matrix reference
    intoMat - numpy.array - optionally, an already existing numpy matrix
                            of the right dimensions, which will be overwritten
                            with the contents of the matrix
                            (only available when running in Visum)

    return - numpy.array - matrix contents

    mat = GetMatrixRaw(Visum, 42)
    mat = GetMatrixRaw(Visum, "C")
    mat = GetMatrixRaw(Visum, {"CODE": "C"})
    """
    matrix = __getMatrix(Visum, which)
    return __CopyToNumpy(Visum, matrix, intoMat)

def SetMatrixRaw(Visum, which, values):
    """Set a matrix from a two-dimensional sequence.

    Uses a much faster mechanism than SetMatrix when called from a script
    running inside Visum.

    visum - COM object - the VISUM object
    which - number - matrix number OR
          - string - matrix code OR
          - dict - matrix reference
    values - numpy array - matrix contents

    return - none

    A = numpy.array(((1,2,3),
                     (4,5,6),
                     (7,8,9)), dtype=numpy.float64)
    SetMatrixRaw(Visum, 2, A)
    SetMatrixRaw(Visum, "C", A)
    SetMatrixRaw(Visum, {"CODE": "C"}, A)
    """
    matrix = __getMatrix(Visum, which)
    __CopyFromNumpy(Visum, matrix, values)

def GetODMatrixRaw(Visum, which, intoMat=None):
    """Get an OD matrix as a numpy array.

    Uses a much faster mechanism than GetODMatrix when called from a script
    running inside Visum.

    visum - COM object - the VISUM object
    which - string - demand segment code OR
          - number - matrix number
    intoMat - numpy.array - optionally, an already existing numpy matrix
                            of the right dimensions, which will be overwritten
                            with the contents of the matrix
                            (only available when running in Visum)

    return - numpy.array - matrix contents

    mat = GetODMatrix(Visum, 2)
    mat = GetODMatrix(Visum, "C")
    """
    matrix = __getODMatrix(Visum, which)
    return __CopyToNumpy(Visum, matrix, intoMat)

def SetODMatrixRaw(Visum, which, values):
    """Set an OD matrix from a numpy array.

    Uses a much faster mechanism than SetODMatrix when called from a script
    running inside Visum.

    visum - COM object - the VISUM object
    which - string - demand segment code OR
          - number - matrix number
    values - numpy.array - matrix contents

    return - none

    A = numpy.array(((1,2,3),
                     (4,5,6),
                     (7,8,9)), dtype=numpy.float64)
    SetODMatrixRaw(Visum, 2, A)
    SetODMatrixRaw(Visum, "C", A)
    """
    matrix = __getODMatrix(Visum, which)
    __CopyFromNumpy(Visum, matrix, values)

# methods for getting and setting the contents of a skim matrix

def GetSkimMatrixRaw(Visum, which, dseg=None, intoMat=None):
    """Get a skim matrix as a numpy array.

    Uses a much faster mechanism than GetSkimMatrix when called from a script
    running inside Visum.

    visum - COM object - the VISUM object
    which - number or code string - matrix number or matrix code string
    dseg - dseg string - string
    intoMat - numpy.array - optionally, an already existing numpy matrix
                            of the right dimensions, which will be overwritten
                            with the contents of the matrix
                            (only available when running in Visum)

    return - numpy.array - matrix contents


    mat = GetSkimMatrixRaw(Visum, 3)

    mat = GetSkimMatrixRaw(Visum, "TT0", "C")
    """
    #if which is an integer then use it, else lookup from string codes and dseg
    if __isNumberType(which):
        mat = Visum.Net.Matrices.ItemByKey(which)
    else:
        mat = Visum.Net.Matrices.ItemByKey(skimLookup(Visum, which, dseg))
    return __CopyToNumpy(Visum, mat, intoMat)

def SetSkimMatrixRaw(Visum, which, values):
    """Set a skim matrix from a two-dimensional sequence.

    Uses a much faster mechanism than SetSkimMatrix when called from a script
    running inside Visum.

    visum - COM object - the VISUM object
    which - number - matrix number
    values - list(list) or numpy.array - matrix contents

    return - none

    A = numpy.array(((1,2,3),
                     (4,5,6),
                     (7,8,9)), dtype=numpy.float64)
    SetSkimMatrixRaw(Visum, 2, A)
    """

    matrix = Visum.Net.Matrices.ItemByKey(which)
    __CopyFromNumpy(Visum, matrix, values)


def CreateVisum(release=None):
    """Create a new VISUM instance.

    release - integer - An integer number describing the release to be used.
                        Examples:
                        9 = the latest installed VISUM 9.?? release
                        94 = the latest installed VISUN 9.4? release
                        942 = VISUM 9.42

    return - COM object - the VISUM object

    visum = CreateVisum(94)
    """

    progid = "Visum.Visum.%d" % release
    return win32com.client.Dispatch(progid)

def CreateObject(progID):
    """Create a new instance of a COM server.

    progID - string - the prog ID of the application

    return - COM object - the application object

    xl = CreateObject("Excel.Application")
    """
    return win32com.client.Dispatch(progID)


def secs2HHMMSS(secs):
    """Format a seconds value as a time string.

    secs - integer - seconds from midnight

    return - string - the formatted string

    timestring = secs2HHMMSS(36060)
    """

    HH, rest = divmod(secs, 60 * 60)
    MM, SS = divmod(rest, 60)
    return "%02d:%02d:%02d" % (HH, MM, SS)

def HHMMSS2secs(hhmmss):
    """Parse a time string and return the value as seconds from midnight.

    hhmmss - string - the formatted string
    return - integer - seconds from midnight

    secs = HHMMSS2secs("10:01:00")
    """
    parts = hhmmss.split(":")
    parts = map(int, parts)
    while len(parts) < 3:
        parts.append(0)
    sec = 0
    for t in parts:
        sec = sec * 60 + t
    return sec

def skimLookup(Visum, code, dseg):
    """function to lookup a skim no from a matrix code and DSeg

    Visum - COM object - Visum object
    code - string - matrix code like TT0
    dseg - string - DSEG string like C
    return - integer or None - integer if exists

    skimLookup(Visum, "TT0","C")
        """

    nos = Visum.Net.Matrices.GetMultiAttValues("NO")
    codes = Visum.Net.Matrices.GetMultiAttValues("CODE")
    dsegs = Visum.Net.Matrices.GetMultiAttValues("DSEGCODE")

    skimNo = dict()

    for i in range(0, len(nos)):
        skimNo[str(codes[i][1]) + "-" + str(dsegs[i][1])] = int(nos[i][1])

    if skimNo.has_key(str(code) + "-" + str(dseg)):
        return skimNo[str(code) + "-" + str(dseg)]
    else:
        return None

def attributeExists(container, attribute):
    """Checks whether an attribute exists for the object type

    container - Visum container object - container object
    attribute - string - attribute name
    return - bool - True or False
    attributeExists(Visum.Net.Zones, "TEST")
    """
    for anAttr in container.Attributes.GetAll:
        if str(anAttr.ID).upper() == attribute.upper():
            return True
    return False

def _GetContainer(Visum, name, names, nos):
    """ Get the container object for the current selection.
        Example: if the current selection is "Links", return
        the Visum.Net.Links container object.
    """
    if name.startswith("POI:"):
        # cut off the prefix and find no of category
        no = nos[names.index(name[5:])]
        # then return the POIs of the category with that no
        return Visum.Net.POICategories.ItemByKey(no).POIs
    else:
        return Visum.Net.__getattr__(name)

def GetContainer(Visum, name):
    """ Get the container object for the current selection.
        Example: if the current selection is "Links", return
        the Visum.Net.Links container object.
    """
    POICatNames = GetMulti(Visum.Net.POICategories, "NAME")
    POICatNos = GetMulti(Visum.Net.POICategories, "NO")
    return _GetContainer(Visum, name, POICatNames, POICatNos)

def ArrayNoneToZero(visumArray):
    """ search for None values in input array and writes 0.0 to ouput numpy array instead

    visumArray - array from GetMultipleAttributes()
                 or list from GetMulti()

    returns - new numpy array with values from VisumArray - but instead None contains 0.0

    """
    newNPArray = numpy.array(visumArray)
    if isinstance(newNPArray[0], numpy.ndarray):
        for actRow in newNPArray:
            for i in xrange(len(actRow)):
                if actRow[i] == None:
                    actRow[i] = 0.0
    else:
        for j in xrange(len(newNPArray)):
            if newNPArray[j] == None:
                newNPArray[j] = 0.0

    return newNPArray

def __getMatrix(Visum, which):
    """Get matrix object from VISUM

    visum - COM object - the VISUM object
    which - number - matrix number OR
          - string - matrix code OR
          - dict - matrix reference

    return - matrix object

    matrix = __getMatrix(Visum, 42)
    matrix = __getMatrix(Visum, "C")
    matrix = __getMatrix(Visum, {"CODE": "C"})
    """
    # check if which is a string, we suppose this must be the matrix code
    if __isStringType(which):
        matrix = __getMatrixByCode(Visum, which)
    elif __isDictType(which):
        matrix = __getMatrixByRef(Visum, which)
    else:
        matrix = Visum.Net.Matrices.ItemByKey(which)
    return matrix

def __getMatrixByCode(Visum, which):
    """Get matrix object from VISUM via matrix code

    Visum - COM object - the VISUM object
    which - string - matrix code

    return - matrix object

    matrix = __getMatrix(Visum, "C")
    """
    counter = 0
    matrix = None
    matrixCodes = Visum.Net.Matrices.GetMultipleAttributes(["NO", "CODE"])
    which = which.decode("iso-8859-15")
    for codePair in matrixCodes:
        if codePair[1] == which:
            matrix = Visum.Net.Matrices.ItemByKey(codePair[0])
            counter = counter + 1
    if counter > 1:
        raise Exception("Multiple matrices with code '%s' detected. No matrix is returned."% which)
    return matrix

def __getMatrixByRef(Visum, which):
    """which is a dict with key,value pairs for a Visum matrix ref"""
    def str1(x):
        if __isStringType(x):
            return str('"'+x+'"')
        else:
            return str(x)

    # build reference string from dict
    ref = [ '[%s] = %s' % (key,str1(val)) for key,val in which.items() ]
    ref = " & ".join(ref)
    ref = "Matrix(" + ref + ")"
    # get matrices matching ref
    matrixlist = Visum.Net.Matrices.ItemsByRef(ref).GetAll
    if not matrixlist:
        raise Exception("No matrix found for reference '%s'."% ref)
    # if exactly one, then return it, otherwise report error
    if len(matrixlist) != 1:
        raise Exception("Reference '%s' is not unique. No matrix is returned."% ref)
    return matrixlist[0]

def __getODMatrix(Visum, which):
    """Get an OD matrix from VISUM

    visum - COM object - the VISUM object
    which - string - demand segment code OR
          - number - matrix number

    return OD matrix

    matrix = __getODMatrix(Visum, 2)
    matrix = __getODMatrix(Visum, "C")
    """
    if __isNumberType(which):
        matrix = Visum.Net.Matrices.ItemByKey(which)
    else:
        dseg = Visum.Net.DemandSegments.ItemByKey(which)
        matrix = dseg.ODMatrix
    return matrix

def __isNumberType(val):
    """
    Returns true if the value val represents a number
    """
    return isinstance(val, numbers.Number)

def __isStringType(val):
    """
    Returns true if the value val represents a string
    """
    return isinstance(val, str)

def __isDictType(val):
    """
    Returns true if the value val represents a dict
    """
    return isinstance(val, dict)

def remove_bom_from_file(filename):
    """ Removes the Byte Order Mark (bom) at the beginning of text files
    """
    # check the filename parameter
    if (filename == None or os.path.isfile(filename) == False):
        return

    # open file
    f = open(filename,'rb')
    # read first 4 bytes
    header = f.read(4)
    # check if we have BOM...
    bom_len = 0

    encodings = [ ( codecs.BOM_UTF32, 4 ),
                 ( codecs.BOM_UTF16, 2 ),
                 ( codecs.BOM_UTF8, 3 ) ]

    for h, l in encodings:
        if header.startswith(h):
            bom_len = l
            break

    f.close()

    # ... and remove appropriate number of bytes
    if  bom_len > 0:
        tmpFileName = filename+"~"
        os.rename( filename, tmpFileName  )
        f = open(filename, "w")
        tmpFile = open(tmpFileName,'rb')
        firstLine = True
        for line in tmpFile:
            if firstLine:
                if bom_len == 3:
                    changedLine = line.replace(codecs.BOM_UTF8,"")
                elif bom_len == 2:
                    changedLine = line.replace(codecs.BOM_UTF16,"")
                elif bom_len == 4:
                    changedLine = line.replace(codecs.BOM_UTF32,"")
                else:
                    changedLine = line

                f.write(changedLine)
                firstLine = False
            else:
                f.write(line)
        f.close()
        tmpFile.close()
        os.remove(tmpFileName)

def ExecuteGraphQL(obj, query, variables=None):
    queryObj = {"query": query}
    if variables is not None:
        queryObj["variables"] = variables
    queryJSON = json.dumps(queryObj)
    resultJSON = obj.AttValue("$GRAPHQL:" + queryJSON)
    resultObj = json.loads(resultJSON)
    return resultObj
