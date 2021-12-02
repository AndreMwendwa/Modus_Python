# -*- coding: iso-8859-15 -*-
"""
Contains classes that implements a wx widget for a button and a combobox
"""

import wx
import numpy
from types import StringTypes
from VisumPy.helpers import GetMulti, _GetContainer, GetAttShortName, GetTableShortName
from __builtin__ import int

class wxAttrIDButton(wx.Button):
    """ This class implements a wx widget for a button which,
        when clicked, lets the user select an attribute of a
        specified net objetx type. Only single selection is allowed.
    """

    def __init__(self, parent, *args, **kwds):
        """ The constructor of the widget. Since most popular GUI builders,
            like wxGlade do not let you supply additional arguments to custom
            widgets, we leave the constructor alone and configure the widget
            using the methods below.
        """
        wx.Button.__init__(self, parent, *args, **kwds)
        self.Bind(wx.EVT_BUTTON, self.OnChoose)
        self.attrID = ""
        self.container = None
        self.editableOnly = False
        self.numericOnly = False
        self.SetAttrID("NO")
        self.specialFirst = ""

    def SetContainer(self, container):
        """ Set the net obj container for which the user will pick an attribute.
            This function must be called before the user gets a chance to click
            the button.

            container - object - the VISUM net obj container

            Example:
            btnAttr.SetContainer(Visum.Net.Links) sets up the widget so that link
            attributes are displayed.
        """
        self.container = container
        self.SetAttrID("...")

    def SetAttrType(self, editableOnly = False, numericOnly = False):
        """ Filter the attributes which will be displayed to the user. This
            method can be called optionally.

            editableOnly - bool - if True, only editable attributes are displayed
            numericOnly - bool - if True, only numeric attributes are displayed

            Example:
            btnAttr.SetAttrType(numericOnly=True) sets up the widget so that only
            numeric attributes, both editable and read-only, are displayed.
        """
        self.editableOnly = editableOnly
        self.numericOnly = numericOnly

    def SetSpecialFirst(self, newSpecialFirst):
        """ Filter the attributes which will be displayed to the user. This
            method can be called optionally.

            editableOnly - bool - if True, only editable attributes are displayed
            numericOnly - bool - if True, only numeric attributes are displayed

            Example:
            btnAttr.SetAttrType(numericOnly=True) sets up the widget so that only
            numeric attributes, both editable and read-only, are displayed.
        """
        self.specialFirst = newSpecialFirst

    def SetAttrID(self, attrID):
        """ Set the current selection by attribute ID. Use the syntax with backslashes
            to specify indirect attributes. This
            method can be called optionally.

            attrID - string - the ID of the attribute that should become the selection.
            displayValue - string - the value that should be displayed (e.g. the attributes short or long name)
        """
        changed = (attrID != self.attrID)
        if changed:
            self.attrID = attrID
            displayValue = GetAttShortName(self.container, attrID)
            self.SetLabel(displayValue)
            self.SetToolTipString(displayValue)
        return changed

    def GetAttrID(self):
        """ Get the current selection as the attribute ID.

            return - string - attribute ID
        """
        return self.attrID

    def OnChoose(self, event):
        """ This event is fired whenever the selection changes.
        """
        lastParent = self.Parent
        while lastParent.Parent != None:
            lastParent = lastParent.Parent

        lastParent.Show(False)
        if self.container == None:
            raise 666
        attrID = self.container.AskAttribute(editableOnly = self.editableOnly,
                                             numericOnly = self.numericOnly,
                                             defaultID = self.attrID,
                                             specialFirstEntry = self.specialFirst)

        changed = self.SetAttrID(attrID)
        self.SetFocus()
        lastParent.Show(True)
        if changed:
            event.Skip()

