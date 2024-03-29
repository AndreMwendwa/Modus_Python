# -*- coding: iso-8859-15 -*-
"""
This module contains a family of functions which emulates user-defined attributes (UDAs)
with analysis time intervals as subattributes. As long as these are not available as a
built-in feature of VISUM, they can be emulated by several user-defined attributes, one
for each time interval. The IDs (and names) of the attributes are regularly formed from
a common prefix (baseattrID) and the code of the time interval. Example: If three time
intervals with codes 0700, 0800, 0900 exist, then a baseattrID of "MyAtt" will generate
proxy UDAs MyAtt_0700, MyAtt_0800, MyAtt_0900.
Convenience functions are provided for creating, getting and setting such proxy UDAs for
all existing time intervals.
"""

from numpy import *

from VisumPy.helpers import GetMulti, SetMulti

def GetTICodes(Visum):
    codes = []
    times = Visum.Procedures.Functions.AnalysisTimes
    for i in xrange(1, times.NumTimeIntervals+1):
        interval = times.TimeInterval(i)
        codes.append(interval.AttValue("CODE").strip())
    return codes

def CreateUDAPerTI(Visum, container, attrID, **kwords):
    """Will generate a set of UDAs according to the naming scheme described above.
    It is an error, if attributes of the generated names already exist.

    visum	- object - the Visum object (must be passed explicitly)
    container - COM object - the network object collection (e.g. Nodes, Links)
    baseattrID - string -	the prefix for the generation of the attribute IDs
    **kwords	Any number of named parameters for the other parameters of AddUserDefinedAttribute, like value type, decimal places, etc.
    return -	none 
    Example: If the intervals with codes 0700, 0800, 0900 exist, 
    CreateUDAPerTI(Visum, Visum.Net.Links, "CO2", vt=2) 
    will create link UDAs CO2_0700, CO2_0800, CO2_0900, of value type double (vt = 2).
    """
    for code in GetTICodes(Visum):
        attname = "%s_%s" % (attrID, code)
        container.AddUserDefinedAttribute(attname, attname, attname, **kwords)
        
def AttrIDsPerTI(Visum, baseattrID, predefined=False):
    """Returns a list of attribute IDs according to the naming scheme described above.
    Works with both UDAs created by CreateUDAPerTI and predefined attributes with
    subattribute AHPI.
    visum	- object - the Visum object (must be passed explicitly)
    baseattrID - string -	the prefix for the generation of the attribute IDs
    predefined - bool - True = the attribute is predefined by VISUM
                        False = the attribute was generated by CreateUDAPerTI
    return - list(string) - attribute IDs
    Example: If the intervals with codes 0700, 0800, 0900 exist, 
    AttrIDsPerTI(Visum, "CO2") 
    will return the list
    ["CO2_0700", "CO2_0800", "CO2_0900"].
    The call
    AttrIDsPerTI(Visum, "IMP_PRTSYS(P)", True) 
    will return the list 
    ["IMP_PRTSYS(P,0700)", "IMP_PRTSYS(P,0800)", "IMP_PRTSYS(P,0900)"].
    """
    if predefined:
        if "(" in baseattrID: # already has subattribute, so append
            base = baseattrID[:-1]
            return [ "%s,%s)" % (base, code) for code in GetTICodes(Visum) ]
        else:
            return [ "%s(%s)" % (baseattrID, code) for code in GetTICodes(Visum) ]
    else:
        return [ "%s_%s" % (baseattrID, code) for code in GetTICodes(Visum) ]

def GetMultiPerTI(Visum, container, baseattrID, predefined=False):
    """Returns the values of attributes per time interval.
    The values are retrieved for all objects of a network object type
    and all time intervals. They are returned as a matrix with one row per
    object (in standard key order) and one column per time interval (ascending).

    visum	- object - the Visum object (must be passed explicitly)
    container - COM object - the network object collection (e.g. Nodes, Links)
    baseattrID - string -	the prefix for the generation of the attribute IDs
    predefined - bool - True = the attribute is predefined by VISUM
                        False = the attribute was generated by CreateUDAPerTI
    return - numpy.array - matrix of attribute values
                              (type double for numeric attributes,
                              strings for all other attributes). 
    A numpy array is returned, if numpy is imported before importing VisumPy.TISupport
    Example: Assume that the intervals with codes 0700, 0800, 0900 and the nodes 1,2,3 exist, and that the node UDA MyAtt_0700 contains the node number itself, MyAtt_0800 contains the square and MyAtt_0900 contains the negative of the node number. Then
    GetMultiPerTI(Visum, Visum.Net.Nodes, "MyAtt")
    will return
    [ [1, 1, -1], [2, 4, -2], [3, 9, -3] ].
    """
    numObj = len(container.GetAll)
    attrIDs = AttrIDsPerTI(Visum, baseattrID, predefined)
    if "numpy" in sys.modules:
        values = zeros((numObj, len(attrIDs)), dtype=float64)
    else:
        values = zeros((numObj, len(attrIDs)), type=float64)
    for i, attr in enumerate(attrIDs):
        values[:,i] = GetMulti(container, attr)
    return values

def SetMultiPerTI(Visum, container, baseattrID, values, predefined=False):
    """Sets the values of attributes per time interval. The values are set
    for all objects of a network object type and all time intervals.
    They are passed as a matrix with one row per object (in standard key order)
    and one column per time interval (ascending).

    visum	- object - the Visum object (must be passed explicitly)
    container - COM object - the network object collection (e.g. Nodes, Links)
    baseattrID - string -	the prefix for the generation of the attribute IDs
    values - numpy.array - The matrix of new values
    predefined - bool - True = the attribute is predefined by VISUM
                        False = the attribute was generated by CreateUDAPerTI
    return -	none
    Example: Assume that the intervals with codes 0700, 0800, 0900 and the
    nodes 1,2,3 exist, then
    GetMultiPerTI(Visum, Visum.Net.Nodes, "MyAtt", [ [1, 1, -1], [2, 4, -2], [3, 9, -3] ])
    will cause UDA MyAtt_0700 to contain the node number itself, MyAtt_0800 the square,
    and MyAtt_0900 the negative of the node number.
    """
    attrIDs = AttrIDsPerTI(Visum, baseattrID, predefined)
    for i, attr in enumerate(attrIDs):
        SetMulti(container, attr, values[:,i])