class wxNetobjtypeCombo(wx.ComboBox):
    """This class implements a wx widget for a combobox
    that contains the network object types for which the full
    range of container methods are available (like Get/SetMulti) and lets the
    user select one of them. Multiple selection is not supported.
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.CB_DROPDOWN | wx.CB_READONLY
        kwds["choices"] = []
        wx.ComboBox.__init__(self, *args, **kwds)

    def InitChoices(self, Visum):
        """ Initialize combobox values with all net objects.
        """
        netobjtypes = [ "Links",
                "Zones",
                "Turns",
                "Nodes",
                "Connectors",
                "Lines",
                "TSystems",
                "Territories",
                "Operators",
                "VehicleUnits",
                "CountLocations",
                "MainZones",
                "LinkTypes",
                "VehicleCombinations",
                "MainNodes",
                "MainTurns",
                "LineRoutes",
                "LineRouteItems",
                "TimeProfiles",
                "TimeProfileItems",
                "SystemRoutes",
                "SystemRouteItems",
                "VehicleJourneys",
                "VehicleJourneyItems",
                "Stops",
                "StopAreas",
                "StopPoints",
                "MainLines",
                "Modes",
                "DemandSegments",
##                "Blocks",
##                "BlockItems",
##                "BlockVersions",
                "VehJourneySections",
                "Detectors",
                "POICategories",
                "Screenlines"]

        attributes = ["NAME", "NO", "CODE"]
        attributeValues = Visum.Net.POICategories.GetMultipleAttributes(attributes)



        self.POICatNames = []
        self.POICatNos = []
        netObjDict = dict()

        # read poicat attributes and fill lists
        for s in attributeValues:
            poiCatName = s[0].encode("iso-8859-15")
            poiCatNo = s[1]
            poiCatCode = s[2].encode("iso-8859-15")

            netobjtypes.append("POI: " + poiCatName)
            netObjDict["POI: " + poiCatName] = "POI: %d %s" % (poiCatNo, poiCatCode)
            self.POICatNames.append(poiCatName)
            self.POICatNos.append(poiCatNo)


        netobjtypes.sort()

        # add net objects (including POI-Categories) to combobox
        for choice in netobjtypes:
            if not choice.startswith("POI:"):
                tmpContainer = _GetContainer(Visum, choice, self.POICatNames, self.POICatNos)
                self.Append(GetTableShortName(tmpContainer, choice), choice)
            else:
                self.Append(netObjDict[choice], choice)

    def GetName(self):
        """ Get the name string of the current selection.
        """
        netObjectName = self.GetClientData(self.GetSelection())
        return netObjectName

    def SetIndex(self, name):
        """ Set the index of the value(name)
        """
        try:
            for i in range(0, self.GetCount()):
                if self.GetClientData(i) == name:
                    self.Select(i)
                    break
        except Exception, dummy:
            return None

    def SetName(self, name):
        """ Set the current selection by its name string.
        """
        self.SetStringSelection(name)

    def GetContainer(self, Visum):
        """ Get the container object for the current selection.
            Example: if the current selection is "Links", return
            the Visum.Net.Links container object.
        """
        return _GetContainer(Visum, self.GetName(), self.POICatNames, self.POICatNos)


class wxNetobjCombo(wx.ComboBox):
    """This class implements a wx widget for a combobox
    that contains all instances of a certain network object type and lets the
    user select one of them. Multiple selection is not supported.
    """

    def __init__(self, *args, **kwds):
        """ The constructor of the widget. Since most popular GUI builders,
            like wxGlade do not let you supply additional arguments to custom
            widgets, we leave the constructor alone and configure the widget
            using the methods below.
        """
        kwds["style"] = wx.CB_DROPDOWN | wx.CB_READONLY
        kwds["choices"] = []
        wx.ComboBox.__init__(self, *args, **kwds)

    def InitChoices(self, container, displayattrs, resultattr = None, filtervector = None, displayformatter = None, key = None, matrixType = "DATA"):
        """ Use this method to specify which attributes should be displayed in
            the combobox and how the selection should be returned. This function
            must be called before the user gets a chance to click the combobox.

            container	- object - the network object container for which the attribute
                                 values are retrieved, e.g. Visum.Net.Links
            displayattrs - list(string) - attributes of that network object type which are
                                          to be displayed as the list entry for an object.
                                          A typical choice is the key attribute(s) of the
                                          network object type. Attribute values are separated
                                          by vertical bars.
            resultattr - string - If passed, it contains the ID of the attribute whose value
                                  is returned for each selected object. If the parameter is
                                  omitted, the object itself is returned instead of an attribute
                                  value.

            filtervector - list(bool) or list of list(bool) where length(list(bool)) == number of objects in container - if passed,
                                  then only the objects for which the corresponding list item is True
                                  are added to the combobox. If filtervector is omitted, all objects
                                  are added.

            displayformatter - function - if passed, this must be a function that takes as many parameters as
                                there are displayattrs and maps them to a string. In effect, the function is called for
                                each combobox entry with the displayattrs values for that entry. The function
                                should return a human-readable string that will be added as the combobox item.
                                If displayformatter is not passed, the values are all concatenated, separated
                                by vertical bars.
            key - key of the matrix to be used as key in the combo box.

            matrixType - limits the search to data matrices ("DATA"), formula ("FORMULA") or both (None).

            Examples:
            cboBlocks.InitChoices(Visum.Net.Blocks,
                                  displayattrs=["ID", "VEHCOMBNAME"])
            will set up a combobox with all Block objects. List entries look like
            "17 | Bus" where 17 is the block ID and "Bus" is the name of the vehicle combination.
            The selection will be returned as a Block object.

            cboLines.InitChoices(Visum.Net.Lines,
                                  displayattrs=["NAME"],
                                  resultattr="NAME")
            will set up a combobox with all Line objects. The line name is used as the
            list entry and the selection is also returned as the line name.

            def linkformatter(no, fromnode, tonode):
                return "%d (%d -> %d)" % (no, fromnode, tonode)

            cboLinks.InitChoices(Visum.Net.Links,
                                 displayattrs=["NO", "FROMNODENO", "TONODENO"],
                                 displayformatter=linkformatter)
            will set up a combobox with all Link objects. List entries look like
            "111 (47 -> 48)" where 111 is the link from node 47 to 48.

            zonetype = numpy.array(VisumPy.helpers.GetMulti(Visum.Net.Zones, "TYPENO"))
            cboZones.InitChoices(Visum.Net.Zones,
                                 displayattrs=["NO"],
                                 filtervector=(zonetype==1))
            will set up a combobox with all Zone objects that have a TYPENO == 1.
        """

        def stdformatter (vals):
            return " | ".join(map(unicode, vals))

        self.Clear()

        dataTypeVals = []
        self.isMatrices = False

        try:
            dataTypeVals = GetMulti(container, "DataSourceType")
            self.isMatrices = True
        except:
            self.isMatrices = False

        dispvals = [ GetMulti(container, disp) for disp in displayattrs ] # a list with one list for each attribute
        dispvals = zip(*dispvals) # a list with one tuple for each item
        activeDataTypeVals = []

        filtervector_internal = numpy.full(len(dispvals), True)
        if isinstance(filtervector, numpy.ndarray) or isinstance(filtervector, tuple): # keep only the tuples for which filtervector == True
            try:
                for elem in filtervector:
                    if len(elem) != len(dispvals):
                        filtervector_internal = numpy.empty(0)
                        break
                    for i in xrange(len(elem)):
                        filtervector_internal[i] = filtervector_internal[i] and elem[i]
            except:
                filtervector_internal = filtervector

            if len(filtervector_internal) != len(dispvals):
                raise Exception("wxNetobjCombo.InitChoices: length of filtervector does not match number of objects in container")
            activedispvals = []
            for i in xrange(len(filtervector_internal)):
                if filtervector_internal[i]:
                    activedispvals.append(dispvals[i])
                    if self.isMatrices == True:
                        activeDataTypeVals.append(dataTypeVals[i])

            dispvals = activedispvals
            if self.isMatrices == True:
                dataTypeVals = activeDataTypeVals

        # ---------------------------------------------------------------
        keyVals = []

        if key == None:
            for vals in dispvals:
                keyVals.append(vals[0])
        else:
            keyVals = GetMulti(container, key)
            if isinstance(filtervector_internal, numpy.ndarray): # keep only the key values for which filtervector_internal == True
                activeKeys = []
                for i in xrange(len(filtervector_internal)):
                    if filtervector_internal[i]:
                        activeKeys.append(keyVals[i])

                keyVals = activeKeys
        # ---------------------------------------------------------------

        if self.isMatrices == True:
            activeDataMatrices = []
            activeKeys = []
            for i in xrange(len(dispvals)):
                if dataTypeVals[i] == matrixType or matrixType == None:
                    activeDataMatrices.append(dispvals[i])
                    activeKeys.append(keyVals[i])

            dispvals = activeDataMatrices
            keyVals = activeKeys

        if displayformatter == None:
            dispvals = [ stdformatter(vals) for vals in dispvals ] # one string for each item
        else:
            dispvals = [ displayformatter(*vals) for vals in dispvals ] # one string for each item
        self.AppendItems(dispvals)

        for i in xrange(len(keyVals)):
            if isinstance(keyVals[i], StringTypes) == True:
                self.SetClientData(i, keyVals[i].encode('iso-8859-15'))
            else:
                self.SetClientData(i, unicode(keyVals[i]))

        if resultattr == None:
            self.resultvals = container.GetAll
        else:
            self.resultvals = GetMulti(container, resultattr)

        if isinstance(filtervector_internal, numpy.ndarray): # keep only the result values for which filtervector_internal == True
            activeresultvals = []
            for i in xrange(len(filtervector_internal)):
                if filtervector_internal[i]:
                    activeresultvals.append(self.resultvals[i])

            self.resultvals = activeresultvals

        if self.isMatrices == True:
            activeresultvalsCorrectDataType = []
            for i in xrange(len(self.resultvals)):
                if dataTypeVals[i] == matrixType or matrixType == None:
                    activeresultvalsCorrectDataType.append(self.resultvals[i])

            self.resultvals = activeresultvalsCorrectDataType

        self.SetSelection(0)

    def GetSelectionData(self):
        """ This method returns the current selection in the form specified by
            the resultattr parameter of InitChoices().
            If you want the index of the selection instead, call the GetSelection()
            method inherited from the wxComboBox base class.
            If you want to set the selection, use the SetSelection() or SetStringSelection()
            method inherited from the wxComboBox base class.
        """
        if self.GetSelection() == wx.NOT_FOUND:
            return None
        else:
            return self.resultvals[self.GetCurrentSelection()]

    def GetSelectedKey(self):
        if self.GetSelection() == wx.NOT_FOUND:
            return None
        else:
            return self.GetClientData(self.GetSelection())

    def SetSelectionByName(self, name):
        """ This method returns the index of a combobox string entry.
            The index has the form specified by the resultattr parameter of InitChoices().
            If you want the index of the selection instead, call the GetSelection()
            method inherited from the wxComboBox base class.
            If you want to set the selection, use the SetSelection() or SetStringSelection()
            method inherited from the wxComboBox base class.
        """

        if self.GetSelection() == wx.NOT_FOUND:
            return None
        else:
            counter = 0
            for displayValue in self.GetItems():
                if displayValue == name:
                    self.SetSelection(counter)
                    return self.resultvals[self.GetCurrentSelection()]
                counter = counter + 1
            self.SetSelection(0)
            return self.resultvals[self.GetCurrentSelection()]

    def __makeString(self, key):
        """ always compare strings
            and if there are ".0"-values from Visum, cut off ".0" for comparison
        """
        if isinstance(key, StringTypes) == False:
            key = unicode(key)
        result = key.replace(".0","")
        return result

    def SetSelectionByKey(self, key):
        """ Set the selection by the value
        """
        searchKey = key
        try:
            if type(key) == unicode or type(key) == str:
                if key.count('|') > 0:
                    splitValue = key.split('|')
                    searchKey = splitValue[0].strip()

            searchKey = self.__makeString(searchKey)

            for i in range(0, self.GetCount()):
                clientDataKey = self.GetClientData(i)
                clientDataKey = self.__makeString(clientDataKey)

                if clientDataKey == searchKey:
                    self.Select(i)
                    return ""
            return searchKey

        except Exception, dummy:
            return searchKey

